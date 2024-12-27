package routes

import (
	"crypto/rand"
	"fmt"

	"github.com/flosch/pongo2"
	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"
	"github.com/stnc/pongo2gin"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"main/models"
)

var (
	db = func() *gorm.DB {
		db, err := gorm.Open(sqlite.Open("db/app.db"), &gorm.Config{})
		if err != nil {
			panic("failed to connect to database")
		}
		models.InitDb(db)
		return db
	}()
	router = gin.Default()
	FLAG   = ""
)

func Run() {
	secret := make([]byte, 16)
	rand.Read(secret)

	store := cookie.NewStore(secret)
	router.Use(sessions.Sessions("session", store))

	router.Static("/static", "./static")
	router.HTMLRender = pongo2gin.TemplatePath("templates")
	getRoutes()
	router.Run(":5000")
}

func AuthRequired(c *gin.Context) {
	session := sessions.Default(c)
	user := session.Get("id")
	if user == nil {
		c.Redirect(302, fmt.Sprintf("/login?next=%s", c.Request.URL.Path))
		return
	}
	c.Next()
}

func InternalRequired(c *gin.Context) {
	session := sessions.Default(c)
	role := session.Get("role")
	if role == "user" {
		c.HTML(401, "message.html", pongo2.Context{
			"message": "Only editors and admins can access this page",
		})
		c.Abort()
		return
	}
	c.Next()
}

func AdminRequired(c *gin.Context) {
	session := sessions.Default(c)
	role := session.Get("role")
	if role != "admin" {
		c.HTML(401, "message.html", pongo2.Context{
			"message": "Only admins can access this page",
		})
		c.Abort()
		return
	}
	c.Next()
}

func getRoutes() {
	index := router.Group("/")
	addIndexRoutes(index)

	comments := router.Group("/comments")
	addCommentRoutes(comments)

	admin := router.Group("/admin")
	addAdminRoutes(admin)
}

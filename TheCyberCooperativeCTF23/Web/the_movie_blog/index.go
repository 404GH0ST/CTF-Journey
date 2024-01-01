package routes

import (
	"crypto/md5"
	"fmt"
	"math/rand"
	"net/http"
	"net/smtp"
	"time"

	"github.com/flosch/pongo2"
	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/microcosm-cc/bluemonday"
	"gorm.io/gorm"
	"main/models"
)

var (
	Sanitizer = bluemonday.UGCPolicy()
)

func addIndexRoutes(rg *gin.RouterGroup) {
	index := rg.Group("")

	index.GET("/", func(c *gin.Context) {
		posts := []models.Posts{}
		db.Preload("Author").Where("draft = false").Find(&posts)
		c.HTML(http.StatusOK, "index/index.html", pongo2.Context{"posts": posts})
	})

	index.GET("/login", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index/login.html", pongo2.Context{})
	})
	index.POST("/login", func(c *gin.Context) {
		session := sessions.Default(c)
		name := c.PostForm("name")
		password := c.PostForm("password")

		var user models.Users
		result := db.Where("name = ? AND password = ?", name, password).First(&user)
		if result.Error == gorm.ErrRecordNotFound {
			c.HTML(http.StatusOK, "message.html", pongo2.Context{
				"message": "Couldn't find a user with those credentials",
			})
			return
		}

		session.Set("id", user.ID)
		session.Set("name", user.Name)
		session.Set("role", user.Role)
		session.Save()

		next, success := c.GetQuery("next")
		if success {
			c.Redirect(302, next)
			return
		}

		c.Redirect(302, "/")
	})

	index.GET("/register", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index/register.html", pongo2.Context{})
	})
	index.POST("/register", func(c *gin.Context) {
		session := sessions.Default(c)
		name := c.PostForm("name")
		email := c.PostForm("email")
		password := c.PostForm("password")

		var check models.Users
		result := db.Where("name = ? OR email = ?", name, email).First(&check)
		if result.Error != gorm.ErrRecordNotFound {
			c.HTML(http.StatusOK, "message.html", pongo2.Context{
				"message": "A user already exists with those credentials",
			})
			return
		}

		user := models.Users{Name: name, Email: email, Password: password, Role: "user"}
		db.Create(&user)

		session.Set("id", user.ID)
		session.Set("name", user.Name)
		session.Set("role", user.Role)
		session.Save()

		next, success := c.GetQuery("next")
		if success {
			c.Redirect(302, next)
			return
		}

		c.Redirect(302, "/")
	})

	index.GET("/reset", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index/reset.html", pongo2.Context{})
	})
	index.POST("/reset", func(c *gin.Context) {
		name := c.PostForm("name")

		if name == "admin" {
			c.HTML(http.StatusOK, "message.html", pongo2.Context{
				"message": "How dare you! My password can't be reset! Are you a criminal?",
			})
			return
		}

		var user models.Users
		result := db.Where("name = ?", name).First(&user)
		if result.Error == gorm.ErrRecordNotFound {
			c.HTML(http.StatusOK, "message.html", pongo2.Context{
				"message": "Couldn't find a user with that username",
			})
			return
		}

		rand.Seed(time.Now().Unix())
		password := []byte(fmt.Sprintf("%s\n", rand.Int()))
		new_password := fmt.Sprintf("%x", md5.Sum(password))
		fmt.Printf("%v", new_password)

		user.Password = new_password
		db.Save(&user)

		from := "***********@*******.****"
		pass := "************************"
		to := user.Email

		msg := "From: " + from + "\n" +
			"To: " + to + "\n" +
			"Subject: Forgot Password Request\n\n" +
			"Your new password is " + new_password

		err := smtp.SendMail("***********:***",
			smtp.PlainAuth("", from, pass, "******************"),
			from, []string{to}, []byte(msg))

		if err != nil {
			fmt.Println("smtp error: %s", err)
			c.HTML(http.StatusOK, "message.html", pongo2.Context{
				"message": "Uh oh! We couldn't send the email. This isn't part of the challenge. Please contact an admin.",
			})
			return
		}

		c.HTML(http.StatusOK, "message.html", pongo2.Context{
			"message": "A new password will be emailed to you. Be sure to check your spam folder!",
		})
	})

	index.Use(AuthRequired)
	{
		index.GET("/:post_id", func(c *gin.Context) {
			session := sessions.Default(c)
			post_id := c.Param("post_id")
			post := models.Posts{}
			db.Preload("Author").Find(&post, post_id)

			comments := []models.Comments{}
			db.Preload("User").Where("post_id = ?", post_id).Find(&comments)

			c.HTML(http.StatusOK, "index/post.html", pongo2.Context{
				"post":      post,
				"comments":  comments,
				"name":      session.Get("name"),
				"Sanitizer": Sanitizer,
			})
		})
	}
}

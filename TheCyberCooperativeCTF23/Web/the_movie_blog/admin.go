package routes

import (
	"fmt"
	"net/http"

	"github.com/flosch/pongo2"
	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/go-resty/resty/v2"
	"main/models"
)

func addAdminRoutes(rg *gin.RouterGroup) {
	admin := rg.Group("")

	admin.Use(AuthRequired)
	admin.Use(InternalRequired)
	{
		admin.GET("/", func(c *gin.Context) {
			c.Redirect(302, "/admin/posts")
		})

		admin.GET("/posts", func(c *gin.Context) {
			posts := []models.Posts{}
			db.Preload("Author").Find(&posts)
			c.HTML(http.StatusOK, "admin/posts.html", pongo2.Context{"posts": posts})
		})

		admin.GET("/posts/:post_id", func(c *gin.Context) {
			post_id := c.Param("post_id")
			post := models.Posts{}
			db.Preload("Author").Find(&post, post_id)
			c.HTML(http.StatusOK, "admin/post.html", pongo2.Context{
				"post":      post,
				"Sanitizer": Sanitizer,
			})
		})
		admin.POST("/posts/:post_id", func(c *gin.Context) {
			post_id := c.Param("post_id")
			title := c.PostForm("title")
			content := c.PostForm("content")

			var post models.Posts
			db.First(&post, post_id)
			post.Title = title
			post.Content = content
			db.Save(&post)

			c.Redirect(302, "/admin/posts")
		})

		admin.GET("/posts/new", func(c *gin.Context) {
			c.HTML(http.StatusOK, "admin/new.html", pongo2.Context{})
		})
		admin.POST("/posts/new", func(c *gin.Context) {
			session := sessions.Default(c)
			user_id := int(session.Get("id").(uint))
			title := c.PostForm("title")
			content := c.PostForm("content")

			post := models.Posts{Title: title, Content: content, AuthorID: user_id, Draft: true}
			db.Create(&post)
			c.Redirect(302, "/admin/posts/")
		})
	}

	admin.Use(AuthRequired)
	admin.Use(AdminRequired)
	{
		admin.POST("/posts/publish", func(c *gin.Context) {
			c.HTML(200, "message.html", pongo2.Context{
				"message": FLAG,
			})
		})
	}
}

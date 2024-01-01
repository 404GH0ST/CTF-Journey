package routes

import (
	"fmt"
	"strconv"

	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
	"main/models"
)

func addCommentRoutes(rg *gin.RouterGroup) {
	comments := rg.Group("")

	comments.Use(AuthRequired)
	{
		comments.POST("/", func(c *gin.Context) {
			session := sessions.Default(c)
			user_id := int(session.Get("id").(uint))
			post_id, _ := strconv.Atoi(c.PostForm("post_id"))
			text := c.PostForm("text")

			comment := models.Comments{Text: text, PostID: post_id, UserID: user_id}
			db.Create(&comment)
			c.Redirect(302, fmt.Sprintf("/%d", post_id))
		})
	}
}

package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {

	r := gin.Default()

	r.Static("/static", "./static")
	r.LoadHTMLGlob("templates/*.html")

	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})

	r.GET("/flag", func(c *gin.Context) {
		secret, _ := c.Cookie("SECRET")
		if secret != (os.Getenv("SECRET")) {
			c.String(http.StatusForbidden, "You are not allowed to see the flag")
			return
		}
		c.String(http.StatusOK, os.Getenv("FLAG"))
	})

	r.Run(":80")
}

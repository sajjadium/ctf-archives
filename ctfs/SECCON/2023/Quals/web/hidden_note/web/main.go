package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"net/http"
	"os"
	"regexp"
	"text/template"

	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"
	"github.com/samber/lo"
)

func getRandomHex(n int) string {
	bytes := make([]byte, n)
	rand.Read(bytes)
	return hex.EncodeToString(bytes)
}

func isHex(str string) bool {
	_, err := hex.DecodeString(str)
	return err == nil
}

func main() {
	router := gin.Default()

	router.LoadHTMLGlob("views/*")

	store := cookie.NewStore([]byte(getRandomHex(32)))
	router.Use(sessions.Sessions("session", store))

	router.Use(func(c *gin.Context) {
		sess := sessions.Default(c)
		user, err := getUser(sess)
		if err != nil {
			c.Status(500)
			return
		}
		user.Query = c.DefaultQuery("query", user.Query)
		if err := user.save(sess); err != nil {
			c.Status(500)
			return
		}
		c.Set("user", user)
		c.Next()
	})

	router.GET("/clear", func(c *gin.Context) {
		sess := sessions.Default(c)
		sess.Clear()
		sess.Save()
		c.Redirect(302, "/")
	})

	router.GET("/", func(c *gin.Context) {
		user := c.MustGet("user").(*User)
		notes, err := user.getNotes(user.Query)
		if err != nil {
			c.Status(500)
			return
		}
		c.HTML(http.StatusOK, "index.html", gin.H{
			"user":   user,
			"notes":  notes,
			"shared": false,
		})
	})

	router.POST("/notes/new", func(c *gin.Context) {
		user := c.MustGet("user").(*User)
		note := new(Note)
		if err := c.Bind(note); err != nil {
			c.Status(400)
			return
		}
		if len(note.Content) > 1024 {
			c.String(400, "Too long content")
			return
		}
		if err := user.createNote(note); err != nil {
			c.Status(500)
			return
		}
		c.Redirect(302, "/")
	})

	router.POST("/notes/delete/:id", func(c *gin.Context) {
		user := c.MustGet("user").(*User)
		id := c.Param("id")
		if id == "" || !isHex(id) {
			c.String(400, "Invalid id")
			return
		}
		if err := user.deleteNote(id); err != nil {
			c.Status(500)
			return
		}
		c.Redirect(302, "/")
	})

	indexTmpl, _ := template.ParseFiles("views/index.html")
	secretPattern := regexp.MustCompile("SECCON{.*}")

	router.GET("/share", func(c *gin.Context) {
		user := c.MustGet("user").(*User)
		notes, err := user.getNotes(user.Query)
		if err != nil {
			c.String(500, "Failed to read notes")
			return
		}

		// Hide your secret notes 🤫
		notes = lo.Filter(notes, func(note Note, _ int) bool {
			return !secretPattern.MatchString(note.Content)
		})

		fileName := getRandomHex(12) + ".html"
		file, err := os.OpenFile(fmt.Sprintf("shared/%s", fileName), os.O_CREATE|os.O_WRONLY, 0600)
		if err != nil {
			c.Status(500)
			return
		}
		if err := indexTmpl.Execute(file, gin.H{
			"user":   user,
			"notes":  notes,
			"shared": true,
		}); err != nil {
			c.Status(500)
			return
		}
		c.Redirect(302, fmt.Sprintf("/shared/%s", fileName))
	})

	router.Static("/shared", "./shared")

	router.Run(":3000")
}

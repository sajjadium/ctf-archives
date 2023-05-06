package main

import (
	"context"
	"crypto/rand"
	"log"
	"math/big"
	"net/http"
	"os"
	"regexp"
	"time"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"github.com/go-redis/redis/v8"
)

type Post struct {
	ID          string    `gorm:"primaryKey"`
	UID         string    `gorm:"column:uid"`
	Title       string    `gorm:"column:title"`
	Description string    `gorm:"column:description"`
	CreatedAt   time.Time `gorm:"column:created_at"`
}

const letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

func randomString(n int) (string, error) {
	b := make([]byte, n)
	for i := range b {
		idx, err := rand.Int(rand.Reader, big.NewInt(int64(len(letters))))
		if err != nil {
			return "", err
		}
		b[i] = letters[idx.Int64()]
	}
	return string(b), nil
}

func (p *Post) BeforeCreate(tx *gorm.DB) (err error) {
	p.ID, err = randomString(10)
	return err
}

func main() {
	// datastores
	/////

	db, err := gorm.Open(sqlite.Open("database.db"), &gorm.Config{})
	if err != nil {
		log.Fatalf("failed to open a database: %s", err.Error())
	}
	db.AutoMigrate(&Post{})

	posts := []Post{}
	db.Where("uid = ?", os.Getenv("ADMIN_UID")).Find(&posts)
	if len(posts) == 0 {
		db.Create(&Post{
			UID:         os.Getenv("ADMIN_UID"),
			Title:       "flag",
			Description: os.Getenv("FLAG"),
		})
	}

	rdb := redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "",
		DB:       0,
	})

	// misc configurations
	/////

	r := gin.Default()
	r.LoadHTMLGlob("./templates/*.html")
	r.Static("/assets", "./assets")

	r.Use(func(c *gin.Context) {
		c.Header("Content-Security-Policy", "script-src 'self'; style-src 'self'; base-uri 'none'")
		c.Next()
	})

	r.Use(func(c *gin.Context) {
		k := c.Query("k")
		v := c.Query("v")
		if matched, err := regexp.MatchString("^[a-zA-Z-]+$", k); matched && err == nil && v != "" {
			c.Header(k, v)
		}
		c.Next()
	})

	r.Use(func(c *gin.Context) {
		uid, err := c.Cookie("uid")
		if err != nil || uid == "" {
			uid, err = randomString(32)
			if err != nil {
				panic(err.Error())
			}
			c.SetCookie("uid", uid, 3600, "/", "", false, true)
		}
		c.Set("uid", uid)
		c.Next()
	})

	// routes
	/////

	r.GET("/", func(c *gin.Context) {
		uid, _ := c.Get("uid")

		posts := []Post{}
		db.Where("uid = ?", uid.(string)).Find(&posts)

		c.HTML(http.StatusOK, "index.html", gin.H{
			"posts": posts,
		})
	})

	r.GET("/reset", func(c *gin.Context) {
		c.Redirect(http.StatusFound, "/")
	})

	r.POST("/notes", func(c *gin.Context) {
		uid, _ := c.Get("uid")
		title := c.PostForm("title")
		description := c.PostForm("description")
		if title == "" || description == "" {
			c.AbortWithStatus(400)
			return
		}

		p := Post{
			UID:         uid.(string),
			Title:       title,
			Description: description,
		}
		db.Create(&p)
		c.Redirect(http.StatusFound, "/notes/"+p.ID)
	})

	r.GET("/notes/:id", func(c *gin.Context) {
		var post Post
		if db.First(&post, "id = ?", c.Param("id")).Error != nil {
			c.AbortWithStatus(404)
			return
		}

		c.HTML(http.StatusOK, "detail.html", gin.H{
			"post": post,
		})
	})

	r.POST("/tell", func(c *gin.Context) {
		if err := rdb.RPush(context.Background(), "query", c.PostForm("path")).Err(); err != nil {
			c.AbortWithStatus(500)
			return
		}
		c.Redirect(http.StatusFound, "/")
	})

	r.Run(":8080")
}

package main

import (
	"fmt"
	"html"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
)

var conn *redis.Client
var useRecaptcha bool
var siteKey string
var secretKey string

type Note struct {
	Id       string `json:"id"`
	Title    string `json:"title"`
	Body     string `json:"body,omitempty"`
	Locked   bool   `json:"locked"`
	Password string `json:"-"`
}

var notes map[string]Note = map[string]Note{}
var masterKey string

var linkPattern = regexp.MustCompile(`\[([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12})\]`)

// replace [(note ID)] to links
func replaceLinks(note string) string {
	return linkPattern.ReplaceAllStringFunc(note, func(s string) string {
		id := strings.Trim(s, "[]")

		note, ok := notes[id]
		if !ok {
			return s
		}

		title := html.EscapeString(note.Title)
		return fmt.Sprintf(
			"<a href=/note/%s title=%s>%s</a>", id, title, title,
		)
	})
}

// escape note to prevent XSS first, then replace newlines to <br> and render links
func renderNote(note string) string {
	note = html.EscapeString(note)
	note = strings.ReplaceAll(note, "\n", "<br>")
	note = replaceLinks(note)
	return note
}

// PUT /api/note/new
func createNoteHandler(c *gin.Context) {
	title := c.PostForm("title")
	if title == "" || len(title) > 765 {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Invalid title",
		})
		return
	}

	body := c.PostForm("body")
	if body == "" || len(body) > 876 {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Invalid body",
		})
		return
	}

	password := c.PostForm("password")
	locked := password != ""
	if len(password) > 346 {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Invalid password",
		})
		return
	}

	id, err := uuid.NewRandom()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"status":  "error",
			"message": "Failed to generate a UUID",
		})
		return
	}

	notes[id.String()] = Note{
		Id:       id.String(),
		Title:    title,
		Body:     body,
		Locked:   locked,
		Password: password,
	}
	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
		"id":     id.String(),
	})
}

var uuidPattern = regexp.MustCompile(`^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$`)

// GET /api/note/:id
func getNoteHandler(c *gin.Context) {
	id := c.Param("id")
	if !uuidPattern.MatchString(id) {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Given ID is not a UUID",
		})
		return
	}

	note, ok := notes[id]
	if !ok {
		c.JSON(http.StatusNotFound, gin.H{
			"status":  "error",
			"message": "Note not found",
		})
		return
	}

	// if note is locked, body should not be sent
	if note.Locked {
		note.Body = ""
	}
	note.Body = renderNote(note.Body)

	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
		"note":   note,
	})
}

// GET /api/note/:id/unlock
func getLockedNoteHandler(c *gin.Context) {
	id := c.Param("id")
	if !uuidPattern.MatchString(id) {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Given ID is not a UUID",
		})
		return
	}

	note, ok := notes[id]
	if !ok {
		c.JSON(http.StatusNotFound, gin.H{
			"status":  "error",
			"message": "Note not found",
		})
		return
	}

	password := c.Query("password")
	if password != note.Password && password != masterKey {
		c.JSON(http.StatusUnauthorized, gin.H{
			"status":  "error",
			"message": "Wrong password",
		})
		return
	}

	note.Body = renderNote(note.Body)

	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
		"note":   note,
	})
}

func init() {
	useRecaptcha = os.Getenv("ENABLE_RECAPTCHA") != ""
	siteKey = os.Getenv("RECAPTCHA_SITE_KEY")
	secretKey = os.Getenv("RECAPTCHA_SECRET_KEY")

	masterKey = os.Getenv("MASTER_KEY")
	if masterKey == "" {
		id, err := uuid.NewRandom()
		if err != nil {
			panic(err)
		}
		masterKey = id.String()
	}
	log.Println("Master Key:", masterKey)

	conn = redis.NewClient(&redis.Options{
		Addr:     os.Getenv("REDIS_ADDR"),
		Password: "",
		DB:       0,
	})

	notes["6f16cd75-c50d-4ea2-b845-a085ff982a57"] = Note{
		Id:       "6f16cd75-c50d-4ea2-b845-a085ff982a57",
		Title:    "Sample",
		Body:     "(ΦωΦ) < meow!",
		Locked:   false,
		Password: "",
	}
}

func main() {
	r := gin.Default()
	r.Static("/static", "./static")
	r.LoadHTMLGlob("views/*.html")

	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})
	r.GET("/note/*_", func(c *gin.Context) {
		c.HTML(http.StatusOK, "note.html", gin.H{
			"useRecaptcha": useRecaptcha,
			"siteKey":      siteKey,
		})
	})

	r.PUT("/api/note/new", createNoteHandler)
	r.GET("/api/note/:id", getNoteHandler)
	r.GET("/api/note/:id/unlock", getLockedNoteHandler)
	r.POST("/api/note/:id/report", reportNoteHandler)

	r.Run()
}

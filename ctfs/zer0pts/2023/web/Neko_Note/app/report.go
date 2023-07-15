package main

import (
	"context"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"net/url"

	"github.com/gin-gonic/gin"
)

type Response struct {
	Success bool `json:"success"`
}

func verifyRecaptcha(token string) (bool, error) {
	v := url.Values{}
	v.Set("secret", secretKey)
	v.Set("response", token)

	r, err := http.PostForm("https://www.google.com/recaptcha/api/siteverify", v)
	if err != nil {
		return false, err
	}
	defer r.Body.Close()

	body, err := io.ReadAll(r.Body)
	if err != nil {
		return false, err
	}

	var res Response
	err = json.Unmarshal([]byte(body), &res)
	if err != nil {
		return false, err
	}

	return res.Success, nil
}

// POST /api/note/:id/report
func reportNoteHandler(c *gin.Context) {
	id := c.Param("id")
	if !uuidPattern.MatchString(id) {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Given ID is not a UUID",
		})
		return
	}

	_, ok := notes[id]
	if !ok {
		c.JSON(http.StatusNotFound, gin.H{
			"status":  "error",
			"message": "Note not found",
		})
		return
	}

	if useRecaptcha {
		token := c.PostForm("token")
		if token == "" {
			c.JSON(http.StatusBadRequest, gin.H{
				"status":  "error",
				"message": "Invalid token",
			})
			return
		}

		ok, err := verifyRecaptcha(token)
		if !ok {
			if err != nil {
				log.Println("verifyRecaptcha", err)
			}

			c.JSON(http.StatusBadRequest, gin.H{
				"status":  "error",
				"message": "Invalid token",
			})
			return
		}
	}

	err := conn.RPush(context.Background(), "report", id).Err()
	if err != nil {
		log.Println("rpush", err)
		c.JSON(http.StatusInternalServerError, gin.H{
			"status":  "error",
			"message": "Failed to report the note to admin. Please contact CTF admin",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
	})
}

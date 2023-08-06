package controllers

import (
	"go-get-it/middlewares"
	"go-get-it/models"
	"go-get-it/sessions"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

func RegisterGuestHandler(app *fiber.App) {

	guestGroup := app.Group("/")
	guestGroup.Get("/", middlewares.IsGuestOnly, ViewIndex)
	guestGroup.Get("/auth", middlewares.IsAuthenticated, AuthIndex)
}
func ViewIndex(c *fiber.Ctx) error {
	return c.Render("index", nil)
}

func AuthIndex(c *fiber.Ctx) error {
	s, err := sessions.RSS.Get(c)
	if err != nil {
		return c.Status(500).SendString("Internal Server Error")
	}

	user_id, ok := s.Get("user_id").(uint)

	if !ok || user_id == 0 {
		return c.Redirect("/login")
	}

	var user models.User
	err = models.GetUserById(&user, user_id)

	if err != nil {
		err := s.Destroy()
		if err != nil {
			return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
		}
		return c.Status(http.StatusNotFound).SendString("User not found")
	}

	return c.Render("authenticated", user)
}

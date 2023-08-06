package middlewares

import (
	"go-get-it/sessions"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

// Middleware to check if the user is authenticated
func IsGuestOnly(c *fiber.Ctx) error {

	session, err := sessions.RSS.Get(c)
	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	user_id, ok := session.Get("user_id").(uint)
	if ok && user_id != 0 {
		return c.Redirect("/auth")
	}

	return c.Next()
}

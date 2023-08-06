package middlewares

import (
	"go-get-it/sessions"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

// Middleware to check if the user is authenticated
func IsAuthenticated(c *fiber.Ctx) error {

	session, err := sessions.RSS.Get(c)
	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	user_id, ok := session.Get("user_id").(uint)

	if !ok || user_id == 0 {
		return c.Redirect("/login")
	}

	return c.Next()
}

func IsAdmin(c *fiber.Ctx) error {
	session, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	isAdmin, ok := session.Get("admin").(bool)

	if !ok || !isAdmin {
		return c.Redirect("/login")
	}

	return c.Next()
}

func IsAccountant(c *fiber.Ctx) error {
	session, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	isAccountant, ok := session.Get("accountant").(bool)

	if !ok || !isAccountant {
		return c.Redirect("/login")
	}

	return c.Next()
}

func IsLocal(c *fiber.Ctx) error {
	if c.IP() != "127.0.0.1" {
		return c.Status(http.StatusForbidden).SendString("Forbidden")
	}

	return c.Next()
}

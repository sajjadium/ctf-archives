package controllers

import (
	"fmt"
	"go-get-it/models"
	"go-get-it/sessions"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

func RegisterAuthHandler(app *fiber.App) {
	app.Get("/logout", LogoutHandler)
	app.Get("/login", ViewLogin)
	app.Get("/register", ViewRegister)
	app.Post("/login", PostLogin)
	app.Post("/register", PostRegister)
}

func ViewLogin(c *fiber.Ctx) error {
	return c.Render("login", nil)
}

func ViewRegister(c *fiber.Ctx) error {
	return c.Render("register", nil)
}

func PostLogin(c *fiber.Ctx) error {
	username := c.FormValue("username")
	password := c.FormValue("password")

	var user models.User

	if err := models.GetUserByUsername(&user, username); err != nil {
		return c.Status(http.StatusUnauthorized).SendString("Invalid Credentials")
	}

	if !user.CheckPassword(password) {
		return c.Status(http.StatusUnauthorized).SendString("Invalid Credentials")
	}

	session, err := sessions.RSS.Get(c)
	if err != nil || session == nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	session.Set("user_id", user.ID)
	session.Set("account_id", user.BankAccount.ID)

	if user.Role == "admin" {
		session.Set("admin", true)
	} else if user.Role == "accountant" {
		session.Set("accountant", true)
	}

	if err = session.Save(); err != nil {
		fmt.Println("Error saving to session")
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	return c.Redirect("/auth")
}

func PostRegister(c *fiber.Ctx) error {
	username := c.FormValue("username")
	password := c.FormValue("password")

	var user models.User
	if err := models.GetUserByUsername(&user, username); err == nil {
		return c.Status(http.StatusUnauthorized).SendString("User already exists")
	}

	if len(password) < 8 {
		return c.Status(http.StatusBadRequest).SendString("Password must be at least 8 characters")
	}

	user = models.User{
		Username: username,
	}

	user.SetPassword(password)

	err := models.CreateUser(&user)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Error creating user")
	}

	session, err := sessions.RSS.Get(c)
	if err != nil || session == nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	session.Set("user", true)
	if err = session.Save(); err != nil {
		fmt.Println("Error saving to session")
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}
	return c.Redirect("/auth")
}

func LogoutHandler(c *fiber.Ctx) error {
	session, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}
	session.Destroy()
	if err := session.Save(); err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	redirectTo := c.Query("redirect_to", "/login")

	return c.Redirect(redirectTo)
}

package controllers

import (
	"go-get-it/middlewares"
	"go-get-it/models"
	"go-get-it/sessions"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

func RegisterAdminHandler(app *fiber.App) {

	adminGroup := app.Group("/admin", middlewares.IsAdmin)
	adminGroup.Get("/", ViewAdminDashboard)
	adminGroup.Get("/users", ViewUsers)
	adminGroup.Get("/accounts", ViewAllBankAccounts)
	app.Get("/users", middlewares.IsAccountant, GetUsers)

}

func ViewAdminDashboard(c *fiber.Ctx) error {
	return c.Render("admin", nil)
}

func ViewUsers(c *fiber.Ctx) error {
	var users []models.User

	if err := models.AllUsers(&users); err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	return c.Render("users", fiber.Map{
		"users": users,
	})
}

func GetUsers(c *fiber.Ctx) error {
	var users []models.User

	if err := models.AllUsers(&users); err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	for _, user := range users {
		user.Password = ""
	}

	return c.JSON(users)
}

func ViewAllBankAccounts(c *fiber.Ctx) error {

	var accounts []models.Account
	err := models.GetAllAccounts(&accounts)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Error fetching accounts")
	}

	s, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	my_account_id, ok := s.Get("account_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	var my_account models.Account
	err = models.FindAccountAndPreloadTransactions(&my_account, my_account_id)
	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	return c.Render("accounts", fiber.Map{
		"accounts":   accounts,
		"my_account": my_account,
	})

}


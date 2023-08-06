package controllers

import (
	"fmt"
	"go-get-it/middlewares"
	"go-get-it/models"
	"go-get-it/sessions"
	"net/http"
	"strconv"

	"github.com/gofiber/fiber/v2"
)

func RegisterAccountHandler(app *fiber.App) {
	accountGroup := app.Group("/account", middlewares.IsAuthenticated)
	accountGroup.Get("/", ViewBankAccount)
	accountGroup.Post("/", PostAccountOperation)
}

func ViewBankAccount(c *fiber.Ctx) error {
	s, err := sessions.RSS.Get(c)

	if err != nil {
		fmt.Println("account.ViewBankAccount", err)
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	account_id, ok := s.Get("account_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	var account models.Account
	err = models.FindAccountAndPreloadTransactions(&account, account_id)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Error finding account")
	}

	return c.Render("bankaccount", fiber.Map{"account": account})
}

func PostAccountOperation(c *fiber.Ctx) error {

	s, err := sessions.RSS.Get(c)

	if err != nil {
		fmt.Println("account.PostAccountOperation", err)
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error: Try login again")
	}

	accountId, ok := s.Get("account_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error: Try login again")
	}

	var account models.Account
	err = models.FindAccountAndPreloadTransactions(&account, accountId)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Error loading bank account")
	}

	operation := c.FormValue("operation")
	amount, err := strconv.ParseFloat(c.FormValue("amount"), 64)
	to := c.FormValue("to", "")

	err = models.CreateOperationTransaction(&account, operation, amount, to)

	if err != nil {
		fmt.Println(err)
		return c.Status(http.StatusBadRequest).SendString("Invalid amount")
	}

	switch operation {
	case "deposit":
		err = account.Deposit(amount)
		break
	case "withdraw":
		err = account.Withdraw(amount)
		break

	}

	if err != nil {
		fmt.Println(err)
		return c.Status(http.StatusInternalServerError).SendString("Error processing operation")
	}

	return c.Redirect("/account")

}

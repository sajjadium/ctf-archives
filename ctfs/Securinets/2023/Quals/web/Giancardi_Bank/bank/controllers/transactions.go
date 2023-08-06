package controllers

import (
	"bytes"
	"fmt"
	"go-get-it/config"
	"go-get-it/middlewares"
	"go-get-it/models"
	"go-get-it/sessions"
	"go-get-it/utils"
	"net/http"
	"strconv"
	"strings"
	"text/template"

	"github.com/gofiber/fiber/v2"
	"golang.org/x/exp/slices"
)

var cachedKeys = make([]string, 0)

func RegisterTransactionsHandlers(app *fiber.App) {

	transactionsRouter := app.Group("/transactions", middlewares.IsAuthenticated) // /api
	transactionsRouter.Get("/", ViewTransactions)
	transactionsRouter.Get("/view/:id", ViewTransaction)
	transactionsRouter.Get("/search", ViewSearchTransaction)
	transactionsRouter.Get("/view/dev/:id", ViewSpecificTransactionsInfo)
	transactionsRouter.Get("/report/gen/:id", middlewares.IsAccountant, GetReport)
	transactionsRouter.Get("/report/info/all", middlewares.IsAccountant, GetReportsKeys)
}

func ViewTransactions(c *fiber.Ctx) error {
	var transactions []models.Transaction

	s, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	accountId, ok := s.Get("account_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	if err := models.AllUserTransactions(&transactions, accountId); err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	return c.Render("transactions", fiber.Map{
		"transactions": transactions,
	})
}

func ViewTransaction(c *fiber.Ctx) error {
	id, err := strconv.Atoi(c.Params("id"))
	if err != nil {
		return c.Status(http.StatusBadRequest).SendString("Invalid Id value")
	}

	order := c.Query("filter", "asc")

	var transaction models.Transaction

	s, err := sessions.RSS.Get(c)
	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	accountId, ok := s.Get("account_id").(uint)

	uid := uint(id)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	if err := models.FindUserTransaction(&transaction, uid, accountId, order); err != nil {
		return c.Status(http.StatusNotFound).SendString("Transaction not found")
	}

	return c.Render("transaction", fiber.Map{
		"transaction": transaction,
	})
}

func ViewSpecificTransactionsInfo(c *fiber.Ctx) error {
	transaction_id, err := c.ParamsInt("id", 0)
	forWhom := c.Query("for", "")

	if err != nil {
		return c.Status(http.StatusBadRequest).SendString("Invalid transaction id")
	}

	if transaction_id == 0 {
		return c.Status(http.StatusBadRequest).SendString("Invalid transaction id")
	}

	s, err := sessions.RSS.Get(c)
	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	accountId, ok := s.Get("account_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	uid := uint(accountId)

	var transaction models.Transaction
	err = models.FindUserTransaction(&transaction, uint(transaction_id), uid, "DESC")

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	tmpl, err := template.New("").Parse(
		"Transaction ID: {{.ID}}| Amount: {{.Amount}}| Description: {{.Description}}| Type: {{.Type}}| Account ID: {{.AccountID}}| Created At: {{.CreatedAt}}|From:" + forWhom,
	)
	if err != nil {
		fmt.Println(err)
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	var tpl bytes.Buffer
	if err := tmpl.Execute(&tpl, &transaction); err != nil {

	}

	res := tpl.String()

	config.CustomLogger.Log(res)

	return c.Render("transaction", fiber.Map{
		"transaction": transaction,
	})

}

func ViewSearchTransaction(c *fiber.Ctx) error {
	var transactions []models.Transaction

	searchQuery := c.Query("search", "")

	s, err := sessions.RSS.Get(c)
	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	accountId, ok := s.Get("account_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	if err := models.FindUserTransactionByDescription(&transactions, searchQuery, accountId); err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	return c.Render(
		"transactions",
		fiber.Map{
			"transactions": transactions,
			"query":        searchQuery,
		},
	)
}

func PostNewTransaction(c *fiber.Ctx) error {
	amount := c.FormValue("amount")
	description := c.FormValue("description")
	trans_type := c.FormValue("type")

	s, err := sessions.RSS.Get(c)
	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	accountId, ok := s.Get("account_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	float_amount, err := strconv.ParseFloat(amount, 64)
	if err != nil {
		return c.Status(http.StatusBadRequest).SendString("Make sure you have entered a valid amount")
	}

	var account models.Account

	if err := models.FindUserAccount(&account, accountId); err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	if account.Balance < float_amount && (trans_type == "widthdraw" || trans_type == "transfer") {
		return c.Status(http.StatusBadRequest).SendString("You do not have enough funds to make this transaction")
	}

	newTransaction := models.Transaction{
		AccountID:   accountId,
		Amount:      float_amount,
		Description: description,
		Type:        trans_type,
	}

	if err := models.CreateTransaction(&newTransaction); err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	return c.Redirect("/transactions")
}

func GetReportsKeys(c *fiber.Ctx) error {
	return c.SendString(strings.Join(cachedKeys, "|"))
}

func GetReport(c *fiber.Ctx) error {
	report_id := c.Params("id", "")

	user_id := c.QueryInt("user_id", 0)

	if report_id == "" {
		return c.Status(http.StatusBadRequest).SendString("Invalid Id value")
	}

	report, _ := models.VerifyReportInCache(report_id)

	if report != "" {
		return c.SendString(report)
	}

	if user_id == 0 {
		return c.Status(http.StatusBadRequest).SendString("Invalid user id")
	}

	report, err := models.GenerateReport(uint(user_id))

	if err != nil {

		fmt.Println("[+] Error generating report, ", err)

		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error: Error generating report")
	}


	report_id = utils.HashStringToSha256(report)

	_ = models.SaveReportInCache(report_id, report)

	if !slices.Contains(cachedKeys, report_id+":"+strconv.Itoa(user_id)) {
		cachedKeys = append(cachedKeys, report_id+":"+strconv.Itoa(user_id))
	}

	c.Response().Header.Set("Content-Type", "text/yaml")

	return c.SendString(report)
}

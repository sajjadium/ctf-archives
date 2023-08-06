package models

import (
	"errors"
	"fmt"
	"go-get-it/config"
	"go-get-it/utils"
	"net/http"
	"net/url"
	"path"
	"strings"
	"time"

	"gopkg.in/yaml.v2"
)

type Transaction struct {
	ID            uint `gorm:"primaryKey,autoIncrement"`
	Account       Account
	AccountID     uint
	Amount        float64 `gorm:"not null"`
	BalanceAfter  float64
	BalanceBefore float64
	Type          string
	Description   string
	CreatedAt     time.Time `gorm:"autoCreateTime"`
	Snapshot      string    `gorm:"type:text"`
}

type TransactionDetails struct {
	From   string `yaml:"from"`
	Result string `yaml:"result"`
}

type TransactionDescription struct {
	Sender             string             `yaml:"sender"`
	Username           string             `yaml:"username"`
	BalanceBefore      float64            `yaml:"balance_before"`
	BalanceAfter       float64            `yaml:"balance_after"`
	Description        string             `yaml:"description"`
	TransactionDetails TransactionDetails `yaml:"transaction_details"`
	Others             interface{}        `yaml:"-"` // This is a hack to get the rest of the fields
}

func (t *Transaction) TableName() string {
	return "transactions"
}

func CreateTransaction(t *Transaction) error {
	err := config.DB.Conn.Create(t).Error
	if err != nil {
		return nil
	}
	return nil
}

func UpdateTransaction(t *Transaction) error {
	err := config.DB.Conn.Model(t).Updates(t).Error
	if err != nil {
		return err
	}
	return nil
}

func FindTransactionByDescription(t *[]Transaction, partialDescription string) error {
	var transactions []Transaction
	err := config.DB.Conn.Where("description LIKE ?", "%"+partialDescription+"%").Find(&transactions).Error
	if err != nil {
		return err
	}
	return nil
}

func FindTransaction(t *Transaction, id uint) error {
	err := config.DB.Conn.Preload("Account").First(t, id).Error
	if err != nil {
		return err
	}
	return nil
}

func FindTransactionByCreatedAt(t *[]Transaction, start time.Time, end time.Time) error {
	err := config.DB.Conn.Where("created_at BETWEEN ? AND ?", start, end).Find(t).Error
	if err != nil {
		return err
	}
	return nil
}

func FindUserTransaction(t *Transaction, id uint, accountId uint, order string) error {
	err := config.DB.Conn.Where("account_id = ?", accountId).First(t, id).Order("createdAt " + order).Error
	if err != nil {
		fmt.Println("models.FindUser Error getting transactions")
		return err
	}
	return nil
}

func AllUserTransactions(transactions *[]Transaction, accountId uint) error {
	err := config.DB.Conn.Where("account_id = ?", accountId).Find(&transactions).Order("createdAt DESC").Error
	if err != nil {
		fmt.Println("models.AllUserTransactions Error getting transactions")
		return err
	}
	return nil
}

func AllTransactions(transactions *[]Transaction) error {
	err := config.DB.Conn.Find(&transactions).Order("createdAt DESC").Error

	if err != nil {
		fmt.Println("models.AllTransactions Error getting transactions")
		return err
	}

	return nil
}

func FindUserTransactionByDescription(t *[]Transaction, partialDescription string, accountId uint) error {
	err := config.DB.Conn.Where("description LIKE ? and account_id = ?", "%"+partialDescription+"%", accountId).Find(t).Error

	if err != nil {
		return err
	}

	return nil
}

func DumpTransactionDescriptionsToYaml(t []TransactionDescription) (string, error) {

	descBytes, err := yaml.Marshal(t)

	if err != nil {
		return "", err
	}

	return string(descBytes), nil
}

func DumpTransactionDescriptionToYaml(t *TransactionDescription) (string, error) {

	descBytes, err := yaml.Marshal(t)

	if err != nil {
		return "", err
	}

	return string(descBytes), nil
}

func ParseTransactionDescriptionFromYaml(desc string) (*TransactionDescription, error) {
	var transactionDescription TransactionDescription
	err := yaml.Unmarshal([]byte(desc), &transactionDescription)
	if err != nil {
		return nil, err
	}
	return &transactionDescription, nil
}

func GenerateTransactionsDescription(t_id uint, td *TransactionDescription) error {

	t := Transaction{}
	err := FindTransaction(&t, t_id)
	if err != nil {
		return err
	}

	u := User{}
	err = GetUserById(&u, t.Account.UserID)

	if err != nil {
		return err
	}

	return nil
}

func (t *Transaction) GetTransactionDescription() (TransactionDescription, error) {
	td := TransactionDescription{}

	td.BalanceBefore = t.BalanceBefore
	td.BalanceAfter = t.BalanceAfter
	descriptionSplitted := strings.Split(t.Description, "|")

	if len(descriptionSplitted) < 3 {
		return td, errors.New("invalid description")
	}

	td.Description = descriptionSplitted[1] + descriptionSplitted[2]

	td.TransactionDetails = TransactionDetails{
		From:   "go-get-it",
		Result: "success",
	}

	return td, nil
}

func CreateOperationTransaction(a *Account, operation string, amount float64, to string) error {
	t := &Transaction{
		AccountID: a.ID,
		Amount:    amount,
		Type:      operation,
	}

	switch operation {
	case "deposit":
		t.BalanceAfter = a.Balance + amount
		t.BalanceBefore = a.Balance
		break
	case "withdraw":
		t.BalanceAfter = a.Balance - amount
		t.BalanceBefore = a.Balance
		break
	case "transfer":
		t.BalanceAfter = a.Balance - amount
		t.BalanceBefore = a.Balance
		break
	default:
		return errors.New("Invalid operation")
	}

	if t.BalanceAfter < 0 {
		return errors.New("Insufficient funds")
	}

	if operation == "transfer" {
		t.Description = fmt.Sprintf("TO:http://127.0.0.1:3000/user/verify/%s|%s|%s", to, operation, time.Now().Format("2006-01-02 15:04"))
	} else {

		t.Description = fmt.Sprintf("TO:http://127.0.0.1:3000/user/verify/%s|%s|%s", to, operation, time.Now().Format("2006-01-02 15:04"))
	}

	if t.DoesPartyExist(t.Description) == false {
		return errors.New("Error creating transaction")
	}

	err := CreateTransaction(t)

	if err != nil {
		fmt.Println("Error creating transaction")
		return err
	}

	return nil
}

func (t *Transaction) FormatDescription() (string, error) {

	parts := strings.Split(t.Description, "|")

	if len(parts) != 3 {
		fmt.Println("Invalid data format")
		return "", errors.New("Invalid data format")
	}

	// Extract URL
	transferURL, err := url.Parse(parts[0][3:]) // remove the "TO:" prefix
	if err != nil {
		fmt.Println("Invalid URL format")
		return "", errors.New("Invalid URL format")
	}

	// Extract user ID from URL path
	userID := strings.TrimPrefix(transferURL.Path, "/user/")

	// Extract operation type
	operation := parts[1]

	// Extract date
	date := parts[2]

	fmt.Printf("UserID: %s, Operation: %s, Date: %s\n", userID, operation, date)

	return date, nil
}

func (t *Transaction) DoesPartyExist(desc string) bool {

	parts := strings.Split(desc, "|")
	transferURL, err := url.Parse(parts[0][3:])

	if err != nil {
		return false
	}

	isLocal := strings.HasPrefix(transferURL.Host, "127.0.0.1:3000") && strings.HasPrefix(transferURL.Path, "/user/")

	if !isLocal {
		return false
	}

	transferURL.Path = path.Clean(transferURL.Path)

	client := &http.Client{}

	req, err := http.NewRequest("GET", transferURL.String(), nil)

	if err != nil {
		return false
	}
	resp, err := client.Do(req)

	if err != nil {
		return false
	}
	defer resp.Body.Close()

	return resp.StatusCode != http.StatusNotFound

}

func GetLatestUserTransactions(userID uint) ([]Transaction, error) {
	var transactions []Transaction

	err := config.DB.Conn.Joins("Account").
		Where("user_id = ?", userID).
		Order("created_at desc").
		Limit(10).
		Find(&transactions).Error

	if err != nil {
		return nil, err
	}

	return transactions, nil
}

func VerifyReportInCache(report_id string) (string, error) {

	value, err := config.Cache.Get(report_id)
	if err != nil || value == "" {
		return "", err
	}

	return value, nil
}

func GenerateReport(userID uint) (string, error) {

	latestTransactions, err := GetLatestUserTransactions(userID)

	if err != nil {
		return "", err
	}

	if len(latestTransactions) == 0 {
		return "", errors.New("No transactions found")
	}

	if len(latestTransactions) < 10 {
		return "", errors.New("Not enough transactions to generate report")
	}

	var report string

	descArray := []TransactionDescription{}

	for _, transaction := range latestTransactions {
		desc, err := transaction.GetTransactionDescription()
		if err != nil {
			return "", err
		}

		descArray = append(descArray, desc)
	}

	report, err = DumpTransactionDescriptionsToYaml(descArray)

	return report, err
}

func SaveReportInCache(reportId string, report string) error {

	report_id := utils.HashStringToSha256(reportId)

	err := config.Cache.Set(report_id, report)
	if err != nil {
		return errors.New("Error saving report in cache")
	}

	return nil
}

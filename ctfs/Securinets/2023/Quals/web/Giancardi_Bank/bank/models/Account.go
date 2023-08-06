package models

import (
	"errors"
	"go-get-it/config"
	"time"
)

type Account struct {
	ID           uint `gorm:"primaryKey,autoIncrement"`
	UserID       uint
	Balance      float64       `gorm:"default:0"`
	Transactions []Transaction `gorm:"foreignKey:AccountID"`
	UpdatedAt    time.Time     `gorm:"autoUpdateTime"`
}

func (a *Account) TableName() string {
	return "accounts"
}

func FindAccountAndPreloadTransactions(account *Account, accountId uint) error {
	err := config.DB.Conn.Preload("Transactions").First(&account, accountId).Error
	if err != nil {
		return err
	}
	return nil
}

func (account *Account) UpdateBalance(amount float64) error {
	account.Balance += amount
	result := config.DB.Conn.Save(account)
	if result.Error != nil {
		return result.Error
	}
	return nil
}

func CreateAccount(account *Account) (*Account, error) {
	result := config.DB.Conn.Create(account)
	if result.Error != nil {
		return nil, result.Error
	}
	return account, nil
}

func FindUserAccount(account *Account, userId uint) error {
	result := config.DB.Conn.Where("user_id = ?", userId).First(&account)
	if result.Error != nil {
		return result.Error
	}
	return nil
}

func GetAllAccounts(account *[]Account) error {
	err := config.DB.Conn.Find(&account).Error

	if err != nil {
		return err
	}

	return nil
}

func (a *Account) Withdraw(amount float64) error {
	if a.Balance < float64(amount) {
		return errors.New("Insufficient funds")
	}

	a.Balance -= float64(amount)
	err := config.DB.Conn.Save(a).Error
	if err != nil {
		return err
	}

	return nil
}

func (a *Account) Deposit(amount float64) error {
	a.Balance += float64(amount)
	err := config.DB.Conn.Save(a).Error
	if err != nil {
		return err
	}
	return nil
}

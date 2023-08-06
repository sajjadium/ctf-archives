package models

import (
	"crypto/rand"
	"fmt"
	"go-get-it/config"
	"os"
)

func checkIfDBInitialized() (bool, error) {
	var u User
	err := GetUserByUsername(&u, "admin")

	if err != nil {
		fmt.Println("models.CheckDbIfInitialized Error getting user", err)
		if err.Error() == "record not found" {
			fmt.Println("models.CheckDbIfInitialized DB not initialized")
			return false, nil
		}
		return true, err
	}

	return true, nil
}

func MustSeedDB() error {
	err := config.DB.Conn.AutoMigrate(&User{}, &Account{}, &Transaction{}, &PetFile{}, &FinanceNote{})

	if err != nil {
		panic(err)
	}

	initialized, err := checkIfDBInitialized()

	if initialized {
		return nil
	}

	if err != nil {
		panic("Error checking if DB is initialized")
	}
	// User 1: Admin
	adminPassword := make([]byte, 32) // Generate a 32-byte random password
	if _, err := rand.Read(adminPassword); err != nil {
		return err
	}
	admin := User{
		Username: "admin",
		Password: string(adminPassword),
		Role:     "admin",
		BankAccount: Account{
			Balance: 10000000, // 10 million dollars
		},
	}

	if err := config.DB.Conn.Create(&admin).Error; err != nil {
		return err
	}

	shadyGuy := User{
		Username: "ShadyGuy",
		Role:     "guest",
		Password: "password",
		BankAccount: Account{
			Balance: 1000000, // 1 million dollars
		},
	}

	if err := config.DB.Conn.Create(&shadyGuy).Error; err != nil {
		return err
	}

	accountant := User{
		Username: "MisterX",
		Role:     "accountant",
		Password: os.Getenv("ACCOUNTANT_PASSWORD"),
		BankAccount: Account{
			Balance: 1000000, // 1 million dollars
		},
	}

	if err := config.DB.Conn.Create(&accountant).Error; err != nil {
		return err
	}

	// Transaction from ShadyGuy to Admin
	transaction := Transaction{
		AccountID:   shadyGuy.BankAccount.ID,
		Amount:      4000000, // 4 million dollars
		Type:        "transact",
		Description: fmt.Sprintf("Transferred to %s", admin.Username),
	}

	if err := config.DB.Conn.Create(&transaction).Error; err != nil {
		return err
	}

	return nil
}

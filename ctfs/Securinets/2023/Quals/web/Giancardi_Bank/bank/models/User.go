package models

import (
	"fmt"
	"go-get-it/config"
	"go-get-it/utils"
	"time"

	"gorm.io/gorm"
)

type User struct {
	gorm.Model

	ID        uint      `gorm:"primaryKey,autoIncrement"`
	CreatedAt time.Time `gorm:"autoCreateTime"`
	UpdatedAt time.Time `gorm:"autoUpdateTime"`

	Password string `gorm:"not null"`
	Username string `gorm:"not null,unique"`

	BankAccount Account
	Role        string `gorm:"default:guest"`
	PetFiles    []PetFile
	Notes       []FinanceNote
}

type PetFile struct {
	gorm.Model
	ID        uint      `gorm:"primaryKey,autoIncrement"`
	CreatedAt time.Time `gorm:"autoCreateTime"`
	UpdatedAt time.Time `gorm:"autoUpdateTime"`
	Path      string    `gorm:"not null"`
	UserID    uint      `gorm:"not null"`
}

type FinanceNote struct {
	gorm.Model
	ID        uint      `gorm:"primaryKey,autoIncrement"`
	CreatedAt time.Time `gorm:"autoCreateTime"`
	UpdatedAt time.Time `gorm:"autoUpdateTime"`
	UserID    uint      `gorm:"not null"`
	Note      string    `gorm:"not null"`
	Title     string    `gorm:"not null,unique"`
}

func (u *User) TableName() string {
	return "users"
}

func (u *User) BeforeCreate(tx *gorm.DB) (err error) {
	passwordHash, err := utils.HashPassword(u.Password)
	if err != nil {
		fmt.Println("User.BeforeCreate: Error hashing password")
		return err
	}

	u.Password = passwordHash

	return nil
}

func CreateUser(u *User) error {

	u.BankAccount = Account{
		Balance:      0,
		Transactions: []Transaction{},
	}

	err := config.DB.Conn.Create(&u).Error

	if err != nil {
		fmt.Println("models.CreateUser Error creating user", err)
		return err
	}
	return nil
}

func AllUsers(users *[]User) error {
	err := config.DB.Conn.Find(users).Error
	if err != nil {
		fmt.Println("models.AllUsers Error getting users")
		return err
	}
	return nil
}

func GetUserById(user *User, userId uint) error {
	err := config.DB.Conn.Model(&User{}).Preload("BankAccount").Preload("Notes").Preload("PetFiles").Where("id = ?", userId).First(&user).Error

	if err != nil {
		fmt.Println("models.GetUser Error getting user", err)
		return err
	}
	return nil
}

func (u *User) UpdatePassword(password string) error {
	u.Password = password

	err := config.DB.Conn.Save(u).Error

	if err != nil {
		fmt.Println("models.UpdatePassword Error getting user")
	}
	return err
}

func GetUserByUsername(u *User, username string) error {
	err := config.DB.Conn.Preload("BankAccount").Where("username = ?", username).First(u).Error

	if err != nil {
		fmt.Println("models.GetUserByUsername Error getting user", err)
		return err
	}

	return nil
}

func (u *User) CheckPassword(password string) bool {
	return utils.CheckPasswordHash(password, u.Password)
}

func (u *User) SetPassword(password string) bool {
	u.Password = password
	return true
}

func CreatePetFile(petFile *PetFile) error {
	err := config.DB.Conn.Create(petFile).Error
	if err != nil {
		return err
	}
	return nil
}

func GetUserPetFiles(petFiles *[]PetFile, userId uint) error {
	err := config.DB.Conn.Where("user_id = ?", userId).Find(&petFiles).Error
	if err != nil {
		fmt.Println("models.GetUserPetFiles", err)
		return err
	}
	return nil
}

func GetUserPetFile(petFiles *PetFile, petFileId, userId uint) error {
	err := config.DB.Conn.Where("user_id = ?", userId).First(&petFiles, petFileId).Error
	if err != nil {
		fmt.Println("models.GetUserPetFile", err)
		return err
	}
	return nil
}

func CreateFinanceNote(note *FinanceNote) error {
	err := config.DB.Conn.Create(note).Error
	if err != nil {
		fmt.Println("models.CreateFinanceNote", err)
		return err
	}
	return nil
}

func UpdateFinanceNote(note *FinanceNote) error {
	err := config.DB.Conn.Save(note).Error
	if err != nil {
		fmt.Println("models.UpdateFinanceNote", err)
		return err
	}
	return nil
}

func GetUserFinanceNotes(notes *[]FinanceNote, userId uint) error {
	err := config.DB.Conn.Where("user_id = ?", userId).Find(notes).Error
	if err != nil {
		fmt.Println("models.GetUserFinanceNotes", err)
		return err
	}
	return nil
}
func GetUserNoteById(note *FinanceNote, noteId uint, userId uint) error {
	err := config.DB.Conn.Where("user_id = ?", userId).First(note, noteId).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			fmt.Println("models.GetUserNoteById", err)
			return err
		}
		return err
	}
	return nil
}

func GetUserFinanceNoteByTitle(note *FinanceNote, title string, userId uint) error {
	err := config.DB.Conn.Where("user_id = ? and title = ?", userId, title).First(note).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return err
		}
		fmt.Println("models.GetUserNoteByTitle Error getting user", err)
		return err
	}
	return nil

}

func GetUserNoteByTitle(note *FinanceNote, title string) error {
	err := config.DB.Conn.Where("title = ?", title).First(note).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return err
		}
		fmt.Println("models.GetUserNoteByTitle Error getting user", err)
		return err
	}
	return nil

}

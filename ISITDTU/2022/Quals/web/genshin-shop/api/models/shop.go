package models

import "github.com/jinzhu/gorm"

type Product struct {
	gorm.Model
	Title       string `json:"title"`
	Description string `json:"description"`
	Banner      string `json:"banner"`
	Price       uint64 `json:"price"`
}

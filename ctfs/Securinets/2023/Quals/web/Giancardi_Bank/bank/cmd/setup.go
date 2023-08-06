package main

import (
	"go-get-it/config"
	"go-get-it/models"
)

func main() {
	config.MustInitDB()
	models.MustSeedDB()
}

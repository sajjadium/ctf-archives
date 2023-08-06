package config

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

type DBConnection struct {
	Conn *gorm.DB
}

var DB *DBConnection

func MustInitDB() {

	db, err := gorm.Open(sqlite.Open("db/db.sqlite"), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})

	if err != nil {
		panic("failed to connect database")
	}

	DB = &DBConnection{db}
}

func (db *DBConnection) Close() error {
	sqlDB, err := db.Conn.DB()
	if err != nil {
		return err
	}
	return sqlDB.Close()
}

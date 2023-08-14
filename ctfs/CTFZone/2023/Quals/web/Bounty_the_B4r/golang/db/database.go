package db

import (
	"fmt"
	"os"
	"time"

	"github.com/google/uuid"
	"gorm.io/driver/postgres"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Database struct {
	Impl *gorm.DB
}

func Connect() (*Database, error) {
	var impl *gorm.DB
	var err error
	if os.Getenv("IS_PROD") != "" {
		const (
			ENV_DB_USER = "DB_USER"
			ENV_DB_PASS = "DB_PASS"
			ENV_DB_HOST = "DB_HOST"
			ENV_DB_PORT = "DB_PORT"
			ENV_DB_NAME = "DB_NAME"
		)

		dbUsername := os.Getenv(ENV_DB_USER)
		dbPassword := os.Getenv(ENV_DB_PASS)
		dbHost := os.Getenv(ENV_DB_HOST)
		dbPort := os.Getenv(ENV_DB_PORT)
		dbName := os.Getenv(ENV_DB_NAME)

		dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable", dbHost, dbUsername, dbPassword, dbName, dbPort)
		impl, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
		if err != nil {
			return nil, err
		}
	} else {
		impl, err = gorm.Open(sqlite.Open("test.sqlite"), &gorm.Config{})
		if err != nil {
			return nil, err
		}
	}

	return &Database{impl}, nil
}

func (db Database) CreateReport(title string, description string, programId string, severity string, weakness string, reporter uint64) (*Report, error) {
	var bbProgram BBProgram
	res := db.Impl.First(&bbProgram, "id = ?", programId)
	if res.Error != nil {
		return nil, fmt.Errorf("error inserting report to the db: %v", res.Error)
	}
	if res.RowsAffected != 1 {
		return nil, fmt.Errorf("this program doesn't exist")
	}

	now := time.Now().UnixNano()
	rUUID, err := uuid.NewUUID()
	if err != nil {
		return nil, err
	}
	report := Report{
		UUID:        rUUID.String(),
		Title:       title,
		Description: description,
		Program:     programId,
		Severity:    severity,
		Weakness:    weakness,
		Published:   now,
		Reporter:    reporter,
	}

	res = db.Impl.Create(&report)

	if res.Error != nil || res.RowsAffected != 1 {
		return nil, fmt.Errorf("error inserting report to the db: %v", res.Error)
	}

	return &report, nil

}

func (db Database) InitPublicPrograms() error {
	var anyPubProgram BBProgram
	res := db.Impl.Where("type = 0").Find(&anyPubProgram)

	if res.RowsAffected == 0 {
		prUUID, err := uuid.NewUUID()
		if err != nil {
			return err
		}

		pubProgram := BBProgram{
			ID:   prUUID.String(),
			Name: "Hooli Public BB Program",
			Type: ProgramTypePublic,
		}

		res = db.Impl.Create(&pubProgram)
		if res.Error != nil || res.RowsAffected != 1 {
			return fmt.Errorf("error inserting program to the db: %v", res.Error)
		}

	}

	return nil
}

func (db Database) InitFlagReport(flag string) error {
	var report Report
	res := db.Impl.First(&report, "id = ?", 1)

	// First run, create the flag report
	if res.RowsAffected == 0 {
		prUUID, err := uuid.NewUUID()
		if err != nil {
			return err
		}

		program := BBProgram{
			ID:   prUUID.String(),
			Name: "CTFZone Private Program",
			Type: ProgramTypePrivate,
		}

		res = db.Impl.Create(&program)
		if res.Error != nil || res.RowsAffected != 1 {
			return fmt.Errorf("error inserting program to the db: %v", res.Error)
		}

		_, err = db.CreateReport(
			"Very Secret Report~",
			"Flag: "+flag,
			program.ID,
			"Critical",
			"CWE-1",
			7446744073709551610,
		)
		if err != nil {
			return nil
		}
	}
	return nil
}

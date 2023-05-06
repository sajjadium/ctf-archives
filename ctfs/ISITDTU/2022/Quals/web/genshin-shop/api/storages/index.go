package storages

import (
	"encoding/json"
	"os"

	"github.com/ks75vl/genshin-shop-api/models"
	"gorm.io/gorm"
)

type Storage struct {
	conn *gorm.DB
}

type StorageInterface interface {
	Begin() (StorageInterface, error)
	Commit()
	Rollback()
	Migration(dst ...interface{}) error
}

type ProductStorageInterface interface {
	StorageInterface
	GetAllProductsId() (*[]uint, error)
	GetProductById(id uint) (*models.Product, error)
}

func NewStorage(conn *gorm.DB) *Storage {
	return &Storage{conn: conn}
}

func (s *Storage) Begin() (StorageInterface, error) {
	tx := s.conn.Begin()
	if tx.Error != nil {
		return nil, tx.Error
	}
	return NewStorage(tx), nil
}

func (s *Storage) Commit() {
	s.conn.Commit()
}

func (s *Storage) Rollback() {
	s.conn.Rollback()
}

func (s *Storage) Migration(dst ...interface{}) error {
	var defaultProduct []models.Product
	var data []byte
	var e error

	if e = s.conn.AutoMigrate(dst...); e != nil {
		return e
	}

	if data, e = os.ReadFile("default.json"); e != nil {
		return e
	}
	if e = json.Unmarshal(data, &defaultProduct); e != nil {
		return e
	}

	return s.conn.Save(defaultProduct).Error
}

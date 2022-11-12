package storages

import (
	"github.com/jinzhu/gorm"
	"github.com/ks75vl/genshin-shop-api/models"
)

func (s *Storage) GetAllProductsId() (*[]uint, error) {
	ret := make([]uint, 0)
	return &ret, s.conn.Model(&models.Product{}).Select("id").Find(&ret).Error
}

func (s *Storage) GetProductById(id uint) (*models.Product, error) {
	ret := &models.Product{Model: gorm.Model{ID: id}}
	return ret, s.conn.Model(ret).First(ret).Error
}

package api

import (
	"github.com/ks75vl/genshin-shop-api/models"
	"github.com/ks75vl/genshin-shop-api/storages"
	"go.uber.org/zap"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

func (a *api) setupStorage() bool {
	conn, e := gorm.Open(mysql.Open(a.config.MySql.ToDSN()), &gorm.Config{
		DisableNestedTransaction: true,
	})
	if e != nil {
		a.logger.Error("can not setup storage", zap.Error(e))
		return false
	}
	sqlDB, e := conn.DB()
	if e != nil {
		a.logger.Error("can not configure storage", zap.Error(e))
		return false
	}
	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetMaxOpenConns(100)

	a.storage = storages.NewStorage(conn)
	if e := a.storage.Migration(&models.Product{}); e != nil {
		a.logger.Error("can not initialize storage", zap.Error(e))
		return false
	}

	return true
}

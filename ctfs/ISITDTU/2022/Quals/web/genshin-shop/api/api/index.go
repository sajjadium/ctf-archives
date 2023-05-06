package api

import (
	"context"

	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"github.com/ks75vl/genshin-shop-api/configs"
	"github.com/ks75vl/genshin-shop-api/storages"
	"go.uber.org/zap"
)

type api struct {
	router  *gin.Engine
	config  *configs.YamlConfig
	logger  *zap.Logger
	context context.Context
	storage *storages.Storage
}

type HttpCommonHdlInterface interface {
	parseHttpRequet(t interface{}, b binding.Binding) func(c *gin.Context)
	authorizeHeader(key, value string) func(*gin.Context)
}

type HttpCtfHdlInterface interface {
	genshinShop1Flag(c *gin.Context)
	feedback(c *gin.Context)
}

type HttpProductHdlInterface interface {
	getAllProduct(c *gin.Context)
	getProductById(c *gin.Context)
	advertise(c *gin.Context)
}

type ApiErrorInterface interface {
	apiStorageError(c *gin.Context, e error)
	apiBadRequest(c *gin.Context, e error)
	apiNotFound(c *gin.Context, message string)
	apiUnauthorized(c *gin.Context)
}

type ApiInterface interface {
	Run() bool
	Setup() bool
	Release() bool
}

func New(config *configs.YamlConfig) ApiInterface {
	return &api{
		config: config,
	}
}

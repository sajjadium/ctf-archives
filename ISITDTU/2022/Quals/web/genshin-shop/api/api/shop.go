package api

import (
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/ks75vl/genshin-shop-api/models"
	"github.com/ks75vl/genshin-shop-api/storages"
	"gorm.io/gorm"
)

type advertiseReq struct {
	Url string `form:"url" binding:"required"`
}

type getAllProductReq struct{}

type getProductByIdReq struct {
	Id uint `form:"id" binding:"required"`
}

func (a *api) advertise(c *gin.Context) {
	req, ok := c.Value(HttpParsedRequestCtxKey).(*advertiseReq)
	if !ok {
		c.AbortWithStatus(http.StatusBadRequest)
		return
	}

	c.Redirect(http.StatusFound, req.Url)
}

func (a *api) genshinShop1Flag(c *gin.Context) {
	c.AbortWithStatusJSON(http.StatusOK, gin.H{"_genshin_shop_1": a.config.Flag.GenshinShop1})
}

func (a *api) getAllProduct(c *gin.Context) {
	var productStorage storages.ProductStorageInterface = a.storage
	var h ApiErrorInterface = a
	var ret *[]uint
	var e error

	_, ok := c.Value(HttpParsedRequestCtxKey).(*getAllProductReq)
	if !ok {
		c.AbortWithStatus(http.StatusBadRequest)
		return
	}

	if ret, e = productStorage.GetAllProductsId(); e != nil {
		h.apiStorageError(c, e)
		return
	}

	c.JSON(http.StatusOK, *ret)
}

func (a *api) getProductById(c *gin.Context) {
	var productStorage storages.ProductStorageInterface = a.storage
	var h ApiErrorInterface = a
	var req *getProductByIdReq
	var ret *models.Product
	var e error
	var ok bool

	if req, ok = c.Value(HttpParsedRequestCtxKey).(*getProductByIdReq); !ok {
		h.apiBadRequest(c, errors.New("can not parse request"))
		return
	}

	if ret, e = productStorage.GetProductById(req.Id); e != nil && !errors.Is(e, gorm.ErrRecordNotFound) {
		h.apiStorageError(c, e)
		return
	}
	if e != nil {
		h.apiNotFound(c, "product not found")
		return
	}

	c.JSON(http.StatusOK, ret)
}

package api

import (
	"context"
	"net/http"
	"reflect"

	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"go.uber.org/zap"
)

type ginContextKey uint32

const HttpParsedRequestCtxKey ginContextKey = 0x92200010
const HttpFlagLengthCtxKey ginContextKey = 0x92200011

func (a *api) parseHttpRequet(t interface{}, b binding.Binding) func(c *gin.Context) {
	return func(c *gin.Context) {
		var h ApiErrorInterface = a

		// Parse req.
		req := reflect.New(reflect.TypeOf(t).Elem()).Interface()
		if e := c.ShouldBindWith(req, b); e != nil {
			h.apiBadRequest(c, e)
			return
		}

		// Assign to gin context.
		ctx := context.Background()
		ctx = context.WithValue(ctx, HttpParsedRequestCtxKey, req)
		c.Request = c.Request.Clone(ctx)

		// Next middleware.
		c.Next()
	}
}

func (a *api) authorizeHeader(key, value string) func(*gin.Context) {
	return func(c *gin.Context) {
		var h ApiErrorInterface = a

		if v := c.GetHeader(key); v != value {
			h.apiUnauthorized(c)
			return
		}

		c.Next()
	}
}

func (a *api) apiStorageError(c *gin.Context, e error) {
	a.logger.Error("storage error", zap.Error(e))
	c.JSON(http.StatusOK, gin.H{
		"error":   http.StatusInternalServerError,
		"message": http.StatusText(http.StatusInternalServerError),
	})
}

func (a *api) apiBadRequest(c *gin.Context, e error) {
	a.logger.Warn("bad request", zap.Error(e))
	c.AbortWithStatusJSON(http.StatusOK, gin.H{
		"error":   http.StatusBadRequest,
		"message": e.Error(),
	})
}

func (a *api) apiNotFound(c *gin.Context, message string) {
	c.AbortWithStatusJSON(http.StatusOK, gin.H{
		"error":   http.StatusNotFound,
		"message": message,
	})
}

func (a *api) apiUnauthorized(c *gin.Context) {
	c.AbortWithStatusJSON(http.StatusOK, gin.H{
		"error":   http.StatusUnauthorized,
		"message": http.StatusText(http.StatusUnauthorized),
	})
}

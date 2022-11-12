package api

import (
	"time"

	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"go.uber.org/zap"
)

func (a *api) setupHttp() bool {
	var r *gin.Engine = a.router
	var p HttpProductHdlInterface = a
	var c HttpCommonHdlInterface = a
	var f HttpCtfHdlInterface = a

	r.SetTrustedProxies(nil)
	r.Use(func(c *gin.Context) {
		start := time.Now()
		path := c.Request.URL.Path
		query := c.Request.URL.RawQuery
		c.Next()
		cost := time.Since(start)
		a.logger.Info(path,
			zap.Int("status", c.Writer.Status()),
			zap.String("method", c.Request.Method),
			zap.String("path", path),
			zap.String("query", query),
			zap.String("ip", c.ClientIP()),
			zap.String("user-agent", c.Request.UserAgent()),
			zap.String("errors", c.Errors.ByType(gin.ErrorTypePrivate).String()),
			zap.Duration("cost", cost),
		)

	})
	r.Use(gin.Recovery())

	r.GET("/advertise", c.parseHttpRequet(&advertiseReq{}, binding.Query), p.advertise)
	r.GET("/products", c.parseHttpRequet(&getAllProductReq{}, binding.Query), p.getAllProduct)
	r.GET("/product", c.parseHttpRequet(&getProductByIdReq{}, binding.Query), p.getProductById)
	r.GET("/flag", c.authorizeHeader("X-FLAG-KEY", "4FC20F2F-9970-42B6-824B-D9BEBB10315C"), f.genshinShop1Flag)
	r.POST("/feedback", c.parseHttpRequet(&feedbackReq{}, binding.JSON), f.feedback)

	return true
}

func (a *api) serveHTTP() error {
	err := make(chan error)
	go func() {
		err <- a.router.Run(a.config.Http.ToString())
	}()

	select {
	case <-a.context.Done():
		return a.context.Err()
	case e := <-err:
		return e
	}
}

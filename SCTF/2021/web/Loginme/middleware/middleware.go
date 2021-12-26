package middleware

import (
	"github.com/gin-gonic/gin"
)

func LocalRequired() gin.HandlerFunc {
	return func(c *gin.Context) {
		if c.GetHeader("x-forwarded-for") != "" || c.GetHeader("x-client-ip") != "" {
			c.AbortWithStatus(403)
			return
		}
		ip := c.ClientIP()
		if ip == "127.0.0.1" {
			c.Next()
		} else {
			c.AbortWithStatus(401)
		}
	}
}

package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
    "github.com/REDACTED/REDACTED"
)

func main() {
    router := gin.Default()
    router.StaticFile("/", "./index.html")
    router.POST("/parse", parse)
    router.Run("0.0.0.0:8080")
}

func parse(c *gin.Context) {
    buf ,err := c.GetRawData()
    if(err != nil){
        c.IndentedJSON(http.StatusBadRequest, err.Error())
        return
    }
    jsonStr, err := REDACTED.REDACTED().REDACTED("ctf", string(buf[:]))
    if err != nil {
        c.IndentedJSON(http.StatusInternalServerError, err.Error())
        return
    }
    c.IndentedJSON(http.StatusOK, jsonStr)
}

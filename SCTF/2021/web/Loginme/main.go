package main

import (
	"html/template"
	"loginme/middleware"
	"loginme/route"
	"loginme/templates"

	"github.com/gin-gonic/gin"
)

func main() {
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()
	templ := template.Must(template.New("").ParseFS(templates.Templates, "*.tmpl"))
	r.SetHTMLTemplate(templ)

	r.Use(gin.Logger())
	r.Use(gin.Recovery())
	authorized := r.Group("/admin")
	authorized.Use(middleware.LocalRequired())
	{
		authorized.GET("/index", route.Login)
	}

	r.GET("/", route.Index)
	r.Run(":9999")
}

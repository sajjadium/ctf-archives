package main

import (
	"fmt"
	"github.com/beego/beego/v2/server/web"
	"net/http/httputil"
	"net/url"
)

type MainController struct {
	web.Controller
}

func (this *MainController) Get() {
	this.Ctx.WriteString("OK")
}

func (this *MainController) Put() {
	targetURL := "http://python-microservice/"
	url, err := url.Parse(targetURL)
	if err != nil {
		panic(fmt.Sprintf("failed to parse the URL: %v", err))
	}
	proxy := httputil.NewSingleHostReverseProxy(url)
	proxy.ServeHTTP(this.Ctx.ResponseWriter, this.Ctx.Request)
}

func main() {
	web.Router("/", &MainController{})
	web.Run()
}

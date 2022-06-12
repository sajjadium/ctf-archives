package main

import (
	"math/rand"
	"os"
	"time"

	"github.com/kataras/iris/v12"
	"github.com/kataras/iris/v12/middleware/accesslog"
)

const defaultFormatter = "{{.Now.Format .TimeFormat}}|{{.Code}}|{{.Method}}|{{.Path}}|{{.IP}}|{{.Request}}\n"

var AccessLog *accesslog.AccessLog

func init() {
	rand.Seed(time.Now().UnixNano())
}

var letterRunes = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

// RandStringRunes Generate a random string
func RandStringRunes(n int) string {
	b := make([]rune, n)
	for i := range b {
		b[i] = letterRunes[rand.Intn(len(letterRunes))]
	}
	return string(b)
}

// initialize access log
func makeAccessLog() {
	AccessLog = accesslog.File("./access.log")
	AccessLog.AddOutput(os.Stdout)
	AccessLog.SetFormatter(&accesslog.Template{Text: defaultFormatter})
}

func main() {
	app := iris.New()
	tmpl := iris.HTML("./views", ".html")
	app.RegisterView(tmpl)
	makeAccessLog()
	app.UseRouter(AccessLog.Handler)
	app.Get("/", indexHandler)
	app.Get("/start", startLoggingHandler)
	app.HandleDir("/logs", iris.Dir("./logs"))
	app.Listen(":80")
}

func indexHandler(ctx iris.Context) {
	ctx.View("index.html")
}

func startLoggingHandler(ctx iris.Context) {
	formatter := ctx.URLParamDefault("formatter", defaultFormatter)
	if formatter == "" {
		formatter = defaultFormatter
	}
	logPath := "logs/" + RandStringRunes(10)
	f, err := os.Create(logPath)
	if err != nil {
		ctx.WriteString("failed")
		return
	}
	AccessLog.SetFormatter(&accesslog.Template{Text: formatter})
	AccessLog.SetOutput(f)
	ctx.Redirect(logPath)
}

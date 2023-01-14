package main

import (
	"errors"
	"fmt"
	"html/template"
	"io"
	"net/http"
	"os"

	"github.com/google/uuid"
	"github.com/gorilla/sessions"
	"github.com/labstack/echo-contrib/session"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	_ "github.com/mattn/go-sqlite3"
)

type Template struct {
	templates *template.Template
}

func (t *Template) Render(w io.Writer, name string, data interface{}, c echo.Context) error {
	return t.templates.ExecuteTemplate(w, name, data)
}

func ensureDir(dirName string) error {
	err := os.Mkdir(dirName, os.ModeDir|0666)
	if err == nil {
		return nil
	}
	if os.IsExist(err) {
		info, err := os.Stat(dirName)
		if err != nil {
			return err
		}
		if !info.IsDir() {
			return errors.New("path exists but is not a directory")
		}
		return nil
	}
	return err
}

func isValidUUID(u string) bool {
	_, err := uuid.Parse(u)
	return err == nil
}

func isLoggedIn(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		sess, _ := session.Get("session", c)
		if auth, ok := sess.Values["loggedIn"].(bool); !ok || !auth {
			return c.JSON(http.StatusOK, map[string]interface{}{
				"message": "failed",
				"path":    "/?message=Please+Login+First",
			})
		}

		return next(c)
	}
}

func main() {
	e := echo.New()

	// e.Debug = true

	e.Use(session.Middleware(sessions.NewCookieStore([]byte(os.Getenv("SESSION_KEY")))))
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	e.Use(middleware.SecureWithConfig(middleware.SecureConfig{
		XSSProtection:         "1; mode=block",
		ContentTypeNosniff:    "nosniff",
		XFrameOptions:         "",
		HSTSMaxAge:            0,
		ContentSecurityPolicy: "default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'self' http://" + os.Getenv("PUBLIC_DOMAIN_FRONTEND") + ":1337 http://frontend.magic.world:1337",
	}))

	e.Use(middleware.BodyLimit("20K"))
	e.Use(middleware.CSRFWithConfig(middleware.CSRFConfig{
		TokenLookup:    "form:_csrf,header:X-CSRF-TOKEN",
		CookieHTTPOnly: true,
	}))
	t := &Template{
		templates: template.Must(template.ParseGlob("public/*.html")),
	}
	e.Renderer = t

	e.Static("/assets", "public/assets/")
	e.File("/", "public/index.html")

	e.POST("/register", registerHandler)
	e.POST("/login", loginHandler)

	e.GET("/auth", func(c echo.Context) error {
		data := map[string]interface{}{
			"csrf": c.Get(middleware.DefaultCSRFConfig.ContextKey).(string),
		}
		return c.Render(http.StatusOK, "login-register.html", data)
	})

	e.GET("/upload.html", func(c echo.Context) error {

		data := map[string]interface{}{
			"csrf": c.Get(middleware.DefaultCSRFConfig.ContextKey).(string),
		}
		return c.Render(http.StatusOK, "upload.html", data)

	}, isLoggedIn)

	e.POST("/upload", uploadHandler, isLoggedIn)

	e.Any("/file/:uuid/:filename", viewFileHandler, isLoggedIn)

	e.GET("/myfiles", getAllOwnedFilesHandler, isLoggedIn)

	e.Any("/isLoggedIn", func(c echo.Context) error {
		sess, _ := session.Get("session", c)
		if auth, ok := sess.Values["loggedIn"].(bool); !ok || !auth {
			return c.JSON(http.StatusOK, map[string]interface{}{
				"message": "failed",
				"path":    "/?message=Hello+Guest!",
			})
		}

		return c.JSON(http.StatusOK, map[string]interface{}{
			"message": "success",
			"path":    fmt.Sprintf("/?message=Hello+%s!", sess.Values["username"].(string)),
		})
	})

	e.Logger.Fatal(e.Start("localhost:1234"))
}

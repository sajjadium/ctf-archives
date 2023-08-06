package main

import (
	"log"

	"go-get-it/config"
	"go-get-it/controllers"
	"go-get-it/models"
	"go-get-it/sessions"

	"github.com/gofiber/fiber/v2/middleware/logger"

	"github.com/gofiber/template/html/v2"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
)

// User struct (replace this with your actual user model)
type User struct {
	ID       int
	Username string
	Password string
}

func init() {
	config.MustInitLogger()
	sessions.MustInitRedisStore()
	config.MustInitCache(1)
	config.MustInitDB()
	models.MustSeedDB()

}
func main() {
	defer config.Cache.Close()
	defer config.DB.Close()
	defer sessions.RSS.Storage.Close()

	// Load HTML templates
	engine := html.New("./templates", ".html")
	app := fiber.New(fiber.Config{
		AppName:                 "Go Get It",
		EnablePrintRoutes:       true,
		EnableIPValidation:      true,
		Views:                   engine,
		EnableTrustedProxyCheck: true,
	})

	app.Use(cors.New())
	app.Use(logger.New(logger.Config{
		Format: "[${ip}]:${port} ${status} - ${method} ${path}\n",
	}))

	// Routes
	controllers.RegisterGuestHandler(app)
	controllers.RegisterAccountHandler(app)
	controllers.RegisterAdminHandler(app)
	controllers.RegisterUserHandler(app)
	controllers.RegisterTransactionsHandlers(app)
	controllers.RegisterAuthHandler(app)

	// Static files
	app.Static("/static", "./static")
	app.Static("/uploads", "./uploads")

	// Start the server
	log.Fatal(app.Listen(":3000"))
}

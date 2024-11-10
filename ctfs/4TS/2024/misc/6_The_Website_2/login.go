package web

import (
	"fil-rouge/internal/db"
	"net/http"

	"github.com/labstack/echo/v4"
)

type LoginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func Login(s *Server) func(c echo.Context) error {
	return func(c echo.Context) error {
		var req LoginRequest
		if err := c.Bind(&req); err != nil {
			return err
		}

		// Get the user from database
		var user db.User
		db.DB.QueryRow("SELECT * FROM users WHERE login = '"+req.Username+"' AND password = '"+req.Password+"'").Scan(&user.ID, &user.Login, &user.IsAdmin, &user.Password)

		return c.JSON(http.StatusServiceUnavailable, map[string]interface{}{
			"status":  "error",
			"message": "I could contact the database but the service is down, come back later",
		})
	}
}

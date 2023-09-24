package web

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"dictionary/internal/storage"

	"github.com/gin-gonic/gin"
)

// Server is the API web server.
type Server struct {
	wordStorage *storage.Genji
	httpServer  *http.Server
}

// NewServer initializes a new Server using the specified word storage.
func NewServer(wordStorage *storage.Genji) *Server {
	gin.SetMode(gin.ReleaseMode)

	server := &Server{
		wordStorage: wordStorage,
	}

	engine := gin.New()
	engine.StaticFile("/", "./front/dist/index.html")
	engine.Static("/assets", "./front/dist/assets")
	engine.GET("/api/exists", server.existsHandler)

	server.httpServer = &http.Server{
		Addr:              ":8000",
		ReadHeaderTimeout: time.Second * 2,
		IdleTimeout:       time.Minute,
		Handler:           http.TimeoutHandler(engine, time.Second*10, "timed out"),
	}

	return server
}

// ListenAndServe runs ListenAndServe on the underlying http.Server.
func (s *Server) ListenAndServe() error {
	if err := s.httpServer.ListenAndServe(); err != nil {
		return fmt.Errorf("serving HTTP: %w", err)
	}

	return nil
}

// Shutdown performs a graceful shutdown of the HTTP server with a timeout.
func (s *Server) Shutdown() error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := s.httpServer.Shutdown(ctx); err != nil {
		return fmt.Errorf("shuttind down server: %w", err)
	}

	return nil
}

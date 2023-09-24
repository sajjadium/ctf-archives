package web

import (
	"blog/internal/storage"
	"context"
	"errors"
	"fmt"
	"io/fs"
	"log/slog"
	"os"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/encryptcookie"
)

type blogRepository interface {
	SaveBlog(ctx context.Context, b *storage.Blog) error
	GetBlog(ctx context.Context, blogID string) (*storage.Blog, error)
}

type reviewQueue interface {
	EnqueueReview(ctx context.Context, blogID string) error
}

// Server handles HTTP requests, including the frontend static and the API.
type Server struct {
	app        *fiber.App
	repository blogRepository
	queue      reviewQueue
	logger     *slog.Logger
}

// NewServer initializes a new HTTP server which will use the specified components for handling requests.
func NewServer(repository blogRepository, queue reviewQueue, secretKeyPath string) (*Server, error) {
	s := &Server{
		repository: repository,
		queue:      queue,
		app: fiber.New(fiber.Config{
			AppName:                      "picoblog",
			CaseSensitive:                true,
			DisablePreParseMultipartForm: true,
			DisableStartupMessage:        true,
			StrictRouting:                true,
		}),
		logger: slog.With("component", "web"),
	}

	secretKey, err := readOrGenerateSecret(secretKeyPath)
	if err != nil {
		return nil, err
	}

	s.app.Use(encryptcookie.New(encryptcookie.Config{
		Key: secretKey,
	}))

	s.app.Use(func(ctx *fiber.Ctx) error {
		ctx.Set(fiber.HeaderXFrameOptions, "DENY")
		ctx.Set(fiber.HeaderContentSecurityPolicy, "frame-ancestors 'none';")
		return ctx.Next()
	})

	s.app.Route("/api", func(router fiber.Router) {
		router.Use(cookieMiddleware)
		router.Post("/blogs", s.createBlog)
		router.Post("/posts", s.createPost)
		router.Get("/user", s.getUserInfo)
		router.Post("/review", s.reviewBlog)
	})

	s.app.Get("/", sendIndex)
	s.app.Get("/blog/*", sendIndex)
	s.app.Static("/css", "front/build/css")
	s.app.Static("/_app", "front/build/_app")

	return s, nil
}

// Listen sets up a new listener and runs the HTTP server on it,
// accepting connections in the current goroutine.
func (s *Server) Listen(addr string) error {
	if err := s.app.Listen(addr); err != nil {
		return fmt.Errorf("listening on %s: %w", addr, err)
	}

	return nil
}

// Shutdown shuts down the server with the specified timeout.
func (s *Server) Shutdown(timeout time.Duration) error {
	if err := s.app.ShutdownWithTimeout(timeout); err != nil {
		return fmt.Errorf("shutting down app: %w", err)
	}

	return nil
}

func sendIndex(ctx *fiber.Ctx) error {
	return ctx.SendFile("front/build/index.html")
}

func readOrGenerateSecret(path string) (string, error) {
	data, err := os.ReadFile(path)
	if err == nil {
		return string(data), nil
	} else if !errors.Is(err, fs.ErrNotExist) {
		return "", fmt.Errorf("reading secret key from file: %w", err)
	}

	key := encryptcookie.GenerateKey()

	if err := os.WriteFile(path, []byte(key), 0400); err != nil {
		return "", fmt.Errorf("writing secret key to file: %w", err)
	}

	return key, nil
}

package main

import (
	"blog/internal/review"
	"blog/internal/storage"
	"blog/internal/web"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"log/slog"
)

const (
	gracefulShutdownTimeout  = time.Second * 10
	componentShutdownTimeout = time.Second * 5
)

func main() {
	slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, nil)))

	if err := mainErr(); err != nil {
		slog.Error("encountered fatal error", "error", err)
		os.Exit(1)
	}
}

func mainErr() error {
	listenAddr := os.Getenv("LISTEN_ADDR")
	secretPath := os.Getenv("SECRET_PATH")
	s3Endpoint := os.Getenv("S3_ENDPOINT")
	s3KeyID := os.Getenv("S3_KEY_ID")
	s3SecretKey := os.Getenv("S3_SECRET_KEY")
	s3Bucket := os.Getenv("S3_BUCKET")
	redisAddr := os.Getenv("REDIS_ADDR")

	storage, err := storage.NewS3Storage(s3Endpoint, s3KeyID, s3SecretKey, s3Bucket)
	if err != nil {
		return fmt.Errorf("initializing storage: %w", err)
	}

	queue := review.NewQueue(redisAddr, "blogs")

	server, err := web.NewServer(storage, queue, secretPath)
	if err != nil {
		return fmt.Errorf("initializing web server: %w", err)
	}

	slog.Info("running web server", "addr", listenAddr)

	serverErrCh := make(chan error)
	go func() {
		serverErrCh <- server.Listen(listenAddr)
	}()

	shutdown := make(chan os.Signal, 1)
	signal.Notify(shutdown, os.Interrupt, syscall.SIGTERM)

	var runtimeErr error
	select {
	case runtimeErr = <-serverErrCh:
		slog.Error("unexpected web server error, performing shutdown", "error", runtimeErr)
	case <-shutdown:
		slog.Info("performing graceful shutdown")
	}

	done := make(chan bool, 1)
	go func() {
		defer close(done)

		if err := server.Shutdown(componentShutdownTimeout); err != nil {
			slog.Error("unexpected error while shutting down web server", "error", err)
		}
	}()

	select {
	case <-done:
	case <-time.After(gracefulShutdownTimeout):
		slog.Warn("graceful shutdown timed out, forcefully shutting everything down")
	}

	return runtimeErr
}

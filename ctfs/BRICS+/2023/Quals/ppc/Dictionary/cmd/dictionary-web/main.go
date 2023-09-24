package main

import (
	"errors"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"dictionary/internal/flags"
	"dictionary/internal/storage"
	"dictionary/internal/web"
	"dictionary/words"

	"golang.org/x/exp/slog"
)

func main() {
	slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, nil)))

	if err := run(); err != nil {
		slog.Error("encountered fatal error", "error", err)
		os.Exit(1)
	}
}

func run() error {
	slog.Info("began database initialization")

	flag := os.Getenv("FLAG")
	if flag == "" {
		return errors.New("flag is empty")
	}

	flagParts := flags.Split(flag, 32, 40)

	// Initialize dictionaries with word loader and flag parts
	genjiStorage, err := storage.OpenGenji("genjidb")
	if err != nil {
		return fmt.Errorf("opening storage: %w", err)
	}

	defer genjiStorage.Close()

	if err := genjiStorage.Initialize(words.List, flagParts); err != nil {
		return fmt.Errorf("initializing storage: %w", err)
	}

	slog.Info("database initialized successfully")

	// Initialize and run HTTP server
	server := web.NewServer(genjiStorage)
	webCh := make(chan error, 1)

	slog.Info("running web server")
	go func() {
		webCh <- server.ListenAndServe()
	}()

	// Wait for graceful shutdown or server error
	shutdown := make(chan os.Signal, 1)
	signal.Notify(shutdown, os.Interrupt, syscall.SIGTERM)

	var webErr error
	select {
	case webErr = <-webCh:
		slog.Error("unexpected web server error, performing shutdown", "error", err)
	case <-shutdown:
		slog.Info("performing graceful shutdown")
	}

	// Perform graceful shutdown
	done := make(chan bool, 1)
	go func() {
		defer close(done)

		if err := server.Shutdown(); err != nil {
			slog.Error("unexpected error while shutting down web server", "error", err)
		}
	}()

	select {
	case <-done:
	case <-time.After(10 * time.Second):
		slog.Warn("server shutdown timed out")
	}

	return webErr
}

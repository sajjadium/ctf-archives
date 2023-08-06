package config

import (
	"log"
	"os"
	"time"
)

type Logger struct {
	logPath string
	file    *os.File
}

var CustomLogger *Logger

func MustInitLogger() {
	logPath := os.Getenv("LOG_PATH")
	if logPath == "" {
		logPath = "log.txt"
	}
	logger, err := NewLogger(logPath)
	if err != nil {
		panic(err)
	}
	CustomLogger = logger
}

func NewLogger(logPath string) (*Logger, error) {
	f, err := os.OpenFile(logPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return nil, err
	}
	return &Logger{logPath: logPath, file: f}, nil
}

func (l *Logger) Log(logMsg string) {
	logger := log.New(l.file, "", 0)
	logTime := time.Now().Format(time.RFC3339)
	logLine := "[" + logTime + "] " + logMsg
	logger.Println(logLine)
}

func (l *Logger) Close() error {
	err := l.file.Close()
	if err != nil {
		return err
	}
	return nil
}

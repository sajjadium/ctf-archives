package api

import (
	"log"
	"time"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

// Set logger.
func (a *api) setupLogger() bool {

	// 1. Create zap logger config.
	zapCfg := zap.Config{
		Encoding:    "console",
		Level:       zap.NewAtomicLevelAt(zap.InfoLevel),
		OutputPaths: []string{"stderr"},
		EncoderConfig: zapcore.EncoderConfig{
			MessageKey:   "message",
			TimeKey:      "time",
			LevelKey:     "level",
			CallerKey:    "caller",
			EncodeCaller: zapcore.FullCallerEncoder,
			EncodeLevel: func(level zapcore.Level, enc zapcore.PrimitiveArrayEncoder) {
				enc.AppendString("[" + level.CapitalString() + "]")
			},
			EncodeTime: func(t time.Time, enc zapcore.PrimitiveArrayEncoder) {
				enc.AppendString(t.Format("2006-01-02 15:04:05"))
			},
		},
	}

	// 2. Create zap logger.
	var e error
	a.logger, e = zapCfg.Build()
	if e != nil {
		log.Printf("Can not create logger, e=%v\n", e)
		return false
	}

	// 3. Return.
	return true
}

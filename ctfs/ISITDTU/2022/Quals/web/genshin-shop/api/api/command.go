package api

import (
	"context"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"golang.org/x/sync/errgroup"
)

func (a *api) Setup() bool {
	a.router = gin.New()
	a.router.ContextWithFallback = true

	if ok := a.setupLogger(); !ok {
		return false
	}

	if ok := a.setupStorage(); !ok {
		return false
	}

	if ok := a.setupHttp(); !ok {
		return false
	}

	return true
}

func (a *api) Run() bool {
	var g *errgroup.Group
	g, a.context = errgroup.WithContext(context.Background())

	// Run HTTP.
	g.Go(a.serveHTTP)

	// Check error.
	if e := g.Wait(); e != nil {
		a.logger.Error("can not run service", zap.Error(e))
		return false
	}

	return true
}

func (a *api) Release() bool {
	if a.logger != nil {
		a.logger.Sync()
	}
	return true
}

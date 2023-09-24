package web

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"golang.org/x/exp/slog"
)

func (s *Server) existsHandler(ctx *gin.Context) {
	word := ctx.Query("word")

	exists, err := s.wordStorage.WordExists(word)
	if err != nil {
		slog.Error("unexpected error running WordExists", "error", err)

		ctx.Status(http.StatusInternalServerError)
		return
	}

	if exists {
		ctx.Status(http.StatusOK)
	} else {
		ctx.Status(http.StatusNotFound)
	}
}

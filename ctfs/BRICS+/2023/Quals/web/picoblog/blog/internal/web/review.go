package web

import (
	"net/http"

	"github.com/gofiber/fiber/v2"
)

// reviewBlog runs the blog reviewal process on the user's blog.
func (s *Server) reviewBlog(ctx *fiber.Ctx) error {
	blogIDVal := ctx.Locals(blogIDLocalsKey{})
	if blogIDVal == nil {
		return fiber.ErrUnauthorized
	}

	blogID, ok := blogIDVal.(string)
	if !ok {
		s.logger.Error("blog ID context value isn't a string", "blog_id_val", blogIDVal)
		return fiber.ErrInternalServerError
	}

	if err := s.queue.EnqueueReview(ctx.Context(), blogID); err != nil {
		s.logger.Error("queueing blog for review", "blog_id", blogID, "error", err)
		return fiber.ErrInternalServerError
	}

	ctx.Status(http.StatusOK)
	return nil
}

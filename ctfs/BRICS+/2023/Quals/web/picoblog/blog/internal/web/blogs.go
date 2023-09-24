package web

import (
	"blog/internal/markup"
	"blog/internal/storage"
	"errors"

	"github.com/gofiber/fiber/v2"
)

// createBlog initializes a new blog and sets a cookie allowing the user to administer said the new blog.
func (s *Server) createBlog(ctx *fiber.Ctx) error {
	req := new(createBlogRequest)
	if err := ctx.BodyParser(req); err != nil || !req.validate() {
		return fiber.ErrBadRequest
	}

	blogID, cookie := generateBlogID()
	blog := &storage.Blog{
		ID:    blogID,
		Name:  req.Name,
		Posts: []storage.Post{},
	}

	repoErr := s.repository.SaveBlog(ctx.Context(), blog)
	if err := s.handleRepoError(blogID, repoErr); err != nil {
		return err
	}

	s.logger.Info("initialized new blog", "blog_id", blogID)
	ctx.Cookie(cookie)

	return ctx.JSON(createBlogResponse{BlogID: blogID})
}

// createPost adds a new post to a user's blog.
func (s *Server) createPost(ctx *fiber.Ctx) error {
	req := new(createPostRequest)
	if err := ctx.BodyParser(req); err != nil || !req.validate() {
		return fiber.ErrBadRequest
	}

	blogIDVal := ctx.Locals(blogIDLocalsKey{})
	if blogIDVal == nil {
		return fiber.ErrUnauthorized
	}

	blogID, ok := blogIDVal.(string)
	if !ok {
		s.logger.Error("blog ID context value isn't a string", "blog_id_val", blogIDVal)
		return fiber.ErrInternalServerError
	}

	repoBlog, repoErr := s.repository.GetBlog(ctx.Context(), blogID)
	if err := s.handleRepoError(blogID, repoErr); err != nil {
		return err
	}

	repoBlog.Posts = append(repoBlog.Posts, storage.Post{
		Title:   req.Title,
		Content: markup.ToHTML(req.Content),
	})

	repoErr = s.repository.SaveBlog(ctx.Context(), repoBlog)
	if err := s.handleRepoError(blogID, repoErr); err != nil {
		return err
	}

	return nil
}

// getUserInfo returns information about the current user.
func (s *Server) getUserInfo(ctx *fiber.Ctx) error {
	blogIDVal := ctx.Locals(blogIDLocalsKey{})
	if blogIDVal == nil {
		return fiber.ErrUnauthorized
	}

	blogID, ok := blogIDVal.(string)
	if !ok {
		s.logger.Error("blog ID context value isn't a string", "blog_id_val", blogIDVal)
		return fiber.ErrInternalServerError
	}

	return ctx.JSON(getUserInfoResponse{BlogID: blogID})
}

func (s *Server) handleRepoError(blogID string, err error) error {
	if err == nil {
		return nil
	}

	if errors.Is(err, storage.ErrTooLarge) {
		return fiber.ErrInsufficientStorage
	} else if errors.Is(err, storage.ErrNotExists) {
		return fiber.ErrNotFound
	}

	s.logger.Error("unexpected error from repository", "blog_id", blogID, "error", err)
	return fiber.ErrInternalServerError
}

package web

import (
	"encoding/base32"

	"github.com/gofiber/fiber/v2"
	"gitlab.com/NebulousLabs/fastrand"
)

const (
	blogCookieName = "blog"
	blogIDLength   = 20
)

type blogIDLocalsKey struct{}

var idEncoding = base32.StdEncoding.WithPadding(base32.NoPadding)

func generateBlogID() (string, *fiber.Cookie) {
	blogID := idEncoding.EncodeToString(fastrand.Bytes(blogIDLength))
	return blogID, &fiber.Cookie{
		Name:  blogCookieName,
		Value: blogID,
		// Secure:   true,
		HTTPOnly: true,
		SameSite: fiber.CookieSameSiteStrictMode,
	}
}

func cookieMiddleware(ctx *fiber.Ctx) error {
	blogID := ctx.Cookies(blogCookieName)
	if blogID != "" {
		ctx.Locals(blogIDLocalsKey{}, blogID)
	}

	return ctx.Next()
}

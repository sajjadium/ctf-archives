package render

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
	"github.com/go-rod/rod/lib/proto"
)

type Renderer interface {
	RenderStory(ctx context.Context, tenantID string, storyID int64) ([]byte, error)
}

type renderer struct {
	url  string
	flag string
}

func (e *renderer) RenderStory(ctx context.Context, tenantID string, storyID int64) ([]byte, error) {

	path, _ := launcher.LookPath()
	launcher := launcher.New().Bin(path).Headless(true)
	u := launcher.MustLaunch()
	browser := rod.New().ControlURL(u).Trace(true).MustConnect()
	log.Printf("Rendering story %d to image", storyID)
	defer browser.MustClose()

	storyURL := getURL(e.url, storyID)

	browser.SetCookies([]*proto.NetworkCookieParam{
		{
			Name:  "tenantID",
			Value: tenantID,
			URL:   storyURL,
		},
		{
			Name:  "flag",
			Value: e.flag,
			URL:   storyURL,
		},
	})
	log.Printf("Opening story %d at %s", storyID, storyURL)
	page, err := browser.Timeout(5 * time.Second).Page(proto.TargetCreateTarget{URL: storyURL})
	if err != nil {
		return nil, fmt.Errorf("failed to open page: %w", err)
	}
	elem, err := page.Timeout(10 * time.Second).Element("#story-card")

	if err != nil {
		return nil, fmt.Errorf("failed to find element: %w", err)
	}
	buf, err := elem.Screenshot(proto.PageCaptureScreenshotFormatPng, 90)
	if err != nil {
		return nil, fmt.Errorf("failed to screenshot: %w", err)
	}

	log.Printf("Rendering story %d completed successfully", storyID)
	return buf, nil
}

func getURL(url string, storyID int64) string {
	return fmt.Sprintf("%s/render/%d", url, storyID)
}

// NewRenderer creates a new renderer
// frontendURL, for example "http://localhost:5173", is the base URL of the
// frontend.
func NewRenderer(frontendURL, flag string) Renderer {
	return &renderer{url: frontendURL, flag: flag}
}

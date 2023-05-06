package api

import (
	"context"
	"errors"
	"net/http"
	"net/url"
	"time"

	"github.com/chromedp/cdproto/cdp"
	"github.com/chromedp/cdproto/network"
	"github.com/chromedp/chromedp"
	"github.com/gin-gonic/gin"
)

type feedbackReq struct {
	Message string `json:"message" binding:"omitempty,required"`
	Url     string `json:"url" binding:"required"`
}

func createViewFeedbackTask(feedbackMessage, feedbackUrl string, origin *url.URL, cookies ...string) chromedp.Tasks {
	// Unused parameters
	_ = feedbackMessage

	// Return new task
	return chromedp.Tasks{
		chromedp.ActionFunc(func(ctx context.Context) error {
			expr := cdp.TimeSinceEpoch(time.Now().Add(180 * 24 * time.Hour))
			for i := 0; i < len(cookies); i += 2 {
				err := network.SetCookie(cookies[i], cookies[i+1]).
					WithExpires(&expr).
					WithDomain(origin.Hostname()).
					Do(ctx)
				if err != nil {
					return err
				}
			}
			return nil
		}),
		chromedp.Navigate(feedbackUrl),
	}
}

func (a *api) feedback(c *gin.Context) {
	var h ApiErrorInterface = a
	var feedbackUrl, origin *url.URL
	var e error

	req, ok := c.Value(HttpParsedRequestCtxKey).(*feedbackReq)
	if !ok {
		h.apiBadRequest(c, errors.New("bad request"))
		return
	}

	if len(req.Url) <= 0 {
		c.AbortWithStatusJSON(http.StatusOK, true)
		return
	}

	if feedbackUrl, e = url.Parse(req.Url); e != nil {
		h.apiBadRequest(c, e)
		return
	}

	if origin, e = url.Parse(a.config.Http.Origin); e != nil {
		h.apiBadRequest(c, e)
		return
	}

	if (feedbackUrl.Hostname() != origin.Hostname()) || (feedbackUrl.Port() != origin.Port()) || (feedbackUrl.Scheme != origin.Scheme) {
		h.apiBadRequest(c, errors.New("invalid origin"))
		return
	}

	go func(m, u string, o *url.URL, h, f string) {
		contexRemote, cancelRemote := chromedp.NewRemoteAllocator(context.Background(), h)
		context1, cancel1 := chromedp.NewContext(contexRemote)
		task := createViewFeedbackTask(m, u, o, "_genshin_shop_2", f)

		e := chromedp.Run(context1, task)
		if e != nil {
			return
		}

		// Waiting for a while.
		time.Sleep(time.Duration(a.config.ChromeDp.Lifespan) * time.Second)
		cancel1()
		cancelRemote()
	}(req.Message, feedbackUrl.String(), origin, a.config.ChromeDp.ToString(), a.config.Flag.GenshinShop2)

	c.AbortWithStatusJSON(http.StatusOK, true)
}

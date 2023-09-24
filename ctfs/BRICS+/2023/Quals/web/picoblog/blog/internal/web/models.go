package web

const (
	maxBlogNameLength    = 100
	maxPostTitleLength   = 100
	maxPostContentLength = 256
)

type createBlogRequest struct {
	Name string `json:"name"`
}

func (req *createBlogRequest) validate() bool {
	return len(req.Name) > 0 && len(req.Name) <= maxBlogNameLength
}

type createBlogResponse struct {
	BlogID string `json:"blog_id"`
}

type createPostRequest struct {
	Title   string `json:"title"`
	Content string `json:"content"`
}

func (req *createPostRequest) validate() bool {
	return len(req.Title) > 0 && len(req.Title) <= maxPostTitleLength && len(req.Content) > 0 && len(req.Content) <= maxPostContentLength
}

type getUserInfoResponse struct {
	BlogID string `json:"blog_id"`
}

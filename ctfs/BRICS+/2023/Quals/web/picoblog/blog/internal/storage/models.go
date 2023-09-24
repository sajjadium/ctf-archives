package storage

// Blog is a model describing a single blog.
type Blog struct {
	ID    string `json:"-"`
	Name  string `json:"name"`
	Posts []Post `json:"posts"`
}

// Post is a single blog post.
type Post struct {
	Title   string `json:"title"`
	Content string `json:"content"`
}

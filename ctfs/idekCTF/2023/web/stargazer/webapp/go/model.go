package main

type User struct {
	Username string `json:"username" form:"username"`
	Password string `json:"password" form:"password"`
}

type FilesUpload struct {
	UUID        string
	Title       string
	ContentType string
	Filename    string
	Username    string
}

package controller

import (
	"github.com/val1d/bb_ctf/db"
)

type server struct {
	db db.Database
}


func NewServer(db db.Database) *server {
	return &server{db: db}
}
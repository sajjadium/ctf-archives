package controller

import "net/http"

func getUserID(r *http.Request) uint64 {
	ctx := r.Context()
	uid := ctx.Value("user_id").(uint64)
	return uid
}
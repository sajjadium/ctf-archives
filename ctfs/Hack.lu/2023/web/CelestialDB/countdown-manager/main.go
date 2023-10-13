package main

import (
	"log"
	"net/http"
)

func main() {
	db := connectDb()
	defer db.Close()
	mux := setupRouter(db)
	log.Print("Listening...")
	http.ListenAndServe(":3000", mux)
}

package main

import (
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/jackc/pgx/v4/pgxpool"
)

func setupRouter(db *pgxpool.Pool) http.Handler {
	r := mux.NewRouter()

	// API
	setupAPI(r.PathPrefix("/api").Subrouter(), db)

	// serve static files
	r.PathPrefix("/").Handler(http.FileServer(http.Dir("./static/")))

	return r
}

func queryParam(r *http.Request, name string) string {
	return r.URL.Query().Get(name)
}

func send(w http.ResponseWriter, msg string) {
	w.Write([]byte(msg))
}

func sendError(w http.ResponseWriter, err error, prefix string) {
	send(w, prefix+": "+err.Error())
}

func sendJson(w http.ResponseWriter, data interface{}) error {
	return json.NewEncoder(w).Encode(data)
}

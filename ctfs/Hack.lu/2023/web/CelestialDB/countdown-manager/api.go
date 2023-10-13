package main

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/jackc/pgx/v4/pgxpool"
)

type Counter struct {
	Id        int64   `json:"id"`
	Name      string  `json:"name"`
	Count     int64   `json:"count"`
	CreatedAt string  `json:"createdAt"`
	CreatedBy string  `json:"createdBy"`
	UpdatedAt string  `json:"updatedAt"`
	UpdatedBy *string `json:"updatedBy"`
}

type CounterCreation struct {
	Name      string `json:"name"`
	Count     int64  `json:"count"`
	CreatedBy string `json:"createdBy"`
}

type CounterUpdate struct {
	Decrement *int64  `json:"decrement"`
	UpdatedBy *string `json:"updatedBy"`
}

func setupAPI(r *mux.Router, db *pgxpool.Pool) {
	r.HandleFunc("/counters", func(w http.ResponseWriter, r *http.Request) {
		counters, err := getAllCounters(db)
		if err != nil {
			sendError(w, err, "Query error")
			return
		}
		sendJson(w, counters)
	}).Methods("GET")

	r.HandleFunc("/counters", func(w http.ResponseWriter, r *http.Request) {
		var creation CounterCreation
		err := json.NewDecoder(r.Body).Decode(&creation)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		if creation.Name == "" {
			http.Error(w, "Name is required", http.StatusBadRequest)
			return
		}
		creation.Count = positiveInt(creation.Count)
		counter, err := createCounter(db, creation)
		if err != nil {
			sendError(w, err, "Create error")
			return
		}
		sendJson(w, counter)
	}).Methods("POST")

	r.HandleFunc("/counters/{id}", func(w http.ResponseWriter, r *http.Request) {
		id, err := strconv.ParseInt(mux.Vars(r)["id"], 10, 64)
		if err != nil {
			sendError(w, err, "Invalid id")
			return
		}
		counter, err := getCounter(db, id)
		if err != nil {
			sendError(w, err, "Query error")
			return
		}
		sendJson(w, counter)
	}).Methods("GET")

	r.HandleFunc("/counters/{id}", func(w http.ResponseWriter, r *http.Request) {
		id, err := strconv.ParseInt(mux.Vars(r)["id"], 10, 64)
		if err != nil {
			sendError(w, err, "Invalid id")
			return
		}
		var update CounterUpdate
		err = json.NewDecoder(r.Body).Decode(&update)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		var decr int64
		if update.Decrement != nil {
			decr = positiveInt(*update.Decrement)
		} else {
			decr = 1
		}
		var updateBy string
		if update.UpdatedBy != nil {
			updateBy = *update.UpdatedBy
		} else {
			updateBy = "anonymous"
		}
		counter, err := updateCounter(db, id, decr, updateBy)
		if err != nil {
			sendError(w, err, "Update error")
			return
		}
		sendJson(w, counter)
	}).Methods("PUT")

	r.HandleFunc("/counters/{id}", func(w http.ResponseWriter, r *http.Request) {
		id, err := strconv.ParseInt(mux.Vars(r)["id"], 10, 64)
		if err != nil {
			sendError(w, err, "Invalid id")
			return
		}
		err = deleteCounter(db, id)
		if err != nil {
			sendError(w, err, "Delete error")
			return
		}
		w.WriteHeader(http.StatusNoContent)
	}).Methods("DELETE")
}

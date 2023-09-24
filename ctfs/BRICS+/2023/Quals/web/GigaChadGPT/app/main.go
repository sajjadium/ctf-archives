package main

import (
	"context"
	"database/sql"
	"fmt"
	"github.com/francoispqt/gojay"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

type Query struct {
	Q         string `json:"q"`
	MaxTokens int    `json:"maxTokens"`
}

func (q *Query) UnmarshalJSONObject(dec *gojay.Decoder, key string) error {
	switch key {
	case "q":
		return dec.String(&q.Q)
	case "maxTokens":
		return dec.Int(&q.MaxTokens)
	}
	return nil
}
func (q *Query) NKeys() int {
	return 2
}

func main() {
	db, err := sql.Open("mysql", fmt.Sprintf("app:%s@tcp(db:3306)/app", os.Getenv("MYSQL_PASSWORD")))
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	http.HandleFunc("/api/predict", func(w http.ResponseWriter, request *http.Request) {
		ct := request.Header.Get("Content-Type")
		if ct != "application/json" {
			w.WriteHeader(http.StatusBadRequest)
			fmt.Fprintf(w, "Invalid request\n")
			return
		}

		var q Query
		dec := gojay.NewDecoder(request.Body)
		if err := dec.DecodeObject(&q); err != nil {
			w.WriteHeader(http.StatusBadRequest)
			log.Printf("Failed to decode json: %v", err)
			fmt.Fprintf(w, "Invalid request\n")
			return
		}

		ctx, cancel := context.WithTimeout(request.Context(), time.Second*3)
		defer cancel()
		rows, err := db.QueryContext(ctx, `SELECT reply FROM replies WHERE LOWER(prompt) LIKE '%`+strings.ToLower(q.Q)+`%' LIMIT 1`)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			log.Printf("Failed to query db: %v", err)
			fmt.Fprintf(w, "Failed to query db\n")
			return
		}
		defer rows.Close()

		var reply string
		if !rows.Next() {
			reply = "I'm a language model, I can't do it."
		} else {
			if err := rows.Scan(&reply); err != nil {
				log.Printf("Failed to scan db: %v", err)
			}
			// TODO: handle maxTokens param.
		}

		data, err := gojay.Marshal(reply)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			fmt.Fprintf(w, "Failed to encode json\n")
			return
		}

		w.WriteHeader(http.StatusOK)
		w.Write(data)
		return
	})
	log.Println(http.ListenAndServe(":5000", nil))
}

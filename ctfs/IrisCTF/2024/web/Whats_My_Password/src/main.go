package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"regexp"
	"syscall"

	_ "github.com/go-sql-driver/mysql"
)

var DB *sql.DB
var Mux = http.NewServeMux()
var UsernameRegex = `[^a-z0-9]`

type Account struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func startWeb() {
	fmt.Println("Starting very secure login panel (promise)")

	fs := http.FileServer(http.Dir("/home/user/web"))
	Mux.Handle("/", fs)

	Mux.HandleFunc("/api/login", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		var input Account

		decoder := json.NewDecoder(r.Body)
		decoder.Decode(&input)

		if input.Username == "" {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte("Missing Username"))
			return
		}
		if input.Password == "" {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte("Missing Password"))
			return
		}

		matched, err := regexp.MatchString(UsernameRegex, input.Username)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		if matched {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte("Username can only contain lowercase letters and numbers."))
			return
		}

		qstring := fmt.Sprintf("SELECT * FROM users WHERE username = \"%s\" AND password = \"%s\"", input.Username, input.Password)

		query, err := DB.Query(qstring)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			fmt.Println(err)
			return
		}
		defer query.Close()

		if !query.Next() {
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Invalid username / password combination!"))
			return
		}

		var result Account
		err = query.Scan(&result.Username, &result.Password)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			fmt.Println(err)
			return
		}
		encoded, err := json.Marshal(result)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			fmt.Println(err)
			return
		}

		w.Write(encoded)
	})

	http.ListenAndServe(":1337", Mux)
}

func main() {
	fmt.Println("Establishing connection to MySql")
	db, err := sql.Open("mysql", "readonly_user:password@tcp(127.0.0.1:3306)/uwu")
	if err != nil {
		fmt.Println(err)
		return
	}
	DB = db

	defer DB.Close()

	startWeb()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan
}

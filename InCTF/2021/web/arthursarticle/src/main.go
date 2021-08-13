package main

import (
	"crypto/md5"
	"encoding/hex"
	"flag"
	"fmt"
	"html"
	"log"
	"math/rand"
	"net/http"
	"os"
	"regexp"
	"strings"
	"time"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
)

const adminID = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
const adminNOTE = "inctf{flag}"

var Notes = make(map[string]string)

// Prevent XSS on api-endpoints ¬‿¬
var cType = map[string]string{
	"Content-Type":            "text/plain",
	"x-content-type-options":  "nosniff",
	"X-Frame-Options":         "DENY",
	"Content-Security-Policy": "default-src 'none';",
}

func cookGenerator() string {
	hash := md5.Sum([]byte(string(rand.Intn(30))))
	return hex.EncodeToString((hash)[:])
}

func headerSetter(w http.ResponseWriter, header map[string]string) {
	for k, v := range header {
		w.Header().Set(k, v)
	}
}

func getIDFromCooke(r *http.Request, w http.ResponseWriter) string {
	var cooke, err = r.Cookie("id")
	re := regexp.MustCompile("^[a-zA-Z0-9]+$")
	var cookeval string
	if err == nil && re.MatchString(cooke.Value) && len(cooke.Value) <= 35 && len(cooke.Value) >= 30 {
		cookeval = cooke.Value
	} else {
		cookeval = cookGenerator()
		c := http.Cookie{
			Name:     "id",
			Value:    cookeval,
			SameSite: 2,
			HttpOnly: true,
			Secure:   false,
		}
		http.SetCookie(w, &c)
	}
	return cookeval
}

func add(w http.ResponseWriter, r *http.Request) {

	id := getIDFromCooke(r, w)
	if id != adminID {
		r.ParseForm()
		noteConte := r.Form.Get("content")
		if len(noteConte) < 75 {
			Notes[id] = noteConte
		}
	}
	fmt.Fprintf(w, "OK")
}

func get(w http.ResponseWriter, r *http.Request) {
	id := getIDFromCooke(r, w)
	x := Notes[id]
	headerSetter(w, cType)
	if x == "" {
		fmt.Fprintf(w, "404 No Note Found")
	} else if regexp.MustCompile("<[a-zA-Z0-9]").MatchString(x) {
		fmt.Fprintf(w, html.EscapeString(x))
	} else {
		fmt.Fprintf(w, x)
	}
}

func find(w http.ResponseWriter, r *http.Request) {

	id := getIDFromCooke(r, w)

	param := r.URL.Query()
	x := Notes[id]

	var which string
	str, err := param["condition"]
	if !err {
		which = "any"
	} else {
		which = str[0]
	}

	var start bool
	str, err = param["startsWith"]
	if !err {
		start = strings.HasPrefix(x, "arthur")
	} else {
		start = strings.HasPrefix(x, str[0])
	}
	var responseee string
	var end bool
	str, err = param["endsWith"]
	if !err {
		end = strings.HasSuffix(x, "morgan")
	} else {
		end = strings.HasSuffix(x, str[0])
	}

	if which == "starts" && start {
		responseee = x
	} else if which == "ends" && end {
		responseee = x
	} else if which == "both" && (start && end) {
		responseee = x
	} else if which == "any" && (start || end) {
		responseee = x
	} else {
		_, present := param["debug"]
		if present {
			delete(param, "debug")
			delete(param, "startsWith")
			delete(param, "endsWith")
			delete(param, "condition")

			for v, d := range param {
				for _, k := range d {

					if regexp.MustCompile("^[a-zA-Z0-9{}_;-]*$").MatchString(k) && len(d) < 5 {
						w.Header().Set(v, k)
					}
					break
				}
				break
			}
		}
		responseee = "404 No Note Found"
	}
	headerSetter(w, cType)
	fmt.Fprintf(w, responseee)
}

// Reset notes every 30 mins.  No Vuln in this
func resetNotes() {
	Notes[adminID] = adminNOTE
	for range time.Tick(time.Second * 1 * 60 * 30) {
		Notes = make(map[string]string)
		Notes[adminID] = adminNOTE
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	var dir string
	flag.StringVar(&dir, "dir", "./public", "the directory to serve files from. Defaults to the current dir")
	flag.Parse()
	go resetNotes()
	r := mux.NewRouter()
	s := r.Host("chall.notepad15.gq:1515").Subrouter()
	s.HandleFunc("/add", add).Methods("POST")
	s.HandleFunc("/get", get).Methods("GET")
	s.HandleFunc("/find", find).Methods("GET")
	s.PathPrefix("/").Handler(http.StripPrefix("/", http.FileServer(http.Dir(dir))))
	fmt.Println("Server started at http://0.0.0.0:3000")
	loggedRouter := handlers.LoggingHandler(os.Stdout, r)
	srv := &http.Server{
		Addr: "0.0.0.0:3000",
		// Good practice to set timeouts to avoid Slowloris attacks.
		WriteTimeout: time.Second * 15,
		ReadTimeout:  time.Second * 15,
		IdleTimeout:  time.Second * 60,
		Handler:      loggedRouter, // Pass our instance of gorilla/mux in.
	}
	if err := srv.ListenAndServe(); err != nil {
		log.Println(err)
	}
}

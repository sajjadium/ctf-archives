package main

import (
	"os"
	"fmt"
	"log"
	"html"
	"time"
	"strconv"
	"net/http"
	"io/ioutil"
	"math/rand"
	"encoding/hex"
	"database/sql"
	"encoding/json"
	"html/template"
	"crypto/sha256"
	
	"github.com/gorilla/mux"
	"github.com/nu7hatch/gouuid"
	"github.com/gorilla/handlers"
	_ "github.com/mattn/go-sqlite3"
	"github.com/gomarkdown/markdown"
	
)

var indexTmpl = template.Must(template.ParseFiles("./templates/index.html"))
var previewTmpl = template.Must(template.ParseFiles("./templates/preview.html"))

type Unsanitized struct {
	Raw string `json:"raw"`
}

type Sanitized struct {
	Sanitized string `json:Sanitized`
	Raw string `json:Raw`
	Hash string `json:Hash`
}

type Preview struct {
	Error string
	Data template.HTML
}

type CreatePost struct {
	Raw string 
	Hash string
}

type Config struct {
	admin_bucket string
	admin_token string
	admin_hash string
	secret string
	modulus int
	seed int
	a int
	c int
}

var CONFIG Config
var db *sql.DB

func createToken() (string, string) {
	token, _ := uuid.NewV4()
	h := sha256.New()
    h.Write([]byte(token.String() + CONFIG.secret))
    sha256_hash := hex.EncodeToString(h.Sum(nil))
    return string(sha256_hash), token.String()
}

func verifyToken(token, input string) bool {
	h := sha256.New()
    h.Write([]byte(token  + CONFIG.secret))
    sha256_hash := hex.EncodeToString(h.Sum(nil))
	
	if string(sha256_hash) == input {
		return true
	} 
	return false
}

func getadminhash() string {
	token := CONFIG.admin_token
	h := sha256.New()
    h.Write([]byte(token + CONFIG.secret))
    sha256_hash := hex.EncodeToString(h.Sum(nil))
	log.Println("Generated admin's hash ", sha256_hash)
    return string(sha256_hash)
}

func save_post(bucket, data string) int {
	postid := ((CONFIG.seed * CONFIG.a) + CONFIG.c) % CONFIG.modulus
	CONFIG.seed = postid
	stmt, _ := db.Prepare("INSERT INTO posts(postid, bucket, note) VALUES (?, ?, ?)")
	stmt.Exec(postid, bucket, data)
	return postid
}

func sanitize(raw string) string {
	return html.EscapeString(raw)
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	indexTmpl.Execute(w, nil)
}

func previewHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	res := Preview{Error: "", Data: ""}

	postid, found := mux.Vars(r)["postid"]
	if found {
		bucketid := vars["bucketid"]
		fmt.Println("Requested for", bucketid, postid)
		id, _ := strconv.ParseInt(postid, 10, 64)
		rows, err := db.Query("SELECT note FROM posts WHERE bucket = ? AND postid = ?", bucketid, id)
		checkErr(err)

		counter := 0
		var note string

		for rows.Next(){
			if err := rows.Scan(&note); err != nil {
				log.Fatal("Unable to scan results:", err)
			}
			counter++
		}
		
		if counter == 0 {
			res = Preview{Error: "Note not found.", Data: ""}
		} else if counter != 1 {
			res = Preview{Error: "Could not find notes.", Data: ""}
		} else {
			res = Preview{Error: "", Data: template.HTML(note)}
		}
	} 
	previewTmpl.Execute(w, res)
}

func filterHandler(w http.ResponseWriter, r *http.Request) {
	reqBody, _ := ioutil.ReadAll(r.Body)
	w.Header().Set("Content-Type", "application/json")
	var unsanitized Unsanitized

	err := json.Unmarshal(reqBody, &unsanitized)

	if err != nil {
        
		log.Println("Error decoding JSON. err = %s", err)
        fmt.Fprintf(w, "Error decoding JSON.")
		
    } else {
		var cookie, isset = r.Cookie("Token") 
		
		hash, token := createToken()

		sanitized_data := markdown.ToHTML([]byte(sanitize(unsanitized.Raw)), nil, nil)

		if isset == nil {
			if cookie.Value == CONFIG.admin_token {
				hash = CONFIG.admin_hash
				token = CONFIG.admin_token
			}
		} 
		
		cookie = &http.Cookie{Name: "Token", Value: token, HttpOnly: true, Path: "/api"}
		result := Sanitized{Sanitized: string(sanitized_data), Raw: unsanitized.Raw, Hash: hash}
		http.SetCookie(w, cookie)
		json.NewEncoder(w).Encode(result)
	}
}

func createHandler(w http.ResponseWriter, r *http.Request) {
	reqBody, _ := ioutil.ReadAll(r.Body)
	w.Header().Set("Content-Type", "application/json")

	type Response struct {
		Status string
		PostId int
		Bucket string
	}
	var createpost CreatePost

	if json.Unmarshal(reqBody, &createpost) != nil {
        log.Println("There was an error decoding json. \n")
		json.NewEncoder(w).Encode(Response{Status: "Save Error"})
    } else {
		var cookie, err = r.Cookie("Token")

		if err == nil {
			var token = cookie.Value
			if verifyToken(token, createpost.Hash) || (createpost.Hash == CONFIG.admin_hash){
				bucket := CONFIG.admin_bucket
				data := createpost.Raw

				if createpost.Hash != CONFIG.admin_hash {
					id , _ := uuid.NewV4()
					bucket = id.String()
					data = string(markdown.ToHTML([]byte(sanitize(data)), nil, nil))
				} else {
					data = string(markdown.ToHTML([]byte(data), nil, nil))
				}
				
				postid := save_post(bucket, data)
				log.Println("Saved post to", postid)
				json.NewEncoder(w).Encode(Response{Status: "success", Bucket: bucket, PostId: postid})
			} else {
				log.Println("Verification failed for ", createpost.Hash, token)
				json.NewEncoder(w).Encode(Response{Status: "Token not verified"})
			}
		} else {
			json.NewEncoder(w).Encode(Response{Status: "Invalid body."})
		}
	}
}

func flag(w http.ResponseWriter, r *http.Request) {
	var cookie, err = r.Cookie("Token")
	res := Preview{Error: "", Data: "'"}
    if err == nil {
		if cookie.Value == CONFIG.admin_token {
			res.Data = template.HTML(CONFIG.admin_token)
		} else {
			res.Data = template.HTML("You are not admin.")
		}
	}
	previewTmpl.Execute(w, res)	
}

func debug(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
		type Response struct {
			Admin_bucket string
			VAL_A int
			VAL_B int
		}
	json.NewEncoder(w).Encode(Response{Admin_bucket: CONFIG.admin_bucket, VAL_A: CONFIG.a, VAL_B: CONFIG.c})
}

func clear_database() {
	for range time.Tick(time.Second * 1 * 60 * 30) {
		stmt, _ := db.Prepare("DELETE FROM posts")
		stmt.Exec()
		log.Println("Cleared database.")
	}
}

func handleRequests() {
	route := mux.NewRouter().StrictSlash(true)
	go clear_database()

	fs := http.FileServer(http.Dir("./static/"))
	route.PathPrefix("/static/").Handler(http.StripPrefix("/static/", fs))
	route.HandleFunc("/", indexHandler)
	route.HandleFunc("/demo",  previewHandler).Methods("GET")
	route.HandleFunc("/api/flag", flag).Methods("GET")
	route.HandleFunc("/api/filter", filterHandler).Methods("POST")
	route.HandleFunc("/api/create", createHandler).Methods("POST")
	route.HandleFunc("/{bucketid}/{postid}", previewHandler).Methods("GET")
	route.HandleFunc("/_debug",  debug).Methods("GET")

	loggedRouter := handlers.LoggingHandler(os.Stdout, route)
	srv := &http.Server{
		Addr: "0.0.0.0" + os.Getenv("PORT"),
		WriteTimeout: time.Second * 15,
        ReadTimeout:  time.Second * 15,
        IdleTimeout:  time.Second * 60,
        Handler:      loggedRouter,
	}

	if err := srv.ListenAndServe(); err != nil {
		log.Println(err)
	}
}

func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	db, _ = sql.Open("sqlite3", "./database.db")
	
	stmt, _ := db.Prepare("CREATE TABLE IF NOT EXISTS posts (postid, bucket, note)")
	stmt.Exec()

	stmt, _ = db.Prepare("DELETE FROM posts")
	stmt.Exec()

	a, _ := strconv.Atoi(os.Getenv("VAL_A"))
	c, _ := strconv.Atoi(os.Getenv("VAL_B"))

	CONFIG = Config{
		admin_bucket: os.Getenv("ADMIN_BUCKET"),
		admin_token: os.Getenv("FLAG"),
		secret: os.Getenv("SECRET"),
		admin_hash: getadminhash(), 
		modulus: 99999999999,
		seed: rand.Intn(9e15) + 1e15, 
		a: a, 
		c: c,
	}

	fmt.Println("App running on http://localhost", os.Getenv("PORT"))
	handleRequests()
}
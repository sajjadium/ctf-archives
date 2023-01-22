package main

import (
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/dgrijalva/jwt-go"
	_ "github.com/mattn/go-sqlite3"
)

var jwtKey = []byte("my_secret_key")

type Claims struct {
	Note string
	jwt.StandardClaims
}

type user struct {
	Username string `json:"username"`
	Password string `json:"password"`
	Notes    string `json:"note"`
	Key      string `json:"key"`
}

type user_query struct {
	Username string `json:"username"`
	Password string `json:"password"`
	Key      string `json:"key"`
}

func generateJWT(w http.ResponseWriter, r *http.Request, data string) {

	expirationTime := time.Now().Add(170 * time.Hour)
	claims := &Claims{
		Note: data,
		StandardClaims: jwt.StandardClaims{

			ExpiresAt: expirationTime.Unix(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	tokenString, err := token.SignedString(jwtKey)

	if err != nil {

		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	http.SetCookie(w, &http.Cookie{
		Name:     "token",
		Value:    tokenString,
		Expires:  expirationTime,
		HttpOnly: true,
		Secure:   true,
		SameSite: http.SameSiteNoneMode,
	})
}

func addUserNotes(db *sql.DB, newPerson user) {
	if newPerson.Username == "" || newPerson.Password == "" || newPerson.Notes == "" || newPerson.Key == "" {
		return
	}
	stmt, _ := db.Prepare("INSERT INTO user_notes (id, username, password, note, key) VALUES (?, ?, ?, ?, ?)")
	stmt.Exec(nil, newPerson.Username, newPerson.Password, newPerson.Notes, newPerson.Key)
	defer stmt.Close()

	fmt.Printf("Added %v %v \n", newPerson.Username, newPerson.Key)
}

func getUserNotes(db *sql.DB, query user_query) string {

	row := db.QueryRow("select note from user_notes where username=? and password=? and key=?", query.Username, query.Password, query.Key)
	var note string
	row.Scan(&note)
	return note
}

func search(w http.ResponseWriter, req *http.Request) {

	c, err := req.Cookie("token")
	if err != nil {
		if err == http.ErrNoCookie {
			w.WriteHeader(http.StatusUnauthorized)
			return
		}
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	tknStr := c.Value

	Note_Data := &Claims{}

	tkn, err := jwt.ParseWithClaims(tknStr, Note_Data, func(token *jwt.Token) (interface{}, error) {
		return jwtKey, nil
	})
	if err != nil {
		if err == jwt.ErrSignatureInvalid {
			w.WriteHeader(http.StatusUnauthorized)
			return
		}
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	if !tkn.Valid {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}
	search_value := req.URL.Query()["query"]
	if len(search_value[0]) < 0 {
		return
	}

	hint := req.URL.Query()["hint"]
	if len(hint[0]) < 0 {
		return
	}
	// hint about note
	var with_hint string
	if len(hint[0]) > 0 {
		with_hint = with_hint + Note_Data.Note
		for i := range hint[0] {
			with_hint = with_hint + string(hint[0][i])
		}
	}

	if search_value[0] == Note_Data.Note[0:len(search_value[0])] {
		var cont_len int
		retrived := Note_Data.Note[0:len(search_value[0])]
		cont_len = len(retrived)
		w.Header().Set("Content-Length", strconv.Itoa(cont_len))
		w.Write([]byte(retrived))
	} else {
		var cont_len int
		cont_len = len(hint[0]) + 5                                 // +5 use to "Hint:"
		given_hint := with_hint[len(Note_Data.Note):len(with_hint)] //slicing the hint from note_data and hint
		w.Header().Set("Content-Length", strconv.Itoa(cont_len))
		w.Write([]byte("Hint:" + given_hint))
	}
}
func errorResponse(w http.ResponseWriter, message string, httpStatusCode int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(httpStatusCode)
	resp := make(map[string]string)
	resp["message"] = message
	jsonResp, _ := json.Marshal(resp)
	w.Write(jsonResp)
}
func generate_note(w http.ResponseWriter, req *http.Request) {
	var p user
	headerContentTtype := req.Header.Get("Content-Type")
	if headerContentTtype != "application/json" {
		errorResponse(w, "Content Type is not application/json", http.StatusUnsupportedMediaType)
		return
	}
	var unmarshalErr *json.UnmarshalTypeError

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&p)
	if err != nil {
		if errors.As(err, &unmarshalErr) {
			errorResponse(w, "Bad Request. Wrong Type provided for field "+unmarshalErr.Field, http.StatusBadRequest)
		} else {
			errorResponse(w, "Bad Request "+err.Error(), http.StatusBadRequest)
		}
		return
	}
	errorResponse(w, "Success", http.StatusOK)
	db, err := sql.Open("sqlite3", "user_notes")
	if err != nil {
		errorResponse(w, "Bad Request "+err.Error(), http.StatusBadRequest)
	}
	addUserNotes(db, p)
}

func retriveUseNote(w http.ResponseWriter, req *http.Request) {
	var q user_query
	headerContentTtype := req.Header.Get("Content-Type")
	if headerContentTtype != "application/json" {
		errorResponse(w, "Content Type is not application/json", http.StatusUnsupportedMediaType)
		return
	}
	var unmarshalErr *json.UnmarshalTypeError

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&q)
	if err != nil {
		if errors.As(err, &unmarshalErr) {
			errorResponse(w, "Bad Request. Wrong Type provided for field "+unmarshalErr.Field, http.StatusBadRequest)
		} else {
			errorResponse(w, "Bad Request "+err.Error(), http.StatusBadRequest)
		}
		return
	}
	db, err := sql.Open("sqlite3", "user_notes")
	if err != nil {
		errorResponse(w, "Bad Request "+err.Error(), http.StatusBadRequest)
	}
	data := getUserNotes(db, q)
	if len(data) > 0 {
		generateJWT(w, req, data)
	}
	resp := make(map[string]string)
	var newUrl string
	newUrl = "/search?query=bi0s&hint=" + "length of your note is " + strconv.Itoa(len(data))
	resp["url"] = newUrl
	jsonResp, err := json.Marshal(resp)
	w.Write(jsonResp)
}

func home(w http.ResponseWriter, req *http.Request) {
	content, _ := os.ReadFile("index.html")
	w.Write(content)
}
func about(w http.ResponseWriter, req *http.Request) {
	content, _ := os.ReadFile("about.html")
	w.Write(content)
}
func main() {
	const RESOURCE_DIR = "/resources/"
	http.HandleFunc("/", home)
	http.HandleFunc("/about", about)
	http.HandleFunc("/generate", generate_note)
	http.HandleFunc("/getnotes", retriveUseNote)
	http.HandleFunc("/search", search)

	var HandlerResources = http.StripPrefix(RESOURCE_DIR,
		http.FileServer(http.Dir("."+RESOURCE_DIR)),
	)
	http.Handle(RESOURCE_DIR, HandlerResources)
	log.Fatal(http.ListenAndServe(":2222", nil))
}

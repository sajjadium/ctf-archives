package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/buger/jsonparser"
	"github.com/gomodule/redigo/redis"
)

func update_password(id int, username string, password string) error {
	conn, err := redis.Dial("tcp", "manager_users:6379")
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Do("SET", strconv.Itoa(id), fmt.Sprintf("%s,%s", username, password))
	return err
}

func get_user(id int) (name string, ok bool) {
	conn, err := redis.Dial("tcp", "manager_users:6379")
	if err != nil {
		return "", false
	}
	defer conn.Close()
	s_id := strconv.Itoa(id)
	str, err := redis.String(conn.Do("GET", s_id))
	if err != nil {
	    return "", false
	}
	return strings.Split(str, ",")[0], true
}

func update(w http.ResponseWriter, req *http.Request) {
	body, err := io.ReadAll(req.Body)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	uid, err := jsonparser.GetInt(body, "id")
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	username, ok := get_user(int(uid))
	if !ok {
		fmt.Fprintf(w, `{"error": "Invalid UID"}`)
	} else {
		password, err := jsonparser.GetString(body, "password")
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
		err = update_password(int(uid), username, password)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
		fmt.Fprintf(w, `{"msg": "Password successfully updated"}`)
	}

}

func main() {
	http.HandleFunc("/", update)
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal(err)
	}
}

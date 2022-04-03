package main

import (
	"fmt"
	"net/http"
	"os/exec"
	"regexp"
)

import (
	"github.com/gorilla/mux"
)

func detonate(w http.ResponseWriter, r *http.Request) {
	fn_arg := r.URL.Query().Get("name")
	reg, err := regexp.Compile("[^a-zA-Z0-9]+")
	if err != nil {
		return
	}
	fn := reg.ReplaceAllString(fn_arg, "")

	c := exec.Command("/detonations/" + fn)
	_ = c.Run()
}

func logRequest(handler http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("%s %s %s\n", r.RemoteAddr, r.Method, r.URL)
		handler.ServeHTTP(w, r)
	})
}

func main() {
	fmt.Println("[+] Started webserver ")

	router := mux.NewRouter()
	router.HandleFunc("/detonate", detonate).Methods("GET")

	http.ListenAndServe(":9000", logRequest(router))
}

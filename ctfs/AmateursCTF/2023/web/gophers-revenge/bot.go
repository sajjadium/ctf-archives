package main

import (
	"bytes"
	"crypto/rand"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"

	"git.mills.io/prologic/go-gopher"
)

var flag = []byte{}

func randomString(length int) string {
	b := make([]byte, length+2)
	rand.Read(b)
	return fmt.Sprintf("%x", b)[2 : length+2]
}

func main() {
	content, err := os.ReadFile("flag.txt")
	if err != nil {
		log.Fatal(err)
	}
	flag = content

	http.HandleFunc("/submit", Submit)
	http.HandleFunc("/", Index)
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}

func Index(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "index.html")
}

func Submit(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	u, err := url.Parse(r.Form.Get("url"))
	if err != nil || u.Host != "amt.rs:31290" {
		w.Write([]byte("Invalid url"))
		return
	}

	w.Write([]byte(Visit(r.Form.Get("url"))))
}

func Visit(gopherURL string) string {
	fmt.Println(gopherURL)
	res, err := gopher.Get(gopherURL)
	if err != nil {
		return fmt.Sprintf("Something went wrong: %s", err.Error())
	}

	rawURL, _ := strings.CutPrefix(res.Dir.Items[2].Selector, "URL:")
	fmt.Println(rawURL)

	u, err := url.Parse(rawURL)
	if err != nil || !strings.HasSuffix(u.Host, "amt.rs") {
		return "Invalid url"
	}

	resp, err := http.Post(u.String(), "application/x-www-form-urlencoded", bytes.NewBuffer([]byte(fmt.Sprintf("username=%s&password=%s", randomString(20), flag))))

	if err != nil {
		return "Failed to make request"
	}

	cookies := resp.Cookies()
	token := ""
	for _, c := range cookies {
		if c.Name == "token" {
			token = c.Value
		}
	}

	if token != "" {
		return fmt.Sprintf("Thanks for sending in a flag! Use the following token once i get the gopher-catcher frontend setup: %s", token)
	} else {
		return "Something went wrong, my sever should have sent a cookie back but it didn't..."
	}
}

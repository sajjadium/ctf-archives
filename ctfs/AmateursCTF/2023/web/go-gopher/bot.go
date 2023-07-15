package main

import (
	"bytes"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"

	"git.mills.io/prologic/go-gopher"
)

var flag = []byte{}

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
	if err != nil || !strings.HasPrefix(u.Host, "amt.rs") {
		w.Write([]byte("Invalid url"))
		return
	}

	w.Write([]byte(Visit(r.Form.Get("url"))))
}

func Visit(url string) string {
	fmt.Println(url)
	res, err := gopher.Get(url)
	if err != nil {
		return fmt.Sprintf("Something went wrong: %s", err.Error())
	}
	h, _ := res.Dir.ToText()
	fmt.Println(string(h))

	url, _ = strings.CutPrefix(res.Dir.Items[2].Selector, "URL:")
	fmt.Println(url)
	_, err = http.Post(url, "text/plain", bytes.NewBuffer(flag))

	if err != nil {
		return "Failed to make request"
	}

	return "Successful visit"
}

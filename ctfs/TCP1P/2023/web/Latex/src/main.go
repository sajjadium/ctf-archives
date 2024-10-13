package main

import (
	"embed"
	"net/http"
	"strings"

	"github.com/rwestlund/gotex"
)

var (
	//go:embed static/*
	static    embed.FS
	blacklist = []string{"\\input", "include", "newread", "openin", "file", "read", "closein",
		"usepackage", "fileline", "verbatiminput", "url", "href", "text", "write",
		"newwrite", "outfile", "closeout", "immediate", "|", "write18", "includegraphics",
		"openout", "newcommand", "expandafter", "csname", "endcsname", "^^"}
)

func readstatic(s string) []byte {
	file, _ := static.ReadFile("static/" + s)
	return file
}

func isSecure(s string) bool {
	for _, keyword := range blacklist {
		if strings.Contains(s, keyword) {
			return false
		}
	}
	return true
}

func main() {
	go func() {
		http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
			if r.Method == "GET" {
				w.Write(readstatic("index.html"))
			} else if r.Method == "POST" {
				latex := r.FormValue("latex")
				if latex == "" || !(isSecure(latex)) {
					w.Write(readstatic("index.html"))
					return
				}
				pdf, err := gotex.Render(latex, gotex.Options{})
				if err != nil {
					http.Error(w, err.Error(), http.StatusInternalServerError)
					return
				}
				w.Header().Add("Content-Type", "application/pdf")
				w.Write(pdf)
			} else {
				http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
			}
		})
		http.ListenAndServe(":8080", nil)
	}()
	select {}
}

package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"strings"
)

func isStringSafe(s string) bool {
	alpha := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \t\n\r"
	for _, c := range s {
		if !strings.ContainsRune(alpha, c) {
			return false
		}
	}
	return true
}

func isSafeJson(j any) bool {
	switch v := j.(type) {
	case string:
		return isStringSafe(v)
	case []any:
		out := true
		for _, lv := range v {
			out = isSafeJson(lv) && out
		}
		return out
	case map[string]any:
		out := true
		for _, mv := range v {
			out = isSafeJson(mv) && out
		}
		return out
	}
	return true
}

func trySanitizeJson(r *http.Request) bool {
	var j any
	var buf bytes.Buffer
	tee := io.TeeReader(r.Body, &buf)
	defer func() {
		r.Body.Close()
		r.Body = io.NopCloser(&buf)
	}()
	if err := json.NewDecoder(tee).Decode(&j); err != nil {
		return true
	}

	return isSafeJson(j)
}

func main() {
	ph := os.Getenv("PROXY_HOST")
	u, err := url.Parse(ph)
	if err != nil {
		log.Fatal(err)
	}

	rp := httputil.NewSingleHostReverseProxy(u)
	http.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
		ct := request.Header.Get("Content-Type")
		if ct == "application/json" {
			safe := trySanitizeJson(request)
			if !safe {
				writer.WriteHeader(http.StatusBadRequest)
				fmt.Fprintf(writer, "No hacking please")
				return
			}
		}
		rp.ServeHTTP(writer, request)
	})
	log.Println(http.ListenAndServe(":5001", nil))
}

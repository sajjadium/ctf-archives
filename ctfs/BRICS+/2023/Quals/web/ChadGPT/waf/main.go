package main

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"strings"
)

func sqlSafe(s string) string {
	s = strings.ReplaceAll(s, "'", "''")
	s = strings.ReplaceAll(s, "\"", "\"\"")
	return s
}

func safeJsonStringValue(j any) any {
	switch v := j.(type) {
	case string:
		return sqlSafe(v)
	case []any:
		var out []any
		for _, lv := range v {
			out = append(out, safeJsonStringValue(lv))
		}
		return out
	case map[string]any:
		var out = make(map[string]any)
		for mk, mv := range v {
			out[mk] = safeJsonStringValue(mv)
		}
		return out
	}
	return j
}

func trySanitizeJson(r *http.Request) (bool, []byte) {
	var j any
	var buf bytes.Buffer
	tee := io.TeeReader(r.Body, &buf)
	defer func() {
		r.Body.Close()
		r.Body = io.NopCloser(&buf)
	}()
	if err := json.NewDecoder(tee).Decode(&j); err != nil {
		return false, nil
	}

	j = safeJsonStringValue(j)
	newJsonBody, err := json.Marshal(j)
	if err != nil {
		return false, nil
	}

	return true, newJsonBody
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
			san, newJsonBody := trySanitizeJson(request)
			if san {
				request.Body = io.NopCloser(bytes.NewReader(newJsonBody))
				request.ContentLength = int64(len(newJsonBody))
			}
		}
		rp.ServeHTTP(writer, request)
	})
	log.Println(http.ListenAndServe(":5001", nil))
}

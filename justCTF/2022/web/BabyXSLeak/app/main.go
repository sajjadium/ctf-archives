package main

import (
	"log"
	"net"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

func isPrivateIP(ipStr string) bool {
	ipv4 := net.ParseIP(ipStr)
	return ipv4.IsPrivate() || ipv4.IsLoopback()
}

func getIP(r *http.Request) string {
	ipStr, _, _ := net.SplitHostPort(r.RemoteAddr)
	return ipStr
}

func CSPMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		begin := time.Now()
		defer func() {
			log.Printf("request ip=%s method=%s duration=%s url=%q\n", r.RemoteAddr, r.Method, time.Now().Sub(begin), r.RequestURI)
		}()

		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("Content-Security-Policy", "script-src 'none';")
		w.Header().Set("Content-Type", "text/plain")
		next.ServeHTTP(w, r)
	})
}

func handleIndex(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Please leak admin flag!"))
}

func handleSearch(w http.ResponseWriter, r *http.Request, flag string) {
	query := r.URL.Query().Get("search")
	msg := r.URL.Query().Get("msg")

	if !strings.Contains(flag, query) {
		w.Write([]byte("Not found"))
	} else {
		w.Write(append([]byte(msg), flag...))
	}
}

func handleBot(w http.ResponseWriter, r *http.Request) {
	url := r.URL.Query().Get("url") // http://192.168.69.69/search/?search=foo&msg=bar
	if err := RunBot(url); err != nil {
		log.Printf("RunBot url=%q err=%+v\n", url, err)
	}
}

func main() {
	flagStr := os.Getenv("FLAG")

	mux := http.NewServeMux()
	mux.HandleFunc("/", handleIndex)
	mux.HandleFunc("/search/", func(w http.ResponseWriter, r *http.Request) {
		if !isPrivateIP(getIP(r)) {
			w.WriteHeader(http.StatusForbidden)
			return
		}
		handleSearch(w, r, flagStr)
	})
	mux.HandleFunc("/debug/", func(w http.ResponseWriter, r *http.Request) {
		handleSearch(w, r, "justCTF{fake_flags}")
	})

	rateLimitBot := make(map[string]time.Time)
	muRateLimitBot := &sync.Mutex{}

	mux.HandleFunc("/bot/", func(w http.ResponseWriter, r *http.Request) {
		isRateLimit := func() bool {
			muRateLimitBot.Lock()
			defer muRateLimitBot.Unlock()

			ip := getIP(r)
			lastRequest, ok := rateLimitBot[ip]
			if !ok {
				rateLimitBot[ip] = time.Now()
			} else if lastRequest.Add(time.Second * 30).After(time.Now()) {
				return true
			} else {
				rateLimitBot[ip] = time.Now()
			}
			return false
		}()

		if isRateLimit {
			w.WriteHeader(http.StatusTooManyRequests)
			return
		}

		handleBot(w, r)
	})

	log.Println("Server listening")
	err := http.ListenAndServe(":80", CSPMiddleware(mux))
	if err != nil {
		panic(err)
	}
}

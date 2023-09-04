package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
)

var (
	port = flag.Int("port", 8081, "The port to listen on")
)

func main() {

	flag.Parse()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		xff := r.Header.Values("X-Forwarded-For")

		ip := strings.Split(r.RemoteAddr, ":")[0]

		if xff != nil {
			ips := strings.Split(xff[len(xff)-1], ", ")
			ip = ips[len(ips)-1]
			ip = strings.TrimSpace(ip)
		}

		if ip != "31.33.33.7" {
			message := fmt.Sprintf("untrusted IP: %s", ip)
			http.Error(w, message, http.StatusForbidden)
			return
		} else {
			w.Write([]byte(os.Getenv("FLAG")))
		}
	})

	log.Printf("Listening on port %d", *port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", *port), nil))
}

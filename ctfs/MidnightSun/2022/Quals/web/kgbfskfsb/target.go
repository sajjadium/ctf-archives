package main

import (
	"crypto/sha1"
	"fmt"
	"golang.org/x/crypto/pbkdf2"
	"io/ioutil"
	"net"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"strings"
)

import (
	"github.com/gorilla/mux"
)

func welcome(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("<!DOCTYPE html><img width=\"1024\" src=\"nord.jpg\"/><body></body></html>"))
}

func img(w http.ResponseWriter, r *http.Request) {
	blyat, _ := os.ReadFile("nord.jpg")
	w.Write([]byte(blyat))
}

func scan_url(w http.ResponseWriter, r *http.Request) {
	fwdAddress := r.Header.Get("X-Forwarded-For")
	if fwdAddress == "" {
		fmt.Println("you need a proxy")
		return
	}

	ipAddress := fwdAddress
	xips := strings.Split(fwdAddress, ", ")
	if len(xips) > 1 {
		ipAddress = xips[0]
	}

	if ipAddress != "95.173.136.70" && ipAddress != "95.173.136.71" && ipAddress != "95.173.136.72" {
		fmt.Println("the proxy needs to come from inside the house")
		return
	}

	url_arg := r.URL.Query().Get("url")

	u, err := url.Parse(url_arg)
	if err != nil {
		fmt.Println(err)
		return
	}

	ips, err := net.LookupIP(u.Host)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Could not get IPs: %v for %v\n", err, u.Host)
		return
	}

	_, fsb1, _ := net.ParseCIDR("213.24.76.0/24")
	_, fsb2, _ := net.ParseCIDR("213.24.77.0/24")

	proceed := false
	for _, ip := range ips {
		if fsb1.Contains(ip) || fsb2.Contains(ip) {
			proceed = true
			break
		}
	}

	if !proceed {
		fmt.Println("Unauthorized mission file")
		return
	}

	dk := pbkdf2.Key([]byte(url_arg), []byte("volodya"), 2*1000*1000, 32, sha1.New)
	fmt.Println("DK", dk)

	client := &http.Client{}
	req, err := http.NewRequest("GET", url_arg, nil)
	if err != nil {
		fmt.Println(err)
		return
	}

	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(" %s", err)
		return
	}
	defer resp.Body.Close()
	_, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("%s", err)
		return
	}
}

func detonate(w http.ResponseWriter, r *http.Request) {
	url_arg := r.URL.Query().Get("url")
	fn_arg := r.URL.Query().Get("name")

	ip := strings.Split(r.RemoteAddr, ":")[0]

	reg, err := regexp.Compile("[^a-zA-Z0-9]+")
	if err != nil {
		return
	}
	fn := reg.ReplaceAllString(fn_arg, "")

	if ip != "127.0.0.1" {
		fmt.Println("wrong ip")
		return
	}

	client := &http.Client{}
	req, err := http.NewRequest("GET", url_arg, nil)
	if err != nil {
		fmt.Println(err)
		return
	}

	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("%s", err)
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("%s", err)
		return
	}

	ioutil.WriteFile("/detonations/"+fn, body, 0755)

	//send to detonator
	client = &http.Client{}
	req, err = http.NewRequest("GET", "http://detonator:9000/detonate?name="+fn, nil)
	if err != nil {
		fmt.Println(err)
		return
	}

	resp, err = client.Do(req)
	if err != nil {
		fmt.Printf("%s", err)
		return
	}
	defer resp.Body.Close()
	_, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("%s", err)
		return
	}

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

	router.HandleFunc("/welcome.html", welcome).Methods("GET")
	router.HandleFunc("/nord.jpg", img).Methods("GET")
	router.HandleFunc("/scan", scan_url).Methods("GET")
	router.HandleFunc("/detonate", detonate).Methods("GET")

	http.ListenAndServe(":15555", logRequest(router))
}

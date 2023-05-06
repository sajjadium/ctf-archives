package main

import (
        "fmt"
        "log"
        "net/http"
        "net/http/httputil"
        "net/url"
        "strings"
)
var invalid = [6]string{"'", "\"", ")", "(", ")","="}

func ProxyRequestHandler(proxy *httputil.ReverseProxy) func(http.ResponseWriter, *http.Request) {
    return func(w http.ResponseWriter, r *http.Request) {
                if(r.Header.Get("X-pro-hacker")!=""){
                     fmt.Fprintf(w, "Hello Hacker!\n")
                     return
                }
                if(strings.Contains(r.Header.Get("flag"), "gimme")){
                    fmt.Fprintf(w, "No flag For you!\n")
                    return
                }
                if(r.Header.Get("Token")!=""){
                    for _, x := range invalid {
                            if(strings.Contains(r.Header.Get("Token"), x)){
                                fmt.Fprintf(w, "Hello Hacker!\n")
                                return  
                            }

                        }
                }
                
        proxy.ServeHTTP(w, r)
    }
}

func main() {
        url, err := url.Parse("http://app:5000")
    if err != nil {
        fmt.Println(err)
    }
        proxy := httputil.NewSingleHostReverseProxy(url)

        http.HandleFunc("/", ProxyRequestHandler(proxy))
        http.HandleFunc("/admin", func(w http.ResponseWriter, r *http.Request) {
                fmt.Fprintf(w, "Hello World!\n")
})
        log.Fatal(http.ListenAndServe(":80", nil))
}

package main

import (
    "fmt"
    "net/http"
    "sync"
)

func fetch(url string, wg *sync.WaitGroup) {
    defer wg.Done()
    resp, err := http.Get(url)
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Printf("Fetched %s with status %s\n", url, resp.Status)
    resp.Body.Close()
}

func main() {
    urls := []string{
        "https://www.google.com",
        "https://www.github.com",
        "https://www.stackoverflow.com",
    }
    var wg sync.WaitGroup
    for _, url := range urls {
        wg.Add(1)
        go fetch(url, &wg)
    }
    wg.Wait()
}

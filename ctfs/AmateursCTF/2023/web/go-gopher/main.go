package main

import (
	"fmt"
	"log"
	"net/url"
	"strings"

	"git.mills.io/prologic/go-gopher"
)

func index(w gopher.ResponseWriter, r *gopher.Request) {
	w.WriteInfo("Welcome to the flag submitter!")
	w.WriteInfo("Please submit all your flags!")
	w.WriteItem(&gopher.Item{
		Type:        gopher.DIRECTORY,
		Selector:    "/submit/user",
		Description: "Submit flags here!",
	})
	w.WriteItem(&gopher.Item{
		Type:        gopher.FILE,
		Selector:    "URL:https://ctf.amateurs.team/",
		Description: "Get me more flags lackeys!!",
	})
	w.WriteItem(&gopher.Item{
		Type:        gopher.DIRECTORY,
		Selector:    "/",
		Description: "Nice gopher proxy",
		Host:        "gopher.floodgap.com",
		Port:        70,
	})
}

func submit(w gopher.ResponseWriter, r *gopher.Request) {
	name := strings.Split(r.Selector, "/")[2]
	undecoded, err := url.QueryUnescape(name)
	if err != nil {
		w.WriteError(err.Error())
	}
	w.WriteInfo(fmt.Sprintf("Hello %s", undecoded))
	w.WriteInfo("Please send a post request containing your flag at the server down below.")
	w.WriteItem(&gopher.Item{
		Type:        gopher.FILE,
		Selector:    fmt.Sprintf("URL:http://example.com/%s", undecoded),
		Description: "Submit here! (gopher doesn't have forms D:)",
		Host:        "error.host",
		Port:        1,
	})
}

func main() {
	mux := gopher.NewServeMux()

	mux.HandleFunc("/", index)
	mux.HandleFunc("/submit/", submit)

	log.Fatal(gopher.ListenAndServe("0.0.0.0:7000", mux))
}

package main

import (
	"bytes"
	"errors"
	"fmt"
	"html/template"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/lestrrat/go-libxml2"
	"github.com/lestrrat/go-libxml2/parser"
	"gopkg.in/gographics/imagick.v2/imagick"
)

type ConvertImageCommand func(args []string) (*imagick.ImageCommandResult, error)

type Converter struct {
	cmd ConvertImageCommand
}

func validateSVG(input []byte) ([]byte, error) {
	data, err := libxml2.Parse(input, parser.Option(2))

	if err != nil {
		return nil, err
	}

	defer data.Free()

	// xsd won't play nicely with svgs :(
	// ensure that root has name svg
	root, err := data.DocumentElement()

	if err != nil || !root.HasChildNodes() {
		log.Println(err)
		return nil, errors.New("invalid document format - no child nodes")
	}

	if strings.ToLower(root.NodeName()) != "svg" {
		return nil, errors.New("invalid document format - missing svg node")
	}

	return []byte(root.String()), nil
}

func (c *Converter) svgToPng(input []byte) ([]byte, error) {
	infile, err := ioutil.TempFile("/tmp", "temp-*.svg")

	if err != nil {
		return nil, err
	}

	defer os.Remove(infile.Name())

	infile.Write(input)

	ofile, err := ioutil.TempFile("/tmp", "temp-*.png")
	if err != nil {
		return nil, err
	}

	defer os.Remove(ofile.Name())

	imagick.Initialize()
	defer imagick.Terminate()
	mw := imagick.NewMagickWand()
	defer mw.Destroy()

	_, err = c.cmd([]string{
		"convert",
		"-background", "none",
		"-density", "1000",
		"-resize", "1000x",
		infile.Name(),
		ofile.Name(),
	})

	if err != nil {
		return nil, err
	}

	ret, err := os.ReadFile(ofile.Name())

	if err != nil {
		return nil, err
	}

	return ret, nil
}

func parseForm(req *http.Request) ([]byte, error) {
	err := req.ParseMultipartForm(1024 * 1024) // no svg should be over a 1mb imo

	if err != nil {
		return nil, err
	}

	var buf bytes.Buffer

	file, _, err := req.FormFile("svgfile")

	if err != nil {
		return nil, err
	}

	defer file.Close()

	io.Copy(&buf, file)

	contents := buf.String()

	// remove custom doctype, dtd
	reg := regexp.MustCompile(`<!DOCTYPE[^>[]*(\[[^]]*\])?>`)
	contentSafe := reg.ReplaceAllString(contents, "")

	return []byte(contentSafe), nil
}

func upload(w http.ResponseWriter, req *http.Request) {
	if req.Method != "POST" {
		http.NotFound(w, req)
		return
	}

	w.Header().Set("Content-Type", "image/png")

	data, err := parseForm(req)

	if err != nil {
		log.Print(req.RemoteAddr, err)
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("500 - Something bad happened!"))
		return
	}

	data, err = validateSVG(data)

	if err != nil {
		log.Print(req.RemoteAddr, err)
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("500 - Something bad happened!"))
		return
	}

	c := &Converter{
		cmd: imagick.ConvertImageCommand,
	}

	pngData, err := c.svgToPng(data)

	if err != nil {
		log.Print(req.RemoteAddr, err)
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("500 - Something bad happened!"))
		return
	}

	w.WriteHeader(http.StatusAccepted)
	io.Copy(w, bytes.NewBuffer(pngData))
}

func headers(w http.ResponseWriter, req *http.Request) {
	for name, headers := range req.Header {
		for _, h := range headers {
			fmt.Fprintf(w, "%v: %v\n", name, h)
		}
	}
}

func main() {
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

	fs := http.FileServer(http.Dir("./static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	http.HandleFunc("/upload", upload)
	http.HandleFunc("/headers", headers)
	http.HandleFunc("/", serveTemplate)
	log.Print("Listening on :5000...")
	err := http.ListenAndServe(":5000", logRequest(http.DefaultServeMux))

	if err != nil {
		log.Println(err)
	}
}

func serveTemplate(w http.ResponseWriter, r *http.Request) {
	lp := filepath.Join("templates", "layout.html")
	fp := filepath.Join("templates", filepath.Clean(r.URL.Path))

	// return index.html if no template defined
	if fp == "templates" {
		fp = "templates/index.html"
	}

	info, err := os.Stat(fp)
	if err != nil {
		if os.IsNotExist(err) {
			http.NotFound(w, r)
			return
		}
	}

	// Return a 404 if the request is for a directory
	if info.IsDir() {
		http.NotFound(w, r)
		return
	}

	tmpl, err := template.ParseFiles(lp, fp)
	if err != nil {
		// Log the detailed error
		log.Print(err.Error())
		// Return a generic "Internal Server Error" message
		http.Error(w, http.StatusText(500), 500)
		return
	}

	err = tmpl.ExecuteTemplate(w, "layout", nil)
	if err != nil {
		log.Print(err.Error())
		http.Error(w, http.StatusText(500), 500)
	}
}

func logRequest(handler http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("%s %s %s\n", r.RemoteAddr, r.Method, r.URL)
		handler.ServeHTTP(w, r)
	})
}

package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"encoding/base64"
	"encoding/json"
	"regexp"
	"strings"
	"time"
	"github.com/google/uuid"
)

const uploadDir = "./public/"
var uuidre *regexp.Regexp
var apphost string
var Mainjs string

func deleteFilesRegularly(directory string, interval time.Duration) {
    ticker := time.NewTicker(interval)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            err := deleteFilesInDirectory(directory)
            if err != nil {
                fmt.Printf("Error deleting files: %v\n", err)
            } else {
                fmt.Println("Files and folders deleted successfully")
            }
        }
    }
}

func deleteFilesInDirectory(directory string) error {
    err := filepath.Walk(directory, func(path string, info os.FileInfo, err error) error {
        if err != nil {
            return err
        }
        err = os.RemoveAll(path)
        if err != nil {
            return err
        }
        return nil
    })
    return err
}

func updatejs(sid string){

	dirPath := filepath.Join("public", sid)
	files, err := ioutil.ReadDir(dirPath)
	if err != nil {
		return
	}

	var fileNames []string
	for _, file := range files {
		if file.Name() != "files.js" {

			fileNames = append(fileNames, file.Name())
		}
	}

	jsonData, err := json.Marshal(fileNames)
	if err != nil {
		return
	}

	base64Data := base64.StdEncoding.EncodeToString(jsonData)
	uencoded := url.QueryEscape(base64Data)
	content := fmt.Sprintf("if(top.location.origin==='%s')\nfileNames = JSON.parse(atob(decodeURIComponent('%s'))),\nid = '%s';", apphost ,uencoded, sid)
	fname := filepath.Join(dirPath,"files.js")
	file, err := os.Create(fname)
	if err != nil {
		panic(err)

	}
	defer file.Close()
	file.WriteString(content)
}

func loginMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie("sid")
		if err != nil || !uuidre.Match([]byte(cookie.Value)) {
			http.SetCookie(w, &http.Cookie{
				Name:  "sid",
				Value: "",
				Path:  "/",
			})	
			http.Error(w, "Invalid Cookie", http.StatusBadRequest)
			return
		}

		path := filepath.Join(uploadDir, cookie.Value)
		if _, err := os.Stat(path); os.IsNotExist(err) {
			http.Error(w, "Invalid Cookie", http.StatusBadRequest)
			return
		}

        next.ServeHTTP(w, r)
    })
}


func mainHandler(w http.ResponseWriter, r *http.Request) {

	cookie, err := r.Cookie("sid")
	if err != nil || cookie.Value == ""{

		id := uuid.New()
		http.SetCookie(w, &http.Cookie{
			Name:  "sid",
			Value: id.String(),
			Path:  "/",
			HttpOnly: true,
			Secure: true,
			SameSite: 4,
			
		})
		path := filepath.Join(uploadDir, id.String())
		os.Mkdir(path, os.ModePerm)
		updatejs(id.String())

	}

	http.ServeFile(w, r, "static/index.html")
}

func uploadHandler(w http.ResponseWriter, r *http.Request) {

	cookie, _ := r.Cookie("sid")
	file, handler, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Error parsing file from form", http.StatusBadRequest)
		return
	}
	defer file.Close()

	// check filename?
	if strings.HasSuffix(handler.Filename, ".js") {
        http.Error(w, "No hack", http.StatusForbidden)
        return
    }

	filePath := filepath.Join(uploadDir,cookie.Value, handler.Filename)
	dst, err := os.Create(filePath)
	if err != nil {
		fmt.Println(err)
		http.Error(w, "Error creating destination file", http.StatusInternalServerError)
		return
	}
	
	defer dst.Close()

	if _, err := io.Copy(dst, file); err != nil {
		http.Error(w, "Error copying file", http.StatusInternalServerError)
		return
	}
	updatejs(cookie.Value)
	http.Redirect(w, r, "/", http.StatusFound)
}

func Deletefile(w http.ResponseWriter,r *http.Request){

	cookie, _ := r.Cookie("sid")
	name := r.URL.Query().Get("file")
	filePath := filepath.Join(uploadDir,cookie.Value, name)
	_, err := os.Stat(filePath)
    if os.IsNotExist(err) || strings.Contains(name,"files.js") ||  strings.Contains(name,"/") || strings.Contains(name,"\\"){
		http.Error(w, "Invalid filename", http.StatusBadRequest)
        return
	}

	err = os.Remove(filePath)
	if err != nil {
		http.Error(w, "Error copying file", http.StatusInternalServerError)
		return
	} 
	updatejs(cookie.Value)	
	http.Redirect(w, r, "/", http.StatusFound)

}

func Filejs(w http.ResponseWriter,r *http.Request){
	cookie, _ := r.Cookie("sid")
	updatejs(cookie.Value)
	fname := filepath.Join("public", cookie.Value, "files.js")
	w.Header().Set("Cross-Origin-Resource-Policy", "same-origin")
	http.ServeFile(w, r, fname)

}

func Mjs(w http.ResponseWriter,r *http.Request){

	http.ServeFile(w, r, "static/main.js")
}

func Css(w http.ResponseWriter,r *http.Request){

	http.ServeFile(w, r, "static/style.css")
}

func main() {
	
    interval := 30 * time.Minute
	go deleteFilesRegularly(uploadDir, interval)

	if _, err := os.Stat(uploadDir); os.IsNotExist(err) {
		os.Mkdir(uploadDir, os.ModePerm)
	}

	uuidre = regexp.MustCompile(`^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$`)
	apphost = os.Getenv("APP_HOST")
    http.Handle("/upload", loginMiddleware(http.HandlerFunc(uploadHandler)))
    http.Handle("/delete", loginMiddleware(http.HandlerFunc(Deletefile)))
    http.Handle("/files.js", loginMiddleware(http.HandlerFunc(Filejs)))
	http.HandleFunc("/main.js", Mjs)
	http.HandleFunc("/style.css", Css)
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("public"))))
	http.HandleFunc("/", mainHandler)
	fmt.Println("Server listening on :3000...")
	http.ListenAndServe(":3000", nil)
}

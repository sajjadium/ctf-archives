package main

import (
    "fmt"
    "time"
    "os"
    "io"
    "io/ioutil"
    "net/http"
    "path/filepath"
    "encoding/json"
    "github.com/gorilla/mux"
    "github.com/google/uuid"
    "github.com/sethvargo/go-limiter/httplimit"
    "github.com/sethvargo/go-limiter/memorystore"
)

func fileExists(path string) bool {
    if _, err := os.Stat(path); os.IsNotExist(err) {
        return false
    }
    return true
}

func jsonResponse(w http.ResponseWriter, code int, payload interface{}) {
    response, _ := json.Marshal(payload)

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(code)
    w.Write(response)
}

func handleNewBucket(w http.ResponseWriter, r *http.Request) {
    id := uuid.New()

    bucketPath := filepath.Join("./buckets/", id.String())
    err := os.Mkdir(bucketPath, 0777)
    if err != nil {
        jsonResponse(w, 500, map[string]interface{}{
            "ok": false,
            "error": "Could not create a bucket",
        })
        return
    }

    jsonResponse(w, 200, map[string]interface{}{
        "ok": true,
        "bucketId": id.String(),
    })
}

func handleUpload(w http.ResponseWriter, r *http.Request) {
	bucketId := r.FormValue("bucketId")
    fmt.Println("Bucket ID:", bucketId)

    if bucketId == "" {
        jsonResponse(w, 400, map[string]interface{}{
            "ok": false,
            "error": "Bucket name is empty",
        })
        return
    }

    bucketPath := filepath.Join("./buckets/", bucketId)
    if !fileExists(bucketPath) {
        jsonResponse(w, 400, map[string]interface{}{
            "ok": false,
            "error": "Destination bucket does not exist, please request a new bucket.",
        })
        return
    }

    files, err := ioutil.ReadDir(bucketPath)
    if err != nil {
        jsonResponse(w, 400, map[string]interface{}{
            "ok": false,
            "error": "Error while reading the destination bucket",
        })
        return
    }

    if len(files) >= 3 {
        jsonResponse(w, 400, map[string]interface{}{
            "ok": false,
            "error": "Bucket already contains 3 or more files",
        })
        return
    }

    file, fileHeader, err := r.FormFile("file")
	if err != nil {
		jsonResponse(w, 500, map[string]interface{}{
            "ok": false,
            "error": "Error occurred while processing the file",
        })
        return
	}

    defer file.Close()

    if fileHeader.Size > 1000 {
        jsonResponse(w, 413, map[string]interface{}{
            "ok": false,
            "error": "File too large",
        })
        return
    }

    filePath := filepath.Join(bucketPath, fileHeader.Filename)
    if fileExists(filePath) {
        jsonResponse(w, 400, map[string]interface{}{
            "ok": false,
            "error": "File already exists",
        })
        return
    }

	dst, err := os.Create(filePath)
	if err != nil {
		jsonResponse(w, 500, map[string]interface{}{
            "ok": false,
            "error": "Error occurred while uploading the file",
        })
        return
	}

	defer dst.Close()

	_, err = io.Copy(dst, file)
	if err != nil {
		jsonResponse(w, 500, map[string]interface{}{
            "ok": false,
            "error": "Error occurred while uploading the file",
        })
        return
	}

    jsonResponse(w, 200, map[string]interface{}{
        "ok": true,
        "filepath": fmt.Sprintf("/files/%s/%s", bucketId, fileHeader.Filename),
    })
}

func handleBucket(w http.ResponseWriter, r *http.Request) {
    params := mux.Vars(r)

    bucketId := params["bucketId"]
    filename := params["filename"]

    bucketPath := filepath.Join("./buckets/", bucketId)
    if !fileExists(bucketPath) {
        jsonResponse(w, 404, map[string]interface{}{
            "ok": false,
            "error": "Bucket does not exist",
        })
        return
    }

    filePath := filepath.Join(bucketPath, filename)
    if !fileExists(filePath) {
        jsonResponse(w, 404, map[string]interface{}{
            "ok": false,
            "error": "File does not exist",
        })
        return
    }

    fmt.Println("Downloading file:", filePath)
    http.ServeFile(w, r, filePath)
}

func main() {
    store, err := memorystore.New(&memorystore.Config{
        Tokens: 15,
        Interval: time.Minute,
    })
    middleware, err := httplimit.NewMiddleware(store, httplimit.IPKeyFunc())
    if err != nil {
        fmt.Println("Err", err)
    }

    r := mux.NewRouter()

    r.HandleFunc("/api/newBucket", handleNewBucket).Methods("POST")
    r.HandleFunc("/api/uploadFile", handleUpload).Methods("POST")

    r.HandleFunc("/files/{bucketId}/{filename}", handleBucket)

    r.PathPrefix("/").Handler(http.FileServer(http.Dir("./static/")))

    fmt.Println("Hosting server on :80")
    http.ListenAndServe(":80", middleware.Handle(r))
}

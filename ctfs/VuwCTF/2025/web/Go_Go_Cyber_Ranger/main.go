package main

import (
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"strings"
	"unsafe"
)

// Application state
var appState = struct {
	inputBuf [32]byte
	flag     [8]byte
}{
	flag: [8]byte{'F', 'L', 'A', 'G', '{', 'a', 'c', '}'},
}

var userBuffer = appState.inputBuf[:]
var secretFlag = appState.flag[:]

func vulnerableHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		// Show form
		response := `
		<html>
		<head><title>Character Validator</title></head>
		<body>
			<h1>Character Validator</h1>
			<p>Enter up to 32 characters. The system validates character count, not byte count!</p>
			<form method="POST">
				<input type="text" name="input" placeholder="Enter text (max 32 characters)" style="width: 400px;">
				<button type="submit">Submit</button>
			</form>
			<br>
			<p><a href="/flag">Check Flag</a></p>
			<img src="/cyberranger.png" alt="Cyber Ranger" style="max-width: 100px;">

		</body>
		</html>
		`
		w.Header().Set("Content-Type", "text/html")
		w.Write([]byte(response))
		return
	}

	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	err := r.ParseForm()
	if err != nil {
		http.Error(w, "Error parsing form", http.StatusBadRequest)
		return
	}

	inputStr := r.FormValue("input")
	if inputStr == "" {
		http.Error(w, "No input provided", http.StatusBadRequest)
		return
	}

	if len([]rune(inputStr)) > 32 {
		http.Error(w, fmt.Sprintf("Input too long! Maximum 32 characters allowed. You provided %d characters.", len([]rune(inputStr))), http.StatusBadRequest)
		return
	}

	for i := range userBuffer {
		userBuffer[i] = 0
	}

	inputBytes := []byte(inputStr)

	bufPtr := unsafe.Pointer(&appState.inputBuf)
	dest := (*[40]byte)(bufPtr)

	copyLen := len(inputBytes)
	if copyLen > 40 {
		copyLen = 40
	}
	for i := 0; i < copyLen; i++ {
		dest[i] = inputBytes[i]
	}

	response := fmt.Sprintf(`
		<html>
		<head><title>Character Validator</title></head>
		<body>
			<img src="/cyberranger.png" alt="Cyber Ranger" style="max-width: 300px;">
			<h1>Character Validator</h1>
			<p>Your input has been validated and stored!</p>
			<p>Buffer contents: %q</p>
			<p>Character count: %d runes</p>
			<p>Byte count: %d bytes</p>
			<p>Buffer size: %d bytes</p>
			<br>
			<form method="POST">
				<input type="text" name="input" placeholder="Enter text (max 32 characters)" style="width: 400px;" value="%s">
				<button type="submit">Submit</button>
			</form>
			<br>
			<p><a href="/flag">Check Flag</a></p>
		</body>
		</html>
	`, string(userBuffer[:]), len([]rune(inputStr)), len(inputBytes), len(userBuffer), url.QueryEscape(inputStr))

	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(response))
}

func flagHandler(w http.ResponseWriter, r *http.Request) {
	secretFlagValue := string(secretFlag[:])

	// Read real flag from file
	realFlagBytes, err := os.ReadFile("flag.txt")
	realFlag := string(realFlagBytes)
	if err != nil {
		// If you get this on the actual server contact our support.
		realFlag = "Contact Support - flag file missing"
	}
	realFlag = strings.TrimSpace(realFlag)

	cmd := exec.Command("/bin/sh", "-c", fmt.Sprintf("test \"%s\" = \"%s\"", realFlag, secretFlagValue))
	output, err := cmd.CombinedOutput()

	var result string
	if err == nil {
		result = "Flag matches!"
	} else {
		result = "Flag does not match."
	}

	if len(output) > 0 {
		result += fmt.Sprintf("<br><br>Command output: <pre>%s</pre>", string(output))
	}

	response := fmt.Sprintf(`
		<html>
		<head><title>Flag</title></head>
		<body>
			<h1>Secret Flag Check</h1>
			<p>Your flag guess value: <strong>%s</strong></p>
			<p>%s</p>
			<p><a href="/">Back</a></p>
		</body>
		</html>
	`, secretFlagValue, result)
	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(response))
}

func imageHandler(w http.ResponseWriter, r *http.Request) {
	imageData, err := os.ReadFile("cyberranger.png")
	if err != nil {
		http.Error(w, "Image not found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "image/png")
	w.Write(imageData)
}

func main() {
	http.HandleFunc("/", vulnerableHandler)
	http.HandleFunc("/flag", flagHandler)
	http.HandleFunc("/cyberranger.png", imageHandler)

	fmt.Println("Starting server on :9984")
	log.Fatal(http.ListenAndServe(":9984", nil))
}

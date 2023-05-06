package main

import (
    "bytes"
    "fmt"
    "html/template"
    "io"
    "log"
    "net"
    "net/http"
    "net/url"
    "os/exec"
    "strings"
)

func main() {
	http.Handle("/admin", http.HandlerFunc(handleAdmin))
	http.Handle("/", http.HandlerFunc(handleRoot))

	log.Fatal(http.ListenAndServe(":3000", nil))
}

func handleAdmin(w http.ResponseWriter, req *http.Request) {
  check_err := func (err error) bool {
    if err != nil {
      w.Header().Set("Content-Type", "text/plain")
      w.WriteHeader(http.StatusInternalServerError)
      fmt.Fprintf(w, "Error occurred: %v\n", err)
      return true
    }
    return false
  }

  client_ip_str := req.Header.Get("Client-Ip")
  client_ip, err := net.ResolveIPAddr("ip", client_ip_str)
  if check_err(err) { return }
  my_ip, err := net.ResolveIPAddr("ip", "backend")
  if check_err(err) { return }

  if client_ip_str != "127.0.0.1" && !client_ip.IP.Equal(my_ip.IP) {
    fmt.Fprintln(w, "You are not allowed to see the flag!")
    return
  }

  res, err := http.PostForm("http://flag:3000/showmeflag", url.Values{}) 
  if check_err(err) { return }
  defer res.Body.Close()

  body, err := io.ReadAll(res.Body)
  if check_err(err) { return }

  w.Header().Set("Content-Type", "text/plain")
  w.WriteHeader(http.StatusOK)
  w.Write(body)
}

func handleRoot(w http.ResponseWriter, req *http.Request) {
  if req.URL.Path != "/" {
    http.NotFound(w, req)
    return
  }

  check_err := func (err error) bool {
    if err != nil {
      w.Header().Set("Content-Type", "text/plain")
      w.WriteHeader(http.StatusInternalServerError)
      fmt.Fprintf(w, "Error occurred: %v\n", err)
      return true
    }
    return false
  }

  if req.Method == "GET" {
    tmpl, err := template.ParseFiles("index.html")
    if check_err(err) { return }

    w.Header().Set("Content-Type", "text/html")
    w.WriteHeader(http.StatusOK)
    tmpl.Execute(w, nil)
    return
  }

  f, _, err := req.FormFile("file")
  if check_err(err) { return }
  defer f.Close()

  script, err := io.ReadAll(f)
  if check_err(err) { return }

  // First, check if the posted file is actually a Postscript file.
  // 1. check `file` output
  cmd := exec.Command("file", "-")
  cmd.Stdin = bytes.NewReader(script)
  var stdout1 bytes.Buffer
  var stderr1 bytes.Buffer
  cmd.Stdout = &stdout1
  cmd.Stderr = &stderr1

  err = cmd.Run()
  if check_err(err) { return }

  err_str1 := stderr1.String()
  if err_str1 != "" {
    w.Header().Set("Content-Type", "text/plain")
    w.WriteHeader(http.StatusInternalServerError)
    fmt.Fprintf(w, "file returned error: [redacted]\n")
    return
  }

  out_str1 := stdout1.String()
  if !strings.Contains(out_str1, "PostScript document text") {
    w.Header().Set("Content-Type", "text/plain")
    w.WriteHeader(http.StatusBadRequest)
    fmt.Fprintf(w, "Get out, poor hacker!\n")
    return
  }

  // 2. check if ps2ps can actually process the file
  cmd = exec.Command("ps2ps", "/dev/stdin", "/dev/stdout")
  cmd.Stdin = bytes.NewReader(script)
  var stdout2 bytes.Buffer
  var stderr2 bytes.Buffer
  cmd.Stdout = &stdout2
  cmd.Stderr = &stderr2

  err = cmd.Run()
  if check_err(err) { return }

  err_str2 := stderr2.String()
  if err_str2 != "" {
    w.Header().Set("Content-Type", "text/plain")
    w.WriteHeader(http.StatusInternalServerError)
    fmt.Fprintf(w, "ps2ps returned error: [redacted]\n")
    return
  }

  // Seems fine. So now let's send the file to the ps2pdf daemon
  x_forwarded_for := req.Header.Get("X-Forwarded-For")
  ips := strings.Split(x_forwarded_for, ", ")
  ps2pdf := ips[len(ips)-1]
  tcp_addr, err := net.ResolveTCPAddr("tcp", ps2pdf + ":3000")
  conn, err := net.DialTCP("tcp", nil, tcp_addr)
  if check_err(err) { return }
  
  _, err = conn.Write(script)
  if check_err(err) { return }
  conn.CloseWrite()

  var resp []byte
  resp, err = io.ReadAll(conn)
  if check_err(err) { return }

  if bytes.Contains(resp, []byte("Error")) {
    fmt.Fprintln(w, "Something went wrong.")
    return
  }

  w.Header().Set("Content-Type", "application/pdf")
  w.WriteHeader(http.StatusOK)
  w.Write(resp)
}

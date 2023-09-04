package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"net/url"
	"strings"
)

func main() {
	targetUrlFlag := flag.String("target", "http://localhost:8081", "Target URL")
	port := flag.Int("port", 8080, "The port to listen on")
	flag.Parse()

	targetUrl, err := url.Parse(*targetUrlFlag)
	if err != nil {
		log.Fatalf("Error parsing target URL: %s", err)
	}

	ln, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	log.Printf("Listening on port %d\n", *port)
	if err != nil {
		log.Fatalf("Error listening: %s", err)
	}
	defer ln.Close()

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Printf("Error accepting connection: %s", err)
			continue
		}

		go func() {
			defer conn.Close()

			scanner := bufio.NewScanner(conn)
			var rawRequest bytes.Buffer
			for scanner.Scan() {
				line := scanner.Text()
				if line == "" {
					break
				}
				fmt.Fprintf(&rawRequest, "%s\r\n", line)
			}
			if err := scanner.Err(); err != nil {
				log.Printf("Error reading request: %s", err)
				return
			}

			clientIP := strings.Split(conn.RemoteAddr().String(), ":")[0]

			request, err := parseRequest(rawRequest.Bytes(), clientIP, targetUrl.Host)
			if err != nil {
				log.Printf("Error parsing request: %s", err)
				return
			}

			client := http.Client{}
			resp, err := client.Do(request)
			if err != nil {
				log.Printf("Error proxying request: %s", err)
				return
			}
			defer resp.Body.Close()

			// Write the response to the connection
			writer := bufio.NewWriter(conn)
			resp.Write(writer)
			writer.Flush()
		}()
	}
}

func parseRequest(raw []byte, clientIP, targetHost string) (*http.Request, error) {
	var method, path, version string
	headers := make([][]string, 0)
	reader := bytes.NewReader(raw)
	scanner := bufio.NewScanner(reader)
	scanner.Scan()
	fmt.Sscanf(scanner.Text(), "%s %s %s", &method, &path, &version)

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			break
		}
		parts := strings.SplitN(line, ":", 2)
		if len(parts) == 2 {
			headers = append(headers, []string{strings.TrimSpace(parts[0]), strings.TrimSpace(parts[1])})
		}
	}

	for i, v := range headers {
		if strings.ToLower(v[0]) == "x-forwarded-for" {
			headers[i][1] = fmt.Sprintf("%s, %s", v[1], clientIP)
			break
		}
	}

	headerMap := make(map[string][]string)
	for _, v := range headers {
		value := headerMap[v[0]]

		if value != nil {
			value = append(value, v[1])
		} else {
			value = []string{v[1]}
		}

		headerMap[v[0]] = value
	}

	request := &http.Request{
		Method:        method,
		URL:           &url.URL{Scheme: "http", Host: targetHost, Path: path},
		Proto:         version,
		ProtoMajor:    1,
		ProtoMinor:    1,
		Header:        headerMap,
		Body:          io.NopCloser(reader),
		ContentLength: int64(reader.Len()),
	}
	return request, nil
}

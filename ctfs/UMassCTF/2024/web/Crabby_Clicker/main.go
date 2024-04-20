package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
	"time"
)

type RequestHandler struct {
	burgers int
	conn    net.Conn
}

var GLOBAL_STATE RequestHandler

func main() {
	// Listen on TCP port 8080 on all interfaces.
	ln, err := net.Listen("tcp", ":1337")
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		return
	}
	defer ln.Close()
	fmt.Println("Listening on :1337")

	GLOBAL_STATE = RequestHandler{burgers: 0, conn: nil}

	for {
		// Accept a connection.
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			return
		}

		// burger to the GLOBAL_STATE from the request handler so we can track between requests
		handler := RequestHandler{burgers: GLOBAL_STATE.burgers, conn: conn}
		go handler.handleRequest()
	}
}

func (r *RequestHandler) handleRequest() {
	defer r.conn.Close()

	reader := bufio.NewReader(r.conn)

	for {
		// Set a deadline for reading. If a second passes without reading any data, a timeout will occur.
		r.conn.SetReadDeadline(time.Now().Add(1 * time.Second))

		// Read and parse the request headers
		request, err := readHTTPHeader(reader)
		if err != nil {
			return
		}

		requestLines := strings.Split(request, "\n")
		if len(requestLines) < 1 {
			fmt.Println("Invalid request")
			return
		}

		// Parse the request line
		requestLine := strings.Fields(requestLines[0])
		if len(requestLine) < 3 {
			fmt.Println("Invalid request")
			return
		}

		method := requestLine[0]
		uri := requestLine[1]

		// Check if the request is a valid GET request
		if method != "GET" {
			r.conn.Write([]byte("HTTP/1.1 405 Method Not Allowed\r\n\r\n"))
			return
		}

		// Handle GET request
		if uri == "/" {
			r.generateResponse(`
Welcome to Crabby Clicker!
A HTTP based clicker game where you can earn burgers to get the flag. 
Make a request to /click to gain a burger.
I use my own custom HTTP server implementation to manage the state of the game.
It's not fully working, I am running into some bugs.
			`)
		} else if uri == "/click" {
			// BUG: Weird thing where the state is not updated between requests??
			r.burgers++
			r.generateResponse("burger added")
		} else if uri == "/flag" {
			if r.burgers >= 100 {
				r.generateResponse(fmt.Sprintf("Flag: UMASS{%s}", os.Getenv("FLAG")))
			} else {
				r.generateResponse("Not enough burgers")
			}
		} else {
			r.generateResponse("Not found")
		}
	}
}

func (r *RequestHandler) generateResponse(message string) {
	r.conn.Write([]byte(fmt.Sprintf("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n%s\nburgers: %d\n", message, r.burgers)))
}

func readHTTPHeader(reader *bufio.Reader) (string, error) {
	// Read headers until \r\n\r\n
	var requestLines []string
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			return "", err
		}
		requestLines = append(requestLines, line)
		// Check if the current line marks the end of the headers
		if line == "\r\n" {
			break
		}
	}
	return strings.Join(requestLines, ""), nil
}

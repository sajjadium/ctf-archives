// Package einhorn allows you to communicate with the einhorn master from a Go
// worker.
package einhorn

import (
	"bufio"
	"fmt"
	"net"
	"net/url"
	"path"
	"strings"

	"gopkg.in/yaml.v2"
)

var TmpDir = "/tmp"

type Client struct {
	socket net.Conn
	reader *bufio.Reader
	writer *bufio.Writer
}

type ClientRequest struct {
	RequestId int `yaml:"request_id,omitempty"`
	Command   string
	Args      []string `yaml:",omitempty"`
}

type ClientAckRequest struct {
	Command string
	Pid     int
}

type ClientResponse struct {
	RequestId int `yaml:"request_id"`
	Message   string
	Wait      bool
}

func NewClient(socket net.Conn) *Client {
	return &Client{
		socket: socket,
		reader: bufio.NewReader(socket),
		writer: bufio.NewWriter(socket),
	}
}

func NewClientForPath(path string) (*Client, error) {
	socket, err := net.Dial("unix", path)
	if err != nil {
		return nil, err
	}

	return NewClient(socket), nil
}

func NewClientForName(name string) (*Client, error) {
	return NewClientForPath(path.Join(TmpDir, fmt.Sprintf("einhorn-%s.sock", name)))
}

func (c *Client) SendRequest(req interface{}) error {
	line, err := yaml.Marshal(req)
	if err != nil {
		return err
	}

	encoded := strings.Replace(strings.Replace(string(line), "%", "%25", -1), "\n", "%0A", -1)

	if _, err := c.writer.WriteString(fmt.Sprintf("%s\n", encoded)); err != nil {
		return err
	}
	return c.writer.Flush()
}

func (c *Client) ReadResponse() (*ClientResponse, error) {
	encoded, err := c.reader.ReadString('\n')
	if err != nil {
		return nil, err
	}
	line, err := url.QueryUnescape(encoded)
	if err != nil {
		return nil, err
	}

	var response ClientResponse
	if err := yaml.Unmarshal([]byte(line), &response); err != nil {
		return nil, err
	}

	return &response, nil
}

func (c *Client) Close() {
	c.socket.Close()
}

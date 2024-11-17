package main

import (
	"bufio"
	"crypto/rand"
	"crypto/subtle"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"os"
	"strings"
	"sync"

	"golang.org/x/crypto/argon2"
)

type User struct {
	Username string `json:"username"`
	Password string `json:"password"`
	IsAdmin  bool   `json:"is-admin"`
	Note     string `json:"-"`
}

var usersLock sync.RWMutex
var users []*User = []*User{}

func validateRegistration(arg string) bool {
	var parsed map[string]any
	json.Unmarshal([]byte(arg), &parsed)
	if _, ok := parsed["is-admin"]; ok {
		return false
	}
	if un, ok := parsed["username"]; !ok {
		return false
	} else if u, ok := un.(string); !ok {
		return false
	} else if len(u) < 6 {
		return false
	}
	if pw, ok := parsed["password"]; !ok {
		return false
	} else if p, ok := pw.(string); !ok {
		return false
	} else if len(p) < 16 {
		return false
	}
	return true
}

func register(user User) {
	var salt [32]byte
	rand.Read(salt[:])
	hash := argon2.IDKey([]byte(user.Password), salt[:], 1, 64*1024, 2, 32)
	user.Password = base64.RawStdEncoding.EncodeToString(hash) + ":" + base64.RawStdEncoding.EncodeToString(salt[:])

	usersLock.Lock()
	users = append(users, &user)
	usersLock.Unlock()
}

func login(usernamepw string) *User {
	split := strings.SplitN(usernamepw, " ", 2)
	if len(split) < 2 {
		return nil
	}
	username := split[0]
	password := split[1]

	usersLock.RLock()
	defer usersLock.RUnlock()
	for _, user := range users {
		if user.Username != username {
			continue
		}
		split := strings.SplitN(user.Password, ":", 2)
		hash, _ := base64.RawStdEncoding.DecodeString(split[0])
		salt, _ := base64.RawStdEncoding.DecodeString(split[1])
		pwhash := argon2.IDKey([]byte(password), salt, 1, 64*1024, 2, 32)
		if subtle.ConstantTimeCompare(hash, pwhash) != 1 {
			continue
		}
		return user
	}
	return nil
}

func handleConn(conn net.Conn) {
	defer conn.Close()
	var user *User
	scan := bufio.NewScanner(conn)
	for func() bool { fmt.Fprint(conn, "> "); return true }() && scan.Scan() {
		split := strings.SplitN(scan.Text(), " ", 2)
		command := split[0]
		var arg string
		if len(split) > 1 {
			arg = split[1]
		}
		switch command {
		case "register":
			if !validateRegistration(arg) {
				fmt.Fprintln(conn, "invalid user object, example:\nregister {\"username\":\"thebestuser\",\"password\":\"who stole my schmunguss?\"}")
				continue
			}
			var user User
			json.Unmarshal([]byte(arg), &user)
			register(user)
			conn.Write([]byte("ok\n"))
		case "login":
			user = login(arg)
			if user != nil {
				fmt.Fprintln(conn, "Logged in as", user.Username)
			} else {
				fmt.Fprintln(conn, "Invalid credentials")
			}
		case "write":
			if user == nil {
				fmt.Fprintln(conn, "You must be logged in to do that")
				continue
			}
			fmt.Fprint(conn, ">> ")
			scan.Scan()
			user.Note = scan.Text()
		case "get":
			if arg == "note" {
				if user == nil {
					fmt.Fprintln(conn, "You must be logged in to do that")
					continue
				}
				fmt.Fprintln(conn, user.Note)
			} else if arg == "flag" {
				if user == nil {
					fmt.Fprintln(conn, "You must be logged in to do that")
					continue
				}
				if !user.IsAdmin {
					fmt.Fprintln(conn, "Only admins get the flag")
					continue
				}
				flag := os.Getenv("FLAG")
				if flag == "" {
					flag = "🚨 flag missing 🚨"
				}
				fmt.Fprintln(conn, flag)
			} else if arg == "ip" {
				fmt.Fprintln(conn, conn.RemoteAddr())
			} else if arg == "admin" {
				if user == nil {
					fmt.Fprintln(conn, "You must be logged in to do that")
					continue
				}
				fmt.Fprintln(conn, user.IsAdmin)
			} else if arg == "rand" {
				io.CopyN(conn, rand.Reader, 1024)
			} else {
				fmt.Fprintln(conn, "get what?")
			}
		case "whoami":
			fallthrough
		case "id":
			if user != nil {
				fmt.Fprintln(conn, user.Username)
			} else {
				fmt.Fprintln(conn, "no one")
			}
		case "quit":
			return
		default:
			fmt.Fprintln(conn, "what?")
		}
	}
	if err := scan.Err(); err != nil {
		fmt.Println("err=", err, "addr=", conn.RemoteAddr())
	}
}

func main() {
	var pwBytes [21]byte
	rand.Read(pwBytes[:])
	pw := base64.StdEncoding.EncodeToString(pwBytes[:])
	register(User{Username: "admin", Password: pw, IsAdmin: true})

	l, err := net.Listen("tcp", ":1025")
	if err != nil {
		panic(err)
	}
	for {
		conn, err := l.Accept()
		if err != nil {
			panic(err)
		}
		go handleConn(conn)
	}
}

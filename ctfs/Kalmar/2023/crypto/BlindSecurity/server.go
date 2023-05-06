package main

import (
	"crypto/elliptic"
	"encoding/hex"
	"encoding/json"
	"io/ioutil"
	"log"
	"net"
	"strings"
	"sync"

	"github.com/rot256/pblind"
)

// Number of signatures the service will provide for a given session
const TICKETS int = 243

// Port to listen on
const ADDRESS string = ":4343"

var FLAG string = ""

var CURVE elliptic.Curve = elliptic.P256()

type Request struct {
	Id        string
	Info      []byte
	Operation string
}

type Signature struct {
	Msg  []byte
	Info []byte
	Sig  pblind.Signature
}

type Session struct {
	lock   sync.Mutex
	sk     pblind.SecretKey
	Pk     pblind.PublicKey
	Remain int
}

var SessionsLock sync.Mutex
var Sessions map[string]*Session

func init() {
	// create session map
	Sessions = make(map[string]*Session)

	// load flag
	var err error
	flag, err := ioutil.ReadFile("./flag.txt")
	if err != nil {
		panic(err)
	}
	FLAG = strings.TrimSpace(string(flag))
	log.Println("Flag loaded")
}

// Get or create session corresponding to a given ID in a request.
func getSession(id string) *Session {
	SessionsLock.Lock()
	ses, ok := Sessions[id]
	if !ok {
		// If session doesn't exist, create new session with new signing key
		var err error
		ses = &Session{}
		ses.Remain = TICKETS
		ses.sk, err = pblind.NewSecretKey(CURVE)
		if err != nil {
			panic(err)
		}
		ses.Pk = ses.sk.GetPublicKey()
		Sessions[id] = ses
	}
	SessionsLock.Unlock()
	return ses
}

// Run the partially blind signing protocol
// This can be called TICKETS times per session
func handleSign(ses *Session, req Request, enc *json.Encoder, dec *json.Decoder) error {
	// check if out of tickets
	ses.lock.Lock()
	ok := ses.Remain > 0
	if ok {
		ses.Remain -= 1
	}
	ses.lock.Unlock()
	if !ok {
		return nil
	}

	// compress meta data
	info, err := pblind.CompressInfo(CURVE, req.Info)
	if err != nil {
		return err
	}

	// create new signer
	ses.lock.Lock()
	signer, err := pblind.CreateSigner(ses.sk, info)
	if err != nil {
		return err
	}
	ses.lock.Unlock()

	// interact with the requester
	msg1, err := signer.CreateMessage1()
	if err != nil {
		return err
	}
	if err := enc.Encode(msg1); err != nil {
		return err
	}

	// process second message
	var msg2 pblind.Message2
	if err := dec.Decode(&msg2); err != nil {
		return err
	}
	if err := signer.ProcessMessage2(msg2); err != nil {
		return err
	}

	// create message3
	msg3, err := signer.CreateMessage3()
	if err != nil {
		return err
	}
	return enc.Encode(msg3)
}

// Wait for the client to sent TICKETS + 1 valid signatures on different messages.
// If client does this, then client has successfully forged a signature, and is rewarded with the flag
func handleVerify(ses *Session, req Request, enc *json.Encoder, dec *json.Decoder) error {
	// check if they can provide TICKETS+1 different signatures
	msgs := make(map[string]bool)
	for i := 0; i <= TICKETS; i++ {
		// get the signature
		var sig Signature
		if err := dec.Decode(&sig); err != nil {
			return err
		}

		// check if new
		hmsg := hex.EncodeToString(sig.Msg) + "-" + hex.EncodeToString(sig.Info)
		if msgs[hmsg] {
			return nil
		}
		msgs[hmsg] = true

		// validate
		info, err := pblind.CompressInfo(CURVE, sig.Info)
		if err != nil || !ses.Pk.Check(sig.Sig, info, sig.Msg) {
			return nil
		}
	}

	// if so, give them the flag
	return enc.Encode(FLAG)
}

// Handle incoming connection. Load session for given ID, and call requested operation
func handle(conn net.Conn) {
	defer conn.Close()
	log.Println("Handle connection, from:", conn.RemoteAddr())

	enc := json.NewEncoder(conn)
	dec := json.NewDecoder(conn)

	var req Request
	if err := dec.Decode(&req); err != nil {
		log.Println("Error:", err)
		return
	}

	// lookup session
	ses := getSession(req.Id)

	// send status to user
	ses.lock.Lock()
	err := enc.Encode(ses)
	ses.lock.Unlock()
	if err != nil {
		log.Println("Error:", err)
		return
	}

	// signing operation
	if req.Operation == "Sign" {
		if err := handleSign(ses, req, enc, dec); err != nil {
			log.Println("Error:", err)
		}
	}

	// verify and retrieve flag
	if req.Operation == "Verify" {
		if err := handleVerify(ses, req, enc, dec); err != nil {
			log.Println("Error:", err)
		}
	}
}

func main() {
	// bind to interface
	l, err := net.Listen("tcp", ADDRESS)
	if err != nil {
		panic(err)
	}
	defer l.Close()

	// handle connections
	for {
		conn, err := l.Accept()
		if err != nil {
			log.Println("Failed to accept:", err)
			continue
		}
		go handle(conn)
	}
}

package main

import (
	"bufio"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"encoding/json"
	"fmt"
	"io"
	"os"
)

type RPC struct {
	Method     string        `json:"method"`
	Message    []byte        `json:"message"`
	Signatures *RPCSignature `json:"signatures"`
}

type RPCSignature struct {
	Ecdsa []byte `json:"ecdsa"`
}

type RPCResp struct {
	Success   bool   `json:"success"`
	Signature []byte `json:"signature"`
}

const failure = `{"success": false, "signature": ""}`

func (r *RPC) Execute(privateKey *ecdsa.PrivateKey) []byte {
	if r.Method == "auth" {
		if signature, err := ecdsa.SignASN1(rand.Reader, privateKey, r.Message); err == nil {
			if resp, err := json.Marshal(RPCResp{
				Success:   true,
				Signature: signature,
			}); err == nil {
				return resp
			}
		}
	} else if r.Signatures != nil && len(r.Signatures.Ecdsa) > 0 {
		if ecdsa.VerifyASN1(&privateKey.PublicKey, r.Message, r.Signatures.Ecdsa) {
			if resp, err := json.Marshal(RPCResp{
				Success:   true,
				Signature: []byte(""),
			}); err == nil {
				return resp
			}
		}
	}
	return []byte(failure)
}

func main() {
	fmt.Println("ECDSA authenticator started")

	privateKey, err := ecdsa.GenerateKey(elliptic.P521(), rand.Reader)
	if err != nil {
		panic(err)
	}

	rdr := bufio.NewReader(os.Stdin)
	for {
		switch line, err := rdr.ReadString('\n'); err {
		case nil:
			var rpc RPC
			if err := json.Unmarshal([]byte(line), &rpc); err != nil {
				fmt.Println(failure)
				continue
			}
			if len(rpc.Message) == 0 {
				fmt.Println(failure)
				continue
			}

			fmt.Println(string(rpc.Execute(privateKey)))

		case io.EOF:
			os.Exit(0)
		default:
			os.Exit(1)
		}
	}
}

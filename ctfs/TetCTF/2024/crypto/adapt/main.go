package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"github.com/cosmos/iavl"
	db "github.com/tendermint/tm-db"
	"log"
	"math/big"
	"os"
)

func main() {
	// gen a keypair
	seckey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		log.Panicf("could not generate ecdsa key: %v", err)
	}
	fmt.Println(seckey.X, seckey.Y)

	// init a mutable tree
	tree, err := iavl.NewMutableTree(db.NewMemDB(), 256, false)
	if err != nil {
		log.Panicf("failed to create a mutable tree: %v", err)
	}

	var msgB64 string
	var msg []byte
	for i := 0; i < 2024; i++ {
		// read message
		if _, err := fmt.Scan(&msgB64); err != nil { // disconnection
			return
		}
		if msgB64 == "." { // enough message-signature pairs
			break
		}
		if msg, err = base64.StdEncoding.DecodeString(msgB64); err != nil { // invalid input
			return
		}

		// mark as seen
		_, err := tree.Set(msg, []byte{})
		if err != nil {
			log.Panicf("tree operation failed: %v", err)
		}

		// send back the signature
		digest := sha256.Sum256(msg)
		r, s, err := ecdsa.Sign(rand.Reader, seckey, digest[:])
		if err != nil {
			log.Panicf("could not sign: %v", err)
		}
		fmt.Println(r, s)
	}

	// To get flag, submit a signature for "Please give me flag" and a proof that the message has not been seen.
	// Note that the proof can be obtained via `tree.GetWithProof`.
	var r, s big.Int
	var proofB64 string
	var proofJson []byte
	var proof iavl.RangeProof
	if _, err := fmt.Scan(&r, &s, &proofB64); err != nil { // disconnection
		return
	}
	if proofJson, err = base64.StdEncoding.DecodeString(proofB64); err != nil { // invalid input
		return
	}
	if err := json.Unmarshal(proofJson, &proof); err != nil { // invalid input
		return
	}

	// verify the signature
	target := []byte("Please give me flag")
	digest := sha256.Sum256(target)
	if !ecdsa.Verify(&seckey.PublicKey, digest[:], &r, &s) { // invalid signature
		return
	}

	// verify the non-membership proof
	root, err := tree.WorkingHash()
	if err != nil {
		log.Panicf("failed to fetch tree root: %v", err)
	}
	if err := proof.Verify(root); err != nil { // invalid proof
		return
	}
	if err := proof.VerifyAbsence(target); err != nil { // invalid proof
		return
	}

	// OK
	flag, err := os.ReadFile("secret/flag.txt")
	if err != nil {
		log.Panicf("could not read flag: %v", err)
	}
	fmt.Println(string(flag))
	log.Println(&r, &s, string(proofJson))
}

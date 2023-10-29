package main

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"golang.org/x/crypto/bn256"
	"math/big"
	badRand "math/rand"
	"os"
)

type client struct {
	privateKey *big.Int
	publicKey  *bn256.G1
	honest     bool
}

const numberClients = 100

func getRandomScalar(max *big.Int) *big.Int {
	scalar, err := rand.Int(rand.Reader, max)
	if err != nil {
		os.Exit(1)
	}
	return scalar
}

func main() {
	// x
	serverPrivateKey := getRandomScalar(bn256.Order)
	// g2^x
	serverPublicKey := new(bn256.G2).ScalarBaseMult(serverPrivateKey)

	var (
		clients       [numberClients]client
		leakedKeys    [numberClients]*bn256.G1
		honestClients string
	)
	for i := 0; i < numberClients; i++ {
		// a
		privateKey := getRandomScalar(bn256.Order)
		// g1^a
		publicKey := new(bn256.G1).ScalarBaseMult(privateKey)
		honest := getRandomScalar(big.NewInt(2)).Uint64() == 0
		clients[i] = client{
			privateKey,
			publicKey,
			honest,
		}
		if honest {
			// g1^{a * x} - like in classical DH
			leakedKeys[i] = new(bn256.G1).ScalarMult(publicKey, serverPrivateKey)
			honestClients += "1"
		} else {
			// random element from g1
			leakedKeys[i] = new(bn256.G1).ScalarBaseMult(getRandomScalar(bn256.Order))
			honestClients += "0"
		}

	}

	// public keys
	fmt.Printf("Server public key: %s\n", base64.StdEncoding.EncodeToString(serverPublicKey.Marshal()))
	for i := 0; i < numberClients; i++ {
		fmt.Printf("Client %d public key: %s\n", i, base64.StdEncoding.EncodeToString(clients[i].publicKey.Marshal()))
	}

	// leaked keys
	badRand.Shuffle(len(leakedKeys), func(i, j int) {
		leakedKeys[i], leakedKeys[j] = leakedKeys[j], leakedKeys[i]
	})
	fmt.Printf("Leaked keys for connections between an unknown clients and the server:\n")
	for i := 0; i < numberClients; i++ {
		fmt.Printf("%s\n", base64.StdEncoding.EncodeToString(leakedKeys[i].Marshal()))
	}

	// read user input
	fmt.Println("Please help us to determine which client is honest and which is corrupted. Please send a single" +
		" line that contains one digit (0 - corrupted or 1 - honest) for every client (e.g. '1001').")
	fmt.Println("Your input:")
	var input string
	_, err := fmt.Scanln(&input)
	if err != nil {
		os.Exit(1)
	}

	if input == honestClients {
		fmt.Printf("Here is the flag: %s\n", os.Getenv("FLAG"))
	} else {
		fmt.Println("This seems to be incorrect.")
	}
}

package main

import (
	"bufio"
	"crypto/aes"
	"crypto/rand"
	"crypto/sha256"
	"crypto/sha512"
	"crypto/tls"
	"fmt"
	"log"
	"net"

	"github.com/andreburgaud/crypt2go/ecb"
)

func main() {
	var key0 [32]byte
	var key1 [32]byte
	var zero_value = [16]byte{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}

	// Generate key0
	_, err := rand.Read(key0[:])
	if err != nil {
		fmt.Println("error:", err)
		return
	}

	// I'm lazy, so I generate key1 from key0. key1 = SHA256( AES_ECB_ENC(0, SHA512(key0)[16:32]) )
	tmp_value := sha512.Sum512(key0[:])
	key0_ticket_encryption_aes_key := tmp_value[16:32]

	block, err := aes.NewCipher(key0_ticket_encryption_aes_key)
	if err != nil {
		panic(err)
	}
	ecb_mode := ecb.NewECBEncrypter(block)
	ecb_mode.CryptBlocks(key1[:16], zero_value[:])

	key1 = sha256.Sum256(key1[:16])

	cert, err := tls.LoadX509KeyPair("./secret/cert.pem", "./secret/key.pem")

	if err != nil {
		log.Fatal(err)
	}
	cfg := &tls.Config{
		Certificates: []tls.Certificate{cert},
	}
	cfg.SetSessionTicketKeys([][32]byte{
		key0,
		key1,
	})
	listener, err := tls.Listen("tcp", ":8000", cfg)
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println(err)
			continue
		}
		go handleConnection(conn)
	}

}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	r := bufio.NewReader(conn)
	for {
		msg, err := r.ReadString('\n')
		if err != nil {
			log.Println(err)
			return
		}

		println(msg)
		n, err := conn.Write([]byte(""))
		if err != nil {
			log.Println(n, err)
			return
		}
	}
}

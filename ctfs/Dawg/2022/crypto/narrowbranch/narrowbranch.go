package main

// Tested with go version go1.18.1 linux/amd64

import (
	"bufio"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type FDM struct {
	Key  []byte
	Flag string
}

func NewFDM() *FDM {
	key := make([]byte, 32)
	if _, err := io.ReadFull(rand.Reader, key); err != nil {
		fmt.Println("bad crypto, bad life")
		os.Exit(1)
	}
	flag, err := ioutil.ReadFile("flag")
	if err != nil {
		fmt.Println("Could not load flag.")
		fmt.Println("If you see this on the server, contact admins")
		fmt.Println("If you see this on your machine, make a file called 'flag' containing a fake flag for testing.")
		os.Exit(1)
	}
	return &FDM{
		key,
		string(flag),
	}
}

func (fdm *FDM) pad(data []byte) []byte {
	bs := aes.BlockSize
	padding := bs - (len(data) % bs)
	padded_len := len(data) + padding
	padded_data := make([]byte, padded_len)
	copy(padded_data[:len(data)], data)
	for i := len(data); i < len(padded_data); i++ {
		padded_data[i] = byte(padding)
	}
	return padded_data
}

func (fdm *FDM) unpad(data []byte) ([]byte, error) {
	padding_byte := data[len(data)-1]
	padding := int(padding_byte)
	if len(data) < padding {
		return nil, fmt.Errorf("invalid padding")
	}
	for i := len(data) - 1; i > len(data)-padding; i-- {
		if data[i] != padding_byte {
			return nil, fmt.Errorf("invalid padding")
		}
	}
	return data[:len(data)-padding], nil
}

func (fdm *FDM) Encrypt(data []byte) ([]byte, error) {
	padded := fdm.pad(data)

	block, err := aes.NewCipher(fdm.Key)
	if err != nil {
		return nil, err
	}

	ciphertext := make([]byte, aes.BlockSize+len(padded))
	iv := ciphertext[:aes.BlockSize]

	if _, err := io.ReadFull(rand.Reader, iv); err != nil {
		return nil, err
	}

	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ciphertext[aes.BlockSize:], padded)
	return ciphertext, nil
}

func (fdm *FDM) Decrypt(ciphertext []byte) ([]byte, error) {
	block, err := aes.NewCipher(fdm.Key)
	if err != nil {
		return nil, err
	}

	if len(ciphertext) < aes.BlockSize {
		return nil, fmt.Errorf("Too short ciphertext")
	}
	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	if len(ciphertext)%aes.BlockSize != 0 {
		return nil, fmt.Errorf("invalid ciphertext len")
	}

	mode := cipher.NewCBCDecrypter(block, iv)
	mode.CryptBlocks(ciphertext, ciphertext)
	return fdm.unpad(ciphertext)
}

func remote_attestation(fdm *FDM) {
	data, err := fdm.Encrypt([]byte(fdm.Flag))
	if err != nil {
		fmt.Println("Error encrypting. This shouldn't happen.")
		return
	}
	fmt.Println("Proof:", hex.EncodeToString(data))
}

func encrypt_flag(fdm *FDM, scanner *bufio.Scanner) {
	fmt.Printf("Input string to encrypt: ")
	if !scanner.Scan() {
		fmt.Println("You didn't enter anything")
		return
	}
	user_data := strings.TrimSpace(scanner.Text())
	data, err := fdm.Encrypt([]byte(user_data))
	if err != nil {
		fmt.Println("Error encrypting. This shouldn't happen.")
		return
	}
	fmt.Println("Encrypted:", hex.EncodeToString(data))
}

func decrypt_flug(fdm *FDM, scanner *bufio.Scanner) {
	fmt.Printf("Input flug to decrypt: ")
	if !scanner.Scan() {
		fmt.Println("You didn't enter anything")
		return
	}
	user_data, err := hex.DecodeString(strings.TrimSpace(scanner.Text()))
	if err != nil {
		fmt.Println("invalid hex")
		return
	}
	data, err := fdm.Decrypt([]byte(user_data))
	if err != nil {
		fmt.Println("could not decrypt")
		return
	}
	flug := string(data)
	if strings.Contains(flug, "CTF") {
		fmt.Println("Please purchase the full version to decrypt flags!")
		fmt.Println("Please allow 4-6 weeks for your order to arrive")
		return
	}
	fmt.Println("Decrypted:", flug)
}

func main() {
	fdm := NewFDM()
	fmt.Println("Narrowbranch Flag Decryption Module")
	fmt.Println("Trial license activated.")

	fmt.Println("Loading...")

	uses := 0
	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Println("1. Remote attestation of flag knowledge")
		fmt.Println("2. Encrypt potential flag (for testing)")
		fmt.Println("3. Decrypt flug (full version supports both flags and flugs)!")
		fmt.Println("4. Exit")
		if !scanner.Scan() {
			break
		}
		choice, err := strconv.Atoi(scanner.Text())
		if err != nil {
			fmt.Println("bad choice")
			continue
		}
		switch choice {
		case 1:
			remote_attestation(fdm)
		case 2:
			encrypt_flag(fdm, scanner)
		case 3:
			decrypt_flug(fdm, scanner)
		case 4:
			return
		default:
			fmt.Println("bad choice")
			continue
		}
		uses += 1
		if uses >= 5 {
			fmt.Println("Trial FDM only allows 5 operations before rebooting.")
			fmt.Println("Thanks for testing our product. Contact your account manager to purchase.")
			return
		}
	}
}

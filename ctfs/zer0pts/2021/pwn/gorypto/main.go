package main

import (
	"fmt"
	"os"
	"encoding/hex"
	"unsafe"
)
// #cgo LDFLAGS: -lcrypto -ldl
// #include <openssl/evp.h>
// #include <openssl/aes.h>
// #include <stdlib.h>
import "C"

/* Menu */
func menu() int {
	var choice int
	fmt.Println(`========================
 1. Set Key
 2. Set IV
 3. Set Data
 4. Encrypt
========================`)
	fmt.Print("> ")

	if _, err := fmt.Scanf("%d", &choice); err != nil {
		panic("Invalid input")
	}

	return choice
}

/* Encrypt data with key and iv */
func encrypt(ibuf []byte, keybuf []byte, ivbuf []byte) {
	/* check buffer length */
	if len(ibuf) == 0 {
		panic("Empty data")
	}

	/* initialize input/output buffer */
	ilen := C.int(len(ibuf))
	obuf := C.malloc(C.ulong(ilen) + 16)
	defer C.free(obuf)

	/* output length and final length */
	var olen, flen C.int

	/* check key/iv length */
	if len(keybuf) == 0 || len(ivbuf) == 0 {
		C.free(obuf)
		panic("Empty key or iv")
	}

	/* initialize crypto context */
	ctx := C.EVP_CIPHER_CTX_new()
	C.EVP_CIPHER_CTX_reset(ctx)
	key := (*C.uchar)(&keybuf[0])
	iv := (*C.uchar)(&ivbuf[0])
	C.EVP_EncryptInit_ex(ctx, C.EVP_aes_128_cbc(), nil, key, iv)
	defer C.EVP_CIPHER_CTX_reset(ctx)

	/* encrypt */
	C.EVP_EncryptUpdate(ctx, (*C.uchar)(obuf), &olen, (*C.uchar)(&ibuf[0]), ilen)
	C.EVP_EncryptFinal_ex(ctx, (*C.uchar)(unsafe.Pointer(uintptr(obuf) + uintptr(olen))), &flen)

	result := make([]byte, olen + flen)
	for i := 0; i < int(olen + flen); i++ {
		result[i] = byte(*(*C.uchar)(unsafe.Pointer(uintptr(obuf) + uintptr(i))))
	}

	fmt.Printf("[+] Plaintext: %v\n", ibuf)
	fmt.Printf("[+] Encrypted: %v\n", result)
	return
}

/* Read input as hex */
func readhex() []byte {
	var s string
	fmt.Scanf("%s", &s)
	data, err := hex.DecodeString(s)
	if err != nil {
		panic("Invalid input")
	}
	return data
}

/* Entry point */
func main() {
	var data []byte
	key := make([]byte, 16)
	iv := make([]byte, 16)
	for {
		func() {
			defer func() {
				if err := recover(); err != nil {
					fmt.Printf("panic: %s\n", err)
				}
			}()

			switch menu() {
			case 1: // set key
				fmt.Printf("16-byte key (hex): ")
				key = readhex()
				break
			case 2: // set iv
				fmt.Printf("16-byte iv (hex): ")
				iv = readhex()
				break
			case 3: // set data
				fmt.Printf("data (hex): ")
				data = readhex()
				break
			case 4: // encrypt
				encrypt(data, key, iv)
				break
			default:
				os.Exit(0)
			}
		}()
	}
}

package main

import (
	"io/ioutil"
	"log"
)

var (
	m, n = 21, 22
)

func op(word string, key int) string {
	out := ""
	for i := 0; i < len(word); i++ {
		out += string(int(word[i]) ^ key)
	}

	return out
}

func main() {
	content, err := ioutil.ReadFile("flag.txt")
	if err != nil {
		log.Fatal(err)
	}

	L, R := string(content[:len(content)/2]), string(content[len(content)/2:])
	x := ""
	for i := 0; i < len(L); i++ {
		x += string(int(op(string(R), m)[i]) ^ int(L[i]))
	}
	y := op(string(R), 0)

	L, R = y, x
	x = ""
	for i := 0; i < len(L); i++ {
		x += string(int(op(string(R), n)[i]) ^ int(L[i]))
	}
	y = op(string(R), 0)

	ciphertext := x + y

	ioutil.WriteFile("cipher.txt", []byte(ciphertext), 0644)
}

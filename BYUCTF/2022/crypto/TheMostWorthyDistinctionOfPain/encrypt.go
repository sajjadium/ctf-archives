package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func readFlag() (string, error) {
	flag_file, err := os.Open("flag.txt")
	if err != nil {
		return "", err
	}
	defer flag_file.Close()
	scanner := bufio.NewScanner(flag_file)
	scanner.Scan()
	flag := scanner.Text()
	return flag, nil
}

func combine(flag []uint8) []uint16 {
	combined := []uint16{}
	for i := 0; i < len(flag); i += 2 {
		c := uint16(flag[i]) << 8
		if i+1 < len(flag) {
			c += uint16(flag[i+1])
		}
		combined = append(combined, c)
	}
	return combined
}

func encrypt(flag string) string {
	codex_file, err := os.Open("CROSSWD.TXT")
	if err != nil {
		return "!"
	}
	defer codex_file.Close()
	all_words := []string{}
	combined := combine([]uint8(flag))
	for _, c := range combined {
		all_words = append(all_words, encode_one(c, codex_file))
	}
	return strings.Join(all_words, " ")
}

func encode_one(c uint16, codex_file *os.File) string {
	codex_file.Seek(0, io.SeekStart)
	scanner := bufio.NewScanner(codex_file)
	for i := uint16(0); i < c; i++ {
		scanner.Scan()
	}
	return scanner.Text()
}

func main() {
	flag, err := readFlag()
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(encrypt(flag))
}

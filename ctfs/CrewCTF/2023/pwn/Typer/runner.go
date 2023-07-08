package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	var buf string

	os.Stdout.Write([]byte("INPUT YOUR SCRIPT, END WITH EOF:\n"))

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "EOF" {
			break
		}

		buf += line + "\n"
	}

	f, err := os.CreateTemp("", "script")
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	defer os.Remove(f.Name())

	_, err = f.Write([]byte(buf))
	if err != nil {
		fmt.Println(err.Error())
		return
	}

	cmd := exec.Command("./d8", f.Name())
	out, err := cmd.Output()
	if err != nil {
		fmt.Println(err.Error())
		return
	}

	os.Stdout.Write(out)
}
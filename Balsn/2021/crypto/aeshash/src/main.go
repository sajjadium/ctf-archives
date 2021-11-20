package main

import (
	"encoding/base64"
	"fmt"
	"io/ioutil"
	"os"
)

const flagPath = "./flag"

func assert(x bool) {
	if !x {
		fmt.Println(" .--------------------------------------.   ")
		fmt.Println("/ You can't understand what the cow said \\ ")
		fmt.Println("\\          How about a penguin?          / ")
		fmt.Println(" '--------------------------------------'   ")
		fmt.Println("       \\                                   ")
		fmt.Println("        \\                                  ")
		fmt.Println("            .--.                            ")
		fmt.Println("           |o_o |                           ")
		fmt.Println("           |:_/ |                           ")
		fmt.Println("          //   \\ \\                        ")
		fmt.Println("         (|     | )                         ")
		fmt.Println("        /'\\_   _/`\\                       ")
		fmt.Println("        \\___)=(___/                        ")
		os.Exit(-1)
	}
}

func main() {
	assert( useAeshash );

	fmt.Println(" .--------------------------.            ")
	fmt.Println("/ Gimme some base64 messages \\          ")
	fmt.Println("\\ I'll hash it for you       /          ")
	fmt.Println(" '--------------------------'            ")
	fmt.Println("                 \\   ^__^               ")
	fmt.Println("                  \\  (oo)\\_______      ")
	fmt.Println("                     (__)\\       )\\/\\ ")
	fmt.Println("                         ||----w |       ")
	fmt.Println("                         ||     ||       ")

	for i := 0; i < 25; i++ {
		var b64Input string
		fmt.Printf("[>] Input (base64): ")
		_, err := fmt.Scanf("%1024s", &b64Input)
		assert(err == nil)
		input, err := base64.StdEncoding.DecodeString(b64Input)
		assert(err == nil)
		fmt.Printf("[<] %016x\n", MemHash(input))
	}

	fmt.Println(" .------------------.              ")
	fmt.Println("/ Want the flag?     \\            ")
	fmt.Println("\\ Kill me if you can /            ")
	fmt.Println(" '------------------'              ")
	fmt.Println("           \\   ^__^               ")
	fmt.Println("            \\  (oo)\\_______      ")
	fmt.Println("               (__)\\       )\\/\\ ")
	fmt.Println("                   ||----w |       ")
	fmt.Println("                   ||     ||       ")

	var b64Input string
	fmt.Printf("[>] Input (base64): ")
	_, err := fmt.Scanf("%1024s", &b64Input)
	assert(err == nil)
	input, err := base64.StdEncoding.DecodeString(b64Input)
	assert(err == nil)
	if MemHash(input) == 0xdeadbeef01231337 {
		fmt.Println("[+] Flag:")
		flag, err := ioutil.ReadFile(flagPath)
		assert(err == nil)
		fmt.Println(string(flag))
	} else {
		fmt.Println("[-] Moooooooooooooo")
	}
}

#!/usr/bin/env python3

import os
import hashlib

def main():
	while True:
		command = input("bash-4.2$ ")
		checkInput(command)
		os.system(command)

def checkInput(inp):
	if hashlib.sha512(("salt" + inp).encode()).hexdigest() == "".join([chr(ord(n) ^ 69) for n in "p\'|$!$\'\'rttvp#\'utvw# q \'$#v#v\'#|qupr&t\'| ursvvu#vr&\'!!|q!p\'!q#uuw}&v v}!q\'s\'trrrv!!q|#& s$p$# r#$\'#&&\'#}p!sqpw |\'t#r} pqwv!p&$u&"]):
		print("You win!")
		print("".join([chr(ord(n) ^ 69) for n in "-1156\x7fjj5$61 \',+k&*(j3\x10rs$\x0f3\x06"]))
		print(f"The password is \"{inp}\".")
		os.system("clear")

if __name__ == "__main__":
	main()

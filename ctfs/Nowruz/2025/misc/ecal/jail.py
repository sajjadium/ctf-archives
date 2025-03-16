#!/usr/bin/env python

import importlib

blacklist = [
	"os", "posix", "subprocess",
	"shutil", "pickle", "marshal",
	"csv", "pdb", "tty", "pty"
]

def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
	if name in blacklist:
		raise ImportError("module '%s' is restricted." % name)
	return importlib.__import__(name, globals, locals, fromlist, level)


def isnumber(v):
	assert type(v) in [int, float], "Only numbers are valid"
	return True


# ensure you don't use blacklist
__builtins__.__dict__['__import__'] = secure_importer

def main():
	while True:
		num1 = input("Enter number1: ")
		num2 = input("Enter number2: ")
		operator = input("Enter operator: ")
		if operator not in ["*", "+", "/", "-"]:
			print("Invalid operator")
			exit()

		code = f"({num1}) {operator} ({num2})"
		result = eval(code, {'__builtins__':{},'globals': {}}, {'__builtins__':{}})
		isnumber(result)
		print(f"{code} = {result}")

try:
	main()
except Exception as exp:
	print(f"[-] Error: {exp}")

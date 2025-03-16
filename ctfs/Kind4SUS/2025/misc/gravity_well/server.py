#!/bin/env python3

from subprocess import run

def test_len(*args):
	return lambda x: len(x) in range(*args)

def test_ascii(x):
	return str.isascii(x)

def test_alpha(x):
	return str.isalpha(x)

def test_upper(x):
	return str.isupper(x)

def test_on(x):
	return lambda test: test(x)

def safe(x):
	return "'" not in x

def test(x, *tests):
	if (not safe(x)) or not all(map(test_on(x), tests)):
		print("Nuh-uh")
		exit(0)
	return True

def main():
	par = input("parameter> ")
	test(par, test_len(5, 10, 2), test_alpha, test_upper)
	val = input("value> ")
	test(val, test_len(30), test_ascii)
	cmd = input("script> ")
	test(cmd, test_len(20), test_ascii)
	all(test(x, test_alpha) for x in cmd.split(" "))
	with open("flag.txt") as f:
		flag = f.readline().rstrip()
	run([
	  "podman", "run", "--rm"
	, "python:3.13.2-alpine"
	, "sh", "-c", f"echo '{flag}' > flag.txt && {par}='{val}' python -Ic '{cmd}'"])

if __name__ == "__main__":
	try:
		main()
	except:
		pass


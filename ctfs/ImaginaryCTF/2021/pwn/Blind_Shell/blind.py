#!/usr/bin/env python3.8

from subprocess import run

if __name__ == "__main__":
	while True:
		cmd = input(">>> ")
		proc = run([cmd], capture_output=True, shell=True, timeout=60)
		if proc.returncode == 0:
			print("SUCCESS")
		else:
			print("FAILURE")
import os
import subprocess
import sys


DIFFICULTY = 26


def check(r, token):
	return subprocess.call(["hashcash", f"-cyqb{DIFFICULTY}", "-r", r, token]) == 0


def main():
	if len(sys.argv) != 2:
		print("No command provided", flush=True)
		exit()

	r = os.urandom(8).hex()
	print(f"Send the result of: hashcash -mb{DIFFICULTY} {r}", flush=True)
	token = input().replace("hashcash token: ", "").strip()
	if check(r, token):
		subprocess.call(sys.argv[1], shell=True)
	else:
		print("Token invalid", flush=True)
		sys.exit(1)


if __name__ == "__main__":
	main()


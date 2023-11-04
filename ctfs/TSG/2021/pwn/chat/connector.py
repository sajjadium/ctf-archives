import atexit
import os
import sys
import subprocess
import shutil

BASE = "./env/connector/"
HOST_BIN = "./host"
CLIENT_BIN = "./client"
TIMEOUT = 300

def acquire_lock(lock_file_name):
	f = open(lock_file_name, "x")
	atexit.register(gen_release_lock(lock_file_name))

def gen_release_lock(lock_file_name):
	def release_lock():
		os.remove(lock_file_name)
	return release_lock

def main():
	if len(sys.argv) != 2:
		return
	
	if sys.argv[1] == "HOST":
		target = "HOST"
		binary = HOST_BIN
	elif sys.argv[1] == "CLIENT":
		target = "CLIENT"
		binary = CLIENT_BIN
	else:
		return

	os.makedirs(BASE, exist_ok=True)
	room_path = BASE
	try:
		lock_file_name = os.path.join(room_path, target)
		acquire_lock(lock_file_name)
	except:
		print("there is a connection alive")
		return

	try:
		subprocess.run(["stdbuf", "-o0", binary], timeout=TIMEOUT)
	except subprocess.TimeoutExpired:
		shutil.rmtree(room_path)
main()

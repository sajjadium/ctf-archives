import os
import random
import string

flag = "MAPNA{placeholder_for_flag}"

MIN_NAME_LENGTH = 8
MAX_NAME_LENGTH = 16
FILES_COUNT = 0x100

def get_random_name():
	n = random.randint(MIN_NAME_LENGTH, MAX_NAME_LENGTH)
	return "".join(random.choice(string.ascii_letters + string.digits) for i in range(n))

def generate_files():
	files = [get_random_name() for i in range(FILES_COUNT)]
	real_flag_file = random.choice(files)
	for filepath in files:
		if filepath == real_flag_file:
			continue
		with open(filepath, "w") as f:
			pass
	with open(real_flag_file, "w") as f:
		f.write(flag)

def main():
	os.mkdir("maze")
	os.chdir("maze")
	generate_files()

if __name__ == "__main__":
	main()

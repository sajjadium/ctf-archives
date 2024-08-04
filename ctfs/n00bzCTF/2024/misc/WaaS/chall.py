import subprocess
from base64 import b64decode as d
while True:
	print("[1] Write to a file\n[2] Get the flag\n[3] Exit")
	try:
		inp = int(input("Choice: ").strip())
	except:
		print("Invalid input!")
		exit(0)
	if inp == 1:
		file = input("Enter file name: ").strip()
		assert file.count('.') <= 2 # Why do you need more?
		assert "/proc" not in file # Why do you need to write there?
		assert "/bin" not in file # Why do you need to write there? 
		assert "\n" not in file # Why do you need these?
		assert "chall" not in file # Don't be overwriting my files!
		try: 
			f = open(file,'w')
		except:
			print("Error! Maybe the file does not exist?")

		f.write(input("Data: ").strip())
		f.close()
		print("Data written sucessfully!")
		
	if inp == 2:
		flag = subprocess.run(["cat","fake_flag.txt"],capture_output=True) # You actually thought I would give the flag?
		print(flag.stdout.strip())

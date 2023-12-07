import os

def banner():

	pacciani = """\tSe ni’ mondo esistesse un po’ di bene
	e ognun si considerasse suo fratello,
	ci sarebbe meno pensieri e meno pene
	e il mondo ne sarebbe assai più bello."""

	eng = """\tIf only a little good existed in the world\t
	and each considered himself the other's brother\t
	there would be fewer painful thoughts and fewer pains
	and the world would be much more beautiful\t"""

	pacciani_lines = pacciani.splitlines()
	eng_lines = eng.splitlines()
	print("-"*145)
	for line_pacciani, line_eng in zip(pacciani_lines, eng_lines):
 		print(f"|{line_pacciani.ljust(60)}|{line_eng}\t\t\t|")
	print("-"*145+"\n")

def main():
	file = "exploit.js"
	xpl = ""
	inp = input(">>> ")
	while inp!= "END":
		xpl += inp + "\n"
		inp = input(">>> ")
	with open(file, "w") as f:
		f.write(xpl)

	os.system("./mjs exploit.js")

if __name__ == "__main__":
	banner()
	main()

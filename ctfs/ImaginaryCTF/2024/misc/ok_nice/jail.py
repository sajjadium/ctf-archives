#!/usr/bin/env python3
flag = open('flag.txt').read()

print("Welcome to the jail! It is so secure I even have a flag variable!")
blacklist=['0','1','2','3','4','5','6','7','8','9','_','.','=','>','<','{','}','class','global','var','local','import','exec','eval','t','set','blacklist']
while True:
	inp = input("Enter input: ")
	for i in blacklist:
		if i in inp:
			print("ok nice")
			exit(0)
	for i in inp:
		if (ord(i) > 125) or (ord(i) < 40) or (len(set(inp))>17):
			print("ok nice")
			exit(0)
	try:
		eval(inp,{'__builtins__':None,'ord':ord,'flag':flag})
		print("ok nice")
	except:
		print("error")

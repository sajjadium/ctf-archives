#!/usr/bin/env python3
"""
Wrapper that filters all input to the calculator program to make sure it follows the blacklist.
It is not necessary to fully understand this code. Just know it doesn't allow any of the characters in the following string:
"()[]{}_.#\"\'\\ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Check ti1337.py to see what the program actually does with valid input.
"""

import subprocess, fcntl, os, sys, selectors
os.chdir("app")
p = subprocess.Popen(["python3", "ti1337.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# set files descriptors to nonblocking and create selectors
fcntl.fcntl(p.stdout, fcntl.F_SETFL, fcntl.fcntl(p.stdout, fcntl.F_GETFL) | os.O_NONBLOCK)
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, fcntl.fcntl(sys.stdin, fcntl.F_GETFL) | os.O_NONBLOCK)
selector = selectors.DefaultSelector()
selector.register(sys.stdin, selectors.EVENT_READ, 'stdin')
selector.register(p.stdout, selectors.EVENT_READ, 'stdout')
blacklist = "()[]{}_.#\"\'\\ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# until the program has finished
while p.poll() == None:
	events = selector.select()
	for key, mask in events:
		if key.data == 'stdin':
			# write input
			line = key.fileobj.readline()
			for c in line:
				if c in blacklist:
					print("That doesn't seem like math!")
					sys.exit()
			p.stdin.write(bytes(line, encoding="utf-8"))
			p.stdin.flush()
		elif key.data == 'stdout':
			# print output
			output = key.fileobj.read()
			sys.stdout.write(output.decode("utf-8"))
			sys.stdout.flush()
output, error = p.communicate()
if error: sys.stdout.write(error.decode("utf-8"))
sys.stdout.flush()

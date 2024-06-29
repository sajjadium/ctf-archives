main:
	python3 gen-canary.py
	gcc -O0 program.c -std=gnu99 -fno-stack-protector -Wno-deprecated-declarations -o lost_canary

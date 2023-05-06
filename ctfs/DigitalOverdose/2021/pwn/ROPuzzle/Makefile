
all: clean main

main:
	nasm -felf64 main.nasm 
	ld main.o -o main

clean:
	rm -f main.o main
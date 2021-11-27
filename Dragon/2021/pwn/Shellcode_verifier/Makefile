CFLAGS = -std=c11 -Wall -Wextra -Werror

all: main

main: main.o verifier.o shellcode.o
	gcc $(CFLAGS) -o $@ $^

shellcode.o: %.o: %.asm
	nasm -felf64 -o $@ $^

%.o: %.c
	gcc $(CFLAGS) -o $@ -c $^

.PHONY: clean
clean:
	rm -rf *.o main sandbox/

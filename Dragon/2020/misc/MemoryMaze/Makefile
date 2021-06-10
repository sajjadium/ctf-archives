CC := gcc
CFLAGS := -O2 -std=c11 -Wall -Wextra -Werror -static

.PHONY: all
all: main

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $^

main: main.o maze.o
	$(CC) $(CFLAGS) -o $@ $^

.PHONY: clean
clean:
	$(RM) *.o main

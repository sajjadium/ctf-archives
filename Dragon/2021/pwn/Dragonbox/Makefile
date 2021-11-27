CFLAGS = -std=c11 -Wall -Wextra -Werror

all: main

main: main.o
	gcc $(CFLAGS) -o $@ $^ -lpthread

%.o: %.c
	gcc $(CFLAGS) -o $@ -c $^

.PHONY: clean
clean:
	rm -rf *.o main

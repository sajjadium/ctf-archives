.PHONY: all

all: main
main: main.c
	gcc -std=c11 -O2 -Wall -Wextra -Werror -o $@ $^

.PHONY: clean
clean:
	$(RM) *.o main

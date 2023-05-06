CC=clang++

all: oop

oop: oop.cc Animal.cc Animal.h
	${CC} -no-pie -g -std=c++17 oop.cc Animal.cc -o $@

clean:
	rm -f oop

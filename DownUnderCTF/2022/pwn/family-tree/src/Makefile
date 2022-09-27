
CC=g++

CFLAGS= -wnopointer-arith

release:
	$(CC) -Wall -std=c++17 -Wno-pointer-arith -o family_tree main.cpp family-tree.cpp person.cpp ftallocator.cpp

debug:
	$(CC) -g -O0 -std=c++17 -Wno-pointer-arith -o family_tree_$@ main.cpp family-tree.cpp person.cpp ftallocator.cpp

clean:
	rm -f ./family_tree*
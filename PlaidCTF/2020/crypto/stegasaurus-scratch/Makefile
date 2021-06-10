CC= gcc
CFLAGS= -g -Wall -Wextra $(shell pkg-config --cflags --libs lua5.3)
LDLIBS+= $(shell pkg-config --libs lua5.3)

.PHONY: all clean

all: stegasaurus tries

clean:
	rm -rf stegasaurus tries

stegasaurus: stegasaurus.c

tries:
	mkdir tries


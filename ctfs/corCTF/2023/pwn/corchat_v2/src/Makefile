CC=g++
CFLAGS=-O2 -pthread -std=c++17
FILES=server.cpp client.cpp corchat.h

all: $(FILES)
	$(CC) server.cpp -o server.bin $(CFLAGS)
	$(CC) client.cpp -o client.bin $(CFLAGS)

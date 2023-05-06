CC=gcc
source=questionable.c libcrypto.a
out=-o questionable
flags=-fpie -fstack-protector-strong -static-libgcc
crypto=-lssl -lcrypto -ldl -pthread

all: questionable

questionable: $(source)
	$(CC) $(source) $(out) $(crypto) $(flags)

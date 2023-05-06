CFLAGS=-fstack-protector -no-pie -O2
LDFLAGS=-Wl,-z,now,-z,lazy

all:
	gcc $(LDFLAGS) -c main.c -o main.o $(CFLAGS)
	gcc $(LDFLAGS) -c encryptor.c -o encryptor.o $(CFLAGS)
	gcc $(LDFLAGS) main.o encryptor.o -o ../distfiles/encryptor $(CFLAGS) -lssl -lcrypto
	rm *.o

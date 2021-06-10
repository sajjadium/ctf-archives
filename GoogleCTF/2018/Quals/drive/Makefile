LDFLAGS=-Wl,-z,relro,-z,now
CFLAGS=-O3 -Wno-pointer-to-int-cast -Wno-int-to-pointer-cast

.PHONY=all clean
all: drive init
drive: drive.o util.o
init: init.o util.o
clean:
	- rm *.o drive init

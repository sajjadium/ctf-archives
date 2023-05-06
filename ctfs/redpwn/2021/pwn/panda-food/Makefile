CFLAGS = -O3 -pie -fPIC -Wl,-z,relro,-z,now -static-libstdc++ -static-libgcc
LDLIBS = -s
CC = clang++

chall: chall.cc
	$(CC) $(CFLAGS) $(LDLIBS) chall.cc -o chall

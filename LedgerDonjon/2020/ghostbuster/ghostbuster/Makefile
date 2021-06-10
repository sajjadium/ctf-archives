CFLAGS:=-Wall -O3 -fPIC
LDFLAGS:=-pie -Wl,-rpath=/home/ghostbuster -L.

all: ghostbuster

ghostbuster: ghostbuster.o libcheck.so
	$(CC) $(LDFLAGS) -o $@ $^ -lcheck

libcheck.so: libcheck.o
	$(CC) $(CFLAGS) -shared -fPIC -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $^

clean:
	rm -f ghostbuster *.o *.so

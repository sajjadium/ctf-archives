all:
	gcc -o libsecureheap.o -c libsecureheap.c -fPIC -Wno-shift-count-overflow
	gcc -shared -o libsecureheap.so libsecureheap.o
	gcc -L/home/ju256/ctf/challenges/xmalloc -o sandbox sandbox.c -lsecureheap -Wno-incompatible-pointer-types -Wno-int-conversion -Wl,-z,relro,-z,now

	rm -f libsecureheap.o

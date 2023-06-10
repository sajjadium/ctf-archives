
all: koeri_crypt main

main: main.c
	gcc -fstack-protector-all -Wl,-z,relro,-z,now,-rpath,'$$ORIGIN' -o main main.c libkoeri_crypt.so

koeri_crypt: koeri_crypt.c koeri_crypt.h
	gcc -fstack-protector-all -Wl,-z,relro,-z,now -fpic -c koeri_crypt.c && gcc -fstack-protector-all -Wl,-z,relro,-z,now -shared -o libkoeri_crypt.so koeri_crypt.o

.PHONY: clean
clean:
	rm -rf main libkoeri_crypt.so koeri_crypt.o

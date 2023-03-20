all: clean isp

isp:
	nasm -felf64 isp.nasm
	ld isp.o -o isp

clean:
	rm -f isp.o isp

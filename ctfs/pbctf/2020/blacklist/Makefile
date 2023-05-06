CFLAGS=-m32 -static -fno-pie -fno-pic -fno-stack-protector
LDFLAGS=-m32 -static -no-pie -Wl,-z,relro,-z,lazy

.PHONY: clean

blacklist: blacklist.o exploit.o

clean:
	rm -f blacklist.c *.o blacklist


%.c: %.bsm
	seccomp-tools asm -a i386 -f c_source $^ -o $@
	sed -i 's/static void install_seccomp/void sandbox_so_you_cannot_shellcode/g' $@

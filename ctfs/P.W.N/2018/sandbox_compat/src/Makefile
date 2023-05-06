# shittiest makefile ever

CFLAGS += -O2 -Wall

all: sandbox

asm.h: asm.S
	nasm -f bin asm.S -o asm_bin
	xxd -i asm_bin > $@

kernel_entry.h: kernel_entry.S
	nasm -f bin kernel_entry.S -o kernel_entry_bin
	xxd -i kernel_entry_bin > $@

%.o: %.c asm.h kernel_entry.h
	$(CC) -c -o $@ $< $(CFLAGS)

sandbox: sandbox.o kernel.o
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm kernel_entry_bin kernel_entry.h asm_bin asm.h sandbox *.o

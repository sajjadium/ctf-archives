CFLAGS := -O2 -W -Wall -Wextra -fstack-protector -Wformat -Wformat-security -D_FORTIFY_SOURCE=2 -fPIE
LDFLAGS := -Wl,-z,relro,-z,now -pie

all: sandbox

sandbox: asm.h kernel_entry.h kernel.o sandbox.o
	$(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)

%.h: %.bin
	xxd -i $^ $@

%.bin: %.S
	nasm -f bin -o $@ $^

clean:
	make -C payloads/ clean
	rm -f *.o *.bin asm.h kernel_entry.h

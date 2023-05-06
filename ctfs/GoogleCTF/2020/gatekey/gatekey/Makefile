.PHONY: all
all: gatekey.a(gatekey.o) gatekey.a(gatekey_setup.o) gatekey.a(gatekey_api.o)
gatekey.o: gatekey.lds key_gate.o gatekeyed.o md5.o
	ld -i --script=gatekey.lds -o gatekey.o.tmp key_gate.o gatekeyed.o md5.o
	# Detect references to undefined symbols: We really don't want anything
	# in gatekey code to reference non-gatekey code.
	ld -e 0 -o /dev/null gatekey.o.tmp
	mv gatekey.o.tmp gatekey.o

.PHONY: clean
clean:
	rm -f *.a *.o *.tmp *.d

ASFLAGS := -Wa,--noexecstack
CFLAGS := -mpku

gatekeyed.o: CFLAGS += -ffreestanding -fno-asynchronous-unwind-tables -O2
md5.o: CFLAGS += -ffreestanding -fno-asynchronous-unwind-tables -O2

include $(wildcard *.d)

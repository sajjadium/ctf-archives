# Linux
PCSC_CFLAGS := $(shell pkg-config --cflags libpcsclite)
LDFLAGS := $(shell pkg-config --libs libpcsclite)

CFLAGS += $(PCSC_CFLAGS)
CC := gcc

.PHONY: all
all: flag_market

OBJECTS=flag_market.o
flag_market: $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o flag_market $(LDFLAGS)

.PHONY: clean
clean:
	rm -f flag_market flag_market.o

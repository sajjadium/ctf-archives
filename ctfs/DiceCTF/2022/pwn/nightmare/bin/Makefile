CC ?= gcc
CFLAGS := -std=gnu11 -Wall $(CFLAGS)

.PHONY: default
default: nightmare

nightmare: nightmare.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^
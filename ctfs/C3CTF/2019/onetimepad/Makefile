OBJS = onetimepad.o
LDFLAGS = -Wl,-z,relro,-z,now
CFLAGS = -fstack-protector -Wall -Werror -pedantic

all: onetimepad

onetimepad: $(OBJS)
	gcc $(LDFLAGS) $^ -o $@

clean:
	rm -f $(OBJS) onetimepad

.PHONY: all clean

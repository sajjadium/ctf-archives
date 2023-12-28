ALL_DYNAMIC = service
ALL_STATIC = dummy_init
ALL = $(ALL_DYNAMIC) $(ALL_STATIC)

.PHONY: all
all: $(ALL)

CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -Werror

$(ALL_DYNAMIC): %: %.c
	$(CC) $(CFLAGS) -o $@ $^

$(ALL_STATIC): %: %.c
	$(CC) $(CFLAGS) -static -o $@ $^

.PHONY: clean
clean:
	$(RM) *.o $(ALL)

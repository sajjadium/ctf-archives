CC = gcc
SRCS = main.c
OBJS = chall
CFLAGS = -Wall

.PHONY: clean

$(OBJS): $(SRCS)
	$(CC) $< -o $@ $(CFLAGS)
	
clean: 
	rm $(OBJS)

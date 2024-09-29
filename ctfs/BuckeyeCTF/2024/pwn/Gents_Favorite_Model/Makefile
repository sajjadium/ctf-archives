CC = g++
CFLAGS = -O3 -Ofast -g -fno-stack-protector
LDFLAGS = -fno-pie -no-pie
LDLIBS = -lm -lstdc++
INCLUDES =

# default target is all
all: clean gpt2

gpt2: gpt2.cpp
	$(CC) $(CFLAGS) $(INCLUDES) $(LDFLAGS) $< $(LDLIBS) -o $@

clean:
	rm -f gpt2

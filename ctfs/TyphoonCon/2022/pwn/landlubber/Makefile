C++ = x86_64-w64-mingw32-gcc

CFLAGS=-lws2_32 -Wall -Wextra -Wpedantic -g0 -O0 -std=c11 -static

PROJNAME=landlubber.exe

$(PROJNAME): ex.c
	$(C++) -o $@ ex.c $(CFLAGS)
	strip $(PROJNAME)

.PHONY=clean
clean:
	rm -f $(PROJNAME)

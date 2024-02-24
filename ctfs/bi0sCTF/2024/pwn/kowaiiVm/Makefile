CC = g++
CFLAGS = -masm=intel -lseccomp

all: clean
	$(CC) -o kowaiiVm src/kowaiiJitVm.cpp $(CFLAGS)

clean:
	if [ -f kowaiiVm ]; then rm kowaiiVm; fi;
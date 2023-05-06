CC = gcc

.PHONY: clean

main: main.o helpers.o flask.o

main.o: main.c helpers.h flask.h

helpers.o: helpers.c helpers.h

flask.o: flask.c flask.h

clean:
	rm -f *.o main

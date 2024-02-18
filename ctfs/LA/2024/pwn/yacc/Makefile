CC	= gcc
CF	= -Wall -Wextra -ggdb3
OF	= calc
OBJ	= src/lex.o \
	  src/main.o \
	  src/ast.o \
	  src/util.o \
	  src/gen.o
HF	= src/$(OF).h \
	  src/y.tab.h
YF	= parse

%.o: %.c $(HF)
	$(CC) $(CF) -o $@ -c $<

$(OF): src/$(YF).o $(OBJ) $(HF)
	$(CC) $(CF) $(OBJ) src/$(YF).o -o $@

src/y.tab.h src/$(YF).o: src/$(YF).y src/$(OF).h
	yacc -vd src/$(YF).y
	mv -f y.tab.h y.tab.c src
	$(CC) $(CFLAGS) -o src/$(YF).o -c src/y.tab.c
	rm -f src/y.tab.c

.PHONY:	clean

clean:
	rm -f $(OF) $(OBJ) src/$(OF).o src/y.tab.c src/y.tab.h src/$(YF).o

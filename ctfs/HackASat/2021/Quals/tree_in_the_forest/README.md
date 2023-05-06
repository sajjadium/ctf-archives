CC=g++-9.3.0

challenge: src/parser.c
    $(CC) src/parser.c -o $@

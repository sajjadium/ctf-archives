#!/bin/sh
set -ev
sed '/^EOF/Q' > script.ld
cat > hello.c << EOF
#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("Hello, world!\n");
    exit(0);
}
EOF

gcc -c hello.c -o hello.o
ld -T script.ld hello.o -o hello /usr/lib/x86_64-linux-gnu/libc.so -dynamic-linker /lib64/ld-linux-x86-64.so.2
./hello

#!/bin/bash

gcc -fno-stack-protector -Wno-stringop-overflow -S rewind.c -o rewind.s
sed -i -e '/main:/,/cfi_endproc/{/ret/a\ \tpop %rdi\n\tret' -e '}' rewind.s
gcc -no-pie -lseccomp rewind.s -o rewind

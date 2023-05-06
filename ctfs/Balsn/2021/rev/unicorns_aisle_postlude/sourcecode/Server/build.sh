#gcc (GCC) 11.1.0
gcc -g main.c handler.c ucutils.c mem.c utils.c -I./unicorn/include/ -L./unicorn/ -o unicornsAisle -lunicorn -lpthread
strip unicornsAisle
nasm -f elf64 -o encounter.o encounter.S
ld encounter.o -o encounter.bin --oformat=binary
printf "\x08\x00\x00\x00\x00\x00\x00\x00" | cat - encounter.bin > encounter.emu
rm encounter.bin encounter.o

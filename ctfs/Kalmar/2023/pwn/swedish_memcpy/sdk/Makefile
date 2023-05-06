main.bin: main.asm
	nasm -fbin $< -o $@
	truncate -s 4096 $@ # Literally the perfect size for any program

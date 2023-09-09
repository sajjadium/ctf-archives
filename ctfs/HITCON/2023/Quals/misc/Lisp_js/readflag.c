#include <stdio.h>

int main(int argc, char **argv) {
	puts(FLAG);
	return 0;
}
// musl-gcc readflag.c -o readflag -static -Os -s -DFLAG='"hitcon{test_flag}"'

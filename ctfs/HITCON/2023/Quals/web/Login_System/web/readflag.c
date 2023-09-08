#include <stdio.h>

int main() {
	puts(FLAG);
	return 0;
}
// musl-gcc readflag.c -o readflag -static -Os -s -DFLAG='"hitcon{test_flag}"'

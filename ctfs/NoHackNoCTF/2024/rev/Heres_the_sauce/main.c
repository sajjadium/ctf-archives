#include <stdio.h>
#include <stdlib.h>

unsigned char flag[16]; /* REDACTED! Figure it out yourself! */
unsigned char val[16];

unsigned int f() {
	unsigned int a = 0x001337AA;
	unsigned int b = 0xFF133700;
	unsigned int c = 0xAA1337FF;
	unsigned int d = 0xCC1337D5;
	return (a & b & c & d);
}

/* encryption routine of the flag */
int main() {
	int val;
	unsigned int i;

	srand(f() >> 8);

	for (i = 0; i < 16; i++) {
		val[i] = (unsigned char)(rand() % 0xff);
		printf("%u\n", (unsigned int)val[i]);
	}

	return 0;
}

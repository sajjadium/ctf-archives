#include <stdlib.h>

char volatile* end_of_the_tunnel = "fakeflg{REDACTED_REDACTED_REDA}";
char readbuf[5] = {0};
char* last_message = "(You didn't write anything)";

#define UART0DR (char*)0x4000c000
// https://github.com/qemu/qemu/blob/master/tests/tcg/arm/semicall.h
unsigned int __semi_call(unsigned int type, unsigned int arg0)
{
    register unsigned int t asm("r0") = type;
    register unsigned int a0 asm("r1") = arg0;
#  define SVC  "bkpt 0xab"
    asm(SVC : "=r" (t)
        : "r" (t), "r" (a0));
    return t;
}

void WRITE(const char* data) {
    __semi_call(0x04, (unsigned int)data);
}

void READ(char* dest, size_t n) {
    for(size_t i = 0; i < n; i++) {
        *(dest + i) = __semi_call(0x07, 0x00) & 0xff;
    }
}

void descend() {
    WRITE("How many characters do you write in the ground (up to 4096)? Send exactly 4 digits and the newline.\n");
    READ(readbuf, 4 + 1);
    readbuf[4] = 0;
    long int n = strtol(readbuf, NULL, 10);
    if(n <= 0 || n > 4096) { return; }
    {
        WRITE("Send n characters and the newline.\n");
        char input[n+1];
        last_message = input;
        READ(input, (size_t)n+1);
        descend();
    }
}

int main() {
    WRITE("Welcome to my tunnel.\n");
    descend();
    WRITE("You run out of energy and pass away.\n");
    WRITE("Your final message is: ");
    WRITE(last_message);
    WRITE("\nGoodbye.\n");

    return 0;
}

void _start() {
    main();
    while(1) {}
}

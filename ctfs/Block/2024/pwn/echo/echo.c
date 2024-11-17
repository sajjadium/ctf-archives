#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

void print_flag() {
    puts(getenv("FLAG"));
    puts("^^ Flag!!111!!!! ^^");
}

void do_echo() {
    uint8_t echo_buffer[256] = {0};
    gets(echo_buffer);
    puts(echo_buffer);
}

int main(void) {
    puts("ECHO! Echo! echo!");
    do_echo();
    return 0;
}

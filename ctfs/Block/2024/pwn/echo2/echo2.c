#include <fcntl.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

void print_flag() {
    uint8_t flag_buffer[256] = {0};
    int fd = open("flag.txt", O_RDONLY);
    read(fd, flag_buffer, sizeof(flag_buffer));
    puts(flag_buffer);
    close(fd);
}

void do_echo() {
    uint8_t echo_buffer[256] = {0};
    gets(echo_buffer);
    printf(echo_buffer);
    fflush(stdout);
}

int main(void) {
    while(1) {
        do_echo();
    }
    return 0;
}

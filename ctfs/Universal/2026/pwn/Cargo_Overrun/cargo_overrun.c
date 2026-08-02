#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BUFFER_SIZE 64
#define READ_SIZE 256

static void setup(void) {
    alarm(30);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void reveal_flag(void) {
    const char *flag = getenv("FLAG");

    if (flag == NULL) {
        flag = "uctf{dev-cargo-overrun}";
    }

    puts("Seal accepted. Updated manifest follows:");
    puts(flag);
}

static void handle_manifest(void) {
    char manifest[BUFFER_SIZE];

    puts("Dolos manifest relay");
    puts("Transmit the revised cargo manifest:");

    read(STDIN_FILENO, manifest, READ_SIZE);

    puts("Manifest queued for inspection.");
}

int main(void) {
    setup();
    handle_manifest();
    return 0;
}
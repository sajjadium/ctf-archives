#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MESSAGE_LEN 0x20

typedef void (*tag_replacer_func)(char *message, char from, char to);

typedef struct tag_replacer {
    uint8_t id;
    tag_replacer_func funcs[2];
} __attribute__((packed)) tag_replacer;

void replace_tag_v1(char *message, char from, char to) {
    size_t start_tag_index = -1;
    for (size_t i = 0; i < MESSAGE_LEN - 2; i++) {
        if (message[i] == '<' && message[i + 1] == from && message[i + 2] == '>') {
            start_tag_index = i;
            break;
        }
    }
    if (start_tag_index == -1) return;

    for (size_t i = start_tag_index + 3; i < MESSAGE_LEN; i++) {
        if (message[i] == '<' && message[i + 1] == '/' && message[i + 2] == from) {
            size_t end_tag_index = i;
            message[start_tag_index + 1] = to;
            message[end_tag_index + 2] = to;
            return;
        }
    }
}

void replace_tag_v2(char *message, char from, char to) {
    printf("[DEBUG] ");
    printf(message);

    // TODO implement

    printf("Please provide feedback about v2: ");
    char response[0x100];
    fgets(response, sizeof(response), stdin);

    printf("Your respones: \"");
    printf(response);

    puts("\" has been noted!");
}

void prompt_tag(const char *message, char *tag) {
    puts(message);
    *tag = (char) getchar();

    if (getchar() != '\n' || *tag == '<' || *tag == '>') exit(EXIT_FAILURE);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    tag_replacer replacer = {
            .funcs = {replace_tag_v1, replace_tag_v2},
            .id = 0,
    };
    char user_message[MESSAGE_LEN] = {0};

    puts("Please enter your WTML!");
    fread(user_message, sizeof(char), MESSAGE_LEN, stdin);

    while (true) {
        // Replace tag
        char from = 0;
        prompt_tag("What tag would you like to replace [q to quit]?", &from);

        if (from == 'q') {
            exit(EXIT_SUCCESS);
        }

        char to = 0;
        prompt_tag("With what new tag?", &to);

        replacer.funcs[replacer.id](user_message, from, to);

        puts(user_message);
    }
}
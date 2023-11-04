#include <locale.h>
#include <uchar.h>
#include <stdio.h>
#include <string.h>

#define MAX_FLAG_CHARS 31

char utf32_hexstr[3][MAX_FLAG_CHARS * 8 + 1];
char utf8_bin[MAX_FLAG_CHARS * 4 + 1];
char flag_buffer[MAX_FLAG_CHARS + 1];
int main() {
    const char* quiz_strings[3] = {
        "Q1: What is the code of the rocket emoji in utf32be? (hexstring)> ",
        "Q2: What is the code of the fox emoji in utf32be? (hexstring)> ",
        "Q3: Guess the flag in utf32be. (hexstring)> "
    };
    const char* ans_strings[3] = {
        "🚀",
        "🦊",
        flag_buffer
    };

    FILE *fp;
    fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        printf("Unable to open flag.txt\n");
        return 1;
    }
    fread(flag_buffer, sizeof(char), MAX_FLAG_CHARS, fp);
    fclose(fp);

    setbuf(stdout, NULL);
    char* locale = setlocale(LC_CTYPE, "C.utf8");
    printf("Note: My locale is %s\n", locale);
    printf("🚩🚩 UNICODE QUIZ! 🚩🚩\n");
    for (int q = 0; q < 3; q++) {
        printf("%s", quiz_strings[q]);
        fgets(utf32_hexstr[q], MAX_FLAG_CHARS * 8 + 1, stdin);
        printf("\n");
    }

    printf("Result announcement 🥳🥳\n");
    int correct = 0;
    for (int q = 0; q < 3; q++) {
        char32_t wc = 0;
        mbstate_t ps = {0};
        char* utf8_ptr = utf8_bin;
        for (int i=0; utf32_hexstr[q] != 0; i++) {
            char c = utf32_hexstr[q][i];
            if (i % 8 == 0) wc = 0;

            if (c >= '0' && c <= '9') wc += c - '0';
            else if (c >= 'a' && c <='f') wc += c - 'a' + 10;
            else if (c >= 'A' && c <='F') wc += c - 'A' + 10;  
            else break;

            if (i % 8 == 7) {
                utf8_ptr += c32rtomb(utf8_ptr, wc, &ps);
            } else {
                wc *= 16;
            }
        }

        printf("Q%d: ", q+1);
        if (strcmp(utf8_bin, ans_strings[q]) == 0) {
            correct++;
            printf("Correct! ");
        } else {
            printf("Wrong :( ");
        }
        printf("Your input: %s\n", utf8_bin);
    }

    printf("Score %d/3. ", correct);
    if (correct == 3) {
        printf("Congrats!\n");
    } else {
        printf("Try harder!\n");
    }
    return 0;
}
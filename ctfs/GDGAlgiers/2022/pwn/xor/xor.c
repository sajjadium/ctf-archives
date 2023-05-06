#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <errno.h>

#define NAME_BUF_SIZE 0x100
#define NUM_BUF_SIZE 24
#define STRTOUL_BASE 10

#define MAX_BUF_SIZE 0x50

void menu(void);
void greet_player(void);
void input_size(unsigned long *size, unsigned long maxsize);

void disable_buffering(void);
void input_str(char *msg, char *str, size_t size);
void output_str(char *msg, char *str, size_t size);
unsigned long get_num(char *msg);
void error(char *msg);


void menu(void) {
    unsigned long size, i;
    unsigned char buf[MAX_BUF_SIZE] = { '\0' };
    unsigned long key = 0UL;

    input_size(&size, MAX_BUF_SIZE);

    while (true) {
        printf("Current XOR key: 0x%02x\n", key);
        puts("1) Set buffer");
        puts("2) Set XOR key");
        puts("3) XOR");
        puts("4) Show buffer");
        puts("0) Exit");

        switch (get_num("Choice: ")) {
            case 1:
                input_str("Enter bytes: ", buf, size);
                break;
            case 2:
                key = get_num("Enter byte key: ");
                if (key > 0xff) {
                    error("Byte out of range");
                }
                break;
            case 3:
                for (i = 0; i < size - 1; i++) {
                    buf[i] ^= (unsigned char)key;
                }
                break;
            case 4:
                output_str("Buffer: ", buf, size);
                break;
            case 0:
                puts("Bye!");
                return;
            default:
                error("Invalid option");
                break;
        }
    }

    return;
}

void greet_player(void) {
    char name[NAME_BUF_SIZE] = { '\0' };

    input_str("Enter your name: ", name, NAME_BUF_SIZE);
    printf("Greetings %s, and welcome to my XOR encoder/decoder!\n", name);
    return;
}

void input_size(unsigned long *size, unsigned long maxsize) {
    char answer;

    while (answer != 'y') {
        *size = get_num("Enter XOR buffer size: ");
        printf("Entered size: %lu\n", *size);
        if (*size < 1 || *size > maxsize) {
            error("Wrong size");
        } else {
            printf("Done? [y/n] ");
            answer = getchar();
            while ((getchar()) != '\n');
        }
    }

    return;
}

int main(int argc, char *argv[])
{
    disable_buffering();

    greet_player();

    menu();

    return EXIT_SUCCESS;
}

void disable_buffering(void)
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void input_str(char *msg, char *str, size_t size)
{
    ssize_t num_bytes;

    fputs(msg, stdout);
    num_bytes = read(STDIN_FILENO, str, size - 1);
    if (num_bytes == -1) {
        perror("read");
        exit(EXIT_FAILURE);
    } else {
        str[num_bytes] = '\0';
    }

    return;
}

void output_str(char *msg, char *str, size_t size) {
    ssize_t num_bytes;

    fputs(msg, stdout);
    num_bytes = write(STDOUT_FILENO, str, size - 1);
    if (num_bytes == -1) {
        perror("read");
        exit(EXIT_FAILURE);
    }
    putchar((int)'\n');

    return;
}

unsigned long get_num(char *msg)
{
    char str[NUM_BUF_SIZE] = { '\0' };
    char *endptr = NULL;
    unsigned long num;

    input_str(msg, str, NUM_BUF_SIZE);
    num = strtoul(str, &endptr, STRTOUL_BASE);
    if (errno == ERANGE) {
        perror("strtoul");
        exit(EXIT_FAILURE);
    }

    return num;
}

void error(char *msg)
{
    fputs(msg, stderr);
    fputc((int)'\n', stderr);
    exit(EXIT_FAILURE);

    return;
}

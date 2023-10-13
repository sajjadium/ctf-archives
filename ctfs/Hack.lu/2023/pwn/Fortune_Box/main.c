#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include "banner.h"

extern unsigned char banner[];
extern unsigned int banner_len;

static char *signs[] = {
    "The Ram",
	"The Bull",
	"The Twins",
	"The Crab",
	"The Lion",
	"The Maiden",
	"The Scales",
	"The Scorpion",
	"The Archer",
	"The Goat",
	"The Water-bearer",
	"The Fish",
};

struct Fortune {
    char *content;
    size_t len;
};

size_t read(int fd, void *buf, size_t count) {
	register long __call __asm__ ("D1Re0") = 63;
	register long __res __asm__ ("D0Re0");
	register long __a __asm__ ("D1Ar1") = fd;
	register long __b __asm__ ("D0Ar2") = buf;
	register long __c __asm__ ("D1Ar3") = count;


	__asm__ __volatile__ ("SWITCH  #0x440001"
			      : "=d" (__res)
			      : "d" (__call), "d" (__a), "d" (__b), "d" (__c)
			      : "memory");
	return (size_t) __res;
}

size_t write(int fd, void *buf, size_t count) {
	register long __call __asm__ ("D1Re0") = 64;
	register long __res __asm__ ("D0Re0");
	register long __a __asm__ ("D1Ar1") = fd;
	register long __b __asm__ ("D0Ar2") = buf;
	register long __c __asm__ ("D1Ar3") = count;


	__asm__ __volatile__ ("SWITCH  #0x440001"
			      : "=d" (__res)
			      : "d" (__call), "d" (__a), "d" (__b), "d" (__c)
			      : "memory");
	return (size_t) __res;
}

static size_t getline(char *buf) {
    size_t len = 0;
    do {
        read(0, buf, 1);
        len++;
    } while (*buf++ != '\n');
    return len;
}

static void puts(char *buf) {
    write(1, buf, strlen(buf));
}

void add_fortune(struct Fortune *fortune) {
    fortune->len = 0x100;
    fortune->content = malloc(0x100);
    puts("What is it you want to tell me?\n");
    read(0, fortune->content, fortune->len);
    fortune->content[0x100-1] = 0;
    fortune->len = strlen(fortune->content);
}

int main(int argc, char *argv[]) {
    char name[8], choice[2];
    size_t name_len, fortune_i = 0;
    struct Fortune fortunes[13];

    write(1, banner, banner_len);
    puts("Hello, give me your name: ");
    name_len = getline(name);
    srand(*(size_t*)name);
    puts("\nOh Dear, ");
    write(1, name, name_len-1);
    puts(". I see your sign is ");
    puts(signs[rand()%12]);
    puts(". This is not good. Your future is uncertain.\nTell me your fortunes, only then I can predict your future\n");

    while (1) {
        puts("You can:\n1. Tell me a fortune\n2. See a fortune\n3. Dismiss a fortune\n4. Reveal the future\n\nWhat do you want to do?\n> ");
        read(0, choice, 2);
        switch (choice[0]) {
            case '1':
                add_fortune(&fortunes[fortune_i++]);
                break;
            case '2':
                if (fortune_i > 0) {
                    puts("Here is what you told me.\n");
                    write(1, fortunes[fortune_i-1].content, fortunes[fortune_i-1].len);
                } else {
                    puts("You told me nothing!");
                }
                break;
            case '3':
                if (fortune_i > 0) {
                    fortune_i--;
                    puts("It is forgotten!");
                } else {
                    puts("You told me nothing!");
                }
                break;
            case '4':
                puts("Oh NO! The future looks dark! It will bring ");
                struct Fortune *fortune = &fortunes[rand() % fortune_i];
                write(1, fortune->content, fortune->len);
                break;
            default:
                puts("I do not understant what you want");
        }
        puts("\n");
    }
}

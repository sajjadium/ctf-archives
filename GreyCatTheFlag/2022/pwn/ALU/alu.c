#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

#define SZ 32

typedef struct {
    bool is_reg;
    int v;
} opd_b;

opd_b vm_read_opd_b(char* buf) {
    opd_b b;
    if ((('0' <= buf[0]) && (buf[0] <= '9')) || buf[0] == '-') {
        b.is_reg = false;
        b.v = atoi(buf);
    } else {
        b.is_reg = true;
        b.v = *(u_char*)buf - 'a';
    }
    printf("%d, %d\n", b.is_reg, b.v);
    return b;
}

bool vm_run() {
    int regs['z' - 'a' + 1];
    char line[SZ];

    memset(regs, 0, sizeof regs);

    while (true) {
        printf("> ");
        fgets(line, SZ, stdin);
        if (line[0] == '\n') break;

        int a = *(u_char*)(line + 4) - 'a';
        opd_b bv = vm_read_opd_b(line + 6);
        int b = bv.is_reg ? regs[bv.v] : bv.v;

        if (strncmp(line, "inp", 3) == 0) {
            printf("inp %c > ", a + 'a');
            scanf("%d%*c", &regs[a]);
        } else if (strncmp(line, "add", 3) == 0) {
            regs[a] += b;
        } else if (strncmp(line, "mul", 3) == 0) {
            regs[a] *= b;
        } else if (strncmp(line, "div", 3) == 0) {
            regs[a] /= b;
        } else if (strncmp(line, "mod", 3) == 0) {
            regs[a] %= b;
        } else if (strncmp(line, "eql", 3) == 0) {
            regs[a] = regs[a] == b;
        }
        else break;
    }
    return regs['z' - 'a'] == 0; // no more instrs, eval 'z == 0'
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
    setup();

    char instrs[SZ];

    puts("--- Day 24: Arithmetic Logic Unit ---");
    puts("input MONAD: ");

    bool success = vm_run();

    printf("MONAD says your model number is %s\n", success ? "valid" : "invalid");
}
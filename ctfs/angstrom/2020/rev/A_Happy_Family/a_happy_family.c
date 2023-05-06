#define _GNU_SOURCE

// you can always use a couple of headers
#include <fcntl.h>
#include <setjmp.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

#define ulo unsigned long long
#define CHARS 62
#define PS 32
#define BS 128
#define FLAGSIZE 128
#define BASE 13
#define BL 18
char fifpath[64] = "/tmp/fam-";
FILE *fif;
int fval;

char randchars[CHARS + 1] =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
char basechars[BASE + 1] = "angstromctf20";

// this is the flag for the pwn challenge
void print_flag() {
    gid_t gid = getegid();
    setresgid(gid, gid, gid);
    FILE *file = fopen("flag.txt", "r");
    char flag[FLAGSIZE];
    if (file == NULL) {
        printf("Cannot read flag file.\n");
        exit(1);
    }
    fgets(flag, FLAGSIZE, file);
    printf("%s", flag);
}

void tobase(ulo n, char *ret) {
    ret[BL] = 0;
    for (int i = BL - 1; i >= 0; --i) {
        ret[i] = basechars[n % BASE];
        n /= BASE;
    }
}

void setfif(int val) {
    srand(val);
    for (int i = 9; i < 20; i++) {
        fifpath[i] = randchars[rand() % CHARS];
    }
    fifpath[20] = 0;
    mkfifo(fifpath, 0660);
}

void openfif(char *mode) {
    fif = fopen(fifpath, mode);
    setvbuf(fif, NULL, _IONBF, 0);
}

void closefif() {
    fclose(fif);
    fif = NULL;
}

void parent() {
    char inp[PS + 1];
    puts("  \\   /\n /-----\\\n |  o  |\n | \\|/ |\n | / \\ |\n \\-----/\n  |   |");
    puts("This TV show is so boring, it's just a guy standing still.");
    puts("I need a GOOD TV show to watch with my child.");
    puts("Which TV show do you recommend?");
    fgets(inp, PS + 1, stdin);
    if (strlen(inp) != PS) {
        printf("I haven't even heard of that TV show.\n");
        exit(1);
    }
    char fhalf[PS / 2];
    char shalf[PS / 2 + 1];
    for (int i = 0; i < PS; i++) {
        if (i % 2) {
            shalf[i / 2] = inp[i];
        } else {
            fhalf[i / 2] = inp[i];
        }
    }
    shalf[PS / 2] = 0;
    openfif("w");
    fprintf(fif, "%s\n", shalf);
    closefif();
    ulo n1 = *(ulo *)fhalf;
    ulo n2 = *(ulo *)(fhalf + 8);
    ulo n3;
    ulo n4;
    char c1[BL + 1];
    char c2[BL + 1];
    char c3[BL + 1];
    char c4[BL + 1];
    tobase(n1, c1);
    tobase(~n2, c2);
    char buf[BS];
    openfif("r");
    fgets(buf, BS, fif);
    closefif();
    sscanf(buf, "%llx %llx", &n3, &n4);
    tobase(n3 + 0x1337, c3);
    tobase(n4 - 0x4242, c4);
    if (strcmp(c1, "artomtf2srn00tgm2f") || strcmp(c2, "ng0fa0mat0tmmmra0c") ||
        strcmp(c3, "ngnrmcornttnsmgcgr") || strcmp(c4, "a0fn2rfa00tcgctaot")) {
        printf("Oh I've watched that show, I don't really like it.\n");
        exit(1);
    }
    // This is the flag for the rev challenge
    puts("Wait that name sounds familiar...");
    sleep(1);
    puts("...");
    sleep(1);
    printf("Oh I know why! It's because the flag is actf{%s}!\n", inp);
}

void child() {
    char salf[PS / 2 + 1];
    openfif("r");
    fgets(salf, 256, fif);
    closefif();
    int len = strlen(salf);
    for (int i = 0; i < len; i++) {
        if (salf[i] == '\n') {
            salf[i] = 0;
            break;
        }
    }
    ulo n1 = *(ulo *)salf;
    ulo n2 = *(ulo *)(salf + 8);
    n1 = -n1;
    n2 ^= 0x1234567890abcdefl;
    openfif("w");
    fprintf(fif, "%llx %llx\n", n1, n2);
    closefif();
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    int fval = fork();
    alarm(300);  // sometimes the child processes don't die
    prctl(PR_SET_PDEATHSIG, SIGTERM);
    if (fval == 0) {
        setfif(getpid());
        child();
    } else {
        setfif(fval);
        parent();
    }
}
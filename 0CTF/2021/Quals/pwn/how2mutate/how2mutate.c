#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>

#include "honggfuzz.h"
#include "cmdline.h"
#include "mangle.h"
#include "subproc.h"
#include "libhfcommon/util.h"

char menu[] = "[TODO: menu]";
char *myargs[] = {"how2mutate", "-s", "--", "/bin/true"};

honggfuzz_t hfuzz;
run_t run;
uint8_t **seeds;
int seedssz[10];

void add_seed() {
    int i=0;
    while (i<10 && seeds[i]) i++;
    if (i<10) {
        printf("size: ");
        scanf("%d", &seedssz[i]);
        int sz = seedssz[i]+1;
        if (sz>0 && sz<0x8000) {
            printf("content: ");
            seeds[i] = util_Calloc(sz);
            read(0, seeds[i], seedssz[i]);
        }
    }
}
void mutate_seed() {
    char buf[16];
    printf("index: ");
    read(0, buf, 4);
    if (buf[0]>='0' && buf[0]<='9') {
        int idx = buf[0]-'0';
        if (seeds[idx]) {
            run.dynfile->size = seedssz[idx];
            memcpy(run.dynfile->data, seeds[idx], seedssz[idx]);
            mangle_mangleContent(&run, 1);
            seedssz[idx] = run.dynfile->size;
            seeds[idx] = util_Realloc(seeds[idx], seedssz[idx]);
            memcpy(seeds[idx], run.dynfile->data, seedssz[idx]);
        }
    }
}
void show_seed() {
    for (int i=0; i<10; i++) {
        if (seeds[i]) {
            printf("%d: %s\n", i, seeds[i]);
        }
    }
}
void delete_seed() {
    char buf[16];
    printf("index: ");
    read(0, buf, 4);
    if (buf[0]>='0' && buf[0]<='9') {
        int idx = buf[0]-'0';
        if (seeds[idx]) {
            free(seeds[idx]);
            seeds[idx] = 0;
        }
    }
}
void set_mutate() {
    char buf[16];
    printf("mutationsPerRun: ");
    read(0, buf, 4);
    if (buf[0]>='0' && buf[0]<='9') {
        int x = buf[0]-'0';
        hfuzz.mutate.mutationsPerRun = x;
        run.mutationsPerRun = x;
    }
}


int fuzzone(char* buf) {
    /*
    if (strlen(buf)<0x10) {
        return 0;
    }*/
    int i;
    if (buf[0] == '1') {
        if (buf[1] == '0')
            puts("path 0");
    }
    if (buf[0] == '2') {
        if (buf[1] == buf[2])
            puts("path 1");
    }
    if (buf[0] == '3') {
        if (!memcmp(buf+1, "magic", 5))
            puts("path 2");
    }
    if (buf[0] == '4') {
        if (!memcmp(buf+1, "magicmagic", 10))
            puts("path 3");
    }
    if (buf[0] == '5') {
        int res;
        for (i=1; i<16; i++) res += buf[i];
        if (res == 1000)
            puts("path 4");
    }
    if (buf[0] == '6') {
        int res;
        for (i=1; i<16; i++) res = buf[i] - res;
        if (res == 0)
            puts("path 5");
    }
    if (buf[0] == '7') {
        bool ok=true;
        for (i=1; i<8; i++) {
            if (buf[i] != buf[i+8])
                ok = false;
        }
        if (ok)
            puts("path 6");
    }
    if (buf[0] == '8') {
        bool ok=true;
        for (i=1; i<8; i++) {
            if (buf[i] + buf[i+8] != 256)
                ok = false;
        }
        if (ok)
            puts("path 7");
    }
    if (buf[0] == '9') {
        bool ok=true;
        for (i=2; i<15; i++) {
            buf[i] += buf[i-1];
            if (buf[i] != buf[i+1])
                ok = false;
        }
        if (ok)
            puts("path 8");
    }
    if (buf[0] == '0') {
        bool ok=true;
        for (i=2; i<15; i++) {
            buf[i] -= buf[i-1];
            if (buf[i] != buf[i+1])
                ok = false;
        }
        if (ok)
            puts("path 9");
    }
    return 0;
}

static void* tofuzz(void* arg) {
    for (int c=0; c<0xffffff; c++) {
        for (int i=0; i<10; i++)
            if (seeds[i]) {
                fuzzone(seeds[i]);
            }
    }
}

int main(int argc, char** argv) {
    char buf[16];
    pthread_t fuzzthread;
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    if (!cmdlineParse(4, myargs, &hfuzz)) {
        puts("wtf");
        return 0;
    }
    hfuzz.feedback.cmpFeedback = false;
    hfuzz.mutate.maxInputSz = 0x8000;
    hfuzz.mutate.mutationsPerRun = 1;

    run.global = &hfuzz;
    run.dynfile = (dynfile_t*)util_Calloc(sizeof(dynfile_t));
    run.dynfile->data = util_Calloc(_HF_INPUT_MAX_SIZE);
    run.mutationsPerRun = 1;
    seeds = (uint8_t **)util_Calloc(8*16);
    puts(menu);
    while (1) {
        printf("> ");
        read(0, buf, 4);
        if (buf[0] == '1') {
            add_seed();
        } else if (buf[0] == '2') {
            mutate_seed();
        } else if (buf[0] == '3') {
            show_seed();
        } else if (buf[0] == '4') {
            delete_seed();
        } else if (buf[0] == '5') {
            set_mutate();
        } else if (buf[0] == '6') {
            subproc_runThread(&hfuzz, &fuzzthread, tofuzz, false);
        } else {
            break;
        }
    }
    return 0;
}

#include <stdlib.h>
#include <stdio.h>

#define MAX_PORTALS 5

typedef struct TimePoint TimePoint;
struct TimePoint {
    unsigned long year;
    TimePoint* portals[MAX_PORTALS];
    size_t msgSize;
    char* msg;
};

TimePoint* root;
TimePoint* now;

void prologue() {
    printf("Finally! I've done it! I've invented a portal gun that can open portals to other points in time!\n"
           "I sure hope I don't create any paradoxes on accident or anything...\n"
           "Let's try it out!!\n");

    root = (TimePoint*)calloc(1, sizeof(TimePoint));
    root->year = 2022;
    now = root;
}

int isPortalLegal(unsigned long destination) {
    for(size_t i = 0; i < MAX_PORTALS; i++) {
        TimePoint* pt = now->portals[i];
        if(pt != NULL && pt->year == destination) return 0;
    }
    return 1;
}

void printMessage() {
    if(now->msgSize == 0) return;
    printf("Somebody left notes on the ground. They say:\n");
    fwrite(now->msg, 1, now->msgSize, stdout);
}

void describe() {
    printf("\nThe year is %ld.\n", now->year);
    printMessage();
    for(size_t i = 0; i < MAX_PORTALS; i++) {
        if(now->portals[i] != NULL) {
            printf("There is a portal to the year %ld here\n", now->portals[i]->year);
        }
    }
}

TimePoint* search(TimePoint* pt, unsigned long year, int start) {
    if(pt == root && !start) return NULL;
    if(pt->year == year) return pt;

    TimePoint* result = NULL;
    for(size_t i = 0; i < MAX_PORTALS; i++) {
        if(pt->portals[i] != NULL) {
            result = search(pt->portals[i], year, 0);
            if(result != NULL) break;
        }
    }
    return result;
}

void openPortal(unsigned long year) {
    size_t idx = 0;
    while(idx < MAX_PORTALS) {
        if(now->portals[idx] == NULL) break;
        idx++;
    }

    if(idx == MAX_PORTALS) {
        printf("Too many portals to keep track of!\n");
        return;
    }

    if(!isPortalLegal(year)) {
        printf("There's already a portal to %ld.\n", year);
        return;
    }

    TimePoint* pt = search(root, year, 1);
    if(pt == NULL) {
        pt = (TimePoint*)calloc(1, sizeof(TimePoint));
        pt->year = year;
    }
    now->portals[idx] = pt;
    printf("Opened the portal!\n");
}

void closePortal(unsigned long year) {
    for(size_t i = 0; i < MAX_PORTALS; i++) {
        TimePoint* pt = now->portals[i];
        if(pt != NULL && pt->year == year) {
            if(pt->msgSize > 0) free(pt->msg);
            free(pt);
            now->portals[i] = NULL;
            printf("Closed the portal!\n");
            return;
        }
    }
    printf("There are no portals to %ld here.\n", year);
}

void takePortal(unsigned long year) {
    for(size_t i = 0; i < MAX_PORTALS; i++) {
        TimePoint* pt = now->portals[i];
        if(pt != NULL && pt->year == year) {
            now = pt;
            printf("*portal noises*\n");
            return;
        }
    }
    printf("There are no portals to %ld here.\n", year);
}

void leaveMessage() {
    if(now->msgSize == 0) {
        printf("How many notecards do you want to use? ");
        char nbuf[8];
        fgets(nbuf, 8, stdin);
        size_t sz = atoi(nbuf) * 16;
        
        now->msgSize = sz;
        now->msg = (char*)malloc(sz);
    }

    printf("What do you want to write?\n");
    fgets(now->msg, now->msgSize, stdin);
    printf("Done!\n");
}

int main() {
    setvbuf(stdout, 0, 2, 0);

    prologue();
    while(1) {
        describe(now);
        printf("What will you do? ");
        char x = getchar();
        getchar(); // newline
        if(x == 'm') {
            leaveMessage();
        } else {
            char yrbuf[6];
            fgets(yrbuf, 6, stdin);
            unsigned long year = atoi(yrbuf);
            if(x == 'o') {
                openPortal(year);
            } else if(x == 'c') {
                closePortal(year);
            } else if(x == 't') {
                takePortal(year);
            }
        }
    }
}
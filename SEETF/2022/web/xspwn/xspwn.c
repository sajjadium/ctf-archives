// emcc xspwn.c -g2 --no-entry -o xspwn.js -s EXPORTED_RUNTIME_METHODS=ccall,cwrap -s NO_EXIT_RUNTIME=1

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <emscripten.h>

typedef struct jared {
    char* name;
    struct jared *next;
} JARED;

JARED *HEAD = NULL;

int validateJared(char *name) {
    while (*name) {
        if ((*name < 'a' || *name > 'z') && (*name < 'A' || *name > 'Z') && (*name != ' ')) {
            return 1;
        }
        name++;
    }
    return 0;
}

EMSCRIPTEN_KEEPALIVE
int insertSorted(char *name) {
    
    char *newName = malloc(strlen(name) + 1);
    strcpy(newName, name);

    printf("Inserting: %s\n", newName);
    if (validateJared(newName)) {
        return 1;
    }

    JARED *new = malloc(sizeof(JARED));
    new->name = newName;

    if (HEAD == NULL) {
        new->next = NULL;
        HEAD = new;
        return 0;
    }

    JARED *curr = HEAD;
    JARED *prev = NULL;
    while (curr != NULL) {
        if (strcmp(curr->name, name) > 0) {
            if (prev == NULL) {
                new->next = curr;
                HEAD = new;
                return 0;
            } else {
                new->next = curr;
                prev->next = new;
                return 0;
            }
        }
        prev = curr;
        curr = curr->next;
    }
    prev->next = new;
    new->next = NULL;
    return 0;
}

EMSCRIPTEN_KEEPALIVE
char *getNameAtIndex(int index) {
    JARED *curr = HEAD;
    int i = 0;
    while (curr != NULL) {
        if (i == index) {
            return curr->name;
        }
        i++;
        curr = curr->next;
    }
    return NULL;
}

EMSCRIPTEN_KEEPALIVE
int deleteNameAtIndex(int index) {
    JARED *curr = HEAD;
    JARED *prev = NULL;
    int i = 0;
    while (curr != NULL) {
        if (i == index) {
            prev->next = curr->next;
            free(curr);
            return 0;
        }
        prev = curr;
        curr = curr->next;
        i++;
    }
    return 1;
}

EMSCRIPTEN_KEEPALIVE
int init() {
    insertSorted("Jared Song");
    insertSorted("Jared Leto");
    insertSorted("Jared Kushner");
    return 0;
}

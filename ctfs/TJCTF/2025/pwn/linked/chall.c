#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <inttypes.h>
#include <stdbool.h>

struct event {
    int time;
    char name[128];
    struct event *next;
};

struct eventList {
    int size;
    struct event *head;
};

void displayEvents(struct eventList *events) {
    puts("Calendar events:");

    struct event *cur = events->head;
    for (int i = 0; i < events->size; i++) {
        if (cur->time == 0) {
            break;
        }
        printf("%u:00 - %s\n", cur->time, cur->name);
        cur = cur->next;
    }
    printf("\n\n");
}

void inpcpy(char *dst, char *src) {
    int ind = 0;
    while (src[ind] != '\n') {
        dst[ind] = src[ind];
        ind++;
    }
}

int main() {
    char inputBuffer[256] = {'\0'};
    struct eventList events;
    events.head = malloc(sizeof(struct event));
    events.head->next = NULL;
    events.head->time = 0;
    events.size = 1;

    setbuf(stdout, NULL);

    for (int i = 0; i < 2; i++) {
        puts("Add an event to your calendar:");

        struct event *cur = events.head;
        while (cur->next != NULL) {
            cur = cur->next;
        }
        cur->next = malloc(sizeof(struct event));
        cur->next->next = NULL;
        cur->next->time = 0;
        events.size++;

        printf("Event time? (1-24) ");
        fgets(inputBuffer, sizeof(inputBuffer), stdin);
        int t = atoi(inputBuffer);
        if (t == 0) {
            free(cur->next);
            cur->next = NULL;
            events.size--;
            printf("Invalid integer: %s\n", inputBuffer);
            continue;
        }
        cur->time = t;

        printf("Event name? ");
        fgets(inputBuffer, sizeof(inputBuffer), stdin);
        inpcpy(cur->name, inputBuffer);

        displayEvents(&events);
    }
    
    puts("2 events and still couldn't get the flag?");
    puts("smhmh");
    puts("just run like...");
    puts("cat flag.txt");
    puts("or something like that");
    return 0;
}
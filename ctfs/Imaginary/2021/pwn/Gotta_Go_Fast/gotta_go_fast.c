#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

typedef struct Tribute {
    char name[100];
    short district;
    short index_in_district;
} Tribute;

typedef struct TributeList {
    Tribute* tributes[100];
    struct TributeList* next;
    int in_use;
} TributeList;

TributeList* head;

int list_append(Tribute* t) {
    int offset = 0;
    TributeList* cur = head;
    while (cur->in_use == 100) {
        if (cur->next == NULL) {
            cur->next = malloc(sizeof(TributeList));
            cur->next->next = NULL;
            cur->next->in_use = 0;
        }
        offset += 100;
        cur = cur->next;
    }
    offset += cur->in_use;
    cur->tributes[cur->in_use++] = t;
    return offset;
}

void list_remove(int idx) {
    TributeList* last = head;
    while (last->next != NULL) {
        if (last->next->in_use == 0) {
            free(last->next);
            last->next = NULL;
            break;
        }
        last = last->next;
    }

    TributeList* cur = head;
    while ((cur->in_use == 100 && idx >= 100)) {
        if (!cur->next) {
            abort();
        }
        cur = cur->next;
        idx -= 100;
    }
    Tribute* t = last->tributes[last->in_use - 1];
    last->tributes[last->in_use - 1] = cur->tributes[idx];
    free(last->tributes[last->in_use - 1]);
    cur->tributes[idx] = t;
    last->in_use--;
}

int readint(int lo, int hi) {
    int res = -1;
    while (1) {
        printf("> ");
        scanf("%d", &res);
        if (res >= lo && res <= hi) {
            return res;
        }
    }
}

void init() {
    head = malloc(sizeof(TributeList));
    head->next = NULL;
    head->in_use = 0;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    alarm(180);
}

void menu() {
    puts("What would you like to do?");
    puts(" [0] Draft a new tribute");
    puts(" [1] Remove a tribute from the list (because someone volunteered in their place again, people should really stop doing that, it messes with our management system)");
    puts(" [2] See an overview of the current tributes");
    puts(" [3] Start the games, may the odds be ever in your favor!");
}

void draft() {
    Tribute* t = malloc(sizeof(Tribute));
    puts("For which district will this tribute fight?");
    t->district = readint(1, 12);
    puts("What's the position among the tributes for this district?");
    t->index_in_district = readint(1, 2);
    puts("Least importantly, what's their name?");
    scanf("%99s", t->name);

    printf("Noted, this is tribute %d\n", list_append(t));
}

void undraft() {
    puts("Which tribute should be undrafted?");
    int idx = readint(0, INT_MAX);
    list_remove(idx);
    puts("done.");
}

void list() {
    int idx = 0;
    TributeList* cur = head;
    while (cur) {
        for (int i = 0; i < cur->in_use; i++, idx++) {
            Tribute* t = cur->tributes[i];
            printf("Tribute %d [%s] fights in position %d for district %d.\n", idx, t->name, t->index_in_district, t->district);
        }
        cur = cur->next;
    }
}

void run() {
    puts("TODO: implement this simulation into the matrix.");
    exit(0);
}

int have_diagnosed = 0;
void diagnostics() {
    if (have_diagnosed) {
        puts("I understand things might be broken, but we should keep some semblance of security.");
        abort();
    }
    have_diagnosed = 1;
    puts("I take it the management system was ruined by volunteers again? Just let me know which memory address you need...");
    unsigned long long x = 0;
    scanf("%llu", &x);
    printf("%p\n", *(void**)x);
}

int main() {
    init();

    puts("Welcome to the Hunger Games management system.");

    while (1) {
        menu();
        int choice = readint(0, 4);
        switch (choice) {
            case 0:
                draft();
                break;
            case 1:
                undraft();
                break;
            case 2:
                list();
                break;
            case 3:
                run();
                break;
            case 4:
                diagnostics();
                break;
            default:
                abort(); // Shouldn't happen anyway
        }
    }
}

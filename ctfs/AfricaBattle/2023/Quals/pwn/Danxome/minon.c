#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MINON_SIZE 10
#define MAX_NAME_SIZE 0x40

typedef struct Awhouangan Awhouangan;
typedef struct Gbeto Gbeto;
typedef struct Minon Minon;
typedef void (*speakFunc)(char*);

enum MinonType {
    AWHOUANGAN,
    GBETO
};

struct Minon
{
    speakFunc speak;
    enum MinonType type;
    char* name;
};

struct Danxome
{
    int numOfMinon;
    Minon* minons[MINON_SIZE];
} danxome = { .numOfMinon = 0 };

void Nawi() {
    system("/bin/sh");
}

void print(char* str) {
    system("/usr/bin/date +\"%Y/%m/%d %H:%M.%S\" | tr -d '\n'");
    printf(": %s\n", str);
}

void speak(char* name) {
    print(name);
}

void init() {
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stderr, 0, 2, 0);
  alarm(60);
}

int menu() {
    int choice = -1;
    print("Welcome to Danxome Military zone !!!");
    print("1) Add Minon");
    print("2) Remove Minon");
    print("3) Report Minon Name");
    print("0) Exit");
    
    while (1) {
        printf("> ");
        scanf("%d", &choice);
        if (choice >= 0 && choice < 5) {
            break;
        }
        printf("??\n");
    }
    printf("\n");

    return choice;
}

void add_minon() {
    int choice;
    int size;
    int idx;
    Minon* minon;

    if (danxome.numOfMinon >= MINON_SIZE) {
        print("[ERROR] The Military zone is full.");
        return;
    }

    for (idx = 0; idx < MINON_SIZE; idx++) {
        if (danxome.minons[idx] == NULL) {
            break;
        }
    }

    minon = (Minon*) malloc(sizeof(Minon));

    print("Type of Minon?");
    print("1) Awhouangan");
    print("2) Gbeto");

    while (1) {
        printf("> ");
        scanf("%d", &choice);
        if (choice == 1) {
            minon->type = AWHOUANGAN;
            break;
        } 
        if (choice == 2) {
            minon->type = GBETO;
            break;
        }
        printf("??\n");
    }

    minon->speak = speak;
    print("How long is the name? (max: 64 characters)");   
    while (1) {
        printf("> ");
        scanf("%d", &size);
        if (size >= 0 && size < MAX_NAME_SIZE) {
            minon->name = (char*) malloc(size);
            break;
        } 
        printf("??\n");
    }

    print("Name of minon?");
    printf("> ");
    read(0, minon->name, size);

    danxome.minons[idx] = minon;
    printf("> [DEBUG] Minon is added to Military zone %d\n", idx);
    danxome.numOfMinon++;
}

void remove_minon() {
    int choice;

    if (danxome.numOfMinon <= 0) {
        print("[ERROR] No minon in the Military zone.");
        return;
    }

    print("Zone number? (0-9)");
    while (1) {
        printf("> ");
        scanf("%d", &choice);
        if (choice >= 0 && choice < MINON_SIZE) {
            break;
        }
        printf("??\n");
    }

    if (danxome.minons[choice] == NULL) {
        print("[ERROR] No minon in this zone.");
        return;
    }

    free(danxome.minons[choice]->name);
    free(danxome.minons[choice]);

    printf("> [DEBUG] Minon is removed from zone %d\n", choice);
    
    danxome.numOfMinon--;
}

void report_name() {
    int choice;

    if (danxome.numOfMinon <= 0) {
        print("[ERROR] No minon in the Military zone.");
        return;
    }

    print("Zone number? (0-9)");
    while (1) {
        printf("> ");
        scanf("%d", &choice);
        if (choice >= 0 && choice < MINON_SIZE) {
            break;
        }
        printf("??\n");
    }

    if (danxome.minons[choice] == NULL) {
        print("[ERROR] No minon in this zone.");
        return;
    }

    danxome.minons[choice]->speak(danxome.minons[choice]->name);
}

int main(int argc, char const *argv[]) {
    int leave = 0;
    init();
    while(!leave) {
        switch (menu()) {
        case 1:
            add_minon();
            break;
        case 2:
            remove_minon();
            break;
        case 3:
            report_name();
            break;
        default:
            leave = 1;
        }
        printf("\n");
    }
    return 0;
}
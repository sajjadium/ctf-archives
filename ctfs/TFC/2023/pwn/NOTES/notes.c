#include <stdio.h>
#include <stdlib.h>

#define CONTENT_MAX (long long)256
#define NOTES_MAX 10

typedef struct _note_t {
    char* content;
} note_t;

void win() {
    system("/bin/sh");
}

void menu() {
    printf(
        "1. Add note\n"
        "2. Edit note\n"
        "3. View notes\n"
        "0. Exit\n"
    );
}

int get_index() {
    printf("index> \n");
    int index;
    scanf("%d", &index);
    getchar();
    if (index < 0 || index > NOTES_MAX) {
        return -1;
    }
    return index;
}

note_t* add() {
    note_t* note = malloc(sizeof(note_t));
    note->content = malloc(sizeof(CONTENT_MAX));
    printf("content> \n");
    fgets(note->content, sizeof(CONTENT_MAX), stdin);
    return note;
}

void edit(note_t* note) {
    printf("content> \n");
    fgets(note->content, CONTENT_MAX, stdin);
}

void view(note_t* notes[]) {
    for (int i = 0; i < NOTES_MAX; i += 1) {
        printf("%d. ", i);
        if (notes[i] == NULL) {
            printf("<empty>\n");
        } else {
            printf("%s\n", notes[i]->content);
        }
    }
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    note_t* notes[10] = { 0 };
    
    while (1) {
        menu();
        int input;
        scanf("%d", &input);
        switch (input) {
            case 1: {
                int index = get_index();
                if (index == -1) {
                    break;
                }
                notes[index] = add();
                break;
            }
            case 2: {
                int index = get_index();
                if (index == -1) {
                    break;
                }
                if (notes[index] == NULL) {
                    break;
                }
                edit(notes[index]);
                break;
            }
            case 3:
                view(notes);
                break;
            case 0:
                exit(0);
                break;
            default:
                break;
        }
    }
}
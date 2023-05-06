#include <stdio.h>
#include <stdlib.h>

void win()  {
    system("/bin/sh");
}

void add() {
    float a;
    float b;
    scanf("%f\n", &a);
    scanf("%f\n", &b);

    printf("%f\n", a+b);
}

void sub() {
    float a;
    float b;
    scanf("%f\n", &a);
    scanf("%f\n", &b);

    printf("%f\n", a-b);
}

void mult() {
    float a;
    float b;
    scanf("%f\n", &a);
    scanf("%f\n", &b);

    printf("%f\n",a*b);
}


void menu() {
    printf("LIVE MATH LOVE\n");
    printf("1. Add\n");
    printf("2. Subtract\n");
    printf("3. Multiply\n");
    printf("> ");

    void (*action)();
    int choice;
    scanf("%d\n", &choice);

    if (choice == 1) {
        action = add;
    } else if (choice == 2) {
        action = sub;
    } else if (choice == 3) {
        action = mult;
    }

    action();

    menu();
}


void main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    menu();

}

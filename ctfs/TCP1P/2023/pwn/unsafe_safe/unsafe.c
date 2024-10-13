#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

unsigned long safes[100] = {7955998170729676800};
char *exit_message = "Have a nice day!";

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void deposit() {
    int index = 0;
    int amount = 0;
    puts("Enter the safe number you want to deposit in (0-100): ");
    scanf("%d", &index);
    puts("Enter the amount you want to deposit: ");
    scanf("%d", &amount);
    safes[index] += amount;
}

void login() {
    unsigned long age, input, password;
    char pet_name[5] = "\0\0\0\0\0";
    puts("Input your age: ");
    scanf("%lu", &age);
    if (age < 17) {
        puts("Sorry, this is not a place for kids");
        exit(0);
    }
    puts("Input your pet name: ");
    scanf("%5c", pet_name);
    srand(time(NULL) * (*(short *)pet_name * *(short *)(pet_name + 2) + age));
    password = rand();
    puts("Input your password: ");
    scanf("%lu", &input);
    if (input != password) {
        puts("Password Wrong!");
        exit(0);
    }
}

int main() {
    init();
    login();
    deposit();
    deposit();
    deposit();
    puts(exit_message);
}

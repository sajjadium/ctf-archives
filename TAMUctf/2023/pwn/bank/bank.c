#include <stdio.h>

long accounts[100];
char exit_msg[] = "Have a nice day!";

void deposit() {
    int index = 0;
    long amount = 0;
    puts("Enter the number (0-100) of the account you want to deposit in: ");
    scanf("%d", &index);
    puts("Enter the amount you want to deposit: ");
    scanf("%ld", &amount);
    accounts[index] += amount;
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    deposit();
    deposit();
    puts(exit_msg);
}

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int print_flag() {
    char flag[50];
    FILE *fp = fopen("flag.txt", "r");
    
    if (fp == NULL) {
        perror("Unable to open flag.txt");
        return -1;
    }

    fread(flag, 50, 1, fp);
    puts(flag);
    return 0;
}

long get_secure_random() {
    long random_val;
    FILE *fp = fopen("/dev/urandom", "r");
    
    if (fp == NULL) {
        perror("Unable to open /dev/urandom");
        return -1;
    }

    fread(&random_val, sizeof(random_val), 1, fp);
    fclose(fp);

    return random_val;
}

unsigned long get_guess(){
    char input[22];
    unsigned long guess;
    printf("Enter your guess (between 1 and 18446744073709551615): ");
    fgets(input, sizeof(input), stdin);
    guess = strtoul(input, NULL, 0);
    if (!guess){
        printf("Guess not allowed %s\n", input);
        return 0;
    }
    printf(input);
    printf("What an interesting guess...\n");
    return guess;
}

int main() {
    unsigned long guess;
    unsigned long secret_num = get_secure_random();
   
    setvbuf(stdout, NULL, _IONBF, 0);

    guess = get_guess();

    if (guess == secret_num){
        printf("Wow you actually got it!\n");
        print_flag();
        return 0;
    }
    printf("Because I'm nice, I'll give you one more shot.\n\n");

    guess = get_guess();
    if (guess == secret_num){
        printf("Second time's the charm\n");
        print_flag();
        return 0;
    }
    printf("Better luck next time sailor\n");
    return 0;
}
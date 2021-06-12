#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int length;
    char essay[50];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Hey all!");
    puts("Welcome to Amer Lit!");
    puts("In this class, we will be reading books");
    puts("(wow who would have guessed)");
    puts("and then doing fun things like writing essays!");
    sleep(1);
    puts("Y'know what, let me get a really good example of an essay.");

    FILE *fp = fopen("flag.txt", "r");
    char example_essay[100];

    if (fp == NULL) {
        puts("Oh no, I can't find my former students' essays!");
        puts("How now will I set the bar redicuolously high for new students??");
        puts("[If you are seeing this on the remote server, please contact admin].");
        exit(1);
    }

    fgets(example_essay, sizeof(example_essay), fp);

    sleep(1);
    puts("Actually, on further thought...");
    puts("You're a BCA student, you should be able to write a perfect essay immediately.");
    puts("Let's see it!");

    fgets(essay, sizeof(essay), stdin);
    essay[strcspn(essay, "\n")] = 0;
    length = strlen(essay);

    sleep(1);
    puts("");
    puts("TURNITIN SUBMISSION RECEIVED:");

    printf("╔═");
    for (int i = 0; i < length; ++i) printf("═");
    printf("═╗\n");

    printf("║ ");
    for (int i = 0; i < length; ++i) printf(" ");
    printf(" ║\n");

    printf("║ ");
    for (int i = 0; i < length; ++i) printf(" ");
    printf(" ║\n");

    printf("║ ");
    printf(essay);
    printf(" ║\n");

    printf("║ ");
    for (int i = 0; i < length; ++i) printf(" ");
    printf(" ║\n");

    printf("║ ");
    for (int i = 0; i < length; ++i) printf(" ");
    printf(" ║\n");

    printf("╚═");
    for (int i = 0; i < length; ++i) printf("═");
    printf("═╝\n");

    sleep(2);
    puts("");
    puts("You've clearly put a lot of work and effort into this.");
    puts("How about an 89?");
}

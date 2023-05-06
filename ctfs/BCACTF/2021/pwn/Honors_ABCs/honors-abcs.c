#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

char *correct = "abcdefghijklmnopqrstuvwxyz";

int main() {
    int grade = 0;
    char response[50];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Welcome to your first class at BCA: Honors-level ABCs.");
    puts("Because we expect all our students to be perfect, I'm not going to teach you anything.");
    sleep(2);
    puts("Instead, we're going to have a quiz!");
    puts("And, of course, I expect all of you to know the material already.");
    sleep(2);
    puts("");
    puts("╔════════════════════════╗");
    puts("║ THE QUIZ               ║");
    puts("║                        ║");
    puts("║ 1) Recite the alphabet ║");
    puts("╚════════════════════════╝");
    puts("");
    printf("Answer for 1: ");
    gets(response);

    for (int i = 0; i < 26; ++i) {
        if (response[i] == 0)
            break;
        if (response[i] != correct[i])
            break;

        grade = i * 4;
    }

    if (grade < 60)
        puts("An F? I'm sorry, but you clearly need to study harder.");
    else if (grade < 70)
        puts ("You didn't fail, but you could do better than a D.");
    else if (grade < 80)
        puts("Not terrible, but a C's nothing to write home about.");
    else if (grade < 90)
        puts("Alright, a B's not bad, I guess.");
    else if (grade < 100)
        puts("Ayyy, nice job on getting an A!");
    else if (grade == 100) {
        puts("Perfect score!");
        puts("You are an model BCA student.");
    } else {
        puts("How did you end up here?");
        sleep(2);
        puts("You must have cheated!");
        sleep(2);
        puts("Let me recite the BCA plagarism policy.");
        sleep(2);

        FILE *fp = fopen("flag.txt", "r");

        if (fp == NULL) {
            puts("Darn, I don't have my student handbook with me.");
            puts("Well, I guess I'll just give you a verbal warning to not cheat again.");
            puts("[If you are seeing this on the remote server, please contact admin].");
            exit(1);
        }

        int c;
        while ((c = getc(fp)) != EOF) {
            putchar(c);
            usleep(20000);
        }

        fclose(fp);
    }

    puts("");
    puts("Alright, class dismissed!");
}

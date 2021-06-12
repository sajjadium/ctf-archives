#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int knows_logic = 0;
int knows_algebra = 0;
int knows_functions = 0;

void logic() {
    int p, q, r, s;

    printf("p: ");
    scanf("%d", &p);
    printf("q: ");
    scanf("%d", &q);
    printf("r: ");
    scanf("%d", &r);
    printf("s: ");
    scanf("%d", &s);
    
    knows_logic = (p || q || !r) && (!p || r || !s) && (q != s) && s;
}

void algebra() {
    int x, y, z;

    printf("x: ");
    scanf("%d", &x);
    printf("y: ");
    scanf("%d", &y);
    printf("z: ");
    scanf("%d", &z);

    int eq1 = 5*x - 6*y + 3*z;
    int eq2 = 2*x + 5*y - 7*z;
    int eq3 = 4*x + 8*y + 8*z;

    knows_algebra = (eq1 == 153) && (eq2 == -163) && (eq3 == -28);
}

void functions() {
    int a, b, c;

    printf("a: ");
    scanf("%d", &a);
    printf("b: ");
    scanf("%d", &b);
    printf("c: ");
    scanf("%d", &c);

    int vertex_x = -b / (2*a);
    int vertex_y = a * vertex_x * vertex_x + b * vertex_x + c;
    int discriminant = b * b - 4 * a * c;

    knows_functions = (vertex_x == 2) && (vertex_y == -2) && (discriminant == 16);
}

void quiz() {
    FILE *fp = fopen("flag.txt", "r");
    char flag[100];

    if (fp == NULL) {
        puts("Sorry, all my stuff's a mess.");
        puts("I'll get around to grading your quiz sometime.");
        puts("[If you are seeing this on the remote server, please contact admin].");
        exit(1);
    }

    fgets(flag, sizeof(flag), fp);

    if (knows_logic && knows_algebra && knows_functions) {
        puts("Alright, you passed this quiz.");
        puts("Here's your prize:");
        puts(flag);
    } else {
        puts("Not there yet...");
        puts("Study some more!");
    }
}

int main() {
    char response[50];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Discrete.");
    puts("The top math track.");
    puts("The best BCA students.");
    puts("The crème de la crème.");
    puts("We have high expectations.");
    puts("Answer all the questions correctly.");
    puts("Do not disappoint us.");
    printf("> ");
    gets(response);

    if (strcmp(response, "i will get an A")) {
        puts("I'm sorry, but you obviously don't care about grades.");
        puts("Therefore, you aren't motivated enough to be in our class.");
        puts("Goodbye.");
        exit(1);
    }

    puts("Your quiz have been posted to Schoology.");
    puts("You have twenty minutes.");
    puts("Good luck.");
}

#include "quizz.h"

/******************
 * Constants
 ******************/
const int LEN = 12;

const char *QUESTIONS[] = {
    "Hippopotomonstrosesquipedaliophobia is the fear of what?\n 1) Hippos\n 2) Long words\n 3) Huge buildings\n",
    "Of what was made the first hockey puck ever used?\n 1) Cow dung\n 2) Stone\n 3) Ice\n",
    "What is the correct answer to the next question?\n 1) 2\n 2) 3\n 3) 1\n",
    "What is the correct answer to this question?\n 1) 1\n 2) 2\n 3) 3\n",
    "What was the correct answer to the previous question?\n 1) 3\n 2) 1\n 3) 2\n",
    "How many liters of pee does an average cow produce in one day?\n 1) Ventordici\n 2) Jason's favorite number\n 3) A few drops.\n",
    "What are the most organized objects\n 1) Shoes \n 2) Closets\n 3) Levers\n",
    "The fear of constipation is known as?\n 1) Chlamydia\n 2) Coprastastaphobia\n 3) Chikungunya\n",
    "Which country consumes the most (and produces the best) chocolate in the world?\n 1) Switzerland\n",
    "What is the most stolen food in the world?\n 1) Chocolate\n 2) Bread\n 3) Cheese\n",
    "Golfing is:\n 1) A sport\n 2) The beautiful art of shortening your SHELLCODE\n",
    "Did you like this category?\n 1) Hell yeah!\n",
};

const int SOLUTIONS[] = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, };

/******************
 * Main
 ******************/
int main(int argc, char* argv[]) {

    setvbuf(stdout, NULL, _IONBF, 0);

    FILE *file;

    file = fopen(scores_file, "a");
    fprintf(file,"%s = {", argv[1]);

    int answer;
    int score = 0;
    for (int i = 0; i < LEN; i++) {
        printf("%s\n", QUESTIONS[i]);
        printf("Your answer: ");
        scanf("%d", &answer);

        if (answer == SOLUTIONS[i]) {
            score++;
            printf("Correct!\n\n");
        } else {
            printf("False!\n\n");
        }

        fprintf(file, "%d,", answer);
    }

    fprintf(file, "%d}\n", score);

    fclose(file);
}

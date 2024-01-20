#include "quizz.h"

/******************
 * Constants
 ******************/
const int LEN = 6;

const char *QUESTIONS[] = {
    "What's the total word count of the Lord of The Ring trilogy?\n 1) 579459 \n 2) 545799\n 3) 799545\n",
    "Allegedly, what is written on the Hell's door\n 1) My name is Olaf and I love warm hugs.\n 2) Lasciate ogne speranza, voi ch'intrate.\n 3) Brace yourself, summer is coming.\n",
    "Who was the most productive writer during COVID?\n 1) Brandon Sanderson\n 2) George R.R. Martin\n 3) Your doctor\n",
    "Who is also known as Space Messiah?\n 1) Neil Armstrong\n 2) Yoda\n 3) Muad'Dib\n",
    "Who swims across the universe with exactly four elephants on the back?\n 1) No one\n 2) A'Tuin\n 3) The earth\n",
    "What are the last two words of many books and this category?\n 1) Have fun\n 2) Well done\n 3) The end\n",
};

const int SOLUTIONS[] = { 1, 1, 1, 1, 1, 1, };

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

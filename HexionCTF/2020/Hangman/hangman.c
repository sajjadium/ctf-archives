#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h> 
#include <unistd.h> 

#define WORD_MAX_LEN 32
#define MAX_HP 5
#define MAX_NUM_OF_WORDS 16
#define TRUE 1
#define FALSE 0

struct hangmanGame
{
    char word[WORD_MAX_LEN];
    char *realWord;
    char buffer[WORD_MAX_LEN];
    int wordLen;
    int hp;
};


unsigned int countLinesNum(char *filename)
{
    FILE *file = NULL;
    unsigned int count = 0;
    char c;

    file = fopen(filename, "r");

    if (!file)
    {
        puts("Failed to load list of words...");
        exit(1);
    }

    for (c = getc(file); c != EOF; c = getc(file))
    {
        if (c == '\n')
        {
            count++;
        }
    }

    fclose(file);

    return count;
}
       

char* getWord(char *filename, unsigned int wordMaxLen)
{
    unsigned int i = 0;
    unsigned int numOfWords = countLinesNum(filename);
    unsigned int wordNum = rand() % numOfWords + 1;
    unsigned int wordLen = 0;
    FILE* file = NULL;
    char *word = malloc(wordMaxLen);

    file = fopen(filename, "r");
    if (!file)
    {
        puts("Failed to load list of words...");
        exit(1);
    }

    for (i = 0; i < wordNum && fgets(word, wordMaxLen, file); i++);
    
    wordLen = strlen(word);
    for (i = 0; i < wordLen; i++)
    {
        if (word[i] == '\n')
        {
            word[i] = '\0';
        }
    }

    fclose(file);

    return word;
}
    

void initHangmanGame(struct hangmanGame *game)
{
    int i = 0;
    int len = 0;
    char* filename = "words.list";

    game->hp = MAX_HP;
    game->wordLen = WORD_MAX_LEN;
    
    game->realWord = getWord(filename, WORD_MAX_LEN);

    len = strlen(game->realWord);

    for (i = 0; i < len; i++)
    {
        game->word[i] = '_';
    }
    game->word[i] = 0;
}


void delHangmanGame(struct hangmanGame *game)
{
    free(game->realWord);
}


int guessLetter(struct hangmanGame *game)
{
    int len = strlen(game->realWord);
    int i = 0;
    int correct = FALSE;
    char letter = 0;

    letter = (char)getchar();
    getchar();

    for (i = 0; i < len; i++)
    {
        if (letter == game->realWord[i])
        {
            correct = TRUE;
            game->word[i] = letter;
        }
    }
    if (!correct)
    {
        game->hp--;
    }
    return correct;
}


int guessWord(struct hangmanGame *game)
{
    int i = 0;
    int len = game->wordLen;

    for (i = 0; i <= len; i++)
    {
        game->buffer[i] = (char)getchar();
        if (game->buffer[i] == '\n')
        {
            break;
        }
    }
    game->buffer[i] = 0;
    fflush(stdin);

    if (!strcmp(game->buffer, game->realWord))
    {
        strcpy(game->word, game->buffer);
        return TRUE;
    }
    game->hp--;

    return FALSE;
}


int isWordCompleted(struct hangmanGame *game)
{
    int i = 0;
    int len = strlen(game->word);

    for (i = 0; i < len; i++)
    {
        if (!islower(game->word[i]))
        {
            return FALSE;
        }
    }

    return TRUE;
}


int isDead(struct hangmanGame *game)
{
    return game->hp < 0;
}


void printHangman()
{
    puts(" ___________.._______\n"
         "| .__________))______|\n"
         "| | / /      ||\n"
         "| |/ /       ||\n"
         "| | /        ||.-''.\n"
         "| |/         |/  _  \\\n"
         "| |          ||  `/,|\n"
         "| |          (\\\\`_.'\n"
         "| |         .-`--'.\n"
         "| |        /Y . . Y\\\n"
         "| |       // |   | \\\\\n"
         "| |      //  | . |  \\\\\n"
         "| |     ')   |   |   (`\n"
         "| |          ||'||\n"
         "| |          || ||\n"
         "| |          || ||\n"
         "| |          || ||\n"
         "| |         / | | \\\n"
         "\"\"\"\"\"\"\"\"\"\"|_`-' `-' |\"\"\"|\n"
         "|\"|\"\"\"\"\"\"\"\\ \\       '\"|\"|\n"
         "| |        \\ \\        | |\n"
         ": :         \\ \\       : :\n"
         ". .          `'       . .\n");
}


void gameLoop()
{
    struct hangmanGame game;
    char choice = 0;
    int exit = FALSE;

    initHangmanGame(&game);
    
    do
    {
        printHangman();
        printf("Lives: %d\n", game.hp);
        printf("%s\n", game.word);
        printf("\n1 - Guess letter\n2 - Guess word\n3 - Give up\n");
        printf("Enter choice: ");

        choice = (char)getchar();
        getchar();

        switch (choice)
        {
        case '1':
            printf("Enter letter: ");
            if (guessLetter(&game))
            {
                puts("Correct!");
            }
            else
            {
                puts("Wrong...");
            }            
            break;
        
        case '2':
            printf("Enter word: ");
            if (guessWord(&game))
            {
                puts("Correct!");
            }
            else
            {
                puts("Wrong...");
            }
            break;

        case '3':
            puts("Good bye! :)");
            exit = TRUE;
            break;

        default:
            puts("Invalid choice...");
            break;
        }
    } while (!exit && !isWordCompleted(&game) && !isDead(&game));
   
    if (isWordCompleted(&game))
    {
        puts("Congratulations!!!");
        printf("You've guessed the word \"%s\"!!!\n", game.realWord);
        puts("But it is still not enough to get a flag");
        puts("Have a nice day!");
    }
    if (isDead(&game))
    {
        puts("You've been hanged!!! :/");
        printf("The word you were looking for is %s\n", game.realWord);
    }

    delHangmanGame(&game);
}


int main(int argc, char const *argv[])
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    srand(time(NULL));

    puts("Welcome to the Hangman game!!!");
    puts("In this game, you have to guess the word");
    puts("Else... YOU WILL BE HANGED!!!");
    puts("Good Luck! UwU\n");

    gameLoop();

    return 0;
}



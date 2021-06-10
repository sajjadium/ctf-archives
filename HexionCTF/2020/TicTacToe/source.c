#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ncurses.h>
#include <wchar.h>
#include <locale.h>
#include <math.h>
#include <string.h>
#include "source.h"

char cursorX = 0, cursorY = 0;
char board[9] = {0};
logic_func DIFFICULTY = IMPOSSIBLE;

void moveAI()
{
    int loc = -1;
    int score = -2;
    int i;
    for (i = 0; i < 9; ++i)
    {
        if (board[i] == NONE)
        {
            board[i] = COMPUTER;
            int tempScore = -(*DIFFICULTY)(PLAYER);
            board[i] = NONE;
            if (tempScore > score)
            {
                score = tempScore;
                loc = i;
            }
        }
    }

    board[loc] = COMPUTER;
    drawO(loc / 3, loc % 3);
}

void initialize()
{
	setlocale(LC_ALL, "");
    initscr();
    keypad(stdscr, TRUE);
    cbreak();
	noecho();
    curs_set(0);

    start_color();
    init_pair(1, COLOR_WHITE, COLOR_BLACK); // BORDER_PAIR
    init_pair(2, COLOR_RED, COLOR_GREEN);   // CURSOR_PAIR
    init_pair(3, COLOR_CYAN, COLOR_BLACK);  // O_PAIR
    init_pair(4, COLOR_RED, COLOR_BLACK);   // O_PAIR
	
	cursorX = 0;
	cursorY = 0;
	memset(board, 0, 9);
	
	clear();
    drawBoard();
    attron(CURSOR_PAIR);
    mvaddch((cursorX * 10) + 5, (cursorX * 20) + 10, ' ');
    attroff(CURSOR_PAIR);
}

int startGame()
{
	bool paused = FALSE;
    char ch, win;
	
	while ((ch = getch()) != 'q' && ch != 'Q')
    {
        if (paused)
            continue;

        if (ch == 5 || ch == 'd' || ch == 'D') // right
            drawCursor(1, 0);

        if (ch == 4 || ch == 'a' || ch == 'd') // left
            drawCursor(-1, 0);

        if (ch == 3 || ch == 'w' || ch == 'W') // up
            drawCursor(0, -1);

        if (ch == 2 || ch == 's' || ch == 'S') // down
            drawCursor(0, 1);

        if (ch == ' ')
        {
            if (board[cursorX * 3 + cursorY])
                continue;

            board[cursorX * 3 + cursorY] = PLAYER;
            drawX(cursorX, cursorY);
            moveAI();

            char i = 0;
            // check for draw
            for (i = 0; i < 9; i++)
                if (!board[i])
                    break;

            if ((win = checkWin()) || i == 9)
                paused = TRUE;
        }
    }

    endwin();
	return win;
}

void main(void)
{
	char option = 0, message[100], name[25];
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	
	puts("Please enter your name: ");
	scanf("%24s", name);
	getchar();
	snprintf(message, 100, "Welcome %s!\n", name);
	printf(message);
	
	printf("Press ENTER to begin.\n");
	getchar();
	do
	{
		initialize();

		switch (startGame())
		{
			case PLAYER:
			{			// player won
				FILE *flag = fopen("flag", "r");
				fgets(message, 40, flag);
				puts(message);
				break;
			}

			case COMPUTER: // player lost
				printf("YOU LOST\n");
				break;

			default:
				printf("DRAW\n");
		}
		
		puts("Do you want to play again? [y/n] ");
		scanf("%c", &option);
		getchar();
    } while (option == 'y' || option == 'Y');
	
	puts("Goodbye!");
}
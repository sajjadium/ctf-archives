#pragma once

#define max(a, b) (a > b ? a : b)
#define min(a, b) (a < b ? a : b)

#define BOARD_PAIR COLOR_PAIR(1)
#define CURSOR_PAIR COLOR_PAIR(2)
#define O_PAIR COLOR_PAIR(3)
#define X_PAIR COLOR_PAIR(4)

#define MAX_X 60
#define MAX_Y 30

#define COMPUTER 1
#define PLAYER -1
#define DRAW 2
#define NONE 0

#define convertXY(_x, _y) \
    _x = (_x * 20) + 10;  \
    _y = (_y * 10) + 5

extern char cursorX, cursorY;
extern char board[9];
typedef int (*logic_func)(char);

int mod(int a, int b)
{
    int r = a % b;
    return r < 0 ? r + b : r;
}

void drawBoard(void)
{
    resizeterm(31, 61);
    attron(BOARD_PAIR);

    // draw border and lines
    box(stdscr, 0, 0);
    mvvline(1, 20, 0, 30);
    mvvline(1, 40, 0, 30);
    mvhline(10, 1, 0, 60);
    mvhline(20, 1, 0, 60);

    // draw crosses
    cchar_t left = {0, L'├'}, right = {0, L'┤'}, top = {0, L'┬'}, bot = {0, L'┴'}, crs = {0, L'┼'};
    mvadd_wch(0, 20, &top);
    mvadd_wch(0, 40, &top);
    mvadd_wch(30, 20, &bot);
    mvadd_wch(30, 40, &bot);

    mvadd_wch(10, 0, &left);
    mvadd_wch(20, 0, &left);
    mvadd_wch(10, 60, &right);
    mvadd_wch(20, 60, &right);

    mvadd_wch(10, 20, &crs);
    mvadd_wch(10, 40, &crs);
    mvadd_wch(20, 20, &crs);
    mvadd_wch(20, 40, &crs);
    attroff(BOARD_PAIR);
}

void drawO(char midX, char midY)
{
    convertXY(midX, midY);
    for (size_t i = 0, x = 0, y = 0; i < 360; i += 1)
    {
        x = round(6 * cos(i * M_PI / 180));
        y = round(3 * sin(i * M_PI / 180));

        attron(O_PAIR);
        mvaddch(midY + y, midX + x, '*');
        attroff(O_PAIR);
    }
}

void drawX(char midX, char midY)
{
    convertXY(midX, midY);
    for (int x = -6, y = -3; y < 4 && x < 8; x += 2, y++)
    {

        if (y == 0)
        {
            attron(CURSOR_PAIR);
            mvaddch(midY + y, midX + x, '*');
            attron(CURSOR_PAIR);
        }
        else
        {
            attron(X_PAIR);
            mvaddch(midY - y, midX + x, '*');
            mvaddch(midY + y, midX + x, '*');
            attroff(X_PAIR);
        }
    }
}

void drawCursor(char addX, char addY)
{
    char x = cursorX, y = cursorY;
    convertXY(x, y);

    // fix previous
    attron(X_PAIR);
    mvaddch(y, x, ((mvinch(y, x) & 0xFF) == 32) ? ' ' : '*');
    attroff(X_PAIR);

    cursorX = mod((cursorX + addX), 3);
    cursorY = mod((cursorY + addY), 3);
    x = cursorX, y = cursorY;
    convertXY(x, y);

    attron(CURSOR_PAIR);
    mvaddch(y, x, ((mvinch(y, x) & 0xFF) == 32) ? ' ' : '*');
    attroff(CURSOR_PAIR);
}

char checkWin()
{
    unsigned wins[8][3] = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}};
    int i = 0;

    for (i = 0; i < 8; ++i)
    {
        if (board[wins[i][0]] != 0 &&
            board[wins[i][0]] == board[wins[i][1]] &&
            board[wins[i][0]] == board[wins[i][2]])
            return board[wins[i][0]];
    }

    return NONE;
}

// taken from https://gist.github.com/MatthewSteel/3158579
int IMPOSSIBLE(char player)
{
	
    int winner = checkWin(board);
    if (winner != NONE)
        return winner * player;

    char loc = -1;
    char score = -2; 
    for (int i = 0; i < 9; ++i)
    {
        if (board[i] == NONE)
        {
            board[i] = player; 
            int thisScore = -IMPOSSIBLE(player * -1);
            if (thisScore > score)
            {
                score = thisScore;
                loc = i;
            }             
            board[i] = NONE; 
        }
    }
    if (loc == -1)
        return 0;
    return score;
}
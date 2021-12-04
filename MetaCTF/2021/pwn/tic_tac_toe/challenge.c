#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/uio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>



void setup(){
	setvbuf(stdout, 0, _IONBF, 0);
	setvbuf(stdin, 0, _IONBF, 0);
	setvbuf(stderr, 0, _IONBF, 0);
}


int determine_winner(char a){
	switch(a){
		case 'X':
		case 'x':
			return 1;
		case 'o':
		case 'O':
		case '0':
			return 2;
		default:
			break;
	}
	return -1;
}

// A function that returns 1 for X row match and 2 for O row match
int rowCrossed(char board[][3])
{
    for (int i=0; i<3; i++)
    {
        if (board[i][0] == board[i][1] &&
            board[i][1] == board[i][2] &&
            board[i][0] != ' ')
			return determine_winner(board[i][0]);
    }
    return 0;
}

// A function that returns 1 for X column match and 2 for O column match
int columnCrossed(char board[][3])
{
    for (int i=0; i<3; i++)
    {
        if (board[0][i] == board[1][i] &&
            board[1][i] == board[2][i] &&
            board[0][i] != ' ')
			return determine_winner(board[0][i]);
    }
    return 0;
}

// A function that returns 1 for X crossing diagonal and 2 for O crosing diagnol
int diagonalCrossed(char board[][3])
{
    if (board[0][0] == board[1][1] &&
        board[1][1] == board[2][2])
		return determine_winner(board[0][0]);

    if (board[0][2] == board[1][1] &&
        board[1][1] == board[2][0])
		return determine_winner(board[0][2]);

    return 0;
}

void print_winner(int winner){
	switch(winner){
		case 0:
			puts("The game is a CAT");
			break;
		case 1:
			puts("X's win the game");
			break;
		case 2:
			puts("O's win the game");
			break;
		default:
			puts("Something went wrong");
	}
}


//function that reads in the board from the user
int read_board(){
	char board[3][3];
	char counter = 0;

	//read the board in
	while (counter < 9){
		while(1){
			read(0, (char*)board+counter++, 1);

			if (*((char *)board+counter-1) == '\n')
			{
				counter--;
				continue;
			}
			//checks for the last character to be o,O,0,x,X 
			//I was a bit lazy in the checks though, so you need to be consistant when using characters
			//Or the program won't match correctly
			if (*((char*)board + counter-1) == 'o' || *((char*)board + counter-1) == 'O' ||*((char*)board + counter-1) == '0' || *((char*)board + counter-1) == 'x' || *((char*)board + counter-1) == 'X'){
				break;
			}
			puts("Bad Character, try again");
		}
	}

	//now the whole board has been read in, check for a column winner
	if (columnCrossed(board))
		print_winner(columnCrossed(board));
	if (rowCrossed(board))
		print_winner(rowCrossed(board));
	if (diagonalCrossed(board))
		print_winner(diagonalCrossed(board));


	print_winner(0);
}


int main(){
	setup();
	puts("Check out this sweet Tic-Tac-Toe Solver I made!");
	puts("All you have to do is to input your array into the system and I'll tell you who won");
	puts("You can enter them all at once, or one at a time if you prefer");
	read_board();
	_exit(0);

}

//Useless function when you think about it, because it's impossible to get here... Right?
void win(){
	int fd;
	char buffer[100];
	fd = open("./flag.txt",0);
	read(fd, buffer,100);
	write(1,buffer,100);
	_exit(0);
}


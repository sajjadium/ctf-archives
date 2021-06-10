                //This was for csc-250 final project, not very well commented right now will update later for better gameplay and flow
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <ncurses.h>
#include "MonROPoly.h"
#include <time.h>

typedef struct ROPCHAIN{
	void *address;
	char *string;
	struct ROPCHAIN *next;
	struct ROPCHAIN *prev;
}CHAIN;

CHAIN *head = 0,*tail = 0;
char board[45][99];
char * tmpname;
char * seed;
WINDOW* win1, *win2,*win3,*win4;
Player *comp;
int animation = 1;

void jumpChain(){
	endwin();
	if (!head)
		exit(0);
	unsigned long long *location = __builtin_frame_address(0);
	location++;
	while(head){
		*location = (unsigned long long)head->address;
		location++;
		head=head->next;
	}
	printf("Good Luck with your chain");
	sleep(1);
		
}

void viewChain(){
	if(!head){
		printwin4("You do not have a chain");	
		return;
	}
	int counter = 0;
	CHAIN* tmp = head;
	CHAIN* tmp2;
	while(tmp){
		wclear(win3);
		box(win3,'|','-');
		tmp2 = tmp;
		for(int x = 0; x < 5; x++){
			if(tmp2 == NULL)
				break;
			mvwprintw(win3,x+1,1,"%d: %s",x+counter,tmp2->string);
			tmp2 = tmp2->next;
		}
		wrefresh(win3);
		usleep(750000);
		tmp = tmp->next;
		counter+= 1;
	}

}

void gotoJail()//send a player to jail if called
{
	printwin4("Both players go to jail\n Do not pass Start\n Do no collect $200");
	player->i=0;
	player->j=0;
	comp->i=0;
	comp->j=0;
	clearGadgets();
	printBoard();
}

void clearGadgets(){
	if(tail != NULL)
	{
		while(tail->prev){
			tail = tail->prev;
			free(tail->next);
		}
		free(tail);
		tail = NULL;		
	}
	head=tail;
	return;
}

void pop(){//int is to test to pop the last gadget or a random
	CHAIN* tmp = head;
	int counter = 0;
	if(tail && tail->prev){
		tmp = tail;
		tail=tail->prev;
		free(tail->next);
		tail->next= NULL;
	}
	else{//only one gadget exists
		free(tail);
		tail = 0;
		head = tail;
	}

	return;
}

void push(int i, int j){

	int counter;
	int r;
	switch(gadgets[i][j]){
		case -1://jail
			gotoJail();
			break;
		case -2://chance, no dups...unless you go through them all
			counter = 0;
			r = rand()%14;

			while(chancecheck[r]>0){
				r=(r+1)%14;
				counter+=1;	
				if(counter > 14){
					r = 9;
					break;
				}
			}
			chancecheck[r]++;
			chance[r]();
			break;
		case -3://freeparking//jail(visiting) 
			break;
		case -4://pay tax lose last gadget
			printwin4("Pay Hacker Tax\n Lose Last Gadget");
			pop();
			break;
		default:
			if(!head){
				tail = head = malloc(sizeof(CHAIN));
				tail->prev = NULL;
				tail->next = NULL;
			}
			else{
				tail->next = malloc(sizeof(CHAIN));
				tail->next->prev = tail;
				tail = tail->next;
				tail->next = NULL;
			}
			tail->address= (void *)gadgets[i][j];
			tail->string = gadgetsString[i][j];
			break;
	}
}

void changeLoc(int i, int j, int who){//changes a players location, as puts the 1 or 0 where the player is located
	char character = 'P';
	i=i?i*6+2:i+1;
	j=j?j*13+4:j+1;
	if(!who)
	{
		character = 'C';
		j++;
	}
	mvwprintw(win1,i,j,"%c",character);
	winrefresh();
        return;
}
int rollDice()//rolls dice
{
	*((int *)seed) = (*((int*)seed) + 1);
        srand(*((unsigned int *)seed));
        return (rand() % 6)+1;
}

void printwin4(char *string){
	wclear(win4);
	box(win4,'|','-');
	mvwprintw(win4,1,1,string);
	wrefresh(win4);
	sleep(3);
	wclear(win4);
	box(win4,'|','-');
	mvwprintw(win4,2,11,"CHANCE");
}

void printwin3(char *string){
	wclear(win3);
	box(win3,'|','-');
	mvwprintw(win3,1,1,string);
	wrefresh(win3);
	sleep(3);
	wclear(win3);
	box(win3,'|','-');
}

void movePlayer(Player* tmp)//moves the player step by step
{
	int roll = rollDice();
	wclear(win3);
	if (tmp->isPlayer)
		mvwprintw(win3,3,12,"You rolled a %d",roll);
	else
		mvwprintw(win3,3,8,"The computer rolled a %d",roll);

	wrefresh(win3);

	while(roll){
		if(tmp->i == 0 && tmp->j != 6)
			tmp->j++;
		else if(tmp->j == 6 && tmp->i != 6)
			tmp->i++;
		else if(tmp->i == 6 && tmp->j != 0)
			tmp->j--;
		else
			tmp->i--;

		printBoard();
		roll--;
		if(animation)
			usleep(500000);
	}	
	push(tmp->i,tmp->j);

        return;
}

int getchoice(char *string)
{
	char input[10];
	print(string);
	get(input, 10);
	return atoi(input);

}
void invalid(){
	winrefresh();
	mvwprintw(win2,1,1,"Invalid");
	wrefresh(win2);
	sleep(1);

}
void playGame()//starts the game and innitializes everythin
{
	int test = 0;
	while(1)
	{
		test = 0;
		printOptions();
		winrefresh();
		switch(getchoice("what would you like to do?")){
			case 1://roll
				test = 1;
				movePlayer(player);					
				break;
			case 2://toggle Animation
				toggleAnimation();
				break;
			case 3://View Chain
				viewChain();
				break;
			case 4://Jump to chain
				jumpChain();
				break;
			case 5://exit
				endwin();
				exit(0);
				break;
			default://Error
				invalid();	
				break;

		}
		if(test)
			movePlayer(comp);
		
	}
	endwin();
        return;

}
int main()//main
{
	init_game();
        playGame();
        return 0;
}

void init_game(){
	

	player = malloc(sizeof(Player));
	comp = malloc (sizeof(Player));
	tmpname = malloc(sizeof(char)*24);
	seed = malloc(sizeof(int));

	FILE *fp = fopen("/dev/urandom","r");
	if(fp == NULL){
		printf("Sorry /dev/urandom failed to open\n");
		exit(0);
	}
	fread(seed,1,4,fp);
	fclose(fp);
	//seeded, time to start
	init_gadgets();
        init_chance();
	init_window();
	player->i = 6;
        player->j = 0;
	player->isPlayer = 1;
        comp->i = 6;
        comp->j = 0;
	comp->isPlayer = 0;
        createBoard(board);
        printBoard(board);
	editName();
	srand((unsigned int) *seed);


}
void init_window(){
	initscr();
	win1 = newwin(45,100,0,0);
	win2 = newwin(5,40,30,29);
	win3 = newwin(7,40,23,29);
	win4 = newwin(6,28,16,35);
	mvwprintw(win4,2,11,"CHANCE");
	winrefresh();
}

void createBoard() // Creates Board
{
	FILE *fp = fopen("board", "r");

	for(int x = 0; x < 45; x++)
		fgets(board[x], 100,fp);

	fclose(fp);
        return;
}

void printBoard() //Prints Board
{
	for(int x = 0; x < 45; x++)
		mvwprintw(win1,x,0,"%s",board[x]);
	changeLoc(player->i,player->j,1);
	changeLoc(comp->i,comp->j,0);
	wclear(win2);
	winrefresh();
}

void print(char *string){
	mvwprintw(win2,1,1,string);
}

void get(char *string,int n){
	mvwgetnstr(win2, 2,1,string,n);
	wclear(win2);
	box(win2,'|','-');
	wrefresh(win2);
}

void winrefresh(){
	wclear(win2);
	box(win2,'|','-');
	box(win3,'|','-');
	box(win4,'|','-');
	wrefresh(win1);
	wrefresh(win2);
	wrefresh(win3);
	wrefresh(win4);
}

void printOptions(){
	wclear(win3);
	mvwprintw(win3,1,1,"1. Roll the Dice and Move");
	mvwprintw(win3,2,1,"2. Toggle Animation");
	mvwprintw(win3,3,1,"3. View Current Rop Chain");
	mvwprintw(win3,4,1,"4. Execute Chain");
	mvwprintw(win3,5,1,"5. Exit");

}

void editName(){
	//Don't want there to be an overflow so we will buffer the input first
	wclear(win2);	
	box(win2,'|','-');
	
	print("What is your name?");
	get(tmpname,sizeof(Player));//only want to fill the name, this is a safer way to make sure I get the right amount
	strncpy(player->name, tmpname, 24);
}

void toggleAnimation(){
	animation ^= 1;
	wclear(win3);
	box(win3,'|','-');
	mvwprintw(win3,3,9,"Animation Turned %s",(animation?"On":"Off"));
	wrefresh(win3);
	usleep(2000000);
	
}


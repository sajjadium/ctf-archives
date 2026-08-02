#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <time.h>
#include <unistd.h>

char *unlitImg = " \
     _______       \n \
  .-'-------'-.    \n \
 (_____________)";
 
 
 
char *litImg = " \
       )  (        \n \
      (   ) )      \n \
       ) ( (       \n \
     _______       \n \
  .-'-------'-.    \n \
 (_____________)";
 
 
 
 
long litscore = 0;
 
void printBar() {
	puts("-----------------------------------------------------------");
}

void intro() {
	printBar();
	puts("Welcome to LIT Arcade!");
}

void menu() {
	printBar();
	puts("1. LITe a fire");
	puts("2. LITebulb puzzle");
	puts("3. LIT fuse");
	puts("8. Check LIT score");
	puts("9. Propose a LIT Minigame");
	puts("0. Exit LIT Arcade");
	printf("\n> ");
}

// return number of points earned
long game1() {
	printBar();
	puts("LITe a fire for 10 LIT points!");
	
	int track = 1;
	char *buf = (char *) malloc(64);
	while (track) {
		puts("");
		puts(unlitImg);
		puts("\nType 'fire!' to strike a fire!");
		puts("Type 'exit' to give up.\n");
		while (1 == 1) {
			printf("> ");
			buf[read(0, buf, 64) - 1] = 0;
			if (!strcmp(buf, "fire!")) {
				track = (rand()) % 10;
				break;
			}
			else if (!strcmp(buf, "exit")) {
				puts("\nYou give up and earn 0 LIT points.");
				free(buf);
				return 0;
			}
		}
		
	}
	
	puts("");
	puts(litImg);
	puts("\nYou did it! You earn 10 LIT points.");
	free(buf);
	return 10;
}

void toggleRow(int grid[5][5], int row) {
	for (int i = 0; i < 5; i++) {
		grid[row][i] = (1 - grid[row][i]);
	}
}

void toggleColumn(int grid[5][5], int column) {
	for (int i = 0; i < 5; i++) {
		grid[i][column] = (1 - grid[i][column]);
	}
}

void displayGrid(int grid[5][5]) {
	for (int r = 0; r < 5; r++) {
		for (int c = 0; c < 5; c++) {
			printf("%i", grid[r][c]);
		}
		putchar('\n');
	}
}

int checkGrid(int grid[5][5]) {
	for (int r = 0; r < 5; r++) {
		for (int c = 0; c < 5; c++) {
			if (grid[r][c] == 0) return 0;
		}
	}
	return 1;
}

void clearBuffer() {
	int c;
	while ((c = getchar()) != '\n' && c != EOF);
}

long game2() {
	printBar();
	puts("Solve the LITebulb puzzle for 15 LIT points!");
	puts("LITe up the grid by turning all cells into 1s!");
	
	int grid[5][5];
	
	for (int r = 0; r < 5; r++) {
		for (int c = 0; c < 5; c++) {
			grid[r][c] = 0;
		}
	}
	
	// shuffle 15 moves
	for (int i = 0; i < 15; i++) {
		int rc = rand() % 2;
		int idx = rand() % 5;
		
		if (rc == 0) toggleRow(grid, idx);
		else toggleColumn(grid, idx);
	}
	
	while (!checkGrid(grid)) {
		puts("");
		displayGrid(grid);
		
		int rc = 0;
		int idx = 0;
		
		int check = 0;
		
		puts("\nToggle row or column? 0 for row, 1 for column, 2 to exit");
		printf("> ");
		
		while (!check) {
			check = scanf("%d%*c", &rc);
			if (check != 1) {
				clearBuffer();
			}
		}
		
		if (rc == 2) {
			puts("\nYou give up and earn 0 LIT points.");
			return 0;
		}
		
		puts("\nWhich row/column? From 1 to 5");
		printf("> ");
		
		check = 0;
		
		while (!check) {
			check = scanf("%d%*c", &idx);
			if (check != 1) {
				clearBuffer();
			}
		}
		
		idx--;
		
		if (rc == 0) toggleRow(grid, idx);
		else toggleColumn(grid, idx);
	}
	
	
	puts("\nYou did it! You earn 15 LIT points.");
	return 15;
}

void leftNChars(int amount) {
	for (int i = 0; i < amount; i++) {
		printf("\x1B[D");
	}
}

void rightNChars(int amount) {
	for (int i = 0; i < amount; i++) {
		printf("\x1B[C");
	}
}



volatile int numChars = 0;



// Function to set terminal in raw mode
void set_raw_mode(struct termios *old_tio) {
	struct termios new_tio;

	// Get current terminal attributes
	tcgetattr(STDIN_FILENO, old_tio);

	// Set new terminal attributes
	new_tio = *old_tio;
	new_tio.c_lflag &= ~(ICANON);        // Disable canonical mode
	new_tio.c_cc[VMIN] = 1;              // Minimum number of characters to read
	new_tio.c_cc[VTIME] = 0;             // Timeout in deciseconds (0 means no timeout)

	// Set new terminal attributes
	tcsetattr(STDIN_FILENO, TCSANOW, &new_tio);
}

// Function to restore terminal to previous state
void restore_mode(struct termios *old_tio) {
	tcsetattr(STDIN_FILENO, TCSANOW, old_tio);
}



	
const int codeSize = 8;

volatile int running = 1;
volatile int running2 = 1;

volatile int canonicalTio = 1;

// full animation plays before terminating thread
volatile int fuseLosingTimer = 0;
volatile int fuseLosingInput = 0;

char *code;
char *actualCode;


	
pthread_t timer_thread, input_thread;


struct termios old_tio;



void restoreTio() {
	if (!canonicalTio) {
		restore_mode(&old_tio);
		canonicalTio = 1;
	}
}



void winFuse() {
	free(actualCode);
	free(code);
	
	printf("\x1B[3A");
	leftNChars(numChars + 2);
	printf("|  DEFUSED  |\x1B[13D\x1B[3B");
	rightNChars(numChars + 2);
	
	puts("\n\nYou defused the LIT fuse!");
	puts("Your LIT score is doubled!");

	litscore *= 2;
}



void loseFuse(int fromTimer) {
	free(actualCode);
	free(code);
	
	printf("\x1B[3A");
	leftNChars(numChars + 2);
	printf("|  -------  |\x1B[13D\x1B[3B");
	rightNChars(numChars + 2);
	sleep(1);
	
	if (fromTimer) {
		restoreTio();
		pthread_cancel(input_thread);
	}
	
	puts("\n\nBOOM! You died.");
	
	char *name = (char *) malloc(15);
	char *desc = (char *) malloc(15);
	
	printf("\nEnter name for your gravestone: ");
	name[read(0, name, 15) - 1] = 0;
	
	printf("\nEnter text for your gravestone: ");
	desc[read(0, desc, 15) - 1] = 0;
	
	puts  (" ___________________ ");
	puts  ("/                   \\");
	puts  ("|        RIP        |");
	puts  ("|                   |");
	printf("|  %-15s  |\n", name);
	puts  ("|                   |");
	puts  ("|                   |");
	printf("|  %15s  |\n", desc);
	puts  ("|___________________|");
	
	exit(0);
}



void *timer_function(void *arg) {
	int timer = 10;
	
	puts(" ___________");
	puts("|           |");
	printf("|   %d   %d   |\n", timer / 10, timer % 10);
	puts("|___________|");
	
	printf("\n> ");
	
	while (running2 && timer > 0) {
		sleep(1);
		if (!running2) {
			break;
		}
		timer--;
		printf("\x1B[3A");
		leftNChars(numChars + 2);
		printf("|   %d   %d   |\x1B[13D\x1B[3B", timer / 10, timer % 10);
		rightNChars(numChars + 2);
	}
	
	if (running2 != 0 && !fuseLosingInput) {
		// this means input function is still running
		// meaning we ran out of time
		fuseLosingTimer = 1;
		loseFuse(1);
	}
	
	return NULL;
}






void *input_function(void *arg) {

	set_raw_mode(&old_tio);
	canonicalTio = 0;
	int ch;
	
	for (int i = 0; i < codeSize; i++) {
		*(actualCode + i) = (rand() % 10) + '0';
	}
	
	while (running && numChars < codeSize) {
	 	ch = getchar();
	 	*(code + numChars) = ch;
		numChars++;
	}
	
	
	running2 = 0;
	
	if (!strncmp(code, actualCode, codeSize) && !fuseLosingTimer) {
		winFuse();
	}
	else if (!fuseLosingTimer) {
		fuseLosingInput = 1;
		loseFuse(0);
	}
	
	
	
	restore_mode(&old_tio);
	canonicalTio = 1;
	return NULL;
}


void handle_sigint(int sig) 
{ 
	if (!canonicalTio) {
		restore_mode(&old_tio);
		canonicalTio = 1;
	}
	puts("\nKeyboard interrupt, exiting");
	exit(0);
}

long game3() {

	running = 1;
	running2 = 1;
	numChars = 0;
	fuseLosingTimer = 0;
	fuseLosingInput = 0;
	
	actualCode = (char *) malloc(codeSize);
	code = (char *) malloc(codeSize);
	
	
	
	
	
	printBar();
	puts("You have 10 seconds to defuse the LIT fuse!");
	
	// Create the timer thread
	if (pthread_create(&timer_thread, NULL, timer_function, NULL) != 0) {
		perror("Failed to create timer thread");
		return -1;
	}

	// Create the input thread
	if (pthread_create(&input_thread, NULL, input_function, NULL) != 0) {
		perror("Failed to create input thread");
		return -1;
	}
	
	pthread_join(timer_thread, NULL);
	running = 0;
	if (fuseLosingTimer) {
		// if the game ends due to the timer
	}
	else {
		// if the game ends (losing) by input
		restoreTio();
		pthread_join(input_thread, NULL);
	}
	return 0;
}


long considerProposal(char newMinigame[256]) {
	if (strstr(newMinigame, "LIT") != NULL) {
		return 100;
	}
	else if (strstr(newMinigame, "TIL") == NULL) {
		// no mentioning our rival!
		return 1;
	}
}


char newMinigame[256];


long sendProposal() {
	puts("What is the premise of your minigame?");
	
	newMinigame[read(0, newMinigame, 256) - 1] = 0;
	
	puts("Thank you! We will consider your proposal.");
	
	return considerProposal(newMinigame);
}

int main() {
	signal(SIGINT, handle_sigint);
	
	setbuf(stdout, 0x0);
	setbuf(stderr, 0x0);
	
	srand(time(0));
	
	intro();
	int choice = 17;
	while (choice) {
		menu();
		choice = 17;
		int check = scanf("%d%*c", &choice);
		if (check != 1) {
			clearBuffer();
		}
		switch (choice) {
			case 1:
				litscore += game1();
				break;
			case 2:
				litscore += game2();
				break;
			case 3:
				litscore += game3();
				break;
			case 8:
				printf("Your LIT score: %ld\n", litscore);
				break;
			case 9:
				litscore += sendProposal();
				break;
			case 0:
				break;
		}
	}
	
	puts("Goodbye!");
	exit(0);
}

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>

typedef struct note {
	int size;
	int numread;
	double * doublenote;
} note;

note * notes[32];

int created = 0;

void handler() {
	puts("Your session has expired.");
	exit(-1);
}


void menu() {
	puts("Choose your option:");
	puts("1. Create a note.");
	puts("2. View a note.");
	puts("3. Edit a note.");
	puts("4. Delete a note.");
	puts("5. Swap values within notes.");
	puts("6. Exit");
}

void create() {
	char val[8] = {0};
	if(created >= 32) {
		puts("You have reached the max number of available doublenotes!");
		return;
	}
	int index;
	for(index = 0; index < 32; index++) {
		if(notes[index] == 0) {
			break;
		}
	}
	int size;
	puts("Enter the size of your note:");
	fgets(val, 8, stdin);
	size = atoi(val);
	notes[index] = malloc(sizeof(note));
	notes[index]->size = size;
	notes[index]->numread = 0;
	notes[index]->doublenote = malloc(sizeof(double) * size);
	printf("Note created! Your note ID is: %d\n", index);
	created++;
}

void view() {
	char val[8] = {0};
	int choice = -1;
	puts("Enter the note ID which you want to view:");
	fgets(val, 8, stdin);
	choice = atoi(val);
	if(choice < 0 || choice >= 32 || notes[choice] == NULL) {
		puts("Unknown note ID.");
		return;
	}
	for(int i = 0; i < notes[choice]->numread; i++) {
		printf("%d: %.18e\n", i+1, notes[choice]->doublenote[i]);
	}
}

void edit() {
	char val[8] = {0};
	int choice = -1;
        puts("Enter the note ID which you want to edit:");
        fgets(val, 8, stdin);
        choice = atoi(val);
        if(choice < 0 || choice >= 32 || notes[choice] == NULL) {
                puts("Unknown note ID.");
                return;
        }
	if(notes[choice]->size == 0) {
		puts("Nothing to edit!");
		return;
	}
	int numdouble = 0;
	int done = 0;
	double value = 0.0;
	puts("Edit your note here:");
	while(numdouble < notes[choice]->size && !done) {
		printf("%d: ", numdouble+1);
		scanf("%lf", &value);
		notes[choice]->doublenote[numdouble] = value;
		puts("");
		numdouble++;
		while(getchar() != '\n') {}
		if(numdouble < notes[choice]->size) {
			puts("Enter another value? (y/n)");
			char select = getchar();
			while(getchar() != '\n') {}
			if (select != 'y' && select != 'Y') {
				done = 1;
			}
		}
	}
	notes[choice]->numread = numdouble;
	puts("Your note has been updated");
}

void del() {
        char val[8] = {0};
        int choice = -1;
        puts("Enter the note ID which you want to delete:");
        fgets(val, 8, stdin);
        choice = atoi(val);
        if(choice < 0 || choice >= 32 || notes[choice] == NULL) {
                puts("Unknown note ID.");
                return;
        }
	free(notes[choice]->doublenote);
	free(notes[choice]);
	notes[choice] = NULL;
	puts("Note deleted.");
	created--;

}

void swap() {
        char val[8] = {0};
        int choice = -1;
        puts("Enter the note ID which you want to swap values in:");
        fgets(val, 8, stdin);
        choice = atoi(val);
        if(choice < 0 || choice >= 32 || notes[choice] == NULL) {
                puts("Unknown note ID.");
                return;
        }
	puts("Enter which double to swap:");
	fgets(val, 8, stdin);
	int position1 = atoi(val);
	if(position1 < 0 || position1 > notes[choice]->numread) {
		puts("Unknown double.");
		return;
	}
        puts("Enter which double to swap with:");
        fgets(val, 8, stdin);
        int position2 = atoi(val);
        if(position2 < 0 || position2 > notes[choice]->numread) {
                puts("Unknown double.");
                return;
        }
	double temp = notes[choice]->doublenote[position1-1];
	notes[choice]->doublenote[position1-1] = notes[choice]->doublenote[position2-1];
	notes[choice]->doublenote[position2-1] = temp;
	puts("Values successfully swapped.");
}

void bye() {
	puts("Thanks for using our note application!");
	exit(0);
}

int main() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
	signal(SIGALRM, handler);
	alarm(90);
	puts("Welcome to our double-y improved note application!");
	unsigned int option;
	char val[8] = { 0 };
	while (1) {
		menu();
		printf("> ");
		fgets(val, 8, stdin);
		option = atoi(val);
		switch(option) {
			case 1:
				create();
				break;
			case 2:
				view();
				break;
			case 3:
				edit();
				break;
			case 4:
				del();
				break;
			case 5:
				swap();
				break;
			case 6:
				bye();
				break;
			default:
				puts("Invalid option!");
				break;
		}
	}
}

#include <stdlib.h>
#include <stdio.h>
#include <malloc.h>


typedef struct param {
	unsigned int maxsize;
} param_t;

typedef struct datanote {
	unsigned int size;
	char data;
} datanote_t;

void init();
void welcome();
void print_menu();
datanote_t * create_note(unsigned int size, param_t* params);
void show_note(datanote_t * note);
void edit_note(datanote_t * note);


int main() {
	init();
	welcome();

	int choice;
	datanote_t* note = NULL;
	param_t*  params = (param_t*)malloc(sizeof(param_t));
	params->maxsize = 0x7f;

	while(1) {
		print_menu();

		scanf("%d", &choice);
		getchar();
		printf("\n");
		switch (choice) {
			case 1:
				printf("Size: ");
				unsigned int size;
				scanf("%d", &size);
				getchar();
				note = create_note(size, params);
				break;
			case 2:
				show_note(note);
				break;
			case 3:
				edit_note(note);
				break;
			case 4:
				free(note);
				note = 0;
				break;
			default:
				printf("Invalid option.\n");
		}
	}

	return 0;
}


void init() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}


void welcome() {
	printf("	                           %%%%%%%%%%%%%%%%%%                         \n");
	printf("                 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                         \n");
	printf("            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%..............%%%%%%%%       \n");
	printf("            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                 ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%       %%%%%%%%%%%%%%%%%%%%%%%%%%                 ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%  %%%%%%%%   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%  %%%%%%%%%%\\  %%%%%%%%%%%%%%%%%%%%              %%%%##%%      \n");
	printf("            %%%%%%%%%%%%%%%%  %%%%%%%%%%%%\\  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    %%%% ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%  %%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%%%              %%%% ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%  %%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%%%              %%%%%%%%%%      \n");
	printf("            %%%%%%%%%%%%%%%%  %%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    %%%% ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%  %%%%%%%%%%%%/ %%%%%%%%%%%%%%%%%%%%              %%%% ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%  %%%%%%%%/  %%%%%%%%%%%%%%%%%%%%%%..........\n");
	printf("            %%%%%%%%%%%%%%%%       %%%%%%%%%%%%%%%%%%%%%%%%%%              %%%% ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%              %%%% ,%%      \n");
	printf("            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%         \n");
	printf("                  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                         \n");
	printf("                                 %%%%%%%%%%%%%%\n\n");


	printf("      *******************************************\n");
	printf("      *                DUCTFnote                *  \n");
	printf("      *******************************************\n\n");
}


void print_menu() {
	printf("\n");
	printf("1. Create Note\n");
	printf("2. Show Note\n");
	printf("3. Edit Note\n");
	printf("4. Delete Note\n");
	printf(">> ");
}


datanote_t * create_note(unsigned int size, param_t *params) {
	if (size > params->maxsize) {
		printf("Note too big.\n");
		return 0;
	}
	int allocsize = size | 0x80;
	datanote_t * note = (datanote_t*)malloc(allocsize + 8);
	note->size = size;
	return note;
}


void show_note(datanote_t * note) {
	if(!note) {
		printf("No Note.\n");
		return;
	}

	printf("<------------ NOTE 1 ------------>\n");
	fwrite(&(note->data), note->size, 1, stdout);
	printf("\n");
	printf("<-------------------------------->\n");
	printf("\n");
}


void edit_note(datanote_t * note) {
	if(!note) {
		printf("No Note.\n");
		return;
	}

	signed char idx = 0;
	while(idx <= note->size) {
		*(&(note->data)+idx) = fgetc(stdin);
		if (*(&(note->data)+idx) == '\n') {*(&(note->data)+idx) = '\0'; break;}
		idx++;
	}
}

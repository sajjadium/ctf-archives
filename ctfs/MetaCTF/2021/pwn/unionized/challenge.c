#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/uio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

struct created{
	int type;
	int size;

	union Variable {
		char * string;
		int integer;
		long long long_boi;
		char character;

	} variable;
	void (*print)();
	struct created *next;
};

struct created * head;

void setup(){
	setvbuf(stdout, 0, _IONBF, 0);
	setvbuf(stdin, 0, _IONBF, 0);
	setvbuf(stderr, 0, _IONBF, 0);
}

void display_string(struct created *tmp){
	printf("%s\n", tmp->variable.string);
}
void display_int(struct created *tmp){
	printf("%d\n", tmp->variable.integer);
}
void display_long(struct created *tmp){
	printf("%lld\n", tmp->variable.long_boi);
}
void display_character(struct created *tmp){
	printf("%c\n", tmp->variable.character);
}

void create_variable(struct created *tmp){
	while(1){
		int choice;

		puts("What type would you like?\n");
		puts("1. String");
		puts("2. Integer");
		puts("3. Long Long");
		puts("4. Character");
		scanf("%d", &choice);

		switch(choice){
			int size;
			//char *string_alloc;
			case 1:
				while(1){
					printf("What size would you like your string to be\n");
					scanf("%d", &size);
					if(tmp->size < size)
					{
						tmp->variable.string = malloc(size);
						tmp->size = size;
					}
					if(!tmp->variable.string){
						printf("Allocation failed Try again\n");
						sleep(1);
						continue;
					}
						break;
				}
				printf("What is your data\n");
				read(0, tmp->variable.string, tmp->size);
				tmp->type = 1;
				tmp->print = display_string;
				
				break;
			case 2:
				printf("What is your value:\n");
				scanf("%d", &tmp->variable.integer);
				tmp->type = 2;
				tmp->print = display_int;
				break;
			case 3:
				printf("What is your value:\n");
				scanf("%lld", &tmp->variable.long_boi);
				tmp->type = 3;
				tmp->print = display_long;
				break;
			case 4:
				printf("What is your value:\n");
				scanf(" %c", &tmp->variable.character);
				tmp->print = display_character;
				tmp->type = 4;
				break;
			default:
				puts("Bad choice");
				sleep(1);
				continue;		
		}
		break;
	}

}

void create(){
	struct created * tmp = calloc(1,sizeof(struct created));
	
	if (head == NULL){
		head = tmp;
	}
	else{
		struct created *walker = head;
		while(walker->next){
			walker = walker->next;
		}
		walker->next = tmp;
	}
	create_variable(tmp);
}

void edit(){
	struct created * walker = head;
	printf("What index would you like to modify?\n");
	int choice = 0;
	scanf("%d", &choice);
	int counter = 0;
	
	while(walker && counter != choice){
		counter++;
		walker = walker->next;
	}
	if(counter != choice || !walker)
	{
		puts("Index not found\n");
		sleep(1);
		return;
	}
	create_variable(walker);
	puts("Variable created");
	sleep(1);
}

void display(){
	struct created * walker = head;
	int counter = 0;
	while(walker){
		walker->print(walker);
		counter++;
		walker = walker->next;
	}
}

void win(){
	system("/bin/sh");
}

void delete(){
	puts("Not implemented");
	return;
}

void menu(){
	printf("What would you like to do?\n");
	puts("1. Create new object");
	puts("2. Display objects");
	puts("3. Edit Object");
	puts("4. Delete Object");
	puts("5. Exit");
}

int main(){
	int choice;
	setup();
	while(1){
		menu();
		scanf("%d", &choice);
		switch(choice){
			case 1:
				create();
				break;
			case 2:
				display();
				break;
			case 3:
				edit();
				break;
			case 4:
				delete();
				break;
			case 5:
				exit(0);	
				break;
			default:
				printf("Unkown command");
		}
	}
}

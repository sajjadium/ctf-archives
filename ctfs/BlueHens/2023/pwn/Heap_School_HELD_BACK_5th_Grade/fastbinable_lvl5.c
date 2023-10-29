#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


int *addresses[69];
int in_use[69];
int available_memory = 0x4a60;
int sizes[69];

int malloc_chunk() {
	int index;	
	int size = 0;
	puts("Index? ");
	scanf("%d",&index);
	getchar();

	puts("Size? ");
	scanf("%d",&size);
	getchar();	

        if ( (available_memory-size) < 0) {
                puts("Too much spaghetti (not enough memory try freeing some)!");
        	return 1;
        }
	
	if ((0 <= index) && (index <= 69)) {
                sizes[index] = size;
                available_memory = available_memory - sizes[index];
                addresses[index] = malloc(size);
                in_use[index] = addresses[index];
		printf("Only %p room enough for more spaghetti!\n",available_memory);
	} else {
		puts("Bad spaghetti!");
	}
	return 1;
}

void edit_chunk() {
	int index;
	puts("Index? ");
	scanf("%d",&index);
	getchar();
	if ((in_use[index]!=0x0) && (0 <= index) && (index <= 69)) {
		puts("Content? ");
		fgets(addresses[index],sizes[index]-1,stdin);
	} else {
		puts("Bad spaghetti!");
	}
}

void free_chunk() {
	int index;
	puts("Index? ");
	scanf("%d",&index);
	getchar();
	if ((0 <= index) && (index <= 69)) {
		available_memory = available_memory + sizes[index];
		free(addresses[index]);
		in_use[index] = 0x0;
		printf("%p room enough for more spaghetti!\n",available_memory);
	} else {
		puts("Bad spaghetti!");
	}	
}

void view_chunk() {
	int index;
	puts("Index? ");
	scanf("%d",&index);
	if ((0 <= index) && (index <= 69)) {
		puts(addresses[index]);
	} else {
		puts("Bad spaghetti!");
	}	
}

int main() {
	int choice;
	puts("Lose yourself in mom's spagettii\nFree hype music: https://www.youtube.com/watch?v=d1H-51INaPci\n");

	while (1) {
		printf("Menu: \t[1] Malloc spaghetti\n\t[2] Edit spaghetti\n\t[3] Free spaghetti\n\t[4] View spaghetti\n\t[5] Leave the spaghetti\nChoose an option:\n");
		scanf("%d",&choice);
		getchar();
		
		if (choice==1){
			malloc_chunk();
		} else if (choice==2){
			edit_chunk();
		} else if (choice==3){
			free_chunk();
		} else if (choice==4){	
			view_chunk();
		} else if (choice==5) {
			exit(0);
		} 
	}
}


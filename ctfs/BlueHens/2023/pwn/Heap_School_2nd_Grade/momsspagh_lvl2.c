#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


int *addresses[69];
int available_memory = 0x4a60;
int sizes[69];

// note all sizes fixed at 0x111
int size = 0x111;


int malloc_chunk() {
	int index;	
	puts("Index? ");
	scanf("%d",&index);
	getchar();
	
        if ( (available_memory-0x111) < 0) {
                puts("Too much spaghetti (not enough memory try freeing some)!");
        	return 1;
        }
	
	if ((0 <= index) && (index <= 69)) {
                sizes[index] = size;
                available_memory = available_memory - sizes[index];
                addresses[index] = malloc(size);
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
	if ((0 <= index) && (index <= 69)) {
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


#include <stdio.h>
#include <readline/readline.h>
#include <readline/history.h>

#include <stdlib.h>
#include <errno.h>

#define ARR_LEN 10


long int get_num(){
	long int num;

	if( (scanf("%ld",&num)) != 1){
		num = -1;
	}
	while ((getchar()) != '\n');
	return num;
}

long int *get_numbers(){
	/* we're in 2k19, we only want the big stuff */
	long int cnt, *data = 0, tmp;
	int ret = 0;
	
	/* Ask the user how many values he's going to enter */
	printf("How many values do you want to enter?\n>"); 
	cnt = get_num();
	
	/* Allocate some memory using calloc 
	cnt + 1 to also store the cnt in data[0] */
	data = calloc(cnt + 1, sizeof(*data));

	if (data == NULL){
		printf("No, no...");
		exit(0);
	}
	data[0] = cnt;
	
	/* Read from the user and store the values inside the allocated memory */
	for(int i=1; i < cnt + 1; i++){
		if( (tmp = get_num()) == -1){
			break;
		}
		data[i] = tmp;
	}
	return data;
}

void print_average(long int **data){
	int idx = 0;
	long int sum = 0;
	
	printf("average at which idx?\n>");
	idx = get_num();

	/* security */
	if(!(0 <= idx < ARR_LEN) || data[idx] == NULL){exit(0);}

	/* Sum up all values and divide them by the number of values */
	for(int i = 1; i < (data[idx][0] + 1); i++){
		sum += data[idx][i];	
	}
	
	printf("The average is: %lf\n",(double)sum / data[idx][0]);
}

void delete_numbers(long int ** numbers){
	int idx;
	
	printf("delete at which idx?\n>");
	idx = get_num();

	/* security */				
	if(0 <= idx < ARR_LEN && numbers[idx] != NULL){
		free(numbers[idx]);
		
		/* security! */
		numbers[idx] = NULL;
	} else {
		printf("Try harder, lil fella\n");
	}
}

void print_menu(){
	printf("------------------\n");
	printf("What do?\n");
	printf("1) get numbers\n");
	printf("2) print_average\n");
	printf("3) delete_numbers\n>");
}

int get_next_index(long ** numbers){
	for(int i = 0; i < ARR_LEN; i++){
		if(numbers[i] == NULL){
			return i;
		}
	} 
	return -1;
}

int main(){
	int slot;
	long int *data;
	long int **numbers = calloc(ARR_LEN,sizeof(**numbers));

	int num, ret;

    setvbuf( stdout , NULL , _IONBF , 0);

	for(int i=0; i < 50; i++){

		print_menu();
		num = get_num();		

		switch(num){
			case 1:
				slot = get_next_index(numbers);

				if(slot == -1){
					printf("delete first plox\n");
					break;
				}

				data = get_numbers();
				numbers[slot] = data;
				break;

			case 2:
				print_average(numbers);
				break;

			case 3:
				delete_numbers(numbers);
				break;
				
			default:
				break;
		}	
	}
	free(numbers);
}


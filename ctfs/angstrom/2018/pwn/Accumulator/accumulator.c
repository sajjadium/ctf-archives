#include <stdlib.h>
#include <stdio.h>

int main(){

	int accumulator = 0;
	int n;
	while (accumulator >= 0){
		printf("The accumulator currently has a value of %d.\n",accumulator);
		printf("Please enter a positive integer to add: ");

		if (scanf("%d",&n) != 1){
			printf("Error reading integer.\n");
		} else {
			if (n < 0){
				printf("You can't enter negatives!\n");
			} else {
				accumulator += n;
			}
		}
	}
	gid_t gid = getegid();
	setresgid(gid,gid,gid);
	
	printf("The accumulator has a value of %d. You win!\n", accumulator);
	system("/bin/cat flag");

}


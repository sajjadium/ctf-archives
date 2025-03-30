#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

int print_stack(uint8_t *stack, uint32_t size){
	
	printf("--- Print Stack ---\n");

    while(size !=  -1) {
        printf("0x%02x (%c)", stack[size], stack[size]);
		
		if(size <= 9) { 
			printf(" = username[%d]\n", size);
		} else if(size > 9 && size <= 13) {
			printf(" = is_admin[%d]\n", size - 10);
		} else {
			printf("\n");
		}
        size -= 1;
    }
	
	printf("--- End Print ---\n");
}

void print_flag(){
    FILE *fptr;
    char flag[35] = {0};

    fptr = fopen("flag.txt", "r");
    fread(flag, 1, 34, fptr);
    printf("Here is your flag! %s\n", flag);
    fclose(fptr);
}

int main(void) {

    bool is_admin = false;
    char username[10] = "XXXXXXXXXX"; // prefill buffer with X's
    char choice[2];
	
	printf("At it's most basic, a computer exploit is finding a loophole in a programs logic which can cause unintended behavior. In this program, we demonstrate how buffer overflows can corrupt local variables.\n\n");
	printf("To log into this system, please enter your name: ");

    scanf("%s", username);
    print_stack(&username, 13);
    printf("Hello, %s!\n", username);

    if(is_admin == true) {
        printf("%s is admin\n", username);
		printf("Because the program accepts more characters then it has space to hold, you are able to corrupt the is_admin boolean. And because in C, any Boolean value that isn't 0 is considered \"True\", it lets you through!\n");
    } else {
		printf("%s is not admin\n", username);
	}
	
	printf("Do you want to print the flag? (y/n) ");
	scanf("%1s", choice);
	
	if(choice[0] == 'y') {
		if(is_admin == false) {
			printf("You do not have the necessary access!\n");
			return 0;
		}
		
		print_flag();
	}
	
	printf("Exiting!\n");
	
    return 0;
}

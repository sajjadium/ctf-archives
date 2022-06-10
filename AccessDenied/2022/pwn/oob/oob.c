#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int arr[16];


void win(){
	system("cat flag.txt");
}

void main(){
	int index, value;
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    alarm(0x20);
    printf("Enter the index: ");
    scanf("%d", &index);
    printf("Enter the value: ");
    scanf("%d", &value);
    arr[index] = value;
    puts("good bye");
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void printFlag(int status){
	
	printf("Status Code: %d\n",status);
	
	char flag[50];
	FILE *flagFile;
	if ((flagFile = fopen("flag.txt","r")) == NULL) {
		printf("Error opening file.");
		return;
	}
	
	fscanf(flagFile, "%s", flag);
	printf("Here's a flag: %s\n", flag);
	
	_Exit(0);
}

void printCard(char name[]) {
	int nameLen = strlen(name);
	
	char *cardTop = malloc(300);
	strcpy(cardTop, "________________________________________\n");
	strcat(cardTop, "|                                      |\n");
	strcat(cardTop, "|                                      |\n");
	
	char *cardMid = malloc(140);
	strcpy(cardMid, "|  Dear ");
	strcat(cardMid, name);
	

	
	strcat(cardMid, ",");
	for (int i = 0; i < 30-nameLen; i++)
		strcat(cardMid, " ");
	strcat(cardMid, "|\n");
	char *cardBottom = malloc(300);
	strcpy(cardBottom, "");
	for (int i = 0; i < 17; i++)
		strcat(cardBottom, "|  __________________________________  |\n");
	strcat(cardBottom, "|______________________________________|\n");
	
	printf(cardTop);
	printf(cardMid);
	printf(cardBottom);

	return;
	
}


void main(int argc, char **argv) {

	char buf[100];
	memset(buf, 0 , 100);
	
	puts("Welcome to the personal letter program!");
	puts("Give us your name, and we will generate a letter just for you!");
	puts("Enter Name (100 Chars max): ");
	fgets(buf, 100, stdin);
	buf[strlen(buf)-1] = '\0';
	printCard(buf);
	puts("Exiting.\n");

	exit(0);
	
}

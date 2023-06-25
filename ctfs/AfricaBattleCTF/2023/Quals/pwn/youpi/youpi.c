// gcc -o youpi youpi.c
#include <stdio.h>
#include <stdlib.h>

int check = 0;

void youpiii(){
	
	if(check){
		char buffer[20];
		FILE * inputFile = fopen("flag.txt", "r" );
		if ( inputFile == NULL ) {
		    printf( "Cannot open file flag.txt\n" );
		    exit( -1 );
		}
		fgets( buffer, 65, inputFile );
		printf("FLAG: %s",buffer);
	}

}

void main(){

	puts("Welcome to Africa battleCTF.");
    puts("Tell us about your country: ");
    char buf[0x30];
    gets( buf ); 
}

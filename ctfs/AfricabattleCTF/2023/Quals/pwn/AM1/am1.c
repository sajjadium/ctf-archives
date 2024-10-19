//gcc -o am1 am1.c -no-pie
#include <stdio.h>
#include <stdlib.h>


void print_file(char * file)
{
	char buffer[20];
	FILE * inputFile = fopen( file, "r" );
	if ( inputFile == NULL ) {
        printf( "Cannot open file %s\n", file );
        exit( -1 );
    }
    fgets( buffer, 65, inputFile );
    printf("Output: %s",buffer);
}

int main(){


    puts("Welcome to Africa battleCTF.");
    puts("Tell us something about you: ");
    char buf[0x30];
    gets( buf );

    return 0;
}
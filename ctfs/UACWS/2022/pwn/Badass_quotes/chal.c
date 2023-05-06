#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    char term[64];
    char quote[32];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    memset(term, 0, 64);
	memset(quote, 0, 32);

    printf("\nI CaN HaS BaDaSs QuOtE?\n# ");
    gets(quote);

    if (strcmp(term, "BaDaSs I Am") == 0) {
        printf("\n");
        system("cat flag.txt");
    } else if(strlen(term) != 0) {    
	    printf("\nI haz a sad %s...\n\n", term);
    } else {
	    printf("\nI haz a sad...\n\n");
	}

	printf(" ,_     _\n");
	printf(" |\\_,-~/\n");
	printf(" / _  _ |    ,--.\n");
	printf("(  @  @ )   / ,-'\n");
	printf(" \  _T_/-._( (   \n");
	printf(" /         `. \  \n");
	printf("|         _  \ | \n");
	printf(" \ \ ,  /      | \n");
	printf("  || |-_\__   /  \n");
	printf(" ((_/`(____,-'   \n");
	
}

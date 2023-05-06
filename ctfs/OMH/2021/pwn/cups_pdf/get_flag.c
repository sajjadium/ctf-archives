#include <stdlib.h>
#include <stdio.h>

int main(void)
{
	FILE *fp = fopen("/flag", "r");
	char buffer[128];

	if(NULL == fp) {
		perror("fopen");
		return EXIT_FAILURE;
	}

	if(0 == fgets(buffer, sizeof(buffer), fp)) {
		perror("fgets");
		return EXIT_FAILURE;
	}

	puts(buffer);

	return EXIT_SUCCESS;
}

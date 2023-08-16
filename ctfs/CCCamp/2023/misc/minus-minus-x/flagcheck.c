#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <sys/param.h>

#ifndef FLAG
#define FLAG "ALLES!{testflag}"
#endif

bool test_flag(char *inp)
{
	bool res = true;
	int n = MIN(strlen(FLAG), strlen(inp));
	for (int i = 0; i <= n; i++)
		res &= FLAG[i] == inp[i];
	return res;
}

int main(int argc, char **argv)
{
	if (argc < 2)
	{
		printf("usage: flagcheck FLAG\n");
		return 1;
	}
	if (test_flag(argv[1]))
		printf("correct!\n");
	else
		printf("wrong :(\n");
}

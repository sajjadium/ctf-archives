#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "challenge.h"

uint64_t seed;

static void srand(uint64_t _seed)
{
	seed = _seed;
}

static void shuffle_seed(void)
{
	seed = ((seed << 0x20) & 0xffffffff00000000) | ((seed >> 0x20) & 0x00000000ffffffff);
	seed = ((seed << 0x10) & 0xffff0000ffff0000) | ((seed >> 0x10) & 0x0000ffff0000ffff);
}

static void shuffle_seed2(void)
{
	seed = seed ^ 0xdfa185f7ed9e179a;
}

static int rand()
{
	int ret = 0;

	shuffle_seed();
	shuffle_seed2();

	// thanks stackoverflow
	// https://stackoverflow.com/questions/1026327/what-common-algorithms-are-used-for-cs-rand
        seed = (seed * 0x343fd + 0x269ec3);
        ret = (seed >> 0x10) & 0x7FFFFFFF;

	shuffle_seed2();
	shuffle_seed();
	return ret;
}

int main()
{
	char * msg = MSG; // contains only ascii characters

	srand(TRUE_RANDOM_SEED_U64); // seed is 8 bytes from /dev/random
	for (int i = 0; i <= strlen(msg); i++)
	{
		printf("%c", msg[i] ^ rand());
	}
	return 0;
}

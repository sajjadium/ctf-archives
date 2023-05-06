#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>

#include "sha1.h"


static void
rand_str(char *buf, size_t len)
{
	char x[] =
		"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		"abcdefghijklmnopqrstuvwxyz"
		"0123456789";
	int i;

	srand(getpid());

	for (i=0; i<len-1; i++) {
		buf[i] = x[rand() % (sizeof(x)-1)];
	}
	buf[i] = '\0';
}


int
main(int argc, char *argv[])
{
	SHA1_CTX ctx;
	unsigned char goodhash[SHA1_DIGEST_SIZE];
	unsigned char userhash[SHA1_DIGEST_SIZE];
	unsigned char password[256];
	unsigned char salt[16];
	int n;

	assert(strlen(PASSWORD) <= 5);

	rand_str(salt, sizeof(salt));
	printf("Salt: %s\n", salt);
	fflush(stdout);

	SHA1_Init(&ctx);
	SHA1_Update(&ctx, salt, strlen(salt));
	SHA1_Update(&ctx, PASSWORD, strlen(PASSWORD));
	SHA1_Final(&ctx, goodhash);

	for (;;) {
		sleep(1);

		printf("Password: ");
		fflush(stdout);
		fgets(password, sizeof(password), stdin);
		if (password[strlen(password)-1] == '\n') password[strlen(password)-1] = '\0';
		if (password[strlen(password)-1] == '\r') password[strlen(password)-1] = '\0';

		SHA1_Init(&ctx);
		SHA1_Update(&ctx, salt, strlen(salt));
		SHA1_Update(&ctx, password, strlen(password));
		SHA1_Final(&ctx, userhash);

		n = memcmp(userhash, goodhash, sizeof(goodhash));

		if (n < 0) {
			printf("<\n");
			fflush(stdout);
		} else if (n > 0) {
			printf(">\n");
			fflush(stdout);
		} else {
			puts(FLAG);
			return EXIT_SUCCESS;
		}
	}

	return EXIT_FAILURE;
}

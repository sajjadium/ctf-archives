#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <time.h>

#include "sha1.h"


static void
rand_str(char *buf, size_t len)
{
	char x[] =
		"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		"abcdefghijklmnopqrstuvwxyz"
		"0123456789";
	int i;

	srand(getpid() ^ time(NULL));

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
	unsigned char goodpass[6];
	unsigned char userpass[256];
	unsigned char salt[16];
	int n;

	rand_str(goodpass, sizeof(goodpass));

	for (;;) {
		sleep(1);

		rand_str(salt, sizeof(salt));
		printf("Salt: %s\n", salt);
		fflush(stdout);

		SHA1_Init(&ctx);
		SHA1_Update(&ctx, salt, strlen(salt));
		SHA1_Update(&ctx, goodpass, strlen(goodpass));
		SHA1_Final(&ctx, goodhash);

		printf("Password: ");
		fflush(stdout);
		fgets(userpass, sizeof(userpass), stdin);
		if (userpass[strlen(userpass)-1] == '\n') userpass[strlen(userpass)-1] = '\0';
		if (userpass[strlen(userpass)-1] == '\r') userpass[strlen(userpass)-1] = '\0';

		SHA1_Init(&ctx);
		SHA1_Update(&ctx, salt, strlen(salt));
		SHA1_Update(&ctx, userpass, strlen(userpass));
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

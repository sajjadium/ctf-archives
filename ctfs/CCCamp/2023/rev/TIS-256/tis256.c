#include "asm.h"
#include "tpu.h"
#include "util.h"

#include <signal.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

static struct tis tis;
static FILE *tis_stdin = NULL;
static FILE *tis_stdout = NULL;

int (*cleanup)(void) = NULL;
const char *progname = "tis-as";

int
main(int argc, const char **argv)
{
	if (argc < 2 || argc > 4) {
		fprintf(stderr, "Usage: tis-as FILE [STDIN] [STDOUT]\n");
		exit(1);
	}

	if (argc >= 3) {
		tis_stdin = fopen(argv[2], "r");
		if (!tis_stdin) die("fopen '%s':", argv[2]);
	} else {
		tis_stdin = stdin;
	}
	setvbuf(tis_stdin, NULL, _IONBF, 0);

	if (argc >= 4) {
		tis_stdout = fopen(argv[3], "w+");
		if (!tis_stdout) die("fopen '%s':", argv[3]);
	} else {
		tis_stdout = stdout;
	}
	setvbuf(tis_stdout, NULL, _IONBF, 0);

	tis_init(&tis, NULL, NULL);

	tis_load(&tis, argv[1], tis_stdin, tis_stdout);

	while (tis_step(&tis));

	tis_deinit(&tis);

	fprintf(stderr, "steps: %lu\n", tis.steps);
}


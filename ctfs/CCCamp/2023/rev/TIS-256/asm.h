#pragma once

#include "tpu.h"

#include <stdio.h>

size_t asm_print_inst(char *buf, size_t n, struct tpu_inst *inst);
void tis_load(struct tis *tis, const char *filepath,
	FILE *tis_stdin, FILE *tis_stdout);

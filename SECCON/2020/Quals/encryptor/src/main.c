#include <argp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "encryptor.h"

#define FILE_SIZE 0x100

char secret[LEN_KEY];

struct Arguments {
  char path_i[LEN_PATH];
  char path_o[LEN_PATH];
};

static error_t parse_opt(int opt, char *arg, struct argp_state *state)
{
  struct Arguments *args = state->input;

  switch(opt) {
  case 'i':
    /* get input filepath */
    strcpy(args->path_i, arg);
    break;

  case 'o':
    /* get output filepath */
    strcpy(args->path_o, arg);
    break;

  default:
    return ARGP_ERR_UNKNOWN;
  }

  return 0;
}

static char doc[] = "encryptor -- AES-ECB-128 encryptor for SECCON CTF 2020";

static struct argp_option options[] = {
  {"input", 'i', "FILE", 0, "Read input from FILE instead of standard input"},
  {"output", 'o', "FILE", 0, "Write output to FILE instead of standard output"},
  { 0 }
};

static struct argp argp = {options, parse_opt, NULL, doc};

/**
 * Entry point
 */
int main(int argc, char **argv)
{
  int capacity, size, out_size;
  char *input, *output;
  FILE *fp_i, *fp_o;
  struct Arguments args;

  /* parse arguments */
  strcpy(args.path_i, "-");
  strcpy(args.path_o, "-");
  argp_parse(&argp, argc, argv, 0, 0, &args);

  if (strcmp(args.path_i, "-") == 0) {
    /* use stdin as input */
    fp_i = stdin;
  } else {
    /* use file as input */
    fp_i = fopen(args.path_i, "rb");
    if (fp_i == NULL) {
      fprintf(stderr, "No such file: %s\n", args.path_i);
      exit(1);
    }
  }

  if (strcmp(args.path_o, "-") == 0) {
    /* use stdout as output */
    fp_o = stdout;
  } else {
    /* use file as output */
    fp_o = fopen(args.path_o, "wb");
    if (fp_o == NULL) {
      fprintf(stderr, "Cannot write to file: %s\n", args.path_o);
      exit(1);
    }
  }

  /* read input */
  input = malloc(FILE_SIZE);
  capacity = FILE_SIZE;
  size = 0;
  while(!feof(fp_i)) {
    if (size >= capacity) {
      capacity <<= 1;
      input = realloc(input, capacity);
    }
    if (input == NULL) {
      fputs("Memory error\n", stderr);
      fclose(fp_i);
      free(input);
      exit(1);
    }
    size += fread(&input[size], 1, FILE_SIZE, fp_i);
  }

  /* encrypt */
  if ((out_size = encrypt(size, input, secret, &output)) <= 0) {
    fputs("Encryption failed\n", stderr);
    exit(1);
  } else {
    fwrite(output, 1, out_size, fp_o);
    free(output);
  }

  /* cleanup */
  fclose(fp_i);
  fclose(fp_o);
  free(input);
  return 0;
}

/**
 * Load key
 */
__attribute__((constructor))
void load_secret(void) {
  FILE *fp = fopen(PATH_KEY, "rb");
  if (fp) {
    if (fread(secret, 1, LEN_KEY, fp) != LEN_KEY) {
      fputs("[-] KEY must contain at least 16 bytes\n", stderr);
      exit(1);
    }
    fclose(fp);
  } else {
    fputs("[-] Key file not found.\n", stderr);
    exit(1);
  }
}

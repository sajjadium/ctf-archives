// gcc -o challenge challenge.c

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <stdbool.h>
#include <string.h>

bool load_password(char *password) {
  FILE *fp;
  if ((fp = fopen("password.txt", "r")) == NULL)
	return false;

  if (fread(password, 1, 15, fp) != 15)
	return false;

  password[15] = 0;
  fclose(fp);

  return true;
}

void print_flag() {
  FILE *fp = fopen("flag.txt", "r");
  if (fp == NULL)
	return;

  fseek(fp, 0, SEEK_END);
  long fsize = ftell(fp);
  fseek(fp, 0, SEEK_SET);

  char flag[fsize + 1];
  flag[fsize] = 0;

  fread(flag, 1, fsize, fp);
  puts(flag);

  fclose(fp);
}

int main() {
  char password[16];
  char accurate[16];

  if (!load_password(accurate))
	return 1;

  puts("Input password");
  fflush(stdout);
  gets(password);

  if (strcmp(password, accurate) == 0)
	print_flag();
  else
	puts("Sorry, incorrect password\n");
  fflush(stdout);
}

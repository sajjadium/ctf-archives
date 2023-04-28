#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

typedef struct {
  char name[0x100];
  int is_admin;
} auth_t;

auth_t get_auth(void) {
  auth_t user = { .is_admin = 0 };
  printf("Name: ");
  scanf("%s", user.name);
  return user;
}

int main() {
  char flag[0x100] = {};
  auth_t user = get_auth();

  if (user.is_admin) {
    puts("[+] Authentication successful.");
    FILE *fp = fopen("/flag.txt", "r");
    if (!fp) {
      puts("[!] Cannot open '/flag.txt'");
      return 1;
    }
    fread(flag, sizeof(char), sizeof(flag), fp);
    printf("Flag: %s\n", flag);
    fclose(fp);
    return 0;
  } else {
    puts("[-] Authentication failed.");
    return 1;
  }
}

__attribute__((constructor))
void setup(void) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(60);
}

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define KEY_LENGTH 16
#define USER_BUFFER 56
#define N 256
static unsigned char *canary;

void flag(){
  char buf[1024];
  FILE *f = fopen("flag.txt", "r");
  fgets(buf, 1024, f);
  printf("%s\n", buf);
}

void swap(unsigned char *a, unsigned char *b) {
  *a ^= *b;
  *b ^= *a;
  *a ^= *b;
}

void init_RC4_key(unsigned char *S, unsigned char *key){
  int i = 0, j = 0;

  for (i = 0; i < N; i++) {
    S[i] = i;
  }

  for (i = 0; i < N; i++){
    j = (j + S[i] + *(key + i % KEY_LENGTH)) % N;
    swap(&S[i], &S[j]);
  }
}

void RC4_encrypt(unsigned char *S, unsigned char *plaintext, unsigned char *ciphertext){
  int i = 0, j = 0, k = 0, n = 0;

  for (k = 0; k < KEY_LENGTH; k++){
    i = (i + 1) % N;
    j = (j + S[i]) % N;
    swap(&S[i], &S[j]);
    n = S[(S[i] + S[j]) % N];
    *(ciphertext + k) = *(plaintext + k) ^ n;
  }
}

unsigned char* get_random(){
  FILE *fptr = fopen("/dev/urandom", "r");
  unsigned char *random = malloc(KEY_LENGTH);
  fread(random, sizeof(char), KEY_LENGTH, fptr);
  fclose(fptr);
  return random;
}

void update_canary(unsigned char *S, unsigned char* buffer){
  unsigned char *plaintext = calloc(KEY_LENGTH, sizeof(unsigned char));
  unsigned char *ciphertext = calloc(KEY_LENGTH, sizeof(unsigned char));

  RC4_encrypt(S, plaintext, ciphertext);

  memcpy(canary, ciphertext, KEY_LENGTH);
  memcpy(&buffer[32], ciphertext, KEY_LENGTH);

  free(plaintext);
  free(ciphertext);
  plaintext = NULL;
  ciphertext = NULL;
}

int check_canary(unsigned char* buffer){
  for (int i = 0; i < KEY_LENGTH; i++){
    if (buffer[32 + i] != canary[i]){
      return 0;
    }
  }
  return 1;  
}

int check_flag(unsigned char* buffer){
  return buffer[48] == '2' && buffer[49] == '4' 
    && buffer[50] == '7' && buffer[51] == 'D' 
    && buffer[52] == 'U' && buffer[53] == 'C' 
    && buffer[54] == 'T' && buffer[55] == 'F';
}

void user_read(unsigned char *S, unsigned char* buffer){
  memset(buffer, 0, USER_BUFFER);
  update_canary(S, buffer);
  read(0, buffer, USER_BUFFER);
}

int main(int argc, char *argv[]) {
  setbuf(stdout, 0);
  canary = calloc(KEY_LENGTH, sizeof(unsigned char));
  unsigned char *key = get_random();
  unsigned char *buffer = calloc(USER_BUFFER, sizeof(unsigned char));
  unsigned char S[N];

  init_RC4_key(S, key);

  char banner[] = "Can you defeat the challenge canary and pull the flag from the mine?\n> ";
  char canary1[] = "   ___     ___     ___\n";
  char canary2[] = "  (o o)   (o o)   (o o)\n";
  char canary3[] = " (  V  ) (  V  ) (  V  )\n";
  char canary4[] = "/--m-m- /--m-m- /--m-m-\n";
  char canary5[] = "[chirp] No flag for you!\n> ";

  printf("%s", banner);
  while (1) {
    user_read(S, buffer);
    if (check_canary(buffer) && check_flag(buffer)){
      flag();
      exit(0);
    } else {
      printf("%s", canary1);
      printf("%s", canary2);
      printf("%s", canary3);
      printf("%s", canary4);
      printf("%s", canary5);
    }
  }
  
  free(buffer);
  free(key);
  free(canary);
}

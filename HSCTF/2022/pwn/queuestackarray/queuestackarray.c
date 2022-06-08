#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const char delim[2] = " ";

typedef struct Queuestack {
  char* cards[6];
  int head, tail;
} Queuestack;

void setup() {
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 2, 0);
}

void popleft(Queuestack* q) {
  if (q->head == q->tail) {
    puts("Queuestack is empty");
    return;
  }
  free(q->cards[q->head % 6]);
  q->head++;
}

void popright(Queuestack* q) {
  if (q->head == q->tail) {
    puts("Queuestack is empty");
    return;
  }
  free(q->cards[(q->tail-1) % 6]);
  q->tail--;
}


void pushleft(Queuestack* q, char* content) {
  if (q->tail - q->head >= 6) {
    popright(q);
  }
  int len = strlen(content);
  char* card = malloc(len+1);
  q->cards[(q->head - 1) % 6] = card;
  q->head--;
  strncpy(card, content, len);
  card[len] = '\0';
}

void pushright(Queuestack* q, char* content) {
  if (q->tail - q->head >= 6) {
    popleft(q);
  }
  int len = strlen(content);
  char* card = malloc(len+1);
  q->cards[(q->tail) % 6] = card;
  q->tail++;
  strncpy(card, content, len);
  card[len] = '\0';
}

/*
This is just the sort of needless complexity you have
come to expect from your inventory management system.
- Homestuck, page 970
*/
int main() {
  char input[80];
  Queuestack* queuestacks[4];
  char* token;
  setup();

  for (int i = 0; i < 4; i++) {
    queuestacks[i] = (Queuestack*) malloc(sizeof(Queuestack));
  }
    
  while (1) {
    printf("> ");
    fgets(input, 80, stdin);
    if (strlen(input) > 0) input[strlen(input)-1] = 0;
    token = strtok(input, delim);
    if (strncmp(token, "pushleft", 8) == 0) {
      int len = strlen(token);
      int num = token[8] - '1';
      if (num < 0 || num > 3) {
        puts("Queuestack number invalid (try pushleft1)");
        continue;
      }
      char* rest = token + len + 1;
      pushleft(queuestacks[num], rest);
    } else if (strncmp(token, "push", 4) == 0) {
      int len = strlen(token);
      int num = token[4] - '1';
      if (num < 0 || num > 3) {
        puts("Queuestack number invalid (try push1)");
        continue;
      }
      char* rest = token + len + 1;
      pushright(queuestacks[num], rest);
    } else if (strncmp(token, "popright", 8) == 0) {
      int num = token[8] - '1';
      if (num < 0 || num > 3) {
        puts("Queuestack number invalid (try popright1)");
        continue;
      }
      popright(queuestacks[num]);
    } else if (strncmp(token, "pop", 3) == 0) {
      int num = token[3] - '1';
      if (num < 0 || num > 3) {
        puts("Queuestack number invalid (try pop1)");
        continue;
      }
      popleft(queuestacks[num]);
    } else if (strncmp(token, "examine", 7) == 0) {
      int num = token[7] - '1';
      int ind = token[8] - '1';
      if (num < 0 || num > 3 || ind < 0 || ind > 6) {
        puts("Queuestack number invalid (try pop1)");
        continue;
      }
      puts(queuestacks[num]->cards[ind]);
    } else if (strcmp(token, "exit") == 0) {
      puts("goodbye.");
      break;
    } else {
      puts("command not recognized.");
    }
  }
  return 0;
}
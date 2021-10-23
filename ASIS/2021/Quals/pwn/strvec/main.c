#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
  int size;
  void *elements[0];
} vector;

void readline(const char *msg, char *buf, int length) {
  int i;

  printf("%s", msg);
  for (i = 0; i < length-1; i++) {
    if (read(0, &buf[i], 1) != 1 || buf[i] == '\n')
      break;
  }

  buf[i] = '\0';
}

int readint(const char *msg) {
  char buf[0x10] = {0};

  readline(msg, buf, sizeof(buf));
  return atoi(buf);
}

vector *vector_new(int nmemb) {
  if (nmemb <= 0)
    return NULL;

  int size = sizeof(vector) + sizeof(void*) * nmemb;
  vector *vec = (vector*)malloc(size);
  if (!vec)
    return NULL;

  memset(vec, 0, size);
  vec->size = nmemb;

  return vec;
}

void vector_delete(vector *vec) {
  for (int i = 0; i < vec->size; i++)
    free(vec->elements[i]);
  free(vec);
}

void* vector_get(vector *vec, int idx) {
  if (idx < 0 || idx > vec->size)
    return NULL;
  return vec->elements[idx];
}

int vector_set(vector *vec, int idx, void *ptr) {
  if (idx < 0 || idx > vec->size)
    return -1;
  if (vec->elements[idx])
    free(vec->elements[idx]);
  vec->elements[idx] = ptr;
  return 0;
}

int main()
{
  char name[0x10];
  readline("Name: ", name, sizeof(name));
  printf("Hello, %s!\n", name);

  int n = readint("n = ");
  vector *vec = vector_new(n);
  if (!vec)
    return 1;

  while (1) {
    int choice = readint("1. get\n2. set\n> ");

    switch (choice) {
    case 1: {
      int idx = readint("idx = ");
      char *data = (char*)vector_get(vec, idx);
      printf("vec.get(idx) -> %s\n", data ? data : "[undefined]");
      break;
    }

    case 2: {
      int idx = readint("idx = ");
      char *data = (char*)malloc(0x20);
      if (!data)
        break;
      readline("data = ", data, 0x20);

      int result = vector_set(vec, idx, (void*)data);
      printf("vec.set(idx, data) -> %d\n", result);
      if (result == -1)
        free(data);
      break;
    }

    default:
      vector_delete(vec);
      printf("Bye, %s!\n", name);
      return 0;
    }
  }
}

__attribute__((constructor))
void setup(void) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(180);
}

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define ARRAY_SIZE(n) (n * sizeof(long))
#define ARRAY_NEW(n) (long*)alloca(ARRAY_SIZE(n + 1))

int main() {
  long size, index, *arr;

  printf("size: ");
  if (scanf("%ld", &size) != 1 || size < 0 || size > 5)
    exit(0);

  arr = ARRAY_NEW(size);
  while (1) {
    printf("index: ");
    if (scanf("%ld", &index) != 1 || index < 0 || index >= size)
      exit(0);

    printf("value: ");
    scanf("%ld", &arr[index]);
  }
}

__attribute__((constructor))
void setup(void) {
  alarm(180);
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
}

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void Setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

#define SYMBOLS "ABCDEF"

__attribute__((used, hot, noinline))
void Flag() {
  system("/bin/sh");
}

void GenerateGreeting(
  char patternSymbol,
  int patternCount
) {
  char output[2312] = { 0 };
  int outputCursor = 0;
  for (int i = 0; i < patternCount; i += 1) {
    output[outputCursor++] = patternSymbol;
  }
  output[outputCursor++] = '\n';

  printf("enter greeting: \n");
  outputCursor += read(0, &output[outputCursor], 128);

  for (int i = 0; i < patternCount; i += 1) {
    output[outputCursor++] = patternSymbol;
  }
  output[outputCursor++] = '\n';

  printf("%s\n", output);
}

int main() {
  Setup();

  printf("enter pattern character: \n");
  char patternSymbol;
  scanf("%c", &patternSymbol);
  getchar();
  
  printf("enter number of symbols: \n");
  char numberString[512];
  int readAmount = read(0, numberString, sizeof(numberString) - 1);
  numberString[readAmount] = '\0';

  int mappings[sizeof(SYMBOLS)] = { 0 };
  for (int i = 0; i < readAmount; i += 1) {
    char current = numberString[i];
    int index = 0;
    for (const auto symbol: SYMBOLS) {
      if (current == symbol) {
        mappings[index] += 1;
      }
      index += 1;
    }
  }

  int patternCount = 0;
  int power = 1;
  for (int i = 0; i < sizeof(SYMBOLS); ++i) {
    if (mappings[i] > 3) {
      abort();
    }
    patternCount += power * mappings[i];
    power *= 3;
  }

  GenerateGreeting(patternSymbol, patternCount);
}

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv)
{
  int water;
  char bottle[125];

  water = 0;
  printf("Fill the water bottle kid!");
  gets(bottle);

  if(water != 0) {
      system("cat gift.txt");
  } else {
      printf("You are crazy lazy!:)\n");
  }
}

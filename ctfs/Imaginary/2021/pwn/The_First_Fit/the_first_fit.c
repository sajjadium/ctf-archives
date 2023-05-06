#include <stdio.h>
#include <stdlib.h>

int main()
{
  int choice, choice2;
  char *a = malloc(128);
  char *b;
  setvbuf(stdout,NULL,2,0);
  setvbuf(stdin,NULL,2,0);
  while (1) {
    printf("a is at %p\n", a);
    printf("b is at %p\n", b);
    printf("1: Malloc\n2: Free\n3: Fill a\n4: System b\n> ");
    scanf("%d", &choice);
    switch(choice) {
      case 1:
              printf("What do I malloc?\n(1) a\n(2) b\n>> ");
              scanf("%d", &choice2);
              if (choice2 == 1)
                a = malloc(128);
              else if (choice2 == 2)
                b = malloc(128);
              break;
      case 2:
              printf("What do I free?\n(1) a\n(2) b\n>> ");
              scanf("%d", &choice2);
              if (choice2 == 1)
                free(a);
              else if (choice2 == 2)
                free(b);
              break;
      case 3: printf(">> "); scanf("%8s", a); break;
      case 4: system((char*)b); break;
      default: return -1;
    }
  }
  return 0;
}

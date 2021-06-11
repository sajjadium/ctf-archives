#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <malloc.h>

void __attribute((constructor)) setup()
{
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  alarm(0x30);
}

char *strings[0x10] = {0};
size_t sizes[0x10];

void menu()
{
  puts("1) add\n2) show\n3) remove\n4) edit\n5) exit");
  printf("> ");
}

void add();
void show();
void delete();
void edit();

int main()
{ 
  int choice;
  while(1)
  {
    menu();
    scanf("%d", &choice);
    switch(choice)
    {
    case 1:
      add();
      break;
    case 2:
      show();
      break;
    case 3:
      delete();
      break;
    case 4:
      edit();
      break;
    case 5:
      exit(0);
    default:
      puts("Invalid choice... Try Again");
    }
  }
}

void add()
{ 
  int size;
  int idx;
  printf("enter size: ");
  scanf("%d", &size);
  printf("enter idx: ");
  scanf("%d", &idx);
  assert(idx >= 0 && idx<0x10);
  strings[idx] = malloc(size);
  printf("Enter your message: ");
  read(0, strings[idx], size-1);
  sizes[idx] = size;
}

void show()
{
  int idx;
  printf("idx: ");
  scanf("%d", &idx);
  printf("[%d] %s\n",idx, strings[idx]);
}

void delete()
{
  int idx;
  printf("Enter idx: ");
  scanf("%d", &idx);
  assert(idx >= 0 && idx < 0x10);
  free(strings[idx]);
}

void edit()
{
  int idx;
  printf("Enter idx: ");
  scanf("%d", &idx);
  assert(idx >= 0 && idx < 0x10);
  printf("Enter your message: ");
  read(0, strings[idx], sizes[idx]);
}

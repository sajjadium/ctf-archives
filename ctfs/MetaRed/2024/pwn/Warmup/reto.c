// gcc -Wall -fno-stack-protector -z execstack -no-pie -o reto reto.c
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>
 
int main()
{
 
  int var;
  int check = 0x12345678;
  char buf[20];
 
  fgets(buf,45,stdin);
 
  printf("\n[buf]: %s\n", buf);
  printf("[check] %p\n", check);
 
  if ((check != 0x12345678) && (check != 0x54524543))
    printf ("\nClooosse!\n");
 
  if (check == 0x54524543)
   {
     printf("Yeah!! You win!\n");
     setreuid(geteuid(), geteuid());
     system("/bin/bash");
     printf("Byee!\n");
   }
   return 0;
}


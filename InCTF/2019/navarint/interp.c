#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "global.h"
#include "tokens.h"
#include "parser.h"
// #include "vm.h"



void initialise(int argc, char const *argv[])
{
  int i,fd;

  argc--;
  argv++;
  poolsize=1024;
  scope = &symtab;

  if (argc == 1)
  {
    SOURCE = 1;
  }

  if (SOURCE)
  {
    if ((fd=open(*argv,0))<0)
    {
      die("open");
    }
    if ((old_src=src=(char*)malloc(poolsize))<0)
    {
      die("malloc");
    }

    if ((i=read(fd,src,poolsize-1))<0)
    {
      die("read");
    }

    if (!(old_text=text=(long*)malloc(poolsize)))
    {
      die("malloc");
    }
  }

  if (!(stack=(val*)malloc(poolsize)))
  {
    die("malloc");
  }

  if (!(call_stack=(long*)malloc(poolsize)))
  {
    die("malloc");
  }

  if (!(data=(char*)malloc(poolsize)))
  {
    die("malloc");
  }

  memset(stack,0,poolsize);
  memset(call_stack,0,poolsize);
  memset(data,0,poolsize);

  if (SOURCE)
  {
    // But reading from source file is still not supported :(
    memset(text,0,poolsize);
    orig=text;
    text=text-1;
    src[i]='\0';
    close(fd);
  }

  sp = bp = (val*)((long)stack+poolsize);
  cs_sp = cs_bp = (long*)((long)call_stack+poolsize);
  ax.type = 0;
  ax.data = 0;
  pc = 0;

  char* tmp = src;
  src = "func else enum if return sizeof while open read close printf malloc memset memcmp\0";
  i = Func;
  while (i<=While)
  {
    next();
    cur->tok = i;
    i++;
  }
  i=OPEN;
  while (i<=MCMP)
  {
    next();
    cur->class = Sys;
    // cur->value = NULL;
    // cur->tok = Id;
    i++;
  }
  src=tmp;

  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

}
void print_banner()
{
  char* tail = (char*)malloc(0x10);
  memset(tail, '*', 0x10);
  for (int i=0;i<5;i++)
  printf("%s",tail);
  puts("");
  puts(welcome_str);
  for (int i=0;i<5;i++)
  printf("%s",tail);
  puts("");
  puts("");
  free(tail);
}

int main(int argc, char const *argv[])
{
  initialise(argc,argv);
  print_banner();
  program();
  return 0;
}

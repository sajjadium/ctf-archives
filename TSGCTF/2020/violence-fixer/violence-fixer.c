#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>

#define MAXSIZE 0x200
#define ENTS 0x18

typedef enum{
  NOINUSE = 0,
  INUSE = 1,
} USEFLAG;

struct heapinfo{
  unsigned long size;
  unsigned long required_size;
  USEFLAG inuse;
  void *addr;
};

struct heapinfo infos[ENTS];
void *top;
unsigned long top_size;
char beginner = 0;
char useonce = 0;

unsigned long getlong(void)
{
  unsigned int rsize;
  char buf[0x20];
  rsize = read(0,buf,0x20-1);
  buf[rsize] = NULL;
  return strtoull(buf,NULL,10);
}

void menu(void)
{
  printf("\n");
  printf("1: Alloc\n");
  printf("2: Show\n");
  printf("3: Free\n");
  if(beginner==1)
    printf("4: assumption\n");
  printf("0: Delegate your right (only once, not recommended!)\n");
  printf("> ");
}

// Allocate heap and register heap information.
unsigned reg_heap(unsigned long size, int delegate_flag)
{
  unsigned index = -1;

  for(int ix=0;ix!=ENTS;++ix){
    if(infos[ix].inuse == NOINUSE){
      index = ix;
      break; 
    }
  }
  if(index == -1){
    printf("too much entries.\n");
    exit(0);
  }

  infos[index].inuse = INUSE;
  infos[index].required_size = size;
  infos[index].size = ((size + 0x10)>>4)<<4;
  if(delegate_flag!=1){
    malloc(infos[index].size-0x10);
    infos[index].addr = top; 
    *(unsigned long*)(infos[index].addr+8) = infos[index].size|1;
  }else{
    // I don't want to rely on arena...
    infos[index].addr = malloc(infos[index].size-0x10) - 0x10;
  }
  top += infos[index].size;
  return index;
}

// Get content from stdin.
void get_content(unsigned index)
{
  unsigned size;

  size = infos[index].required_size;
  if(read(0,infos[index].addr+0x10,size) <= 0){
    printf("error while reading.\n");
    exit(0);
  }
}

unsigned long get_size(void)
{
  unsigned long size;

  size = getlong();
  if(size<1 || MAXSIZE<size){
    printf("too big.\n");
    exit(0);
  }
  return size;
}

void _alloc(void)
{
  unsigned long size;
  unsigned index;

  printf("size: ");
  size = get_size();
  index = reg_heap(size,0);
  printf("content: ");
  get_content(index);
}

void _show(void)
{
  unsigned index;

  printf("index: ");
  index = getlong();
  if(index < 0 || ENTS <= index){
    printf("invalid index\n");
    exit(0);
  }
  if(infos[index].inuse == NOINUSE){
    printf("No entry.\n");
    return;
  }
  printf("%s\n",infos[index].addr+0x10);
}

void _free(void)
{
  unsigned index;

  printf("index: ");
  index = getlong();
  if(index < 0 || ENTS <= index){
    printf("invalid index\n");
    exit(0);
  }
  if(infos[index].inuse == NOINUSE){
    printf("No entry.\n");
    return;
  }
  free(infos[index].addr+0x10);
  top -= infos[index].size;
  infos[index].inuse = NOINUSE;
}

void init(void)
{
  void *indicator;

  // set buffer
  setvbuf(stdout,NULL,_IONBF,0);
  setvbuf(stdin,NULL,_IONBF,0);
  setvbuf(stderr,NULL,_IONBF,0);

  // init heapinfos 
  for(int ix=0;ix!=ENTS;++ix){
    infos[ix].inuse = NOINUSE;
    infos[ix].addr = NULL;
    infos[ix].size = 0;
  }

  // get heapaddr
  indicator = malloc(0x10);
  top = indicator + 0x20 -0x10;
  top_size = *(unsigned long*)(top+0x8);

  // ask
  printf("Are you beginner?: ");
  if(getchar() == 'y')
    beginner = 1;
  getchar();
}

// Print chunk information.
void print_chunk(unsigned index)
{
  printf("%p : 0x%lx\n",infos[index].addr,infos[index],index);
  printf(" size: 0x%lx\n",infos[index].size+1);
  if(infos[index].inuse == INUSE){
    printf(" INUSE\n\n");
  }else{
    printf(" NOT INUSE\n");
  }
}

// Just for beginners.
void _assumption()
{
  printf("Assumed Heap\n");
  printf("-------------------------\n");
  for(int ix=0;ix!=ENTS;++ix){
    if(infos[ix].addr != NULL)
      print_chunk(ix);
  }
  printf("top = %p\n",top);
}

// Delegate your right to manage heap by your self.
void delegate(void)
{
  if(useonce != 0){
    exit(0);
  }

  printf("\nDelegating your rights would collapse everything,\n");
  printf("Because my program is perfect.\n");
  printf("Your really want to delegate malloc rihgt to arena???");
  printf("> ");

  if(getchar() == 'y'){
    getchar();
    useonce = 1;    
    unsigned long size;
    unsigned index;

    printf("size: ");
    size = get_size();
    index = reg_heap(size,1);
    printf("content: ");
    get_content(index);
  }else{
    getchar();
    printf("I think it's good. No need the help of arena!\n");
  }
}

int main(int argc,char *argv[])
{
  long user_choice;
  init();

  while(1==1){
    menu();
    user_choice = getlong();
    switch(user_choice){
      case 1:
        _alloc();
        break;
      case 2:
        _show();
        break;
      case 3:
        _free();
        break;
      case 4:
        if(beginner == 0)
          return 0;
        _assumption();
        break;
      case 0:
        delegate();
        break;
      default:
        return 0;
    }
  }
}

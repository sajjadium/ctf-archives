#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <seccomp.h>
#include <sys/mman.h>

#define MAX_NOTES 20

void filter(unsigned long start, unsigned long end){
  scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
  if (!ctx) {
      return ;
  }

  if (seccomp_rule_add(ctx, SCMP_ACT_KILL_PROCESS, SCMP_SYS(read), 1,
      SCMP_CMP(1, SCMP_CMP_LT, start)) < 0) {
      return ;
  }

  if (seccomp_rule_add(ctx, SCMP_ACT_KILL_PROCESS, SCMP_SYS(read), 1,
      SCMP_CMP(1, SCMP_CMP_GE, end)) < 0) {
      return ;
  }
  
  if (seccomp_rule_add(ctx, SCMP_ACT_KILL_PROCESS, SCMP_SYS(write), 1,
      SCMP_CMP(1, SCMP_CMP_LT, start)) < 0) {
      return ;
  }

  if (seccomp_rule_add(ctx, SCMP_ACT_KILL_PROCESS, SCMP_SYS(write), 1,
      SCMP_CMP(1, SCMP_CMP_GE, end)) < 0) {
      return ;
  }
  
  if (seccomp_load(ctx) < 0) {
      return ;
  }

  seccomp_release(ctx);
}

char *num;
char *notes[MAX_NOTES];
int sizes[MAX_NOTES];
char *phrases[4];

unsigned long read_num(){
  read(0,num,0x1f);
  return atoll(num);
}

void create(){
  write(1,phrases[0],strlen(phrases[0]));
  unsigned long idx=read_num();
  if(idx>=MAX_NOTES)exit(0);
  write(1,phrases[1],strlen(phrases[1]));
  unsigned long sz=read_num();
  if(sz>=0x1000)exit(0);
  notes[idx]=malloc(sz);
  unsigned long *ptr=0x1337000;
  if(notes[idx]<ptr[0] || notes[idx]>=ptr[1])exit(0); 
  sizes[idx]=sz;
}

void edit(){
  write(1,phrases[0],strlen(phrases[0]));
  unsigned int idx=read_num();
  if(idx>=MAX_NOTES)exit(0);
  write(1,phrases[2],strlen(phrases[2]));
  read(0,notes[idx],sizes[idx]);
}

void delete(){
  write(1,phrases[0],strlen(phrases[0]));
  unsigned int idx=read_num();
  if(idx>=MAX_NOTES)exit(0);
  free(notes[idx]);
}

void show(){
  write(1,phrases[0],strlen(phrases[0]));
  unsigned int idx=read_num();
  if(idx>=MAX_NOTES)exit(0);
  write(1,notes[idx],sizes[idx]);
}

int main(){
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  phrases[0]=strdup("Enter index: \n");
  phrases[1]=strdup("Enter size: \n");
  phrases[2]=strdup("Enter data: \n");
  phrases[3]=strdup("Which option do you choose? \n");
  
  
  FILE* maps = fopen("/proc/self/maps", "r");
  if (!maps) {
      perror("fopen");
      return 1;
  }

  char line[256];
  unsigned long start, end;
  while (fgets(line, sizeof(line), maps)) {
      if (strstr(line, "[heap]")) {
          sscanf(line, "%lx-%lx", &start, &end);
          break;
      }
  }
  fclose(maps);
  
  filter(start,end);
  
  unsigned long *ptr=0x1337000;
  mmap((void *)0x1337000, 0x1000,
                      PROT_READ | PROT_WRITE | PROT_EXEC,
                      MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED,
                      -1, 0);
  
  ptr[0]=start;
  ptr[1]=end;
  mprotect(0x1337000,0x1000,1);
  
  num=malloc(0x20);
  
  while(1){
    write(1,phrases[3],strlen(phrases[3]));
    int option=read_num();
    if(option==1)create();
    if(option==2)edit();
    if(option==3)delete();
    if(option==4)show();
  }
  
  
  return 0;
  
}

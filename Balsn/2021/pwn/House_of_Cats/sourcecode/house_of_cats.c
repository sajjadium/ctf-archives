/* gcc -Wl,-z,now -fpie -fstack-protector-all house_of_cats.c -o house_of_cats */
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<time.h>
#include"SECCOMP.h"

#define MAXSIZE 0x38
#define MINSIZE 0x08
#define MAXENTRY 0x2
#define CATSIZE(x) (x+4)

struct sock_filter seccompfilter[]={
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, ArchField),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, SyscallNum),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_read, 1, 0),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_write, 0, 3),
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, SyscallArg(2)),
  BPF_JUMP(BPF_JMP | BPF_JGT | BPF_K, 0x1e8, 1, 0),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, SyscallNum),
  Allow(open),
  Allow(mprotect),
  Allow(brk),
  Allow(exit),
  Allow(exit_group),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
};

struct sock_fprog filterprog={
  .len=sizeof(seccompfilter)/sizeof(struct sock_filter),
  .filter=seccompfilter
};

typedef struct Cat{
  unsigned int ID;
  char name[MINSIZE];
}CAT;

CAT *CatList[MAXENTRY]={NULL};
int CatExist[MAXENTRY]={0};

void apply_seccomp(){
  if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)){
    perror("Seccomp Error");
    _exit(1);
  }
  if(prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&filterprog)==-1){
    perror("Seccomp Error");
    _exit(1);
  }
  return;
}

void initproc(){
  srand(time(NULL));
  setvbuf(stdin,NULL,_IONBF,0);
  setvbuf(stdout,NULL,_IONBF,0);
  apply_seccomp();
  return;
}

void largebinCheck(){
  size_t *largebin = (size_t*)((size_t)(stdin)+0x650);
  for(int i=0;i<63;i++){
    if((largebin!=(size_t*)(largebin[2]))||(largebin!=(size_t*)(largebin[3]))){
      puts("House Security Check Failed");
      _exit(0);
    }
    largebin=(size_t*)((size_t)largebin+0x10);
  }
  return;
}

void printnum(unsigned int num){
  char buf[0x10];
  memset(buf,0,0x10);
  int cursor = 0xf;
  do{
    buf[cursor]='0'+num%10;
    num/=10;
    cursor--;
  }while(num>0);
  write(STDOUT_FILENO,&(buf[cursor+1]),0x10-(cursor+1));
  return;
}

void printstr(char *buf){
  write(STDOUT_FILENO,buf,strlen(buf));
  return;
}

void readstr(char *buf,int length){
  read(STDIN_FILENO,buf,length);
  return;
}

int menu(){
  puts("🐈  🐈  🐈  🐈  🐈  🐈  🐈  🐈  🐈  🐈");
  puts("🐈       House of Cats      🐈");
  puts("🐈  🐈  🐈  🐈  🐈  🐈  🐈  🐈  🐈  🐈");
  puts("🐈   1. Rescue Leopard cat  🐈");
  puts("🐈   2. Show Leopard cat    🐈");
  puts("🐈   3. Release Leopard cat 🐈");
  puts("🐈   4. Exit                🐈");
  puts("🐈  🐈  🐈  🐈  🐈  🐈  🐈  🐈  🐈  🐈");
  printstr("choice : ");
  int choice=0;
  scanf("%x",&choice);
  return choice;
}

void rescueCat(){
  int idx;
  for(idx=0;idx<MAXENTRY;idx++)
    if(CatExist[idx]==0)
      break;
  if(idx==MAXENTRY){
    puts("No more space for another Leopard cat QAQ");
    _exit(0);
  }
  printstr("Cat name length : ");
  unsigned int namelen=0;
  scanf("%x",&namelen);
  if(CATSIZE(namelen)<MINSIZE || CATSIZE(namelen)>MAXSIZE){
    puts("Invalid name length");
    return;
  }
  CatList[idx] = calloc(1,CATSIZE(namelen));
  if(CatList[idx]==NULL){
    puts("Failed to rescue Leopard cat QAQ");
    _exit(1);
  }
  CatList[idx]->ID = rand();
  printstr("Cat name : ");
  readstr(CatList[idx]->name,namelen);
  CatExist[idx] = 1;
  return;
}

void showCat(){
  printstr("Cat index : ");
  unsigned int idx=0;
  scanf("%x",&idx);
  if(idx<0 || idx>=MAXENTRY || CatExist[idx]==0){
    puts("Cat doesn't exist");
    return;
  }
  printstr("🐈   ID : ");
  printnum(CatList[idx]->ID);
  printstr("\n🐈   Name : ");
  printstr(CatList[idx]->name);
  printstr("\n");
  return;
}

void releaseCat(){
  printstr("Cat index : ");
  unsigned int idx=0;
  scanf("%x",&idx);
  if(idx<0 || idx>=MAXENTRY){
    puts("Cat doesn't exist");
    return;
  }
  free(CatList[idx]);
  CatExist[idx] = 0;
  return;
}

int main(){
  int choice;
  initproc();
  while(1){
    switch(menu()){
      case 1:
        rescueCat();
        break;
      case 2:
        showCat();
        break;
      case 3:
        releaseCat();
        break;
      case 4:
        puts("Bye");
        _exit(0);
      default:
        puts("Invalid Choice");
        break;
    }
    largebinCheck();
  }
  return 0;
}

/*gcc -Wl,-z,now -fpie -fstack-protector-all STACK.c -o STACK*/
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include"SECCOMP.h"

#define MAXTODO 200
#define MAXHISTORY 2
#define TASKNAME_MAXLEN 0x48
#define TODO_MAXLEN 20

typedef struct Task{
  unsigned long long int isfinished;
  unsigned long long int estimatedtime;
  char *todos[MAXTODO];
  char taskname[TASKNAME_MAXLEN];
}TASK;

typedef struct Journal{
  unsigned long long int notask;
  unsigned long long int mostrecent;
  char *archive[MAXHISTORY];
  TASK currenttask;
}JOURNAL;

JOURNAL *myjournal;

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
  Allow(rt_sigreturn),
  Allow(brk),
  Allow(exit),
  Allow(clock_nanosleep),
  Allow(exit_group),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
};

struct sock_fprog filterprog={
  .len=sizeof(seccompfilter)/sizeof(struct sock_filter),
  .filter=seccompfilter
};

void apply_seccomp(){
  if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)){
    perror("Seccomp Error");
    exit(1);
  }
  if(prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&filterprog)==-1){
    perror("Seccomp Error");
    exit(1);
  }
  return;
}

void printerror(char *msg){
  puts(msg);
  exit(1);
}

void* securemalloc(size_t size){
  void *ptr = malloc(size);
  void *programbrk = sbrk(0);
  if(programbrk==(void*)-1 || ptr>=programbrk || ptr==NULL)
    printerror("malloc error");
  return ptr;
}

void securefree(void *ptr){
  void *programbrk = sbrk(0);
  if(programbrk==(void*)-1 || ptr>=programbrk)
    printerror("free error");
  free(ptr);
  return;
}

void printnum(unsigned int num, int length){
  char buf[0x10];
  memset(buf,0,0x10);
  int cursor = 0xf;
  do{
    buf[cursor]='0'+num%10;
    num/=10;
    cursor--;
  }while(num>0);
  if(length!=-1 && length+cursor-0xf>0)
    write(STDOUT_FILENO,"                ",length+cursor-0xf);
  write(STDOUT_FILENO,&(buf[cursor+1]),0x10-(cursor+1));
  return;
}

void printstr(char *buf){
  write(STDOUT_FILENO,buf,strlen(buf));
  return;
}

JOURNAL* newJournal(){
  JOURNAL *journal = securemalloc(sizeof(JOURNAL));
  journal->notask = 1;
  journal->mostrecent = 0;
  for(int i=0;i<MAXHISTORY;i++)
    journal->archive[i]=NULL;
  journal->currenttask.isfinished=1;
  journal->currenttask.estimatedtime=0;
  for(int i=0;i<MAXTODO;i++)
    journal->currenttask.todos[i]=NULL;
  memset(journal->currenttask.taskname,0,TASKNAME_MAXLEN);
  return journal;
}

void init_proc(){
  setvbuf(stdin,NULL,_IONBF,0);
  setvbuf(stdout,NULL,_IONBF,0);
  apply_seccomp();
  myjournal = newJournal();
  return;
}

void archiveTask(){
  if(myjournal->archive[myjournal->mostrecent]!=NULL)
    securefree(myjournal->archive[myjournal->mostrecent]);
  myjournal->archive[myjournal->mostrecent] = securemalloc(TASKNAME_MAXLEN);
  int length = strlen(myjournal->currenttask.taskname);
  if(length>TASKNAME_MAXLEN-1)
    length = TASKNAME_MAXLEN-1;
  memcpy(myjournal->archive[myjournal->mostrecent],myjournal->currenttask.taskname,length);
  myjournal->archive[myjournal->mostrecent][length] = '\0';
  myjournal->mostrecent = (myjournal->mostrecent+1)%MAXHISTORY;
  return;
}

void newTask(){
  if(myjournal->currenttask.isfinished==0){
    puts("Finish the current task before starting a new one");
    return;
  }
  if(myjournal->notask==0)
    archiveTask();
  else
    myjournal->notask=0;
  printstr("Please provide estimated time to finish and name of task (time,name) : ");
  if(scanf("%u,%72s",&myjournal->currenttask.estimatedtime,myjournal->currenttask.taskname)!=2)
    printerror("scanf error");
  myjournal->currenttask.isfinished = 0;
  return;
}

void assignTodo(){
  if(myjournal->currenttask.isfinished==1){
    puts("Create task before assigning todos");
    return;
  }
  unsigned int todoidx=0;
  printstr("TODO ID : ");
  if(scanf("%u",&todoidx)!=1)
    printerror("scanf error");
  if(todoidx<0 || todoidx>=MAXTODO){
    puts("Invalid ID");
    return;
  }
  if(myjournal->currenttask.todos[todoidx]!=NULL){
    printstr("TODO ");
    printnum(todoidx,-1);
    printstr(" is already assigned\n");
    return;
  }
  printstr("TODO ");
  printnum(todoidx,-1);
  printstr(" : ");
  myjournal->currenttask.todos[todoidx] = securemalloc(TODO_MAXLEN);
  if(scanf("%20s",myjournal->currenttask.todos[todoidx])!=1)
    printerror("scanf error");
  return; 
}

void finishTask(){
  if(myjournal->currenttask.isfinished==1){
    puts("No pending task.");
    return;
  }
  printstr("Finishing Task : ");
  printstr(myjournal->currenttask.taskname);
  printstr("\n    TODO(s) : \n");
  for(int i=0;i<MAXTODO;i++){
    if(myjournal->currenttask.todos[i]!=NULL){
      printstr("        ");
      printnum(i,3);
      printstr(") ");
      printstr(myjournal->currenttask.todos[i]);
      printstr("\n");
      securefree(myjournal->currenttask.todos[i]);
      myjournal->currenttask.todos[i] = NULL;
    }
  }
  sleep(myjournal->currenttask.estimatedtime);
  puts("All Done...\n");
  myjournal->currenttask.isfinished = 1;
  return;
}

void showTaskHistory(){
  if(myjournal->notask==1){
    puts("No task created yet");
    return;
  }
  int firstexist;
  for(firstexist = 0;firstexist<MAXHISTORY;firstexist++)
    if(myjournal->archive[(myjournal->mostrecent+firstexist)%MAXHISTORY]!=NULL)
      break;
  printstr("\nRecent ");
  printnum(MAXHISTORY-firstexist+1,-1);
  printstr(" task(s) : \n");
  for(int i = firstexist;i<MAXHISTORY;i++){
    printstr("    ");
    printnum(MAXHISTORY-firstexist+1,3);
    printstr(") ");
    printstr(myjournal->archive[myjournal->mostrecent+i]);
    printstr("\n");
  }
  printstr("    ");
  printnum(MAXHISTORY-firstexist+1,3);
  printstr(") ");
  printstr(myjournal->currenttask.taskname);
  printstr("\n\n");
  return;
}

int menu(){
  puts("📓 ========================📓");
  puts("||  Super TAsk traCKer    ||");
  puts("||========================||");
  puts("|| 1. New task            ||");
  puts("|| 2. Assign TODO to task ||");
  puts("|| 3. Finish task         ||");
  puts("|| 4. Show task history   ||");
  puts("|| 5. Logout              ||");
  puts("============================");
  printstr("choice : ");
  int choice=0;
  if(scanf("%d",&choice)!=1)
    printerror("scanf error");
  return choice;
}

int main(){
  init_proc();
  while(1){
    switch(menu()){
      case 1:
        newTask();
        break;
      case 2:
        assignTodo();
        break;
      case 3:
        finishTask();
        break;
      case 4:
        showTaskHistory();
	break;
      case 5:
	exit(0);
      default:
	puts("Invalid Option");
        break;
    }
  }
  return 0;
}

#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<unistd.h>
#include<string.h>
#include<fcntl.h>
#include<syscall.h>
#include<elf.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<sys/ptrace.h>
#include<sys/user.h>
#include<sys/wait.h>

#define PAGESIZE 0x1000
#define PAGEALIGN_DOWN(x) ((x)&(-PAGESIZE))
#define PAGEALIGN_UP(x) (((x)+(PAGESIZE-1))&(-PAGESIZE))

typedef struct {
  Elf64_Ehdr ehdr;
  Elf64_Phdr phdrs[1];
}Elf64_Hdrs;

char defaultInterp[] = "/lib64/ld-linux-x86-64.so.2";
char libc[] = "libc.so.6";
/* int3 */
char stub[8] = "\xcc\x00\x00\x00\x00\x00\x00\x00";
/* shellcode+BPFcode for write only seccomp */
char seccomp_shellcode[0x70] = "\x90\x90\xbf\x26\x00\x00\x00\x31\xd2\x52\x5e\xff\xc6\x56\x52\x41"
                               "\x5a\x52\x41\x58\xb8\x9d\x00\x00\x00\x50\x0f\x05\x58\xff\xc6\xbf"
                               "\x16\x00\x00\x00\x48\xba\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\x0f\x05"
                               "\x06\x00\x00\x00\x00\x00\x00\x00\xbb\xbb\xbb\xbb\xbb\xbb\xbb\xbb"	//struct sock_filter
                               "\x20\x00\x00\x00\x04\x00\x00\x00\x15\x00\x00\x03\x3e\x00\x00\xc0"	//struct sock_fprog
                               "\x20\x00\x00\x00\x00\x00\x00\x00\x15\x00\x00\x01\x01\x00\x00\x00"
                               "\x06\x00\x00\x00\x00\x00\xff\x7f\x06\x00\x00\x00\x00\x00\x00\x00";

void printError(char *msg){
  puts(msg);
  _exit(0);
}

void initProc(){
  setvbuf(stdin,NULL,_IONBF,0);
  setvbuf(stdout,NULL,_IONBF,0);
  setvbuf(stderr,NULL,_IONBF,0);
  return;
}

int readInt(){
  int num;
  if(scanf("%u",&num)!=1){
    printError("scanf failed");
  }
  getchar();
  return num;
}

void readStr(char *dst,int len){
  char buf[0x200];
  if(len>0x100)
    printError("only supports read size <=0x100");
  if(fread(buf,1,len*2,stdin)!=len*2)
    printError("fread failed");
  for(int i=0;i<len;i++){
    if(buf[i*2]>='0' && buf[i*2]<='9')
      dst[i] = (buf[i*2]-'0')<<4;
    else if(buf[i*2]>='A' && buf[i*2]<='F')
      dst[i] = (buf[i*2]-'A'+10)<<4;
    else if(buf[i*2]>='a' && buf[i*2]<='f')
      dst[i] = (buf[i*2]-'a'+10)<<4;
    else{
      printf("1 : %d %x\n",i,buf[i*2]);
      printError("non hex character");
    }
    if(buf[i*2+1]>='0' && buf[i*2+1]<='9')
      dst[i]|=buf[i*2+1]-'0';
    else if(buf[i*2+1]>='A' && buf[i*2+1]<='F')
      dst[i]|=buf[i*2+1]-'A'+10;
    else if(buf[i*2+1]>='a' && buf[i*2+1]<='f')
      dst[i]|=buf[i*2+1]-'a'+10;
    else{
      printf("2 : %d %x\n",i,buf[i*2+1]);
      printError("non hex character");
    }
  }
  getchar();
  return;
}

void chdirAndReadFile(char *dirname,char *fname,int fnameBufSize){
  char buf[0x100];
  int fd;
  unsigned int fnamelen;
  unsigned int fsize,nsize,chunkoffset;
  if(fnameBufSize<4)
    printError("fname buffer too small");
  if(chdir(dirname)==-1)
    printError("chdir failed");
  memset(fname,0,fnameBufSize);
  memcpy(fname,"./",2);
  printf("filename length : ");
  fnamelen = readInt();
  if(fnamelen>fnameBufSize-3)
    printError("fname too long");
  printf("filename : ");
  readStr(&fname[2],fnamelen);
  if(strpbrk(&fname[2],"./")!=NULL)
    printError("invalid character in filename");
  if(fname[2+fnamelen-1]=='\n')
    fname[2+fnamelen-1]='\x00';
  printf("filesize : ");
  fsize = readInt();
  if(fsize>0x20000)
    printError("file size too large");
  fd = open(fname,O_CREAT|O_WRONLY,S_IRWXU);
  if(fd<0)
    printError("open failed");
  chunkoffset = 0;
  while(fsize>0){
    if(fsize>0x100)
      nsize = 0x100;
    else
      nsize = fsize;
    printf("file content (0x%x~0x%x) : ",chunkoffset,chunkoffset+nsize);
    readStr(buf,nsize);
    if(write(fd,buf,nsize)!=nsize)
      printError("write failed");
    chunkoffset+=nsize;
    fsize-=nsize;
  }
  close(fd);
  return;
}

void lseekChecked(int fd, unsigned long long int offset){
  if(lseek(fd,offset,SEEK_SET)==-1)
    printError("lseek failed");
}

void readChecked(int fd, void *buf, unsigned long long int size){
  if(read(fd,buf,size)!=size)
    printError("read failed");
}

bool checkFile(char *fname, int *hdrsSize, Elf64_Hdrs **hdrs){
  Elf64_Ehdr ehdr;
  Elf64_Phdr *phdr;
  unsigned long long int lastLoad=0;
  unsigned long long int phdr_vaddr=0;
  bool hasInterp=false;
  int fd=open(fname,O_RDONLY);
  if(fd<0)
    printError("open failed");
  readChecked(fd,&ehdr,sizeof(Elf64_Ehdr));
  if(memcmp(ehdr.e_ident,"\x7f\x45\x4c\x46",4))
    printError("invalid magic number");
  if(ehdr.e_ident[4]!=2)
    printError("only 64 bit binary allowed");
  if(ehdr.e_machine!=0x3e)
    printError("only amd64 binary allowed");
  if(ehdr.e_type!=ET_EXEC && ehdr.e_type!=ET_DYN)
    printError("only ET_EXEC/ET_DYN binary allowed");
  if(ehdr.e_phoff!=sizeof(Elf64_Ehdr))
    printError("phdrs must follow immediately after ehdr");
  if(ehdr.e_phnum==0)
    printError("program must have phdrs");
  *hdrsSize = sizeof(Elf64_Ehdr)+ehdr.e_phnum*sizeof(Elf64_Phdr);
  *hdrs = malloc(*hdrsSize);
  if(*hdrs==NULL)
    printError("malloc failed");
  lseekChecked(fd,0);
  readChecked(fd,*hdrs,*hdrsSize);
  phdr = &((*hdrs)->phdrs[0]);
  if(phdr->p_type!=PT_PHDR)
    printError("first phdr entry must be PT_PHDR");
  if(phdr->p_offset!=sizeof(Elf64_Ehdr) || phdr->p_vaddr&(PAGESIZE-1)!=sizeof(Elf64_Ehdr))
    printError("phdr must follow immediately after ehdr");
  phdr_vaddr = phdr->p_vaddr;
  for(int i=1;i<ehdr.e_phnum;i++){
    phdr = &((*hdrs)->phdrs[i]);
    if(phdr->p_type==PT_PHDR)
      printError("PT_PHDR must be at first entry of phdr");
    else if(phdr->p_type==PT_LOAD){
      if(PAGEALIGN_UP(lastLoad)>PAGEALIGN_DOWN(phdr->p_vaddr))
        printError("no overlapping pages");
      if(phdr->p_vaddr+phdr->p_memsz<lastLoad)
        printError("no overflow");
      if(lastLoad==0){
        if(phdr->p_offset!=0)
          printError("first LOAD must start at beginning of ehdr");
        if(phdr->p_vaddr+sizeof(Elf64_Ehdr)!=phdr_vaddr)
          printError("phdr_vaddr must match memory mapping");
      }
      lastLoad = phdr->p_vaddr+phdr->p_memsz;
    }
    else if(phdr->p_type==PT_INTERP){
      hasInterp = true;
      if(phdr->p_filesz!=strlen(defaultInterp)+1)
        printError("only default interpreter allowed");
      char *buf=malloc(phdr->p_filesz);
      if(buf==NULL)
        printError("malloc failed");
      lseekChecked(fd,phdr->p_offset);
      readChecked(fd,buf,phdr->p_filesz);
      if(strcmp(buf,defaultInterp))
        printError("only default interpreter allowed");
      free(buf);
    }
  }
  close(fd);
  return hasInterp;
}

void attach(pid_t pid){
  int status;
  if(ptrace(PTRACE_ATTACH,pid,NULL,NULL)==-1 || waitpid(pid,&status,WUNTRACED)==-1)
    printError("ptrace attach failed");
  return;
}

void detach(pid_t pid){
  if(ptrace(PTRACE_DETACH,pid,NULL,NULL)==-1)
    printError("ptrace detach failed");
  return;
}

void singleStep(pid_t pid){
  int status;
  if(ptrace(PTRACE_SINGLESTEP,pid,NULL,NULL)==-1 || waitpid(pid,&status,WUNTRACED)==-1)
    printError("ptrace singlestep failed");
  return;
}

void nextSyscall(pid_t pid){
  int status;
  if(ptrace(PTRACE_SYSCALL,pid,NULL,NULL)==-1 || waitpid(pid,&status,WUNTRACED)==-1)
    printError("ptrace syscall failed");
  return;
}

void getRegs(pid_t pid, struct user_regs_struct *regs){
  if(ptrace(PTRACE_GETREGS,pid,NULL,regs)==-1)
    printError("ptrace getregs failed");
  return;
}

void setRegs(pid_t pid, struct user_regs_struct *regs){
  if(ptrace(PTRACE_SETREGS,pid,NULL,regs)==-1)
    printError("ptrace setregs failed");
  return;
}

void peekData(pid_t pid, unsigned long long int addr, int size, void *buf){
  for(int i=0;i<size;i+=8)
    *(unsigned long long int*)(&((char*)buf)[i]) = ptrace(PTRACE_PEEKDATA,pid,(void*)(addr+i),0);
  return;
}

void pokeData(pid_t pid, unsigned long long int addr, int size, void *buf){
  for(int i=0;i<size;i+=8)
    if(ptrace(PTRACE_POKEDATA,pid,(void*)(addr+i),*(unsigned long long int*)(&((char*)buf)[i]))==-1)
      printError("ptrace pokedata failed");
  return;
}

void checkPhdr(pid_t pid, unsigned long long int phdr_addr, unsigned long long int phnum, int hdrsSize, Elf64_Hdrs *hdrs){
  /* recheck some stuff at runtime */
  Elf64_Hdrs *runtimeHdrs;
  Elf64_Phdr *phdr;
  unsigned long long int l_addr;
  unsigned long long int strtab_addr;
  char buf[0x10];

  runtimeHdrs = malloc(hdrsSize);
  if(runtimeHdrs==NULL)
    printError("malloc failed");
  peekData(pid, phdr_addr-sizeof(Elf64_Ehdr), hdrsSize, runtimeHdrs);
  if(memcmp(runtimeHdrs,hdrs,hdrsSize))
    printError("No faking hdrs");
  l_addr = phdr_addr-(hdrs->phdrs[0]).p_vaddr;
  for(int i=0;i<phnum;i++){
    phdr = &(hdrs->phdrs[i]);
    if(phdr->p_type==PT_DYNAMIC){
      unsigned long long int dyn_ptr = l_addr+phdr->p_vaddr;
      Elf64_Dyn dyn;
      dyn.d_tag = -1;
      /* first run to locate strtab && check for init related stuff */
      while(dyn.d_tag!=DT_NULL){
        peekData(pid, dyn_ptr, sizeof(Elf64_Dyn), &dyn);
        if(dyn.d_tag==DT_STRTAB)
          strtab_addr = l_addr+dyn.d_un.d_val;
        if(dyn.d_tag==DT_PREINIT_ARRAY || dyn.d_tag==DT_INIT_ARRAY || dyn.d_tag==DT_INIT || dyn.d_tag==DT_PREINIT_ARRAYSZ || dyn.d_tag==DT_INIT_ARRAYSZ)
          printError("init related sections not allowed");
        /* relocations are fine by nature, however, since they have the potential to call functions within binary, it is unsafe to allow it directly
         * sandboxing it during runtime step by step in possible, but too slow
         * since the linker info will still be filled in anyway, we will currently require users to implement their own dlresolve lookup utility
         * then they could further utilize it to resolve other functions */
        if(dyn.d_tag==DT_PLTREL || dyn.d_tag==DT_RELA || dyn.d_tag==DT_REL)
          printError("automatic relocations unsupported");
        dyn_ptr+=sizeof(Elf64_Dyn);
      }
      dyn_ptr = l_addr+phdr->p_vaddr;
      dyn.d_tag = -1;
      /* second run to sanitize loaded libraries */
      while(dyn.d_tag!=DT_NULL){
        peekData(pid, dyn_ptr, sizeof(Elf64_Dyn), &dyn);
        if(dyn.d_tag==DT_NEEDED || dyn.d_tag==DT_AUXILIARY || dyn.d_tag==DT_FILTER){
          peekData(pid, strtab_addr+dyn.d_un.d_val, 0x10, buf);
          if(strcmp(buf,libc))
            printError("only libc.so.6 allowed as library");
        }
        dyn_ptr+=sizeof(Elf64_Dyn);
      }
    }
  }
  return;
}

int main(){
  char fname[0x100];
  int hdrsSize;
  Elf64_Hdrs *hdrs;
  bool hasInterp;
  char *execveArgs[1] = {NULL};

  initProc();
  chdirAndReadFile("/tmp/",fname,0x100);
  hasInterp = checkFile(fname,&hdrsSize,&hdrs);
  pid_t pid=fork();
  if(pid<0)
    printError("fork failed");
  else if(pid==0){
    /* Child */
    asm volatile ("int3;");
    execve(fname,execveArgs,NULL);
  }
  else{
    /* Parent */
    int status;
    struct user_regs_struct regs;
    Elf64_auxv_t av;
    unsigned long long int args_cnt, aux_ptr, env_ptr;
    unsigned long long int phdr_addr, entry_addr, phdr_cnt;
    char orig_code[0x70];
    attach(pid);
    getRegs(pid,&regs);
    /* run till just before execve syscall */
    while(true){
      nextSyscall(pid);
      getRegs(pid,&regs);
      if(regs.orig_rax==__NR_execve)
        break;
    }
    /* do execve */
    singleStep(pid);
    /* get regs after execve immediately */
    getRegs(pid,&regs);
    if(regs.rax!=0)
      printError("execve failed");
    /* check phdr again */
    peekData(pid,regs.rsp,0x8,(char*)&args_cnt);
    aux_ptr = regs.rsp+(args_cnt+1)*8;
    env_ptr = 1;
    while(env_ptr!=0){
      peekData(pid,aux_ptr,0x8,(char*)&env_ptr);
      aux_ptr+=8;
    }
    aux_ptr+=8;
    av.a_type = 1;
    while(av.a_type!=AT_NULL){
      peekData(pid,aux_ptr,sizeof(av),(char*)&av);
      if(av.a_type==AT_PHDR)
        phdr_addr = av.a_un.a_val;
      else if(av.a_type==AT_PHNUM)
        phdr_cnt = av.a_un.a_val;
      else if(av.a_type==AT_ENTRY)
        entry_addr = av.a_un.a_val;
      aux_ptr+=sizeof(av);
    }
    checkPhdr(pid,phdr_addr,phdr_cnt,hdrsSize,hdrs);
    free(hdrs);
    if((entry_addr+0x70)&(PAGESIZE-1)<0x70)
      printError("for sandbox impl ease, please don't split the first 0x70 bytes of code to two pages");
    /* patch addr in seccomp_shellcode */
    *(unsigned long long int*)(&seccomp_shellcode[0x26])=entry_addr+0x30;
    *(unsigned long long int*)(&seccomp_shellcode[0x38])=entry_addr+0x40;
    /* store entrypoint code */
    peekData(pid,entry_addr,0x70,orig_code);
    /* run until entrypoint if has interpreter */
    if(hasInterp){
      pokeData(pid,entry_addr,0x8,stub);
      while(true){
        nextSyscall(pid);
        getRegs(pid,&regs);
        if(regs.rip==entry_addr+1)
          break;
      }
      getRegs(pid, &regs);
      regs.rip-=1;
      setRegs(pid, &regs);
    }
    /* set entrypoint code to seccomp shellcode */
    pokeData(pid,entry_addr,0x70,seccomp_shellcode);
    /* install seccomp */
    for(int i=0;i<20;i++)
      singleStep(pid);
    /* restore original code & regs */
    pokeData(pid,entry_addr,0x70,orig_code);
    setRegs(pid, &regs);
    /* detach and continue */
    detach(pid);
    waitpid(pid,&status,0);
  }
  return 0;
}

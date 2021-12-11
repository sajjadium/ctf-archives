#include"main.h"

void initProc(){
  setvbuf(stdin,NULL,_IONBF,0);
  setvbuf(stdout,NULL,_IONBF,0);
  setvbuf(stderr,NULL,_IONBF,0);
  return;
}

void initGuestContext(GUESTCONTEXT **guestContext){
  int fd;
  *guestContext = malloc(sizeof(GUESTCONTEXT));
  if(*guestContext==NULL) printError("initGuestContext::malloc failed");
  (*guestContext)->canaryPage = ASLR(G_CANARY);
  (*guestContext)->brk = ASLR(G_CODE);
  (*guestContext)->stackBottom = ASLR(G_STACK)+INITSTACKSIZE;
  (*guestContext)->sysMemList = NULL;
  (*guestContext)->usrMemList = NULL;
  (*guestContext)->entry = NOENTRY;
  (*guestContext)->uc = NULL;
  return;
}

void loadCode(char *path,GUESTCONTEXT *guestContext){
  int fd;
  struct stat s;
  size_t entry;
  MEMLIST *meml = NULL;
  fd = open(path,O_RDONLY);
  if(fd<0) printError("loadCode::open failed");
  if(fstat(fd,&s)==-1) printError("loadCode::fstat failed");
  meml = allocMem(UPALIGN(s.st_size),PROT_READ|PROT_WRITE,MAP_PRIVATE,fd,0,guestContext->brk,UC_PROT_READ|UC_PROT_EXEC,NULL,&(guestContext->sysMemList));
  guestContext->brk+=UPALIGN(s.st_size);
  if(close(fd)!=0) printError("loadCode::close failed");
  /* check if the program entry is specified
   * since the first 8 bytes always mark entry point, we can ensure entry!=0
   * thus use 0 as mark where entry does not exist */
  entry = *(size_t*)(meml->mem->hostAddr);
  if(entry!=NOTENTRY){
    if(entry>=meml->mem->size) printError("loadCode:: program entry address exceeds end of program");
    if(guestContext->entry!=NOENTRY) printError("loadCode:: more than 1 program entry specified");
    guestContext->entry = (void*)((size_t)(meml->mem->guestAddr)+entry);
  }
  return;
}

void initUnicorn(uc_arch arch,uc_mode mode,GUESTCONTEXT *guestContext){
  MEMLIST *memEntry;
  void *codeAddr;
  int fd;
  if(uc_open(arch,mode,&(guestContext->uc))!=UC_ERR_OK) printError("initUnicorn::uc_open failed");
  memEntry = guestContext->sysMemList;
  /* register code mem */
  while(memEntry!=NULL){
    registerMemChecked(guestContext->uc,memEntry->mem->guestAddr,memEntry->mem->size,memEntry->mem->guestProt,memEntry->mem->hostAddr);
    memEntry = memEntry->next;
  }
  /* create+register stack mem */
  memEntry = allocMem(INITSTACKSIZE,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0,(void*)((size_t)guestContext->stackBottom-INITSTACKSIZE),UC_PROT_READ|UC_PROT_WRITE,NULL,&(guestContext->sysMemList));
  registerMemChecked(guestContext->uc,memEntry->mem->guestAddr,memEntry->mem->size,memEntry->mem->guestProt,memEntry->mem->hostAddr);
  /* create+register Canary */
  memEntry = allocMem(PAGESIZE,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0,guestContext->canaryPage,UC_PROT_READ,NULL,&(guestContext->sysMemList));
  *(size_t*)memEntry->mem->hostAddr = getRand(64);
  changeMemHostPriv(memEntry,PROT_READ);
  registerMemChecked(guestContext->uc,memEntry->mem->guestAddr,memEntry->mem->size,memEntry->mem->guestProt,memEntry->mem->hostAddr);
  return;
}

int main(int argc,char **argv,char **envp){
  if(argc!=2) printError("Usage : ./unicornsAisle [prog]");
  GUESTCONTEXT *guestContext;
  void *syscallHandlers[SYSCALLHANDLERCNT+1] = SYSCALLHANDLER;
  syscallHandlers[SYSCALLHANDLERCNT] = NULL;
  initProc();
  initGuestContext(&guestContext);
  loadCode(argv[1],guestContext);
  initUnicorn(UC_ARCH_X86,UC_MODE_64,guestContext);
  setupUnicornReg(guestContext->uc,UC_ARCH_X86,UC_MODE_64,guestContext->entry,guestContext->stackBottom,guestContext->canaryPage);
  setupUnicornGenericHandler(guestContext->uc,syscallHandlers,intrHandler,segvHandler,guestContext);
  uc_emu_start(guestContext->uc,(size_t)guestContext->entry,(size_t)guestContext->brk-1,0,0);
  uc_close(guestContext->uc);
  printError("Unicorn halted");
  return 0;
}

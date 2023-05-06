#include"handler.h"

void fetchSyscallRegs(uc_engine *uc,SYSCALLCONTEXT *regval){
  int regs[X86_64SYSCALLREGCNT] = X86_64SYSCALLREG;
  FETCHREG(uc,regs,(size_t*)regval,X86_64SYSCALLREGCNT);
  return;
}

MEMLIST *handlerFetchMemListUtil(MEMLIST** memList,void *addr,bool requireStartIncluded){
  MEMLIST *meml = NULL;
  if(*memList!=NULL){
    meml = searchMemSuccessor(*memList,addr);
    if(meml==NULL)
      *memList = NULL;
    else if(meml->mem->guestAddr<=addr)
      *memList = meml->next;
    else
      *memList = meml;
  }
  if(meml==NULL || (requireStartIncluded && meml->mem->guestAddr>addr))
    return NULL;
  return meml;
}

MEMLIST *handlerFetchMemList(HANDLERMEMSTATE *memState,int guestProtRequired,void *addr){
  MEMLIST *meml;
  meml = handlerFetchMemListUtil(&(memState->sysMemListCur),addr,true);
  if(meml==NULL)
    meml = handlerFetchMemListUtil(&(memState->usrMemListCur),addr,true);
  if(meml==NULL || meml->mem->guestProt&guestProtRequired!=guestProtRequired)
    return NULL;
  return meml;
}

MEMINFO *handlerFetchMemInfo(HANDLERMEMSTATE *memState,int guestProtRequired,void *addr){
  MEMLIST *meml = handlerFetchMemList(memState,guestProtRequired,addr);
  if(meml==NULL)
    return NULL;
  return meml->mem;
}

bool handlerFilterMemUsed(HANDLERMEMSTATE *memState,void *addr,size_t size){
  MEMLIST *meml;
  meml = handlerFetchMemListUtil(&(memState->sysMemListCur),addr,false);
  if(meml==NULL || (size_t)meml->mem->guestAddr>=(size_t)addr+size)
    meml = handlerFetchMemListUtil(&(memState->usrMemListCur),addr,false);
  if(meml==NULL || (size_t)meml->mem->guestAddr>=(size_t)addr+size)
    return false;
  return true;
}

void initHandlerMemState(bool includeSys, bool includeUsr, HANDLERMEMSTATE *memState,GUESTCONTEXT *guestContext){
  if(includeSys)
    memState->sysMemListCur = guestContext->sysMemList;
  else
    memState->sysMemListCur = NULL;
  if(includeUsr)
    memState->usrMemListCur = guestContext->usrMemList;
  else
    memState->usrMemListCur = NULL;
  return;
}

void preludeHandler(uc_engine *uc,uint32_t intno,void *guestContext){
  SYSCALLCONTEXT regval;
  char buf[0x100];
  int fd,size;
  fetchSyscallRegs(uc,&regval);
  if(regval.rax!=0xfedcba9876543210)
    return;
  fd = open("./unicornPrelude",O_RDONLY);
  if(fd<0) printError("preludeHandler::open failed");
  size = read(fd,buf,0xff);
  if(size<0) printError("preludeHandler::read failed");
  buf[size] = '\0';
  puts(buf);
  _exit(0);
}

void interludeHandler(uc_engine *uc,uint32_t intno,void *guestContext){
  SYSCALLCONTEXT regval;
  char key[0x10] = "unicorn";
  char buf[0x100];
  int fd,size;
  fetchSyscallRegs(uc,&regval);
  for(int i=0;i<7;i++){
   if((((size_t*)&regval)[i]&0xffffffffffffff00ULL)!=0xffffffffffffff00ULL) return;
   if((((size_t*)&regval)[i]&0xff)!=key[i]) return;
  }
  fd = open("./unicornInterlude",O_RDONLY);
  if(fd<0) printError("interludeHandler::open failed");
  size = read(fd,buf,0xff);
  if(size<0) printError("interludeHandler::read failed");
  buf[size] = '\0';
  puts(buf);
  _exit(0);
}

void exitHandler(uc_engine *uc,uint32_t intno,void *guestContext){
  SYSCALLCONTEXT regval;
  fetchSyscallRegs(uc,&regval);
  if(regval.rax!=SYS_exit)
    return;
  _exit(regval.rdi);
}

void mmapHandler(uc_engine *uc,uint32_t intno,void *guestContext){
  SYSCALLCONTEXT regval;
  HANDLERMEMSTATE memState;
  MEMLIST *meml;
  fetchSyscallRegs(uc,&regval);
  if(regval.rax!=SYS_mmap)
    return;
  regval.rdi = DOWNALIGN(regval.rdi);
  regval.rsi = UPALIGN(regval.rsi);
  /* only allow read/write pages */
  regval.rdx&= PROT_READ|PROT_WRITE;
  initHandlerMemState(true,true,&memState,(GUESTCONTEXT*)guestContext);
  if(regval.rdi+regval.rsi<=regval.rdi){
    regval.rax = 0xffffffffffffffffULL;
  }
  else if(handlerFilterMemUsed(&memState,(void*)regval.rdi,regval.rsi)==true){
    regval.rax = 0xffffffffffffffffULL;
  }
  else{
    if(memState.usrMemListCur!=NULL){
      /* optimized path to avoid traversing twice */
      meml = allocMem(regval.rsi,regval.rdx,MAP_PRIVATE|MAP_ANONYMOUS,0,-1,(void*)regval.rdi,HOSTPROT2UNICORNPROT(regval.rdx),memState.usrMemListCur->prev,&(((GUESTCONTEXT*)guestContext)->usrMemList));
    }
    else{
      /* generic path with no hinting */
      meml = allocMem(regval.rsi,regval.rdx,MAP_PRIVATE|MAP_ANONYMOUS,0,-1,(void*)regval.rdi,HOSTPROT2UNICORNPROT(regval.rdx),NULL,&(((GUESTCONTEXT*)guestContext)->usrMemList));
    }
    registerMemChecked(uc,meml->mem->guestAddr,meml->mem->size,meml->mem->guestProt,meml->mem->hostAddr);
    regval.rax = regval.rdi;
  }
  regWriteChecked(uc,UC_X86_REG_RAX,(void*)&(regval.rax));
  return;
}

void munmapHandler(uc_engine *uc,uint32_t intno,void *guestContext){
  SYSCALLCONTEXT regval;
  HANDLERMEMSTATE memState;
  MEMLIST *meml;
  size_t cursize;
  fetchSyscallRegs(uc,&regval);
  if(regval.rax!=SYS_munmap)
    return;
  regval.rsi = UPALIGN(regval.rsi);
  if(regval.rdi&PAGEMASK!=0){
    regval.rax = 0xffffffffffffffffULL;
  }
  else if(regval.rdi+regval.rsi<=regval.rdi){
    regval.rax = 0xffffffffffffffffULL;
  }
  else{
    regval.rax = 0;
    /* sys memory(code/stack/canary) should not be released */
    initHandlerMemState(false,true,&memState,(GUESTCONTEXT*)guestContext);
    while(regval.rsi>0){
      meml = handlerFetchMemList(&memState,UC_PROT_DONTCARE,(void*)regval.rdi);
      if(meml!=NULL){
        cursize = (size_t)meml->mem->guestAddr+meml->mem->size-regval.rdi;
	if(cursize>regval.rsi)
          cursize = regval.rsi;
	releaseMem((void*)regval.rdi,cursize,meml,&(((GUESTCONTEXT*)guestContext)->usrMemList));
	unregisterMemChecked(uc,(void*)regval.rdi,cursize);
	regval.rdi+=cursize;
	regval.rsi-=cursize;
      }
      else{
        if(memState.usrMemListCur==NULL){
          /* we have reached end of usrMemList, no need to look further */
          break;
        }
	else if(regval.rdi+regval.rsi<=(size_t)memState.usrMemListCur->mem->guestAddr){
          /* the next page is out of reach */
          break;
	}
        else{
          regval.rsi-= (size_t)memState.usrMemListCur->mem->guestAddr-regval.rdi;
	  regval.rdi = (size_t)memState.usrMemListCur->mem->guestAddr;
        }
      }
    }
  }
  regWriteChecked(uc,UC_X86_REG_RAX,(void*)&(regval.rax));
  return;
}

void writeHandler(uc_engine *uc,uint32_t intno,void *guestContext){
  SYSCALLCONTEXT regval;
  HANDLERMEMSTATE memState;
  MEMINFO *mem, *mem2;
  char buf[0x400];
  fetchSyscallRegs(uc,&regval);
  if(regval.rax!=SYS_write)
    return;
  /* cap size of write to a sane value */
  if(regval.rdx>0x400)
    regval.rdx = 0x400;
  initHandlerMemState(true,true,&memState,(GUESTCONTEXT*)guestContext);
  if(regval.rsi+regval.rdx<regval.rsi){
    regval.rax = 0xffffffffffffffffULL;
  }
  else{
    mem = handlerFetchMemInfo(&memState,UC_PROT_READ,(void*)regval.rsi);
    if(mem==NULL){
      regval.rax = 0xffffffffffffffffULL;
    }
    else if(regval.rsi+regval.rdx<=(size_t)mem->guestAddr+mem->size ||
	    (mem2=handlerFetchMemInfo(&memState,UC_PROT_READ,(void*)((size_t)mem->guestAddr+mem->size)),mem2!=NULL && (size_t)mem2->guestAddr==(size_t)mem->guestAddr+mem->size)){
      /* reading pass allocation boundary is costly since we need to do checks for each page
       * thankfully we only have to do it twice due to read size limit */
      memReadChecked(uc,(void*)regval.rsi,buf,regval.rdx);
      regval.rax = write(regval.rdi,buf,regval.rdx);
    }
    else{
      regval.rax = 0xffffffffffffffffULL;
    }
  }
  regWriteChecked(uc,UC_X86_REG_RAX,(void*)&(regval.rax));
  return;
}

void readHandler(uc_engine *uc,uint32_t intno,void *guestContext){
  SYSCALLCONTEXT regval;
  HANDLERMEMSTATE memState;
  MEMINFO *mem, *mem2;
  char buf[0x400];
  fetchSyscallRegs(uc,&regval);
  if(regval.rax!=SYS_read)
    return;
  /* cap size of read to a sane value */
  if(regval.rdx>0x400)
    regval.rdx = 0x400;
  initHandlerMemState(true,true,&memState,(GUESTCONTEXT*)guestContext);
  if(regval.rsi+regval.rdx<regval.rsi){
    regval.rax = 0xffffffffffffffffULL;
  }
  else{
    mem = handlerFetchMemInfo(&memState,UC_PROT_WRITE,(void*)regval.rsi);
    if(mem==NULL){
      regval.rax = 0xffffffffffffffffULL;
    }
    else if(regval.rsi+regval.rdx<=(size_t)mem->guestAddr+mem->size ||
	    (mem2=handlerFetchMemInfo(&memState,UC_PROT_WRITE,(void*)((size_t)mem->guestAddr+mem->size)),mem2!=NULL && (size_t)mem2->guestAddr==(size_t)mem->guestAddr+mem->size)){
      /* writing pass allocation boundary is costly since we need to do checks for each page
       * thankfully we only have to do it twice due to read size limit */
      regval.rax = read(regval.rdi,buf,regval.rdx);
      memWriteChecked(uc,(void*)regval.rsi,buf,regval.rax);
    }
    else{
      regval.rax = 0xffffffffffffffffULL;
    }
  }
  regWriteChecked(uc,UC_X86_REG_RAX,(void*)&(regval.rax));
  return;
}

void intrHandler(uc_engine *uc,uint32_t intno,void *guestContext){
  printError("uc interrupt occurred");
}

void segvHandler(uc_engine *uc,uint32_t intno,void *guestContext){
  printError("uc segmentation fault");
}

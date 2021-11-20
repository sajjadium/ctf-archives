#include"mem.h"

void *ASLR(GUESTMEMTYPE type){
  void *addr;
  switch(type){
    case G_CANARY:
      addr = (void*)((getRand(ASLRSTRENGTH)<<ASLRALIGN)+CANARYBIAS);
      break;
    case G_CODE:
      addr = (void*)((getRand(ASLRSTRENGTH)<<ASLRALIGN)+CODEBIAS);
      break;
    case G_STACK:
      addr = (void*)((getRand(ASLRSTRENGTH)<<ASLRALIGN)+STACKBIAS);
      break;
    default:
      printError("ASLR:: invalid mem type");
      break;
  }
  return addr;
}

MEMLIST *linkMem(MEMLIST **memList,MEMLIST *hint,MEMINFO *newMem){
  MEMLIST *newEntry;
  MEMLIST *curEntry;
  newEntry = malloc(sizeof(MEMLIST));
  if(newEntry==NULL) printError("linkMem::malloc failed");
  newEntry->mem = newMem;
  if(hint!=NULL)
    curEntry = hint;
  else
    curEntry = *memList;
  if(curEntry==NULL){
    *memList = newEntry;
    newEntry->next = NULL;
    newEntry->prev = NULL;
  }
  else{
    /* we should be 100% sure that newMem is legal here, no need to check */
    while(curEntry->next!=NULL && curEntry->mem->guestAddr<newMem->guestAddr)
      curEntry = curEntry->next;
    if(curEntry->mem->guestAddr<newMem->guestAddr){
      newEntry->next = curEntry->next;
      newEntry->prev = curEntry;
      if(curEntry->next!=NULL)
        curEntry->next->prev = newEntry;
      curEntry->next = newEntry;
    }
    else{
      newEntry->next = curEntry;
      newEntry->prev = curEntry->prev;
      if(curEntry->prev!=NULL)
        curEntry->prev->next = newEntry;
      else
        *memList = newEntry;
      curEntry->prev = newEntry;
    }
  }
  return newEntry;
}

void unlinkMem(MEMLIST **memList,MEMLIST *targetMem){
  if(targetMem->next!=NULL)
    targetMem->next->prev = targetMem->prev;
  if(targetMem->prev!=NULL)
    targetMem->prev->next = targetMem->next;
  else
    *memList = targetMem->next;
  return;
}

MEMLIST *allocMem(size_t size,int prot,int flags,int fd,off_t offset,void *guestAddr,int guestProt,MEMLIST *memListEntry,MEMLIST **memList){
  void *backingMem;
  MEMINFO *mem;
  backingMem = mmap(NULL,size,prot,flags,fd,0);
  if(backingMem==MAP_FAILED) printError("allocMem::mmap failed");
  mem = malloc(sizeof(MEMINFO));
  if(mem==NULL) printError("allocMem::malloc failed");
  mem->size = size;
  mem->hostAddr = backingMem;
  mem->guestAddr = guestAddr;
  mem->hostProt = prot;
  mem->guestProt = guestProt;
  return linkMem(memList,memListEntry,mem);
}

void releaseMem(void *addr,size_t size,MEMLIST *memListEntry,MEMLIST **memList){
  size_t spareSize;
  void *hostAddr;
  MEMINFO *spareMem;
  hostAddr = memListEntry->mem->hostAddr+(addr-memListEntry->mem->guestAddr);
  if(munmap(hostAddr,size)!=0) printError("releaseMem::munmap failed");
  if((size_t)addr+size<(size_t)memListEntry->mem->guestAddr+memListEntry->mem->size){
    spareMem = malloc(sizeof(MEMINFO));
    if(spareMem==NULL) printError("releaseMem::malloc failed");
    spareSize = ((size_t)memListEntry->mem->guestAddr+memListEntry->mem->size)-((size_t)addr+size);
    spareMem->size = spareSize;
    spareMem->hostAddr = (void*)((size_t)hostAddr+size);
    spareMem->guestAddr = (void*)((size_t)addr+size);
    spareMem->hostProt = memListEntry->mem->hostProt;
    spareMem->guestProt = memListEntry->mem->guestProt;
    linkMem(memList,memListEntry,spareMem);
  }
  if(addr>memListEntry->mem->guestAddr){
    memListEntry->mem->size = addr-memListEntry->mem->guestAddr;
  }
  else{
    unlinkMem(memList,memListEntry);
    free(memListEntry->mem);
    free(memListEntry);
  }
  return;
}

void changeMemHostPriv(MEMLIST *memListEntry,int newProt){
  if(mprotect(memListEntry->mem->hostAddr,memListEntry->mem->size,newProt)!=0) printError("changeMemHostPriv::mprotect failed");
  memListEntry->mem->hostProt = newProt;
  return;
}

MEMLIST *searchMemSuccessor(MEMLIST *memList,void *addr){
  MEMLIST *curEntry = memList;
  while(curEntry->next!=NULL && addr>=curEntry->mem->guestAddr)
    curEntry = curEntry->next;
  if(curEntry->mem->guestAddr>addr){
    /* we can only search forward */
    if(curEntry!=memList && (size_t)curEntry->prev->mem->guestAddr+curEntry->prev->mem->size>(size_t)addr)
      return curEntry->prev;
    else
      return curEntry;
  }
  if((size_t)curEntry->mem->guestAddr+curEntry->mem->size>(size_t)addr)
    return curEntry;
  return NULL;
}

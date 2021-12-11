#ifndef __MEM_HEADER__
#define __MEM_HEADER__

#include<stdlib.h>
#include<stddef.h>
#include<sys/mman.h>
#include<unicorn/unicorn.h>
#include"utils.h"

#define PAGEBITS (12)
#define PAGESIZE (1<<PAGEBITS)
#define PAGEMASK (PAGESIZE-1)
#define DOWNALIGN(size) ((size)&(~PAGEMASK))
#define UPALIGN(size) (DOWNALIGN((size)+PAGEMASK))

#define ASLRALIGN (20)
#define ASLRSTRENGTH (21)
#define CANARYBIAS (0x440000000000)
#define CODEBIAS (0x550000000000)
#define STACKBIAS (0x7e0000000000)

#define INITSTACKSIZE (0x1000)

#define UC_PROT_DONTCARE (0)

#define HOSTPROT2UNICORNPROT(prot) (((prot)&PROT_READ ? UC_PROT_READ:0) |\
				    ((prot)&PROT_WRITE ? UC_PROT_WRITE:0) |\
				    ((prot)&PROT_EXEC ? UC_PROT_EXEC:0))

typedef enum GUESTMEMTYPE{ //just for ease of aslr impl
  G_CANARY,
  G_CODE,
  G_STACK,
}GUESTMEMTYPE;

typedef struct MEMINFO{
  void *hostAddr;
  void *guestAddr;
  size_t size;
  int guestProt;
  int hostProt;		//this should not be used in most cases, just keep for sake of completeness
}MEMINFO;

typedef struct MEMLIST{
  MEMINFO *mem;
  struct MEMLIST *next;
  struct MEMLIST *prev;
}MEMLIST;

void *ASLR(GUESTMEMTYPE);
MEMLIST *allocMem(size_t size,int prot,int flags,int fd,off_t offset,void* guestAddr,int guestProt,MEMLIST *memListEntry,MEMLIST **memList);
void releaseMem(void *addr,size_t size,MEMLIST *memListEntry,MEMLIST **memList);
void changeMemHostPriv(MEMLIST *memListEntry,int newProt);
MEMLIST *searchMemSuccessor(MEMLIST *memList,void *addr);
bool filterMemUsed(MEMLIST *memList,void *addr,size_t size);

#endif

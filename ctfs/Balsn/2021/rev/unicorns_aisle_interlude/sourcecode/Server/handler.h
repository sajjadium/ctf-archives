#ifndef __HANDLER_HEADER__
#define __HANDLER_HEADER__

#include<unistd.h>
#include<sys/syscall.h>
#include<unicorn/unicorn.h>
#include"utils.h"
#include"guestcontext.h"
#include"mem.h"
#include"ucutils.h"

typedef struct HANDLERMEMSTATE{
  MEMLIST *sysMemListCur;
  MEMLIST *usrMemListCur;
}HANDLERMEMSTATE;

#define SYSCALLHANDLERCNT 7
#define SYSCALLHANDLER {preludeHandler,interludeHandler,exitHandler,mmapHandler,munmapHandler,writeHandler,readHandler}

void preludeHandler(uc_engine *uc,uint32_t intno,void *user_data);
void interludeHandler(uc_engine *uc,uint32_t intno,void *user_data);
void exitHandler(uc_engine *uc,uint32_t intno,void *user_data);
void mmapHandler(uc_engine *uc,uint32_t intno,void *user_data);
void munmapHandler(uc_engine *uc,uint32_t intno,void *user_data);
void writeHandler(uc_engine *uc,uint32_t intno,void *user_data);
void readHandler(uc_engine *uc,uint32_t intno,void *user_data);
void intrHandler(uc_engine *uc,uint32_t intno,void *user_data);
void segvHandler(uc_engine *uc,uint32_t intno,void *user_data);

#endif

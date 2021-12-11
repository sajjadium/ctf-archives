#ifndef __GUESTCONTEXT_HEADER__
#define __GUESTCONTEXT_HEADER__

#include<unicorn/unicorn.h>
#include"mem.h"

#define NOTENTRY (0)
#define NOENTRY ((void*)0)

typedef struct GUESTCONTEXT{
  void *canaryPage;
  void *brk;
  void *stackBottom;
  MEMLIST *sysMemList;
  MEMLIST *usrMemList;
  void *entry;
  uc_engine *uc;
}GUESTCONTEXT;

#endif

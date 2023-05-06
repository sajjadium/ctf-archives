#ifndef __UCUTILS_HEADER__
#define __UCUTILS_HEADER__

#include<unicorn/unicorn.h>
#include"utils.h"
#include"guestcontext.h"
#include"mem.h"

#define CLEARREG(uc,regs,cnt) {size_t INITREGVALUE=0;\
			       void *INITREGVALUEARR[(cnt)];\
			       for(int SETINITREGVALUESi=0;SETINITREGVALUESi<(cnt);SETINITREGVALUESi++)\
			         INITREGVALUEARR[SETINITREGVALUESi]=(void*)&INITREGVALUE;\
			       regWriteBatchChecked((uc),(regs),INITREGVALUEARR,(cnt));}

#define FETCHREG(uc,regs,regval,cnt) {void *FETCHREGREGVALPTR[(cnt)];\
				      for(int FETCHREGi=0;FETCHREGi<(cnt);FETCHREGi++)\
				        FETCHREGREGVALPTR[FETCHREGi]=(regval)+FETCHREGi;\
				      regReadBatchChecked((uc),(regs),FETCHREGREGVALPTR,(cnt));}

#define X86_64ALLREGCNT (17)
#define X86_64ALLREG {UC_X86_REG_RAX,UC_X86_REG_RBP,UC_X86_REG_RBX,UC_X86_REG_RCX,\
		      UC_X86_REG_RDI,UC_X86_REG_RDX,UC_X86_REG_RIP,UC_X86_REG_RSP,\
		      UC_X86_REG_RSI,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,\
		      UC_X86_REG_R11,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,\
		      UC_X86_REG_R15}

#define X86_64SYSCALLREGCNT (7)
#define X86_64SYSCALLREG {UC_X86_REG_RAX,UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_RDX,UC_X86_REG_R10,UC_X86_REG_R8,UC_X86_REG_R9}

typedef struct SYSCALLCONTEXT{
  size_t rax;
  size_t rdi;
  size_t rsi;
  size_t rdx;
  size_t r10;
  size_t r8;
  size_t r9;
}SYSCALLCONTEXT;

void regWriteBatchChecked(uc_engine *uc,int *regids,void **values,int count);
void regWriteChecked(uc_engine *uc,int regid,void *value);
void regReadBatchChecked(uc_engine *uc,int *regids,void **values,int count);
size_t memReadChecked(uc_engine *uc,void *srcAddr,char *dstBuf,size_t length);
size_t memWriteChecked(uc_engine *uc,void *dstAddr,char *srcBuf,size_t length);
void registerMemChecked(uc_engine *uc,void *addr,size_t size,int prot,void *backingMem);
void unregisterMemChecked(uc_engine *uc,void *addr,size_t size);

void setupUnicornReg(uc_engine *uc,uc_arch arch,uc_mode mode,void *entry,void *stackTop,void *canaryPage);
void setupUnicornGenericHandler(uc_engine *uc,void **syscallHandlers,void *intrHandler,void *segvHandler,GUESTCONTEXT *guestContext);

#endif

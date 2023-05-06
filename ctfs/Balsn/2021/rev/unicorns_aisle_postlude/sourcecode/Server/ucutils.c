#include"ucutils.h"

void regWriteBatchChecked(uc_engine *uc,int *regids,void **values,int count){
  if(uc_reg_write_batch(uc,regids,values,count)!=UC_ERR_OK) printError("regWriteBatchChecked::uc_reg_write_batch failed");
  return;
}

void regWriteChecked(uc_engine *uc,int regid,void *value){
  if(uc_reg_write(uc,regid,value)!=UC_ERR_OK) printError("regWriteChecked::uc_reg_write failed");
  return;
}

void regReadBatchChecked(uc_engine *uc,int *regids,void **values,int count){
  if(uc_reg_read_batch(uc,regids,values,count)!=UC_ERR_OK) printError("regReadBatchChecked::uc_reg_read_batch failed");
  return;
}

void addHookChecked(uc_engine *uc,uc_hook *hh,int type,void *callback,void *userData,uint64_t begin,uint64_t end,int extra){
  if(uc_hook_add(uc,hh,type,callback,userData,begin,end,extra)!=UC_ERR_OK) printError("addHookChecked::uc_hook_add failed");
  return;
}

size_t memReadChecked(uc_engine *uc,void *srcAddr,char *dstBuf,size_t length){
  if(uc_mem_read(uc,(size_t)srcAddr,dstBuf,length)!=UC_ERR_OK) printError("memReadChecked::uc_mem_read failed");
  return length;
}

size_t memWriteChecked(uc_engine *uc,void *dstAddr,char *srcBuf,size_t length){
  if(uc_mem_write(uc,(size_t)dstAddr,srcBuf,length)!=UC_ERR_OK) printError("memWriteChecked::uc_mem_write failed");
  return length;
}

void registerMemChecked(uc_engine *uc,void *addr,size_t size,int prot,void *backingMem){
  if(uc_mem_map_ptr(uc,(size_t)addr,size,prot,backingMem)!=UC_ERR_OK) printError("registerMemChecked::uc_mem_map_ptr failed");
  return;
}

void unregisterMemChecked(uc_engine *uc,void *addr,size_t size){
  if(uc_mem_unmap(uc,(size_t)addr,size)!=UC_ERR_OK) printError("unregisterMemChecked::uc_mem_unmap failed");
  return;
}

void setupUnicornReg(uc_engine *uc,uc_arch arch,uc_mode mode,void *entry,void *stackBottom,void *canaryPage){
  /* unicorn does not provide api to fetch arch from uc_engine, need to pass it ourself */
  switch(arch){
    case UC_ARCH_X86:
      switch(mode){
        case UC_MODE_64:;
	  int regs[X86_64ALLREGCNT] = X86_64ALLREG;
	  size_t canarySeg = (size_t)canaryPage>>16;
	  CLEARREG(uc,regs,X86_64ALLREGCNT);
          regWriteChecked(uc,UC_X86_REG_RIP,(void*)&entry);
          regWriteChecked(uc,UC_X86_REG_RSP,(void*)&stackBottom);
	  /* using segments requires setting up GDT properly, which is too much hassle
	   * abuse DR0 for now */
	  regWriteChecked(uc,UC_X86_REG_DR0,(void*)&canaryPage);
	  break;
	default:
	  printError("setupUnicornRegs:: mode not yet supported");
	  break;
      }
      break;
    default:
      printError("setupUnicornRegs:: arch not yet supported");
      break;
  }
  return;
}

void setupUnicornGenericHandler(uc_engine *uc,void **syscallHandlers,void *intrHandler,void *segvHandler,GUESTCONTEXT *guestContext){
  int idx = 0;
  uc_hook hh;
  for(int idx=0;syscallHandlers[idx]!=NULL;idx+=1)
    addHookChecked(uc,&hh,UC_HOOK_INSN,syscallHandlers[idx],(void*)guestContext,1,0,UC_X86_INS_SYSCALL);
  addHookChecked(uc,&hh,UC_HOOK_INTR,intrHandler,(void*)guestContext,1,0,0);
  addHookChecked(uc,&hh,UC_HOOK_MEM_INVALID,segvHandler,(void*)guestContext,1,0,0);
  return;
}

#include "syscall.h"

uint64_t syscallHandler(uint64_t a1, uint64_t a2, uint64_t a3, uint64_t a4, uint64_t a5, uint64_t a6) {
  uint64_t nr;
  asm("mov %[nr], rax;" : [nr] "=r" (nr));
  switch(nr) {
    case SYS_READ:
      return sys_read(a1, a2, a3);
    case SYS_WRITE:
      return sys_write(a1, a2, a3);
    case SYS_MMAP:
      return sys_mmap(a1, a2, a3, a4, a5, a6);
    case SYS_MUNMAP:
      return sys_munmap(a1, a2);
    case SYS_EXIT:
      sys_exit(a1);
      break;
    case SYS_APPLET_REGISTER:
      return sys_appletRegister(a1, a2);
    case SYS_APPLET_UNREGISTER:
      return sys_appletUnregister(a1);
    case SYS_APPLET_INVOKE:
      return sys_appletInvoke(a1, a2);
    case SYS_APPLET_RESULT:
      return sys_appletResult(a1, a2);
    case SYS_APPLET_STORAGE:
      return sys_appletInspectStorage(a1, a2);
    case SYS_FLAG:
      return sys_flag();
    default:
      return SYS_FAIL;
  }
  return SYS_FAIL;
}


uint64_t sys_read(uint64_t fd, uint64_t ubuf, uint64_t size) {
  uint8_t buf[PAGE_SIZE];
  uint64_t bufPhysCursor, pageOffset = 0;
  if (fd != STDIN_FILENO) return SYS_FAIL;
  if (checkVrange(ubuf, size, PDE64_USER | PDE64_RW) == FAIL) return SYS_FAIL;
  if (size == 0) return 0;
  if (getPhysAddr((uint64_t)buf, PDE64_RW, &bufPhysCursor) == FAIL) panic("sys_read failed"); //kernel stack should always be accessible
  for (uint64_t remainSize = size; remainSize > 0; remainSize--) {
    if (hp_read(fd, bufPhysCursor, 1) == FAIL) return SYS_FAIL;
    pageOffset++;
    bufPhysCursor++;
    if (pageOffset == PAGE_SIZE) {
      memcpy(ubuf, (uint64_t)buf, PAGE_SIZE); 
      pageOffset = 0;
      bufPhysCursor -= PAGE_SIZE;
      ubuf += PAGE_SIZE;
    }
  }
  memcpy(ubuf, (uint64_t)buf, PAGE_OFFSET(size)); 
  return size;
}

uint64_t sys_write(uint64_t fd, uint64_t ubuf, uint64_t size) {
  uint8_t buf[PAGE_SIZE];
  uint64_t bufPhysCursor, pageOffset;
  if (fd != STDOUT_FILENO) return SYS_FAIL;
  if (checkVrange(ubuf, size, PDE64_USER) == FAIL) return SYS_FAIL;
  if (size == 0) return 0;
  if (getPhysAddr((uint64_t)buf, PDE64_RW, &bufPhysCursor) == FAIL) panic("sys_read failed"); //kernel stack should always be accessible
  if (PAGE_OFFSET(size) == 0) {
    memcpy((uint64_t)buf, ubuf, PAGE_SIZE);
    ubuf += PAGE_SIZE;
    pageOffset = PAGE_SIZE;
  } else {
    memcpy((uint64_t)buf, ubuf, PAGE_OFFSET(size));
    ubuf += PAGE_OFFSET(size);
    pageOffset = PAGE_OFFSET(size);
  }
  for (uint64_t remainSize = size; remainSize > 0; remainSize--) {
    if (hp_write(fd, bufPhysCursor, 1) == FAIL) return SYS_FAIL;
    pageOffset--;
    bufPhysCursor++;
    if (pageOffset == 0 && remainSize >= PAGE_SIZE) {
      memcpy((uint64_t)buf, ubuf, PAGE_SIZE);
      pageOffset = PAGE_SIZE;
      bufPhysCursor -= PAGE_SIZE;
      ubuf += PAGE_SIZE;
    }
  }
  return size; 
}

uint64_t sys_mmap(uint64_t vaddr, uint64_t size, uint64_t prot, uint64_t flag, uint64_t fd, uint64_t off) {
  if (!PAGE_ALIGNED(vaddr) || !PAGE_ALIGNED(size) || ADD_OVERFLOW(vaddr, size)) return SYS_FAIL;
  if (size == 0) return SYS_FAIL;
  if (prot & (~PROT_MASK)) return SYS_FAIL;
  if (!(prot & PROT_READ)) return SYS_FAIL;
  if (flag & (~MAP_MASK)) return SYS_FAIL;
  if ((flag & (MAP_ANONYMOUS | MAP_PRIVATE)) != (MAP_ANONYMOUS | MAP_PRIVATE)) return SYS_FAIL;
  if (fd != -1) return SYS_FAIL;
  if (off != 0) return SYS_FAIL;

  if (flag & MAP_FIXED) {
    //We don't allow partial allocation success, but we do allow partial deallocation, so need to check here
    if (!IS_USER_ADDR(vaddr) || !IS_USER_ADDR(vaddr + size)) return SYS_FAIL;
    if (deallocateVrange(vaddr, size, true) == FAIL) return SYS_FAIL; //shouldn't happen, but just in case
  } else {
    if (vaddr == 0) {
      vaddr = g_runtimeContext.userMmapBase;
    }
    uint64_t rVaddr;
    if (searchFreeVrange(vaddr, USER_PAGE_MIN, size, true, &rVaddr) == FAIL) {
      if (searchFreeVrange(vaddr, USER_PAGE_MAX + PAGE_SIZE, size, false, &rVaddr) == FAIL) {
        return SYS_FAIL;
      }
    }
    vaddr = rVaddr;
  }
  if (allocateVrange(vaddr, size, true, (prot & PROT_WRITE) != 0) == FAIL) return SYS_FAIL;
  return vaddr;
}

uint64_t sys_munmap(uint64_t vaddr, uint64_t size) {
  if (deallocateVrange(vaddr, size, true) == FAIL) return SYS_FAIL;
  return SYS_SUCCESS;
}

void __attribute__((noreturn)) sys_exit(uint64_t status) {
  //we only support one user process for now, so exit means kernel should also exit
  hp_exit(status);
}

uint64_t sys_appletRegister(uint64_t ureq, uint64_t ures) {
  uint8_t appletCode[APPLET_SIZE_MAX];
  APPLET_REGISTER_REQ req;
  APPLET_ID res;
  if (checkVrange(ures, sizeof(APPLET_ID), PDE64_USER | PDE64_RW) == FAIL) return SYS_FAIL;
  if (copyFromUser((uint64_t)&req, ureq, sizeof(APPLET_REGISTER_REQ)) == FAIL) return SYS_FAIL;
  if (req.applet.codeLen > APPLET_SIZE_MAX || req.applet.codeLen == 0) return SYS_FAIL;
  if (copyFromUser((uint64_t)appletCode, (uint64_t)req.applet.code, req.applet.codeLen) == FAIL) return SYS_FAIL;
  //fixup into kernel space ptr
  req.applet.code = appletCode;
  if (kAppletRegister(&req, &res) == FAIL) return SYS_FAIL;
  if (copyToUser(ures, (uint64_t)&res, sizeof(APPLET_ID)) == FAIL) return SYS_FAIL;
  return SYS_SUCCESS;
}

uint64_t sys_appletUnregister(uint64_t ureq) {
  APPLET_UNREGISTER_REQ req;
  if (copyFromUser((uint64_t)&req, ureq, sizeof(APPLET_UNREGISTER_REQ)) == FAIL) return SYS_FAIL;
  if (kAppletUnregister(&req) == FAIL) return SYS_FAIL;
  return SYS_SUCCESS;
}

uint64_t sys_appletInvoke(uint64_t ureq, uint64_t ures) {
  uint8_t appletArg[APPLET_ARG_SIZE_MAX];
  APPLET_INVOKE_REQ req;
  APPLET_RECEIPT res;
  if (checkVrange(ures, sizeof(APPLET_RECEIPT), PDE64_USER | PDE64_RW) == FAIL) return SYS_FAIL;
  if (copyFromUser((uint64_t)&req, ureq, sizeof(APPLET_INVOKE_REQ)) == FAIL) return SYS_FAIL;
  if (req.arg.dataLen > APPLET_ARG_SIZE_MAX) return SYS_FAIL;
  if (req.arg.dataLen > 0 && copyFromUser((uint64_t)appletArg, (uint64_t)req.arg.data, req.arg.dataLen) == FAIL) return SYS_FAIL;
  //fixup into kernel space ptr
  req.arg.data = appletArg;
  if (kAppletInvoke(&req, &res, TASK_NIL) == FAIL) return SYS_FAIL;
  if (copyToUser(ures, (uint64_t)&res, sizeof(APPLET_RECEIPT)) == FAIL) return SYS_FAIL;
  return SYS_SUCCESS;
}

uint64_t sys_appletResult(uint64_t ureq, uint64_t ures) {
  uint8_t appletRes[APPLET_RES_SIZE_MAX];
  APPLET_RECEIPT req;
  APPLET_RESULT res;
  APPLET_STATUS status;
  uint64_t uresBuf, uresLen;
  if (copyFromUser((uint64_t)&req, ureq, sizeof(APPLET_RECEIPT)) == FAIL) return SYS_FAIL;
  if (copyFromUser((uint64_t)&res, ures, sizeof(APPLET_RESULT)) == FAIL) return SYS_FAIL;
  uresBuf = (uint64_t)res.res.data;
  uresLen = res.res.dataLen;
  res.res.data = appletRes;
  if (res.res.dataLen > APPLET_RES_SIZE_MAX) {
    res.res.dataLen = APPLET_RES_SIZE_MAX;
  }
  if (kAppletResult(&req, &res) == FAIL) return SYS_FAIL;
  if (res.status == APPLET_DONE) {
    if (checkVrange(uresBuf, res.res.dataLen, PDE64_USER | PDE64_RW) == FAIL) return SYS_FAIL;
    if (copyToUser(uresBuf, (uint64_t)appletRes, res.res.dataLen) == FAIL) return SYS_FAIL;
  } else {
    res.res.dataLen = uresLen; //leave this untouched if no data copy
  }
  res.res.data = (uint8_t*)uresBuf;
  if (copyToUser(ures, (uint64_t)&res, sizeof(APPLET_RESULT)) == FAIL) return SYS_FAIL;
  if (res.status == APPLET_DONE) {
    // remove result from queue, must not fail
    kAppletRecycle(&req);
  }
  return SYS_SUCCESS;
}

uint64_t sys_appletInspectStorage(uint64_t ureq, uint64_t ures) {
  APPLET_STORAGE_REQ req;
  APPLET_STORAGE res;
  if (checkVrange(ures, sizeof(APPLET_STORAGE), PDE64_USER | PDE64_RW) == FAIL) return SYS_FAIL;
  if (copyFromUser((uint64_t)&req, ureq, sizeof(APPLET_STORAGE_REQ)) == FAIL) return SYS_FAIL;
  if (kAppletStorage(&req, &res) == FAIL) return SYS_FAIL;
  if (copyToUser(ures, (uint64_t)&res, sizeof(APPLET_STORAGE)) == FAIL) return SYS_FAIL;
  return SYS_SUCCESS;
}

uint64_t sys_flag() {
  hp_userspaceFlag();
  return SYS_SUCCESS;
}

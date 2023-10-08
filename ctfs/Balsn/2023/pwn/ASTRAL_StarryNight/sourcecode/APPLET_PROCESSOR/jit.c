#include "jit.h"

void runBasicBlock(APPLET_CONTEXT *appletContext, HOST_CONTEXT *hostContext) {
  BASIC_BLOCK_ARG bbArg = {
    .appletContext = appletContext,
    .hostContext = hostContext,
    .jitAddr = appletContext->basicBlockJitAddr[APPLET_CODE_OFFSET(appletContext->regs[APPLET_PC])]
  };
  asm(
    "push %[bbArg];"
    "push rax;"
    "push rdi;"
    "mov rax, [rsp + 0x10];"
    "mov rdi, [rax + 0x10];" //bbArg.jitAddr
    "mov [rsp + 0x10], rdi;"
    "mov rdi, [rax + 0x08];" //bbArg.appletContext
    "mov rax, [rax + 0x00];" //bbArg.hostContext
    "mov [rax + 0x30], rsi;"
    "pop rsi;"
    "mov [rax + 0x38], rsi;"
    "pop rsi;"
    "mov [rax + 0x00], rsi;"
    "push rax;"
    "push rdi;"
    "push 0;" //placeholder to store next block addr
    "lea rsi, [rdi + 0x80];" //appletContext->memory
    "push rsi;" //pointer to memory in APPLET_CONTEXT
    "lea rsi, [rdi + 0xd080];" //appletContext->exitReason
    "push rsi;" //pointer to exit reason in APPLET_CONTEXT
    "mov [rax + 0x08], rcx;"
    "mov [rax + 0x10], rdx;"
    "mov [rax + 0x18], rbx;"
    "mov [rax + 0x20], rsp;"
    "mov [rax + 0x28], rbp;"
    "mov [rax + 0x40], r8;"
    "mov [rax + 0x48], r9;"
    "mov [rax + 0x50], r10;"
    "mov [rax + 0x58], r11;"
    "mov [rax + 0x60], r12;"
    "mov [rax + 0x68], r13;"
    "mov [rax + 0x70], r14;"
    "mov [rax + 0x78], r15;"
    //We don't clobber rsp here for jit simplicity. To manage this, do not map pc to a real register,
    //This is doable since direct modifications of pc is prohibited, and all relative addr insn could be compiled at jit time
    "mov rax, [rdi + 0x00];"
    "mov rcx, [rdi + 0x08];"
    "mov rdx, [rdi + 0x10];"
    "mov rbx, [rdi + 0x18];"
    "mov rbp, [rdi + 0x28];"
    "mov rsi, [rdi + 0x30];"
    "mov r8,  [rdi + 0x40];"
    "mov r9,  [rdi + 0x48];"
    "mov r10, [rdi + 0x50];"
    "mov r11, [rdi + 0x58];"
    "mov r12, [rdi + 0x60];"
    "mov r13, [rdi + 0x68];"
    "mov r14, [rdi + 0x70];"
    "mov r15, [rdi + 0x78];"
    "mov rdi, [rdi + 0x38];"
    //At this point, stack should be [&g_appletContext.exitReason, g_appletContext.memory, g_appletContext, g_hostContext, jitAddr]
    "call [rsp + 0x28];"
    //save APPLET_CONTEXT registers
    "push rax;"
    "mov rax, [rsp + 0x20];"
    "mov [rax + 0x38], rdi;"
    "pop rdi;"
    "mov [rax + 0x00], rdi;"
    "mov [rax + 0x08], rcx;"
    "mov [rax + 0x10], rdx;"
    "mov [rax + 0x18], rbx;"
    "mov [rax + 0x28], rbp;"
    "mov [rax + 0x30], rsi;"
    "mov [rax + 0x40], r8;"
    "mov [rax + 0x48], r9;"
    "mov [rax + 0x50], r10;"
    "mov [rax + 0x58], r11;"
    "mov [rax + 0x60], r12;"
    "mov [rax + 0x68], r13;"
    "mov [rax + 0x70], r14;"
    "mov [rax + 0x78], r15;"
    "pop rdi;"
    "pop rdi;"
    "pop rdi;"
    "mov [rax + 0x20], rdi;" //save next pc into APPLET_CONTEXT
    //load HOST_CONTEXT registers
    "pop rax;"
    "pop rax;" //load g_hostContext
    "pop rdi;" //get rid of jitAddr on stack
    "mov rcx, [rax + 0x08];"
    "mov rdx, [rax + 0x10];"
    "mov rbx, [rax + 0x18];"
    "mov rbp, [rax + 0x28];"
    "mov rsi, [rax + 0x30];"
    "mov rdi, [rax + 0x38];"
    "mov r8,  [rax + 0x40];"
    "mov r9,  [rax + 0x48];"
    "mov r10, [rax + 0x50];"
    "mov r11, [rax + 0x58];"
    "mov r12, [rax + 0x60];"
    "mov r13, [rax + 0x68];"
    "mov r14, [rax + 0x70];"
    "mov r15, [rax + 0x78];"
    "mov rax, [rax + 0x00];"
    :
    : [bbArg] "r" (&bbArg)
    :
  );
  return;
}

uint64_t translateMem(uint64_t addr, uint64_t size, uint64_t *idx) {
  uint64_t region = REGION_IDX(addr);
  uint64_t offset = REGION_OFFSET(addr);
  if ((region >= REGION_CNT) || (offset + size > REGION_SIZE)) return FAIL;
  *idx = region * REGION_SIZE + offset;
  return SUCCESS;
}

uint64_t getMem(APPLET_CONTEXT *appletContext, uint64_t addr, uint64_t size, uint64_t *val) {
  uint64_t offset;
  if (size == 0 || size > 8) return FAIL;
  if (translateMem(addr, size, &offset) == FAIL) return FAIL;
  *val = 0;
  for (int i = size - 1; i >= 0; i--) {
    *val = (*val << 8) + appletContext->memory[offset + i];
  }
  return SUCCESS;
}

uint64_t setMem(APPLET_CONTEXT *appletContext, uint64_t addr, uint8_t *src, uint64_t size) {
  uint64_t offset;
  if (translateMem(addr, size, &offset) == FAIL) return FAIL;
  memcpy(&appletContext->memory[offset], src, size);
  return SUCCESS;
}

void flushBasicBlockTable(APPLET_CONTEXT *appletContext) {
  mprotect(appletContext->jitBuf, JIT_BUF_SIZE, PROT_READ | PROT_WRITE);
  for (uint64_t i = 0; i < APPLET_CODE_SIZE; i++) {
    appletContext->basicBlockJitAddr[i] = JIT_NIL;
  }
  return;
}

void jitBasicBlock(APPLET_CONTEXT *appletContext) {
  uint64_t opcode, r1, r2, imm, pc = appletContext->regs[APPLET_PC];
  appletContext->basicBlockJitAddr[APPLET_CODE_OFFSET(pc)] = (uint64_t)(&appletContext->jitBuf[appletContext->jitBufCursor]);
  mprotect(appletContext->jitBuf, JIT_BUF_SIZE, PROT_READ | PROT_WRITE);
  if (appletContext->jitBufCursor >= JIT_BUF_SIZE - JIT_BUF_PRESERVE) {
    flushBasicBlockTable(appletContext);
  }
  while (getMem(appletContext, pc, 1, &opcode) != FAIL) {
    if        ((opcode >= 0x08) && (opcode < 0x10))  {
      if (getMem(appletContext, pc + 1, (opcode & 7) + 1, &imm) == FAIL) break;
      pc += 1 + (opcode & 7) + 1;
      PUSH_IMM(appletContext, pc, imm, (opcode & 7) + 1);
    } else if ((opcode >= 0x10) && (opcode < 0x20))  {
      if (getMem(appletContext, pc + 1, 1, &r1) == FAIL) break;
      r1 &= 0xf;
      if ((r1 == APPLET_PC) || (r1 == APPLET_LR)) break;
      pc += 2;
      if ((opcode & 8) == 0) {
        POP(appletContext, pc, r1, (opcode & 7) + 1);
      } else {
        PUSH(appletContext, pc, r1, (opcode & 7) + 1);
      }
    } else if ((opcode >= 0x20) && (opcode < 0x30))  {
      if (getMem(appletContext, pc + 1, 1, &r1) == FAIL) break;
      r2 = r1 >> 4;
      r1 &= 0xf;
      if ((r1 == APPLET_PC) || (r1 == APPLET_LR) || (r2 == APPLET_PC) || (r2 == APPLET_LR)) break;
      pc += 2;
      if ((opcode & 8) == 0) {
        MEM_LOAD(appletContext, pc, r1, r2, (opcode & 7) + 1);
      } else {
        MEM_STORE(appletContext, pc, r1, r2, (opcode & 7) + 1, 0);
      }
    } else if ((opcode >= 0x30) && (opcode < 0x40))  {
      if (getMem(appletContext, pc + 1, 1, &r1) == FAIL) break;
      if (getMem(appletContext, pc + 2, (opcode & 7) + 1, &imm) == FAIL) break;
      r1 &= 0xf;
      if ((r1 == APPLET_PC) || (r1 == APPLET_LR)) break;
      pc += 2 + (opcode & 7) + 1;
      if ((opcode & 8) == 0) {
        IMM_LOAD(appletContext, r1, imm);
      } else {
        MEM_STORE_IMM(appletContext, pc, r1, imm, (opcode & 7) + 1);
      }
    } else if ((opcode >= 0x40) && (opcode < 0x48))  {
      if (getMem(appletContext, pc + 1, 2, &imm) == FAIL) break;
      pc += 3;
      if (imm & 0x8000) {
        imm = pc + imm - 0x10000;
      } else {
        imm = pc + imm;
      }
      switch(opcode) {
        case 0x40:
          PUSH(appletContext, pc, APPLET_LR, 6);
          PUSH(appletContext, pc, APPLET_BP, 6);
          REG_OPS(appletContext, OP_MOV, APPLET_BP, APPLET_SP);
          IMM_LOAD(appletContext, APPLET_LR, pc);
          /* fall through */
        case 0x41:
          COND_BRANCH(appletContext, pc, imm, 0, false, true);
          break;
        case 0x42:
          COND_BRANCH(appletContext, pc, imm, 4, false, false);
          break;
        case 0x43:
          COND_BRANCH(appletContext, pc, imm, 3, false, false);
          break;
        case 0x44:
          COND_BRANCH(appletContext, pc, imm, 1, false, false);
          break;
        case 0x45:
          COND_BRANCH(appletContext, pc, imm, 1, true, false);
          break;
        case 0x46:
          COND_BRANCH(appletContext, pc, imm, 5, false, false);
          break;
        case 0x47:
          COND_BRANCH(appletContext, pc, imm, 2, false, false);
          break;
      }
      goto BLOCK_DONE;
    } else if ((opcode >= 0x50) && (opcode < 0x5b))  {
      if (getMem(appletContext, pc + 1, 1, &r1) == FAIL) break;
      r2 = r1 >> 4;
      r1 &= 0xf;
      if ((r1 == APPLET_PC) || (r1 == APPLET_LR) || (r2 == APPLET_PC) || (r2 == APPLET_LR)) break;
      pc += 2;
      switch(opcode) {
        case 0x50:
          REG_OPS(appletContext, OP_ADD, r1, r2);
          break;
        case 0x51:
          REG_OPS(appletContext, OP_SUB, r1, r2);
          break;
        case 0x52:
          REG_MULDIV(appletContext, pc, r1, r2, false);
          break;
        case 0x53:
          REG_MULDIV(appletContext, pc, r1, r2, true);
          break;
        case 0x54:
          REG_OPS(appletContext, OP_AND, r1, r2);
          break;
        case 0x55:
          REG_OPS(appletContext, OP_OR, r1, r2);
          break;
        case 0x56:
          REG_OPS(appletContext, OP_XOR, r1, r2);
          break;
        case 0x57:
          REG_SHIFT(appletContext, r1, r2, true);
          break;
        case 0x58:
          REG_SHIFT(appletContext, r1, r2, false);
          break;
        case 0x59:
          REG_OPS(appletContext, OP_MOV, r1, r2);
          break;
        case 0x5a:
          REG_CMP(appletContext, r1, r2);
          break;
      }
    } else if ((opcode >= 0xfd) && (opcode < 0x100)) {
      pc += 1;
      SET_EXIT_REASON(appletContext, opcode - 0xfc);
      if (opcode == 0xfd) {
        REG_OPS(appletContext, OP_MOV, APPLET_SP, APPLET_BP);
        POP(appletContext, pc, APPLET_BP, 6);
        EMIT(appletContext, "\x48\x89\x6c\x24\x18", 5); /* mov [rsp + 0x18], lr */
        POP(appletContext, pc, APPLET_LR, 6);
      } else {
        SET_RESUME_ADDR(appletContext, pc);
      }
      goto BLOCK_DONE;
    } else                                           {
      break;
    }
    if (appletContext->jitBufCursor >= JIT_BUF_SIZE - JIT_BUF_PRESERVE) {
      SET_EXIT_REASON(appletContext, EXIT_NEXT);
      SET_RESUME_ADDR(appletContext, pc);
      goto BLOCK_DONE;
    }
  }
  SET_EXIT_REASON(appletContext, EXIT_DONE);
  SET_RESUME_ADDR(appletContext, pc);
BLOCK_DONE:
  EMIT(appletContext, "\xc3", 1); /* ret */
  mprotect(appletContext->jitBuf, JIT_BUF_SIZE, PROT_READ | PROT_EXEC);
  return;
}

void initAppletContext(APPLET_CONTEXT *appletContext) {
  appletContext->jitBuf = NULL;
  return;
}

uint64_t resetAppletContext(APPLET_CONTEXT *appletContext) {
  void *jitBuf = NULL;
  if (appletContext->jitBuf != NULL) {
    jitBuf = appletContext->jitBuf;
  }
  memset(appletContext, '\0', sizeof(APPLET_CONTEXT));
  if (jitBuf != NULL) {
    appletContext->jitBuf = jitBuf;
  } else {
    appletContext->jitBuf = mmap(NULL, JIT_BUF_SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
  }
  if (appletContext->jitBuf == (void*)-1) return FAIL;
  flushBasicBlockTable(appletContext);
  appletContext->regs[APPLET_PC] = APPLET_CODE_SEG_ADDR;
  appletContext->regs[APPLET_LR] = 0xffffffffffffffff;
  appletContext->regs[APPLET_SP] = APPLET_STACK_SEG_ADDR + APPLET_STACK_SIZE;
  appletContext->regs[APPLET_BP] = APPLET_STACK_SEG_ADDR + APPLET_STACK_SIZE;
  return SUCCESS;
}

//the caller is responsible for setting up appletContext + verifying passed parameters
void runApplet(APPLET_CONTEXT *appletContext, SNAPSHOT *snapshot, void (*callback)(SNAPSHOT *snapshot)) {
  HOST_CONTEXT hostContext;
  jitBasicBlock(appletContext);
  while (true) {
    runBasicBlock(appletContext, &hostContext);
    switch(appletContext->exitReason) {
      case EXIT_NEXT:
        if (callback != NULL) {
          callback(snapshot);
        }
        if (appletContext->basicBlockJitAddr[APPLET_CODE_OFFSET(appletContext->regs[APPLET_PC])] == JIT_NIL) {
          jitBasicBlock(appletContext);
        }
        break;
      case EXIT_INVOKE:
      case EXIT_DONE:
        return;
      default:
        appletContext->exitReason = EXIT_DONE;
        return;
    }
  }
}

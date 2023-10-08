#ifndef __JIT_HEADER__
#define __JIT_HEADER__

#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <sys/mman.h>
#include "device.h"
#include "snapshot.h"

#define SUCCESS 0
#define FAIL 0xffffffffffffffff

#define APPLET_REG_CNT 0x10
#define APPLET_RES_ADDR 0
#define APPLET_RES_LEN 1
#define APPLET_INVOKE_RES_ADDR 3
#define APPLET_PC 4
#define APPLET_LR 5
#define APPLET_INP_LEN 11
#define APPLET_CALLER 12
#define APPLET_FLAG 13
#define APPLET_SP 14
#define APPLET_BP 15

#define APPLET_FAIL 0

#define APPLET_INPUT_SEG_ADDR 0x000000000
#define APPLET_STORAGE_SEG_ADDR 0x100000000
#define APPLET_CODE_SEG_ADDR 0x200000000
#define APPLET_STACK_SEG_ADDR 0x300000000
#define APPLET_GENERAL_SEG_ADDR 0x400000000
#define APPLET_CONTEXT_MEMORY_SIZE 0x5000

#define APPLET_CODE_SIZE 0x1000
#define APPLET_STACK_SIZE 0x1000
#define APPLET_CODE_OFFSET(addr) ((addr) & (APPLET_CODE_SIZE - 1))

#define REGION_CNT 5
#define REGION_SHIFT 32
#define REGION_SIZE 0x1000
#define REGION_IDX(addr) ((addr) >> REGION_SHIFT)
#define REGION_MASK ((1ULL << REGION_SHIFT) - 1)
#define REGION_OFFSET(addr) ((addr) & REGION_MASK)

#define JIT_NIL 0

#define JIT_BUF_SIZE 0x2000000
#define JIT_BUF_PRESERVE 0x800

#define EXIT_NEXT 1
#define EXIT_INVOKE 2
#define EXIT_DONE 3

#define REG_RAX 0
#define REG_RCX 1
#define REG_RDX 2

#define COND_JB 2
#define COND_JNE 5
#define COND_JBE 6

#define OP_ADD 0x01
#define OP_SUB 0x29
#define OP_AND 0x21
#define OP_OR  0x09
#define OP_XOR 0x31
#define OP_MOV 0x89
#define OP_CMP 0x39

#define EMIT(_APPLET_CONTEXT, _CODE, _CODE_LEN) { \
  memcpy(&((_APPLET_CONTEXT)->jitBuf[(_APPLET_CONTEXT)->jitBufCursor]), _CODE, _CODE_LEN); \
  (_APPLET_CONTEXT)->jitBufCursor += _CODE_LEN; \
}

// push reg
#define HOST_PUSH_REG(_APPLET_CONTEXT, _REG) { \
  uint64_t HPU_asmByte = 0x50 | (_REG & 7); \
  if (_REG & 8) { \
    EMIT(_APPLET_CONTEXT, "\x41", 1); \
  } \
  EMIT(_APPLET_CONTEXT, &HPU_asmByte, 1); \
}

// pop reg
#define HOST_POP_REG(_APPLET_CONTEXT, _REG) { \
  uint64_t HPO_asmByte = 0x58 | (_REG & 7); \
  if (_REG & 8) { \
    EMIT(_APPLET_CONTEXT, "\x41", 1); \
  } \
  EMIT(_APPLET_CONTEXT, &HPO_asmByte, 1); \
} \

// appletContext->exitReason = reason
#define SET_EXIT_REASON(_APPLET_CONTEXT, _REASON) { \
  uint64_t SER_asmByte = 0x0000000000c7 | ((_REASON) << 16); \
  HOST_PUSH_REG(_APPLET_CONTEXT, REG_RAX);                    /* push rax */ \
  EMIT(_APPLET_CONTEXT, "\x48\x8b\x44\x24\x10", 5);           /* mov rax, [rsp + 0x10] */ \
  EMIT(_APPLET_CONTEXT, &SER_asmByte, 6);                     /* mov [rax], _REASON */ \
  HOST_POP_REG(_APPLET_CONTEXT, REG_RAX);                     /* pop rax */ \
}

// resumeAddr = const
#define SET_RESUME_ADDR(_APPLET_CONTEXT, _NEXT_PC) { \
  uint64_t SRA_asmByte = _NEXT_PC; \
  HOST_PUSH_REG(_APPLET_CONTEXT, REG_RAX);                    /* push rax */ \
  EMIT(_APPLET_CONTEXT, "\x48\xb8", 2); \
  EMIT(_APPLET_CONTEXT, &SRA_asmByte, 8);                     /* mov rax, _VAL */ \
  EMIT(_APPLET_CONTEXT, "\x48\x89\x44\x24\x20", 5);           /* mov [rsp + 0x20], rax */ \
  HOST_POP_REG(_APPLET_CONTEXT, REG_RAX);                     /* pop rax */ \
}

// assert reg <cond> val
#define BAILOUT_CHECK(_APPLET_CONTEXT, _PC, _REG, _VAL, _COND, _AUX_CNT) { \
  uint64_t BCH_asmByte; \
  BCH_asmByte = 0x00000000f88148 | ((_VAL) << 24) | (((_REG) & 8) >> 3) | (((_REG) & 7) << 16); \
  EMIT(_APPLET_CONTEXT, &BCH_asmByte, 7);                     /* cmp reg, val */ \
  BCH_asmByte = (0x1f70 | (_COND)) + ((((((_REG) & 8) >> 3) + 1) * (_AUX_CNT)) << 8); \
  EMIT(_APPLET_CONTEXT, &BCH_asmByte, 2);                     /* j<cond> CHECK_PASS */ \
  for (uint64_t i = (_AUX_CNT); i > 0; i--) { \
    HOST_POP_REG(_APPLET_CONTEXT, _REG);                      /* pop reg1 */ \
  } \
  SET_EXIT_REASON(_APPLET_CONTEXT, EXIT_DONE);                /* appletContext->exitReason = EXIT_DONE */ \
  SET_RESUME_ADDR(_APPLET_CONTEXT, _PC);                      /* resumeAddr = pc */ \
  EMIT(_APPLET_CONTEXT, "\xc3", 1);                           /* ret */ \
                                                              /* CHECK_PASS: */ \
}

// op reg1, reg2
#define REG_OPS(_APPLET_CONTEXT, _OP, _REG1, _REG2) { \
  uint64_t RPS_asmByte = 0xc00048 | ((_OP) << 8) | (((_REG1) & 8) >> 3) | (((_REG1) & 7) << 16) | (((_REG2) & 8) >> 1) | (((_REG2) & 7) << 19); \
  EMIT(_APPLET_CONTEXT, &RPS_asmByte, 3); \
}

// shl / shr reg1, reg2
#define REG_SHIFT(_APPLET_CONTEXT, _REG1, _REG2, _SHIFT_RIGHT) { \
  uint64_t RSH_asmByte; \
  if ((_REG2) != REG_RCX && (_REG1) == REG_RCX) { \
    REG_OPS(_APPLET_CONTEXT, OP_XOR, _REG1, _REG2);           /* xor reg1, reg2 */ \
    REG_OPS(_APPLET_CONTEXT, OP_XOR, _REG2, _REG1);           /* xor reg2, reg1 */ \
    REG_OPS(_APPLET_CONTEXT, OP_XOR, _REG1, _REG2);           /* xor reg1, reg2 */ \
    RSH_asmByte = 0xe0d348 | ((_SHIFT_RIGHT) ? 0x80000 : 0) | (((_REG2) & 8) >> 3) | (((_REG2) & 7) << 16); \
    EMIT(_APPLET_CONTEXT, &RSH_asmByte, 3);                   /* shl / shr reg2, cl */ \
    REG_OPS(_APPLET_CONTEXT, OP_XOR, _REG1, _REG2);           /* xor reg1, reg2 */ \
    REG_OPS(_APPLET_CONTEXT, OP_XOR, _REG2, _REG1);           /* xor reg2, reg1 */ \
    REG_OPS(_APPLET_CONTEXT, OP_XOR, _REG1, _REG2);           /* xor reg1, reg2 */ \
  } else { \
    HOST_PUSH_REG(_APPLET_CONTEXT, REG_RCX);                  /* push rcx */ \
    REG_OPS(_APPLET_CONTEXT, OP_MOV, REG_RCX, _REG2);         /* mov rcx, reg2 */ \
    RSH_asmByte = 0xe0d348 | ((_SHIFT_RIGHT) ? 0x80000 : 0) | (((_REG1) & 8) >> 3) | (((_REG1) & 7) << 16); \
    EMIT(_APPLET_CONTEXT, &RSH_asmByte, 3);                   /* shl / shr reg1, cl */ \
    HOST_POP_REG(_APPLET_CONTEXT, REG_RCX);                   /* pop rcx */ \
  } \
}

// mul / div reg1, reg2
#define REG_MULDIV(_APPLET_CONTEXT, _PC, _REG1, _REG2, _DIV) { \
  uint64_t RMD_asmByte = 0xe1f748 | ((_DIV) ? 0x100000 : 0); \
  if (_DIV) { \
    BAILOUT_CHECK(_APPLET_CONTEXT, _PC, _REG2, 0, COND_JNE, 0); /* assert reg2 != 0 */ \
  } \
  if ((_REG1) != REG_RAX) { \
    HOST_PUSH_REG(_APPLET_CONTEXT, REG_RAX);                  /* push rax */ \
  } \
  if ((_REG1) != REG_RDX) { \
    HOST_PUSH_REG(_APPLET_CONTEXT, REG_RDX);                  /* push rdx */ \
  } \
  if ((_REG2) == REG_RAX) { \
    if ((_REG1) == REG_RCX) { \
      REG_OPS(_APPLET_CONTEXT, OP_XOR, _REG1, _REG2);         /* xor reg1, reg2 */ \
      REG_OPS(_APPLET_CONTEXT, OP_XOR, _REG2, _REG1);         /* xor reg2, reg1 */ \
      REG_OPS(_APPLET_CONTEXT, OP_XOR, _REG1, _REG2);         /* xor reg1, reg2 */ \
    } else { \
      HOST_PUSH_REG(_APPLET_CONTEXT, REG_RCX);                /* push rcx */ \
      REG_OPS(_APPLET_CONTEXT, OP_MOV, REG_RCX, _REG2);       /* mov rcx, reg2 */ \
      REG_OPS(_APPLET_CONTEXT, OP_MOV, REG_RAX, _REG1);       /* mov rax, reg1 */ \
    } \
  } else { \
    REG_OPS(_APPLET_CONTEXT, OP_MOV, REG_RAX, _REG1);         /* mov rax, reg1 */ \
    HOST_PUSH_REG(_APPLET_CONTEXT, REG_RCX);                  /* push rcx */ \
    REG_OPS(_APPLET_CONTEXT, OP_MOV, REG_RCX, _REG2);         /* mov rcx, reg2 */ \
  } \
  if (_DIV) { \
    REG_OPS(_APPLET_CONTEXT, OP_XOR, REG_RDX, REG_RDX);       /* xor rdx, rdx */ \
  } \
  RMD_asmByte = 0xe1f748 | ((_DIV) ? 0x100000 : 0); \
  EMIT(_APPLET_CONTEXT, &RMD_asmByte, 3);                     /* mul / div rcx */ \
  if ((_REG1) != REG_RCX || (_REG2) != REG_RAX) { \
    HOST_POP_REG(_APPLET_CONTEXT, REG_RCX);                   /* pop rcx */ \
  } \
  if ((_REG1) != REG_RDX) { \
    HOST_POP_REG(_APPLET_CONTEXT, REG_RDX);                   /* pop rdx */ \
  } \
  if ((_REG1) != REG_RAX) { \
    REG_OPS(_APPLET_CONTEXT, OP_MOV, _REG1, REG_RAX);         /* mov reg1, rax */ \
    HOST_POP_REG(_APPLET_CONTEXT, REG_RAX);                   /* pop rax */ \
  } \
}

#define REG_CMP(_APPLET_CONTEXT, _REG1, _REG2) { \
  HOST_PUSH_REG(_APPLET_CONTEXT, REG_RAX);                    /* push rax */ \
  HOST_PUSH_REG(_APPLET_CONTEXT, REG_RDX);                    /* push rdx */ \
  REG_OPS(_APPLET_CONTEXT, OP_CMP, _REG1, _REG2);             /* cmp reg1, reg2 */ \
  EMIT(_APPLET_CONTEXT, "\x41\x0f\x92\xc5", 4);               /* setb flag */ \
  EMIT(_APPLET_CONTEXT, "\x0f\x97\xc0", 3);                   /* seta al */ \
  EMIT(_APPLET_CONTEXT, "\x0f\x94\xc2", 3);                   /* sete dl */ \
  EMIT(_APPLET_CONTEXT, "\x49\xc1\xe5\x02", 4);               /* shl flag, 2 */ \
  EMIT(_APPLET_CONTEXT, "\x48\xd1\xe0", 3);                   /* shl rax, 1 */ \
  REG_OPS(_APPLET_CONTEXT, OP_OR, APPLET_FLAG, REG_RAX);      /* or flag, rax */ \
  REG_OPS(_APPLET_CONTEXT, OP_OR, APPLET_FLAG, REG_RDX);      /* or flag, rdx */ \
  EMIT(_APPLET_CONTEXT, "\x49\xc1\xe5\x3d", 4);               /* shl flag, 61 */ \
  EMIT(_APPLET_CONTEXT, "\x49\xc1\xed\x3d", 4);               /* shr flag, 61 */ \
  HOST_POP_REG(_APPLET_CONTEXT, REG_RDX);                     /* pop rdx */ \
  HOST_POP_REG(_APPLET_CONTEXT, REG_RAX);                     /* pop rax */ \
}

#define COND_BRANCH(_APPLET_CONTEXT, _PC, _TARGET, _FLAGMASK, _NOTSET, _UNCOND) { \
  uint64_t CBR_asmByte; \
  SET_EXIT_REASON(_APPLET_CONTEXT, EXIT_NEXT);                /* appletContext->exitReason = EXIT_NEXT */ \
  if (!(_UNCOND)) { \
    HOST_PUSH_REG(_APPLET_CONTEXT, REG_RAX);                  /* push rax */ \
    HOST_PUSH_REG(_APPLET_CONTEXT, APPLET_FLAG);              /* push flag */ \
    IMM_LOAD(_APPLET_CONTEXT, REG_RAX, _TARGET);              /* mov rax, target */ \
    CBR_asmByte = 0x00e58349 | ((_FLAGMASK) << 24); \
    EMIT(_APPLET_CONTEXT, &CBR_asmByte, 4);                   /* and flag, flagMask */ \
    IMM_LOAD(_APPLET_CONTEXT, APPLET_FLAG, _PC);              /* mov flag, pc */ \
    if (_NOTSET) { \
      EMIT(_APPLET_CONTEXT, "\x49\x0f\x45\xc5", 4);           /* cmovnz rax, flag */ \
    } else { \
      EMIT(_APPLET_CONTEXT, "\x49\x0f\x44\xc5", 4);           /* cmovz rax, flag */ \
    } \
    HOST_POP_REG(_APPLET_CONTEXT, APPLET_FLAG);               /* pop flag */ \
    EMIT(_APPLET_CONTEXT, "\x48\x89\x44\x24\x20", 5);         /* mov [rsp + 0x20] (resumeAddr), rax */ \
    HOST_POP_REG(_APPLET_CONTEXT, REG_RAX);                   /* pop rax */ \
  } else { \
    SET_RESUME_ADDR(_APPLET_CONTEXT, _TARGET);                /* resumeAddr = pc */ \
  } \
}

// requires that no additional registers are pushed on stack when invoked
// translate reg to host address + push original reg onto stack (for later restore)
#define MEM_TRANSLATE(_APPLET_CONTEXT, _PC, _REG, _SIZE) { \
  uint64_t MTR_asmByte; \
  HOST_PUSH_REG(_APPLET_CONTEXT, _REG);                       /* push reg */ \
  MTR_asmByte = 0x20e8c148 | (((_REG) & 8) >> 3) | (((_REG) & 7) << 16); \
  EMIT(_APPLET_CONTEXT, &MTR_asmByte, 4);                     /* shr reg, 32 */ \
  MTR_asmByte = 0x0ce0c148 | (((_REG) & 8) >> 3) | (((_REG) & 7) << 16); \
  EMIT(_APPLET_CONTEXT, &MTR_asmByte, 4);                     /* shl reg, 12 */ \
  BAILOUT_CHECK(_APPLET_CONTEXT, _PC, _REG, 0x5000ULL, COND_JB, 1);  /* assert reg < 0x5000 */ \
  \
  MTR_asmByte = 0x1824440348 | (((_REG) & 8) >> 1) | (((_REG) & 7) << 19); \
  EMIT(_APPLET_CONTEXT, &MTR_asmByte, 5);                     /* add reg, [rsp + 0x18] (appletContext->memory) */ \
  HOST_PUSH_REG(_APPLET_CONTEXT, _REG);                       /* push reg */ \
  MTR_asmByte = 0x0824448b48 | (((_REG) & 8) >> 1) | (((_REG) & 7) << 19); \
  EMIT(_APPLET_CONTEXT, &MTR_asmByte, 5);                     /* mov reg, [rsp + 0x08] (original reg) */ \
  MTR_asmByte = 0x20e0c148 | (((_REG) & 8) >> 3) | (((_REG) & 7) << 16); \
  EMIT(_APPLET_CONTEXT, &MTR_asmByte, 4);                     /* shl reg, 0x20 */ \
  MTR_asmByte = 0x20e8c148 | (((_REG) & 8) >> 3) | (((_REG) & 7) << 16); \
  EMIT(_APPLET_CONTEXT, &MTR_asmByte, 4);                     /* shr reg, 0x20 */ \
  BAILOUT_CHECK(_APPLET_CONTEXT, _PC, _REG, 0x1000ULL, COND_JB, 2);  /* assert reg < 0x1000 */ \
  \
  HOST_PUSH_REG(_APPLET_CONTEXT, _REG);                       /* push reg */ \
  MTR_asmByte = 0x00c08348 | ((_SIZE) << 24) | (((_REG) & 8) >> 3) | (((_REG) & 7) << 16); \
  EMIT(_APPLET_CONTEXT, &MTR_asmByte, 4);                     /* add reg, size */ \
  BAILOUT_CHECK(_APPLET_CONTEXT, _PC, _REG, 0x1000ULL, COND_JBE, 3); /* assert reg <= 0x1000 */ \
  \
  HOST_POP_REG(_APPLET_CONTEXT, _REG);                        /* pop reg (region offset) */ \
  MTR_asmByte = 0x0024440348 | (((_REG) & 8) >> 1) | (((_REG) & 7) << 19); \
  EMIT(_APPLET_CONTEXT, &MTR_asmByte, 5);                     /* add reg, [rsp] (&appletContext->memory[region]) */ \
  EMIT(_APPLET_CONTEXT, "\x48\x83\xc4\x08", 4);               /* add rsp, 8 */ \
}

#define MEM_LOAD(_APPLET_CONTEXT, _PC, _REG1, _REG2, _SIZE) { \
  uint64_t MLO_asmByte; \
  MEM_TRANSLATE(_APPLET_CONTEXT, _PC, _REG2, _SIZE); \
  MLO_asmByte = 0x008b48 | (((_REG1) & 8) >> 1) | (((_REG1) & 7) << 19) | (((_REG2) & 8) >> 3) | (((_REG2) & 7) << 16); \
  EMIT(_APPLET_CONTEXT, &MLO_asmByte, 3);                     /* mov reg1, [reg2] */ \
  if ((_SIZE) != 8) { \
    MLO_asmByte = 0x00e0c148 | (((8 - (_SIZE)) * 8) << 24) | (((_REG1) & 8) >> 3) | (((_REG1) & 7) << 16); \
    EMIT(_APPLET_CONTEXT, &MLO_asmByte, 4);                   /* shl reg1, ((8 - size) * 8) */ \
    MLO_asmByte = 0x00e8c148 | (((8 - (_SIZE)) * 8) << 24) | (((_REG1) & 8) >> 3) | (((_REG1) & 7) << 16); \
    EMIT(_APPLET_CONTEXT, &MLO_asmByte, 4);                   /* shr reg1, ((8 - size) * 8) */ \
  } \
  if ((_REG1) == (_REG2)) { \
    EMIT(_APPLET_CONTEXT, "\x48\x83\xc4\x08", 4);             /* add rsp, 8 */ \
  } else { \
    HOST_POP_REG(_APPLET_CONTEXT, _REG2);                     /* pop reg2 */ \
  } \
}

//expect original reg1 to be on [rsp + 8] in case reg1 = reg2, clobbers reg2
#define MEM_STORE_UTIL(_APPLET_CONTEXT, _REG1, _REG2, _SIZE, _ADJUST) { \
  uint64_t MSU_asmByte; \
  uint64_t MSU_reg = _REG2; \
  if ((_REG1) == (_REG2)) { \
    if ((_REG1) == REG_RAX) { \
      HOST_PUSH_REG(_APPLET_CONTEXT, REG_RCX);                /* push rcx */ \
      EMIT(_APPLET_CONTEXT, "\x48\x8b\x4c\x24\x10", 5)        /* mov rcx, [rsp + 0x10] */ \
      MSU_reg = REG_RCX; \
    } else { \
      HOST_PUSH_REG(_APPLET_CONTEXT, REG_RAX);                /* push rax */ \
      EMIT(_APPLET_CONTEXT, "\x48\x8b\x44\x24\x10", 5)        /* mov rax, [rsp + 0x10] */ \
      MSU_reg = REG_RAX; \
    } \
  } \
  if (_ADJUST != 0) { \
    MSU_asmByte = 0x00c08348 | ((_ADJUST) << 24) | (((MSU_reg) & 8) >> 3) | (((MSU_reg) & 7) << 16); \
    EMIT(_APPLET_CONTEXT, &MSU_asmByte, 4);                   /* add reg2', adjust (required for push) */ \
  } \
  if ((_SIZE) != 8) { \
    MSU_asmByte = 0x00e0c148 | (((8 - (_SIZE)) * 8) << 24) | (((MSU_reg) & 8) >> 3) | (((MSU_reg) & 7) << 16); \
    EMIT(_APPLET_CONTEXT, &MSU_asmByte, 4);                   /* shl reg2', ((8 - size) * 8) */ \
    MSU_asmByte = 0x00e8c148 | (((8 - (_SIZE)) * 8) << 24) | (((MSU_reg) & 8) >> 3) | (((MSU_reg) & 7) << 16); \
    EMIT(_APPLET_CONTEXT, &MSU_asmByte, 4);                   /* shr reg2', ((8 - size) * 8) */ \
  } \
  MSU_asmByte = 0x003348 | (((MSU_reg) & 8) >> 1) | (((MSU_reg) & 7) << 19) | (((_REG1) & 8) >> 3) | (((_REG1) & 7) << 16); \
  EMIT(_APPLET_CONTEXT, &MSU_asmByte, 3);                     /* xor reg2', [reg1] */ \
  if ((_SIZE) != 8) { \
    MSU_asmByte = 0x00e0c148 | (((8 - (_SIZE)) * 8) << 24) | (((MSU_reg) & 8) >> 3) | (((MSU_reg) & 7) << 16); \
    EMIT(_APPLET_CONTEXT, &MSU_asmByte, 4);                   /* shl reg2', ((8 - size) * 8) */ \
    MSU_asmByte = 0x00e8c148 | (((8 - (_SIZE)) * 8) << 24) | (((MSU_reg) & 8) >> 3) | (((MSU_reg) & 7) << 16); \
    EMIT(_APPLET_CONTEXT, &MSU_asmByte, 4);                   /* shr reg2', ((8 - size) * 8) */ \
  } \
  MSU_asmByte = 0x003148 | (((_REG1) & 8) >> 3) | (((_REG1) & 7) << 16) | (((MSU_reg) & 8) >> 1) | (((MSU_reg) & 7) << 19); \
  EMIT(_APPLET_CONTEXT, &MSU_asmByte, 3);                     /* xor [reg1], reg2' */ \
  if ((_REG1) == (_REG2)) { \
    if ((_REG1) == REG_RAX) { \
      HOST_POP_REG(_APPLET_CONTEXT, REG_RCX);                 /* pop rcx */ \
    } else { \
      HOST_POP_REG(_APPLET_CONTEXT, REG_RAX);                 /* pop rax */ \
    } \
  } \
}

// store <size> [reg1], reg2
#define MEM_STORE(_APPLET_CONTEXT, _PC, _REG1, _REG2, _SIZE, _ADJUST) { \
  MEM_TRANSLATE(_APPLET_CONTEXT, _PC, _REG1, _SIZE); \
  HOST_PUSH_REG(_APPLET_CONTEXT, _REG2);                      /* push reg2 */ \
  MEM_STORE_UTIL(_APPLET_CONTEXT, _REG1, _REG2, _SIZE, _ADJUST); \
  HOST_POP_REG(_APPLET_CONTEXT, _REG2);                       /* pop reg2 */ \
  HOST_POP_REG(_APPLET_CONTEXT, _REG1);                       /* pop reg1 */ \
}

// load <size> reg, imm
#define IMM_LOAD(_APPLET_CONTEXT, _REG, _VAL) { \
  uint64_t ILO_asmByte; \
  ILO_asmByte = 0xb848 | (((_REG) & 8) >> 3) | (((_REG) & 7) << 8); \
  EMIT(_APPLET_CONTEXT, &ILO_asmByte, 2); \
  ILO_asmByte = _VAL; \
  EMIT(_APPLET_CONTEXT, &ILO_asmByte, 8);                     /* mov reg, val */ \
}

// store <size> [reg], imm
#define MEM_STORE_IMM(_APPLET_CONTEXT, _PC, _REG, _VAL, _SIZE) { \
  MEM_TRANSLATE(_APPLET_CONTEXT, _PC, _REG, _SIZE); \
  if (_REG == REG_RAX) { \
    HOST_PUSH_REG(_APPLET_CONTEXT, REG_RDX);                  /* push rdx */ \
    IMM_LOAD(_APPLET_CONTEXT, REG_RDX, _VAL);                 /* mov rdx, val */ \
    MEM_STORE_UTIL(_APPLET_CONTEXT, _REG, REG_RDX, _SIZE, 0); \
    HOST_POP_REG(_APPLET_CONTEXT, REG_RDX);                   /* pop rdx */ \
  } else { \
    HOST_PUSH_REG(_APPLET_CONTEXT, REG_RAX);                  /* push rax */ \
    IMM_LOAD(_APPLET_CONTEXT, REG_RAX, _VAL);                 /* mov rsx, val */ \
    MEM_STORE_UTIL(_APPLET_CONTEXT, _REG, REG_RAX, _SIZE, 0); \
    HOST_POP_REG(_APPLET_CONTEXT, REG_RAX);                   /* pop rax */ \
  } \
  HOST_POP_REG(_APPLET_CONTEXT, _REG);                        /* pop reg */ \
}

// pop <size> reg
#define POP(_APPLET_CONTEXT, _PC, _REG, _SIZE) { \
  uint64_t POP_asmByte = 0x00c68349 | ((_SIZE) << 24); \
  MEM_LOAD(_APPLET_CONTEXT, _PC, _REG, APPLET_SP, _SIZE); \
  if ((_REG) != APPLET_SP) { \
    EMIT(_APPLET_CONTEXT, &POP_asmByte, 4);                   /* add sp, size */ \
  } \
}

// push <size> reg
#define PUSH(_APPLET_CONTEXT, _PC, _REG, _SIZE) { \
  uint64_t PSH_asmByte = 0x00ee8349 | ((_SIZE) << 24); \
  EMIT(_APPLET_CONTEXT, &PSH_asmByte, 4);                     /* sub sp, size */ \
  MEM_STORE(_APPLET_CONTEXT, _PC, APPLET_SP, _REG, _SIZE, (_REG == APPLET_SP) ? (_SIZE) : 0); \
}

// push <size> imm
#define PUSH_IMM(_APPLET_CONTEXT, _PC, _VAL, _SIZE) { \
  uint64_t PSI_asmByte = 0x00ee8349 | ((_SIZE) << 24); \
  EMIT(_APPLET_CONTEXT, &PSI_asmByte, 4);                     /* sub sp, size */ \
  MEM_TRANSLATE(_APPLET_CONTEXT, _PC, APPLET_SP, _SIZE); \
  HOST_PUSH_REG(_APPLET_CONTEXT, REG_RAX);                    /* push rax */ \
  IMM_LOAD(_APPLET_CONTEXT, REG_RAX, _VAL);                   /* mov rax, val */ \
  MEM_STORE_UTIL(_APPLET_CONTEXT, APPLET_SP, REG_RAX, _SIZE, 0); \
  HOST_POP_REG(_APPLET_CONTEXT, REG_RAX);                     /* pop rax */ \
  HOST_POP_REG(_APPLET_CONTEXT, APPLET_SP);                   /* pop sp */ \
}

typedef struct HOST_CONTEXT {
  uint64_t regs[APPLET_REG_CNT];
} HOST_CONTEXT;

typedef struct APPLET_CONTEXT {
  uint64_t regs[APPLET_REG_CNT];
  uint8_t memory[APPLET_CONTEXT_MEMORY_SIZE];
  uint64_t basicBlockJitAddr[APPLET_CODE_SIZE];
  uint64_t exitReason;
  uint8_t *jitBuf;
  uint64_t jitBufCursor;
} APPLET_CONTEXT;

typedef struct BASIC_BLOCK_ARG {
  HOST_CONTEXT *hostContext;
  APPLET_CONTEXT *appletContext;
  uint64_t jitAddr;
} BASIC_BLOCK_ARG;


void runApplet(APPLET_CONTEXT *appletContext, SNAPSHOT *snapshot, void (*callback)(SNAPSHOT *snapshot));
void initAppletContext(APPLET_CONTEXT *appletContext);
uint64_t resetAppletContext(APPLET_CONTEXT *appletContext);
uint64_t translateMem(uint64_t addr, uint64_t size, uint64_t *idx);
uint64_t setMem(APPLET_CONTEXT *appletContext, uint64_t addr, uint8_t *src, uint64_t size);

#endif

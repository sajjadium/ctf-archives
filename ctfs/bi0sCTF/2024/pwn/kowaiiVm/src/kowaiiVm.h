#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>
#include <string.h>
#include <seccomp.h>
#include <sys/syscall.h>
#include <time.h>
#include <fcntl.h>
#include <iostream>
#include <sstream>
#include <vector>


#define SECCOMP
#define ERROR_CODE        0x45
#define MAX_FUNC_ENTRIES  0x80
#define MAX_FUNC_SIZE     0x100
#define MAX_REGS          0x6
#define MAX_BIN_SIZE      0x10000
#define STACK_SIZE        0x1000
#define BSS_SIZE          0x4000
#define CODE_START_ADDR   0x1000

/* JIT settings*/
#define JIT_SIZE          0x10000       // JIT memory size
#define JIT_CC            0xa           // Call count required to JIT a function
#define JIT_MS            0xa           // Minimum size of function to be JITed


/* Opcodes */
#define ADD               0xb0
#define SUB               0xb1
#define MUL               0xb2
#define SHR               0xb3
#define SHL               0xb4
#define PUSH              0xb5
#define POP               0xb6
#define GET               0xb7
#define SET               0xb8
#define MOV               0xb9
#define CALL              0xba
#define RET               0xbb
#define NOP               0xbc
#define HLT               0xbf

/* JIT Constants */
#define x64_REG           0x2           // since vm regs start at r10 and not r8
#define x64_NOREG         0xffff
#define x64_RAX           0xfff0
#define x64_RCX           0xfff1
#define x64_RDX           0xfff2
#define x64_RBX           0xfff3

#define x64_ADD           0xc0014d      // add        r1X, r1X
#define x64_SUB           0xc0294d      // sub        r1X, r1X
#define x64_MUL           0xe0f749      // mul        r1X, r1X
#define x64_SHR           0xe8d349      // shr        r1X,  cl
#define x64_SHL           0xe0d349      // shl        r1X,  cl
#define x64_PUSH          0x5041        // push       r1X
#define x64_POP           0x5841        // pop        r1X
#define x64_CALLA         0xd0ff        // call       rXx                 
#define x64_MOVNN         0xc0894d      // mov        r1X, r1X
#define x64_MOVAN         0xc0894c      // mov        rXx, r1X
#define x64_MOVALI        0xb0          // mov         Xl, imm
#define x64_MOVAI         0xb848        // mov        rXx, imm
#define x64_MOVNI         0xb841        // mov       r1Xd, imm
#define x64_XCHGAN        0x9049        // xchg       rXx, r1X
#define x64_MOVPN         0x80894c      // mov  [rXx+imm], r1X
#define x64_MOVNP         0x808b4c      // mov        r1X, [rXx+imm] 
#define x64_RET           0xc3          // ret

/* Structs */
typedef unsigned long     u64;
typedef unsigned int      u32;
typedef unsigned short    u16;
typedef unsigned char     u8;

typedef struct __attribute__((__packed__)) kowaiiFuncEntry
{
    u16 hash;
    u64 addr;
    u8 size;
    u8 callCount;
} kowaiiFuncEntry;

typedef struct __attribute__((__packed__)) kowaiiBin
{
    u8 kowaii[6];
    u16 entry;
    u32 magic;
    u16 bss;
    u8 no_funcs;
    kowaiiFuncEntry funct[];
} kowaiiBin;

typedef struct __attribute__((__packed__)) kowaiiRegisters
{
    u64 x[MAX_REGS];
    u8 *pc;
    u64 *sp; 
    u64 *bp;
} kowaiiRegisters;

void error(const char*);
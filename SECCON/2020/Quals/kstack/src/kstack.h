#ifndef PROC_KSTACK
#define PROC_KSTACK

#define CMD_PUSH 0x57ac0001
#define CMD_POP  0x57ac0002

typedef struct _Element {
  int owner;
  unsigned long value;
  struct _Element *fd;
} Element;

#endif

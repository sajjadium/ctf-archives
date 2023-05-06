#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

int32_t readint() {
  uint8_t buf[14] = {};
  for (size_t i = 0; i < 13; i++) {
    if ((buf[i] = getchar()) == -1) exit(1);
    if (buf[i] == '\n') {
      buf[i] = '\0';
      break;
    }
  }
  return atoi(buf);
}

int main() {
  void *op_fp, *read_fp;
  uint64_t operand;
  int32_t r1 = 0, r2 = 0, r3 = 0, a = 0;

  int32_t* readreg() {
    if (getchar() != 'r') exit(1);
    switch (readint()) {
      case 1: return &r1;
      case 2: return &r2;
      case 3: return &r3;
      case 0: return &a;
      default: exit(1);
    }
  }

  uint32_t readimm() {
    if (getchar() != '#') exit(1);
    return readint();
  }

  printf(
    "Welcome to NEMU!\n"
    "We now only have following 6 instructions:\n"
    "     1) LOAD [imm]: Load value [imm] into ACC register\n"
    "     2) MOV  [reg]: Copy data stored in AC register into [reg] register\n"
    "     3) INC  [reg]: Increment the value stored in [reg] register\n"
    "     4) DBL  [reg]: Double the value stored in [reg] register\n"
    "     5) ADDI [imm]: Add value [imm] to the value of ACC register\n"
    "     6) ADD  [reg]: Add value stored in [reg] register to the value of ACC register\n"
  );

  while (1) {
    printf(
      "Current register status: \n"
      "REG1(r1): 0x%08x\n"
      "REG2(r2): 0x%08x\n"
      "REG3(r3): 0x%08x\n"
      " ACC(r0): 0x%08x\n\n",
      r1, r2, r3, a
    );
    printf("opcode: ");
    switch (readint()) {
      case 1: {
        void load(uint64_t imm) { a = imm; }
        op_fp = load;
        read_fp = readimm;
        break;
      }
      case 2: {
        void mov(uint64_t* reg) { *reg = a; }
        op_fp = mov;
        read_fp = readreg;
        break;
      }
      case 3: {
        void inc(uint64_t* reg) { *reg += 1; }
        op_fp = inc;
        read_fp = readreg;
        break;
      }
      case 4: {
        void dbl(uint64_t* reg) { *reg *= 2; }
        op_fp = dbl;
        read_fp = readreg;
        break;
      }
      case 5: {
        void addi(uint64_t imm) { a += imm; }
        op_fp = addi;
        read_fp = readimm;
        break;
      }
      case 6: {
        void add(uint64_t* reg) { a += *reg; }
        op_fp = add;
        read_fp = readreg;
        break;
      }
      default:
        exit(1);
    }
    printf("operand: ");
    ((void (*)(uint64_t))op_fp)(((uint64_t(*)())read_fp)());
  }
}

__attribute__((constructor))
static int init(void) {
  alarm(180);
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  return 0;
}

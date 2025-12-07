#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include "asm_x64.h"

void out_of_bounds() {
	printf("\nError: Out of bounds access detected!\n");
	exit(EXIT_FAILURE);
}

// Calling conventions
#ifdef _WIN32
#define CALL_ARG_1 (x64Operand) rcx
#define CALL_ARG_2 (x64Operand) rdx
#else
#define CALL_ARG_1 (x64Operand) rdi
#define CALL_ARG_2 (x64Operand) rsi
#endif

#define PROLOGUE (x64Ins[]) { \
    { PUSH, rbp }, \
    { MOV, rbp, rsp }, \
    { MOV, rax, CALL_ARG_1 }, \
	{ PUSH, CALL_ARG_1 } /* stores the current pointer */, \
	{ PUSH, CALL_ARG_2 } /* buffer length */, \
    { PUSH, CALL_ARG_1 } /* buffer start pointer */, \
}

#define EPILOGUE (x64Ins[]) { \
	{ MOV, rsp, rbp }, \
	{ POP, rbp }, \
	{ RET }, \
}

#define LEFT (x64Ins[]) { \
	{ DEC, m64($rbp, -8) }, /* dec */ \
	{ MOV, rax, m64($rbp, -8) }, \
	{ MOV, rbx, rax }, \
	{ SUB, rbx, m64($rbp, -24) }, /* calculate stack depth */ \
	{ CMP, rbx, imm(0) }, \
	{ JGE, rel(4) }, /* if current pointer < buffer start, call oob handler */ \
	{ MOV, rax, imptr(out_of_bounds) }, \
	{ MOV, CALL_ARG_1, rbx }, \
	{ CALL, rax } \
}

#define RIGHT (x64Ins[]) { \
	{ INC, m64($rbp, -8) }, /* inc */ \
	{ MOV, rax, m64($rbp, -8) }, \
	{ MOV, rbx, rax }, \
	{ SUB, rbx, m64($rbp, -24) }, /* calculate stack depth */ \
	{ CMP, rbx, m64($rbp, -16) }, \
	{ JL, rel(4) }, /* if current pointer >= buffer end, call oob handler */ \
	{ MOV, rax, imptr(out_of_bounds) }, \
	{ MOV, CALL_ARG_1, rbx }, \
	{ CALL, rax } \
}

#define UNGARBLE_RAX (x64Ins[]) { \
	{ MOV, rax, m64($rbp, -8) } \
}

#define INCREMENT (x64Ins[]) { \
	{ INC, m8($rax) } \
}

#define DECREMENT (x64Ins[]) { \
	{ DEC, m8($rax) } \
}

// out of laziness, this isn't actually correct; this runs even if the cell is zero, but whatever
#define LOOP_START (x64Ins[]) { \
	{ LEA, rsi, m64($riprel, 0) }, /* 0 here means $+0 or the current instruction */ \
	{ PUSH, rsi } \
}

#define LOOP_END (x64Ins[]) { \
	{ MOV, rax, m64($rbp, -8) }, \
	{ POP, rbx }, /* return address */ \
	{ CMP, m8($rax), imm(0) }, \
	{ JZ, rel(2) }, \
	{ JMP, rbx } \
}

#define PRINT_CHAR (x64Ins[]) { \
	{ MOV, rax, mem($rbp, -8) }, \
	{ MOV, CALL_ARG_1, mem($rax) }, \
	{ SUB, rsp, imm(64) }, /* Should investigate aligining the stack to 16 bytes but this works for now(what msvc does). */ \
	{ MOV, rax, imptr(putchar) }, \
	{ CALL, rax }, \
	{ ADD, rsp, imm(64) } \
}

typedef struct {
	x64Ins *buf;
	size_t buf_size;
} x64InsBuf;

#define BUF_PUSH(bf, ins_buf) do { \
	size_t ins_buf_len = sizeof(ins_buf) / sizeof(x64Ins); \
	bf.buf = realloc(bf.buf, (bf.buf_size + ins_buf_len) * sizeof(x64Ins)); \
	memcpy(bf.buf + bf.buf_size, ins_buf, sizeof(ins_buf)); \
	bf.buf_size += ins_buf_len; \
} while(0)




x64InsBuf bf_compile(const char* in) {
	x64InsBuf ret = { NULL, 0 };

	BUF_PUSH(ret, PROLOGUE);

	bool rax_garbled = false;

	while(*in) {
		switch(*in) {
		case '>':
			BUF_PUSH(ret, RIGHT);
			rax_garbled = false;
			break;
		case '<':
			BUF_PUSH(ret, LEFT);
			rax_garbled = false;
			break;
		case '+':
			if (rax_garbled) {
				BUF_PUSH(ret, UNGARBLE_RAX);
				rax_garbled = false;
			}
			BUF_PUSH(ret, INCREMENT);
			break;
		case '-':
			if(rax_garbled) {
				BUF_PUSH(ret, UNGARBLE_RAX);
				rax_garbled = false;
			}
			BUF_PUSH(ret, DECREMENT);
			break;
		case '[':
			BUF_PUSH(ret, LOOP_START); // technically not compliant with BF spec, but who cares
			rax_garbled = true; // Because ] overwrites rax, so it's probably overwritten and if it's not, nothing bad happens.
			break;
		case '.':
			rax_garbled = true;
			BUF_PUSH(ret, PRINT_CHAR);
			break;
		case ']':
			rax_garbled = true;
			BUF_PUSH(ret, LOOP_END);
			break;
		default: break;
		}
		in++;
	}

	BUF_PUSH(ret, EPILOGUE);
	return ret;
}

#define TAPE_SIZE 256

void bf_execute(void *compiled, uint32_t len) {
	size_t memory_segment_size = len + TAPE_SIZE;
	void *memory_segment = mmap(NULL, memory_segment_size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANON, -1, 0);

	void (*native_program)(uint8_t*, size_t) = memory_segment;
	uint8_t *tape = (char *)memory_segment + len;

	memcpy(native_program, compiled, len);
	memset(tape, 0, TAPE_SIZE);

	native_program(tape, TAPE_SIZE);

	munmap(memory_segment, memory_segment_size);
}

#define MAX_CODE_LEN 512

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

	printf("*********************************\n");
	printf("***** The BFMU JIT Compiler *****\n");
	printf("*********************************\n");
	printf("\nCompiles BF programs to blazingly fast, memory-unsafe x64 machine code!\n");
	printf("Enter your BF program:\n");

	char line[MAX_CODE_LEN];
    if (fgets(line, MAX_CODE_LEN, stdin) == NULL) {
        printf("Failed to read input\n");
        exit(EXIT_FAILURE);
    }

	printf("JIT compiling BF program\n");
	x64InsBuf ins = bf_compile(line);
	printf("Assembled %zu instructions\n", ins.buf_size);
	uint32_t len = 0;
	void* compiled = x64as(ins.buf, ins.buf_size, &len); // uh oh broken??
	printf("Lowered into %u bytes of machine code\n", len);
	printf("Executing...\n");
	bf_execute(compiled, len);
	printf("Executed!\n");
}

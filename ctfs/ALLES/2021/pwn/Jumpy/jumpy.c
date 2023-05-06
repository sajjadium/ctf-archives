#include <sys/mman.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>

void ignore_me_init_buffering() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

typedef struct instruction_t
{
    char *mnemonic;
    uint8_t opcode;
} instruction_t;

const uint8_t OP_RET = 0xc3;
const uint8_t OP_SHORT_JMP = 0xeb;
const uint8_t OP_MOV_EAX_IMM32 = 0xb8;

const instruction_t INSNS[3] = {
    {"ret", OP_RET},
    {"jmp", OP_SHORT_JMP},
    {"moveax", OP_MOV_EAX_IMM32},
};

uint8_t *cursor;
uint8_t *mem;

void emit_opcode(uint8_t opcode)
{
    *cursor++ = opcode;
}
void emit_imm32()
{
    scanf("%d", (uint32_t *)cursor);
    cursor += sizeof(uint32_t);
}

int8_t emit_imm8()
{
    scanf("%hhd", (int8_t *)cursor++);
    return *(int8_t *)(cursor - 1);
}

const instruction_t *isns_by_mnemonic(char *mnemonic)
{
    for (int i = 0; i < sizeof(INSNS) / sizeof(INSNS[0]); i++)
        if (!strcmp(mnemonic, INSNS[i].mnemonic))
            return &INSNS[i];
    return NULL;
}

bool is_supported_op(uint8_t op)
{
    for (int i = 0; i < sizeof(INSNS) / sizeof(INSNS[0]); i++)
        if (op == INSNS[i].opcode)
            return true;
    return false;
}

int main(void)
{
    ignore_me_init_buffering();
    printf("this could have been a V8 patch...\n");
    printf("... but V8 is quite the chungus ...\n");
    printf("... so here's a small and useless assembler instead\n\n");

    mem = mmap((void*)0x1337000000, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    memset(mem, 0xc3, 0x1000);
    cursor = mem;

    printf("supported insns:\n");
    printf("- moveax $imm32\n");
    printf("- jmp $imm8\n");
    printf("- ret\n");
    printf("- (EOF)\n");
    printf("\n");

    uint8_t **jump_targets = NULL;
    size_t jump_target_cnt = 0;

    {
        while (1)
        {
            printf("> ");
            char opcode[10] = {0};
            scanf("%9s", opcode);
            const instruction_t *insn = isns_by_mnemonic(opcode);
            if (!insn)
                break;

            emit_opcode(insn->opcode);
            switch (insn->opcode)
            {
            case OP_MOV_EAX_IMM32:
                emit_imm32();
                break;
            case OP_SHORT_JMP:
                jump_targets = reallocarray(jump_targets, ++jump_target_cnt, sizeof(jump_targets[0]));
                int8_t imm = emit_imm8();
                uint8_t *target = cursor + imm;
                jump_targets[jump_target_cnt - 1] = target;
                break;
            case OP_RET:
                break;
            }
        }
    }

    for (int i = 0; i < jump_target_cnt; i++)
    {
        if (!is_supported_op(*jump_targets[i]))
        {
            printf("invalid jump target!\n");
            printf("%02x [%02x] %02x\n", *(jump_targets[i] - 1), *(jump_targets[i] + 0), *(jump_targets[i] + 1));
            exit(1);
        }
    }

    uint64_t (*code)() = (void *)mem;
    mprotect(code, 0x1000, PROT_READ | PROT_EXEC);
    printf("\nrunning your code...\n");
    alarm(5);
    printf("result: 0x%lx\n", code());
}

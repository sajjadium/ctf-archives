#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <stdlib.h>

#define CODE_START 0x400000
#define DATA_START 0xa00000

typedef struct _CCPU {
    uint64_t regs[16];
    uint64_t rip;
    uint64_t rflags;
} CCPU;

typedef struct _Memory {
    char *data;
    uint64_t start;
    uint64_t size;
} Memory;

typedef struct _Mapping {
    struct _Mapping *next;
    Memory mem;
} Mapping;

enum OPERATIONS {
    NOP,
    MOVRI,
    MOVMI,
    MOVRR,
    MOVMR,
    MOVRM,
    ADDRR,
    ADDMR,
    ADDRM,
    ADDRI,
    ADDMI,
    SUBRI,
    SUBMI,
    SUBRR,
    SUBMR,
    SUBRM,
    MULR,
    MULM,
    DIVR,
    DIVM,
    CALLR,
    CALLM,
    RET,
    CALLI,
    PUSHR,
    PUSHI,
    PUSHM,
    POPR,
    POPM, 
    CMPRI,
    CMPMI,
    CMPRR,
    CMPRM,
    CMPMR,
    ANDRI,
    ANDMI,
    ANDMR,
    ANDRR,
    ANDRM,
    XORRI,
    XORMI,
    XORMR,
    XORRR,
    XORRM,
    JMPR,
    JMPI,
    JMPM,
    JZ,
    JNZ,
    SYSCALL,
    ILL,
    RR,
    MR,
    RM,
    RI,
    MI
};

typedef struct _Instruction {
    uint32_t executed;
    uint32_t opcode;
    uint64_t operand1val;
    uint64_t operand2val;
    uint64_t operand3val;
    uint32_t op1;
    uint32_t op2;
    uint32_t op3;
    uint32_t op1_m;
    uint32_t op2_m;
    uint32_t op3_m;
    uint64_t size;
    uint8_t modrm;
    char * cached_op1_base;
    char * cached_op2_base;
} Instruction;

typedef struct _Pipeline {
    Instruction queued[32];
    uint32_t queued_size;
} Pipeline;


typedef struct _Program {
    CCPU cpu;
    Pipeline pipe;
    Mapping mapping;
} Program;

char *get_reg(uint64_t index){
    switch(index){
        case 0: {
            return "r00";
        }
        case 1: {
            return "r01";
        }
        case 2: {
            return "r02";
        }
        case 3: {
            return "r03";
        }
        case 4: {
            return "r04";
        }
        case 5: {
            return "r05";
        }
        case 6: {
            return "r06";
        }
        case 7: {
            return "r07";
        }
        case 8: {
            return "r08";
        }
        case 9: {
            return "r09";
        }
        case 10: {
            return "r10";
        }
        case 11: {
            return "r11";
        }
        case 12: {
            return "r12";
        }
        case 13: {
            return "r13";
        }
        case 14: {
            return "r14";
        }
        case 15: {
            return "r15";
        }
        case 0x64:{
            return "no_reg";
        }
        default: {
            return "UNK!";
        }
    }
}

char *get_mem_ptr(Mapping *m, uint64_t addr, uint64_t size){
    uint64_t end = addr + size;
    while(m != NULL){
        if ((m->mem.start <= addr) && ((m->mem.start + m->mem.size) > addr)){
            if ((m->mem.start < end) && ((m->mem.start + m->mem.size) >= end)){
                return m->mem.data + (addr - m->mem.start);
            }
        }
        m = m->next;
    }
    return NULL;
}

int fill_instr_rr_mr(Instruction *instr, char * buffer, uint16_t prefix){
    if (prefix == 0xfff){
        return 1;
    }
    uint8_t W,R,X,B;
    W = (prefix >> 3) & 1;
    R = (prefix >> 2) & 1;
    X = (prefix >> 1) & 1;
    B = (prefix) & 1;
    uint8_t modRM = *buffer;
    buffer++;
    uint8_t r = (modRM >> 3)&7;
    uint8_t m = (modRM)&7;
    uint8_t mod = modRM >> 6;
    uint8_t r1_index = (R << 3) | r;
    uint8_t r2_index = (B << 3) | m;
    uint16_t sib = 0xfff;
    uint8_t sib_scale, sib_index, sib_base;
    instr->modrm = modRM;
    if (m == 4){
        sib = *buffer & 0xff;
        buffer++;
        sib_scale = sib >> 6;
        sib_index = (sib>>3) & 7;
        sib_base = sib & 7;
        int news;
        switch(sib_scale){
            case 0:{
                news = 1;
                break;
            }
            case 1:{
                news=  2;
                break;
            }
            case 2:{
                news = 4;
                break;
            }
            case 3:{
                news = 8;
            }
        }
        sib_scale = news;
    }
    if (mod == 3){
        instr->opcode = RR;
        instr->op1 = r2_index;
        instr->op2 = r1_index;
        instr->size = 3;
    }else if(mod == 0){
        instr->opcode = MR;
        instr->op3 = r1_index;
        instr->size = 3;
        if (sib == 0xfff){
            instr->op1 = r2_index;
        }else{
            instr->size += 1;
            uint8_t bb = (B << 3)|sib_base;
            uint8_t xi = (X << 3)|sib_index;
            instr->size = 4;
            switch(bb){
                case 13:
                case 5:{
                    uint32_t data = *(uint32_t *)(buffer);
                    buffer += 4;
                    instr->size += 4;    
                    if (xi == 4){
                        instr->operand1val = data; 
                    }else{
                        instr->op2 = bb;
                        instr->op2_m = sib_scale;
                        instr->operand1val = data;
                    }
                    break;
                }
                default:{
                    instr->op1 = bb;
                    if (xi != 4) {
                        instr->op2 = xi;
                        instr->op2_m = sib_scale;
                    }
                }
            }
        }

    }else if(mod == 1){
        uint8_t data = *buffer;
        buffer += 1;
        instr->opcode = MR;
        instr->op3 = r1_index;
        instr->operand1val = data;
        instr->size = 4;
        if (sib == 0xfff){
            instr->op1 = r2_index;
        }else{
            instr->size += 1;
            uint8_t bb = (B << 3)|sib_base;
            uint8_t xi = (X << 3)|sib_index;
            instr->op1 = bb;
            if (xi != 4){
                instr->op2 = xi;
                instr->op2_m = sib_scale;
            }
        }
    }else if(mod == 2){
        uint32_t data = *(uint32_t *)(buffer);
        buffer += 4;
        instr->opcode = MR;
        instr->op3 = r1_index;
        instr->operand1val = data;
        instr->size = 7;
        if (sib == 0xfff){
            instr->op1 = r2_index;
        }else{
            instr->size += 1;
            uint8_t bb = (B << 3)|sib_base;
            uint8_t xi = (X << 3)|sib_index;
            instr->op1 = bb;
            if (xi != 4){
                instr->op2 = xi;
                instr->op2_m = sib_scale;
            }
        }
    }
    return 0;
}

int fill_instr_ri_mi_imm(Instruction *instr, char * buffer, uint16_t prefix, uint32_t sz){
    if (prefix == 0xfff){
        return 1;
    }
    uint8_t W,R,X,B;
    W = (prefix >> 3) & 1;
    R = (prefix >> 2) & 1;
    X = (prefix >> 1) & 1;
    B = (prefix) & 1;
    uint8_t modRM = *buffer;
    buffer++;
    uint8_t r = (modRM >> 3)&7;
    uint8_t m = (modRM)&7;
    uint8_t mod = modRM >> 6;
    uint8_t r1_index = (R << 3) | r;
    uint8_t r2_index = (B << 3) | m;
    uint16_t sib = 0xfff;
    instr->modrm = modRM;
    uint8_t sib_scale, sib_index, sib_base;
    if (m == 4){
        sib = *buffer & 0xff;
        buffer++;
        sib_scale = sib >> 6;
        sib_index = (sib>>3) & 7;
        sib_base = sib & 7;
        int news;
        switch(sib_scale){
            case 0:{
                news = 1;
                break;
            }
            case 1:{
                news=  2;
                break;
            }
            case 2:{
                news = 4;
                break;
            }
            case 3:{
                news = 8;
            }
        }
        sib_scale = news;
    }

    if (mod == 3){
        instr->opcode = RI;
        instr->op1 = r2_index;
        instr->size = 3;
    }else if(mod == 0){
        instr->opcode = MI;
        
        instr->size = 3;
        if (sib == 0xfff){
            instr->op1 = r2_index;
        }else{
            instr->size += 1;
            uint8_t bb = (B << 3)|sib_base;
            uint8_t xi = (X << 3)|sib_index;
            instr->size = 4;
            switch(bb){
                case 13:
                case 5:{
                    uint32_t data = *(uint32_t *)(buffer);
                    buffer += 4;
                    instr->size += 4;    
                    if (xi == 4){
                        instr->operand1val = data; 
                    }else{
                        instr->op2 = bb;
                        instr->op2_m = sib_scale;
                        instr->operand1val = data;
                    }
                    break;
                }
                default:{
                    instr->op1 = bb;
                    if (xi != 4) {
                        instr->op2 = xi;
                        instr->op2_m = sib_scale;
                    }
                }

            }
        }

    }else if(mod == 1){
        uint8_t data = *buffer;
        buffer += 1;
        instr->opcode = MI;
        instr->operand1val = data;
        instr->size = 4;
        if (sib == 0xfff){
            instr->op1 = r2_index;
        }else{
            instr->size += 1;
            uint8_t bb = (B << 3)|sib_base;
            uint8_t xi = (X << 3)|sib_index;
            instr->op1 = bb;
            if (xi != 4){
                instr->op2 = xi;
                instr->op2_m = sib_scale;
            }
        }
    }else if(mod == 2){
        uint32_t data = *(uint32_t *)(buffer);
        buffer += 4;
        instr->opcode = MI;
        instr->operand1val = data;
        instr->size = 7;
        if (sib == 0xfff){
            instr->op1 = r2_index;
        }else{
            instr->size += 1;
            uint8_t bb = (B << 3)|sib_base;
            uint8_t xi = (X << 3)|sib_index;
            instr->op1 = bb;
            if (xi != 4){
                instr->op2 = xi;
                instr->op2_m = sib_scale;
            }
        }
    }
    uint64_t val = 0;
    if (sz){
        if (sz == 4){
            uint32_t d = *(uint32_t *)buffer;
            val = (int32_t)d;
        }else if (sz == 1){
            uint8_t d = *buffer;
            val = (int8_t)d;
        }
        instr->operand3val = val;
        instr->size += sz;
    }
    return 0;
}

int fill_instr_rm(Instruction *instr, char *buffer, uint16_t prefix){
    if (prefix == 0xfff)
        return 1;
    uint8_t modRM = *buffer;
    buffer++;
    uint8_t r = (modRM >> 3)&7;
    uint8_t m = (modRM)&7;
    uint8_t mod = modRM >> 6;
    uint8_t W,R,X,B;
    W = (prefix >> 3) & 1;
    R = (prefix >> 2) & 1;
    X = (prefix >> 1) & 1;
    B = (prefix) & 1;
    uint8_t r1_index = (R << 4)|r ;
    uint8_t r2_index = (B << 4) | m;
    uint16_t sib = 0xfff;
    uint8_t sib_scale, sib_index, sib_base;
    if (m == 4){
        sib = *buffer & 0xff;
        buffer++;
        sib_scale = sib >> 6;
        sib_index = (sib>>3) & 7;
        sib_base = sib & 7;
        int news;
        switch(sib_scale){
            case 0:{
                news = 1;
                break;
            }
            case 1:{
                news=  2;
                break;
            }
            case 2:{
                news = 4;
                break;
            }
            case 3:{
                news = 8;
            }
        }
        sib_scale = news;
    }
    instr->opcode = RM;
    if(mod == 0){
        instr->op1 = r1_index;
        instr->size = 3;
        if (sib == 0xfff){    
            instr->op2 = r2_index;
        }else{
            instr->size += 1;
            uint8_t bb = (B << 3)|sib_base;
            uint8_t xi = (X << 3)|sib_index;
            instr->size = 4;
            switch(bb){
                case 13:
                case 5:{
                    uint32_t data = *(uint32_t *)(buffer);
                    buffer += 4;
                    instr->size += 4;    
                    if (xi == 4){
                        instr->operand2val = data; 
                    }else{
                        instr->op3 = bb;
                        instr->op3_m = sib_scale;
                        instr->operand2val = data;
                    }
                    break;
                }
                default:{
                    instr->op2 = bb;
                    if (xi != 4) {
                        instr->op3 = xi;
                        instr->op3_m = sib_scale;
                    }
                }
            }
        }
    }else if(mod == 1){
        uint8_t data = *buffer;
        buffer += 1;
        instr->size = 4;
        instr->op1 = r1_index;
        instr->operand2val = data;
        if (sib == 0xfff){
            instr->op2 = r2_index;
        }else{
            instr->size += 1;
            uint8_t bb = (B << 3)|sib_base;
            uint8_t xi = (X << 3)|sib_index;
            instr->op2 = bb;
            if (xi != 4){
                instr->op3 = xi;
                instr->op3_m = sib_scale;
            }
        }
    }else if(mod == 2){
        uint32_t data = *(uint32_t *)(buffer);
        buffer += 4;
        instr->size = 7;
        instr->op1 = r1_index;
        if (sib == 0xfff){
            instr->op2 = r2_index;
        }else{
            instr->size += 1;
            uint8_t bb = (B << 3)|sib_base;
            uint8_t xi = (X << 3)|sib_index;
            instr->op2 = bb;
            if (xi != 4){
                instr->op3 = xi;
                instr->op3_m = sib_scale;
            }
        }
        instr->operand2val = data;
    }else{
        instr->opcode = ILL;
    }
    return 0;
}


uint8_t fetch_instruction(Program *prog, uint64_t start, Instruction *instr){
    
    instr->opcode = ILL;
    instr->op1 = 0x64;
    instr->op2 = 0x64;
    instr->op3 = 0x64;
    instr->op1_m = 0;
    instr->op2_m = 0;
    instr->op3_m = 0;
    instr->operand1val = 0;
    instr->operand2val = 0;
    instr->operand3val = 0;
    instr->cached_op1_base = 0;
    instr->cached_op2_base = 0;
    char *buffer = get_mem_ptr(&prog->mapping, start, 1);
    if (buffer != NULL){
        uint16_t prefix = *buffer;
        uint8_t opcode;
        uint8_t modRM;
        uint8_t mod, W, R, X ,B = 0;
        buffer++;
        if ((prefix & 0xf0) == 0x40){
            opcode = *buffer;
            W = (prefix >> 3) & 1;
            R = (prefix >> 2) & 1;
            X = (prefix >> 1) & 1;
            B = (prefix) & 1;
            buffer++;
        }else{
            if(prefix == 0x66){
                goto error;
            }
            opcode = prefix;
            prefix = 0xfff;
        }
        switch(opcode){
            case 0x01: {
                int res = fill_instr_rr_mr(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RR:{
                        instr->opcode = ADDRR;
                        break;
                    }
                    case MR:{
                        instr->opcode = ADDMR;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x03: {
                int res = fill_instr_rm(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RM:{
                        instr->opcode = ADDRM;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x5: {
                if (prefix == 0xfff){
                    goto error;
                }
                uint8_t W,R,X,B;
                W = (prefix >> 3) & 1;
                R = (prefix >> 2) & 1;
                X = (prefix >> 1) & 1;
                B = (prefix) & 1;
                uint32_t data = *(uint32_t *)buffer;
                int64_t da = (int32_t)data;
                buffer += 4;
                instr->opcode = ADDRI;
                instr->op1 = 0;
                instr->operand3val = da;
                instr->size = 6;
                break;
            }
            case 0xf: {
                uint8_t next = *buffer;
                ++buffer;
                switch(next){
                    case 0x05:{
                        instr->opcode = SYSCALL;
                        instr->size = 2;
                        break;
                    }
                    case 0x84:{
                        uint32_t data = *(uint32_t *)buffer;
                        uint64_t da = (int32_t)data;
                        instr->opcode = JZ;
                        instr->operand1val = da;
                        instr->size = 6;
                        break;
                    }
                    case 0x85:{
                        uint32_t data = *(uint32_t *)buffer;
                        uint64_t da = (int32_t)data;
                        instr->opcode = JZ;
                        instr->operand1val = da;
                        instr->size = 6;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x21: {
                int res = fill_instr_rr_mr(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RR:{
                        instr->opcode = ANDRR;
                        break;
                    }
                    case MR:{
                        instr->opcode = ANDMR;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x23: {
                int res = fill_instr_rm(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RM:{
                        instr->opcode = ANDRM;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x25:{
                if (prefix == 0xfff){
                    goto error;
                }
                uint8_t W,R,X,B;
                W = (prefix >> 3) & 1;
                R = (prefix >> 2) & 1;
                X = (prefix >> 1) & 1;
                B = (prefix) & 1;
                uint32_t data = *(uint32_t *)buffer;
                int64_t da = (int32_t)data;
                buffer += 4;
                instr->opcode = ANDRI;
                instr->op1 = 0;
                instr->operand3val = da;
                instr->size = 6;
                break;
            }
            case 0x29: {
                int res = fill_instr_rr_mr(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RR:{
                        instr->opcode = SUBRR;
                        break;
                    }
                    case MR:{
                        instr->opcode = SUBMR;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x2b: {
                int res = fill_instr_rm(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RM:{
                        instr->opcode = SUBRM;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x2d:{
                if (prefix == 0xfff){
                    goto error;
                }
                uint8_t W,R,X,B;
                W = (prefix >> 3) & 1;
                R = (prefix >> 2) & 1;
                X = (prefix >> 1) & 1;
                B = (prefix) & 1;
                uint32_t data = *(uint32_t *)buffer;
                int64_t da = (int32_t)data;
                buffer += 4;
                instr->opcode = SUBRI;
                instr->op1 = 0;
                instr->operand3val = da;
                instr->size = 6;
                break;
            }
            case 0x31: {
                int res = fill_instr_rr_mr(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RR:{
                        instr->opcode = XORRR;
                        break;
                    }
                    case MR:{
                        instr->opcode = XORMR;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x33: {
                int res = fill_instr_rm(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RM:{
                        instr->opcode = XORRM;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x35:{
                if (prefix == 0xfff){
                    goto error;
                }
                uint8_t W,R,X,B;
                W = (prefix >> 3) & 1;
                R = (prefix >> 2) & 1;
                X = (prefix >> 1) & 1;
                B = (prefix) & 1;
                uint32_t data = *(uint32_t *)buffer;
                int64_t da = (int32_t)data;
                buffer += 4;
                instr->opcode = XORRI;
                instr->op1 = 0;
                instr->operand3val = da;
                instr->size = 6;
                break;
            }
            case 0x39:{
                int res = fill_instr_rr_mr(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RR:{
                        instr->opcode = CMPRR;
                        break;
                    }
                    case MR:{
                        instr->opcode = CMPMR;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x3b: {
                int res = fill_instr_rm(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RM:{
                        instr->opcode = CMPRM;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x3d:{
                if (prefix == 0xfff){
                    goto error;
                }
                uint8_t W,R,X,B;
                W = (prefix >> 3) & 1;
                R = (prefix >> 2) & 1;
                X = (prefix >> 1) & 1;
                B = (prefix) & 1;
                uint32_t data = *(uint32_t *)buffer;
                int64_t da = (int32_t)data;
                buffer += 4;
                instr->opcode = CMPRI;
                instr->op1 = 0;
                instr->operand3val = da;
                instr->size = 6;
                break;
            }
            case 0x68:{
                uint32_t data = *(uint32_t *)buffer;
                instr->opcode = PUSHI;
                instr->operand1val = data;
                instr->size = 5;
                break;
            }
            case 0x6a:{
                uint8_t data = *buffer;
                instr->opcode = PUSHI;
                instr->operand1val = data;
                instr->size = 2;
                break;
            }
            case 0x74:{
                uint8_t data = *buffer;
                instr->opcode = JZ;
                instr->operand1val = (int8_t)data;
                instr->size = 2;
                break;
            }
            case 0x75:{
                uint8_t data = *buffer;
                instr->opcode = JNZ;
                instr->operand1val = (int8_t)data;
                instr->size = 2;
                break;
            }
            case 0x81:{
                int res = fill_instr_ri_mi_imm(instr, buffer, prefix, 4);
                if (res){
                    goto error;
                }
                uint8_t m = (instr->modrm >> 3) & 7;
                switch(instr->opcode){
                    case RI:{
                        switch(m){
                            case 0:{
                                instr->opcode = ADDRI;
                                break;
                            }
                            case 4:{
                                instr->opcode = ANDRI;
                                break;
                            }
                            case 5:{
                                instr->opcode = SUBRI;
                                break;
                            }
                            case 6:{
                                instr->opcode = XORRI;
                                break;
                            }
                            case 7:{
                                instr->opcode = CMPRI;
                                break;
                            }
                            default:{
                                goto error;
                            }
                        }
                        break;
                    }
                    case MI:{
                        switch(m){
                            case 0:{
                                instr->opcode = ADDMI;
                                break;
                            }
                            case 4:{
                                instr->opcode = ANDMI;
                                break;
                            }
                            case 5:{
                                instr->opcode = SUBMI;
                                break;
                            }
                            case 6:{
                                instr->opcode = XORMI;
                                break;
                            }
                            case 7:{
                                instr->opcode = CMPMI;
                                break;
                            }
                            default:{
                                goto error;
                            }
                        }
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x83:{
                int res = fill_instr_ri_mi_imm(instr, buffer, prefix, 1);
                if (res){
                    goto error;
                }
                uint8_t m = (instr->modrm >> 3) & 7;
                switch(instr->opcode){
                    case RI:{
                        switch(m){
                            case 0:{
                                instr->opcode = ADDRI;
                                break;
                            }
                            case 4:{
                                instr->opcode = ANDRI;
                                break;
                            }
                            case 5:{
                                instr->opcode = SUBRI;
                                break;
                            }
                            case 6:{
                                instr->opcode = XORRI;
                                break;
                            }
                            case 7:{
                                instr->opcode = CMPRI;
                                break;
                            }
                            default:{
                                goto error;
                            }
                        }
                        break;
                    }
                    case MI:{
                        switch(m){
                            case 0:{
                                instr->opcode = ADDMI;
                                break;
                            }
                            case 4:{
                                instr->opcode = ANDMI;
                                break;
                            }
                            case 5:{
                                instr->opcode = SUBMI;
                                break;
                            }
                            case 6:{
                                instr->opcode = XORMI;
                                break;
                            }
                            case 7:{
                                instr->opcode = CMPMI;
                                break;
                            }
                            default:{
                                goto error;
                            }
                        }
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x89: {
                int res = fill_instr_rr_mr(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RR:{
                        instr->opcode = MOVRR;
                        break;
                    }
                    case MR:{
                        instr->opcode = MOVMR;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x8b: {
                int res = fill_instr_rm(instr, buffer, prefix);
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RM:{
                        instr->opcode = MOVRM;
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0x8f: {
                uint8_t r = prefix;
                if (prefix == 0xfff)
                    r = 0;
                int res = fill_instr_rr_mr(instr, buffer, r);
                uint8_t m = (instr->modrm >> 3) & 7;
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RR:{
                        switch(m){
                            default:
                                goto error;
                        }
                        break;
                    }
                    case MR:{
                        switch(m){
                            case 0:{
                                instr->opcode = POPM;
                                break;
                            }
                            default:
                                goto error;
                        }
                        break;
                    }
                    default:
                        goto error;
                }
                if (prefix == 0xfff)
                    instr->size--;
                break;
            }
            case 0x90: {
                instr->opcode = NOP;
                instr->size = 1;
                break;
            }
            case 0xc3: {
                instr->opcode = RET;
                instr->size = 1;
                break;
            }
            case 0xc7: {
                int res = fill_instr_ri_mi_imm(instr, buffer, prefix, 4);
                if (res){
                    goto error;
                }
                uint8_t m = (instr->modrm >> 3) & 7;
                switch(instr->opcode){
                    case RI:{
                        instr->opcode = MOVRI;
                        break;
                    }
                    case MI:{
                        switch(m){
                            case 0:{
                                instr->opcode = MOVMI;
                                break;
                            }
                            default:{
                                goto error;
                            }
                        }
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0xe8: {
                uint32_t data = *(uint32_t *)buffer;
                buffer += 4;
                uint64_t da = (int32_t)data;
                instr->opcode = CALLI;
                instr->operand1val = da;
                instr->size = 5;
                break;
            }
            case 0xe9: {
                uint32_t data = *(uint32_t *)buffer;
                buffer += 4;
                uint64_t da = (int32_t)data;
                instr->opcode = JMPI;
                instr->operand1val = da;
                instr->size = 5;
                break;
            }
            case 0xeb: {
                uint8_t data = *buffer;
                buffer += 1;
                uint64_t da = (int8_t)data;
                instr->opcode = JMPI;
                instr->operand1val = da;
                instr->size = 2;
                break;
            }
            case 0xf7: {
                int res = fill_instr_ri_mi_imm(instr, buffer, prefix, 0);
                if (res){
                    goto error;
                }
                uint8_t m = (instr->modrm >> 3) & 7;
                switch(instr->opcode){
                    case RI:{
                        switch(m){
                            case 4:{
                                instr->opcode = MULR;
                                break;
                            }
                            case 6:{
                                instr->opcode = DIVR;
                                break;
                            }
                            default:{
                                goto error;
                            }
                        }
                        break;
                    }
                    case MI:{
                        switch(m){
                            case 4:{
                                instr->opcode = MULM;
                                break;
                            }
                            case 6:{
                                instr->opcode = DIVM;
                                break;
                            }
                            default:{
                                goto error;
                            }
                        }
                        break;
                    }
                    default:
                        goto error;
                }
                break;
            }
            case 0xff: {
                uint8_t r = prefix;
                if (prefix == 0xfff)
                    r = 0;
                int res = fill_instr_rr_mr(instr, buffer, r);
                uint8_t m = (instr->modrm >> 3) & 7;
                if (res){
                    goto error;
                }
                switch(instr->opcode){
                    case RR:{
                        switch(m){
                            case 2:{
                                instr->opcode = CALLR;
                                break;
                            }
                            case 4:{
                                instr->opcode = JMPR;
                                break;
                            }
                            default:
                                goto error;
                        }
                        break;
                    }
                    case MR:{
                        switch(m){
                            case 6:{
                                instr->opcode = PUSHM;
                                break;
                            }
                            case 4:{
                                instr->opcode = JMPM;
                                break;
                            }
                            case 2:{
                                instr->opcode = CALLM;
                                break;
                            }
                            default:
                                goto error;
                        }
                        break;
                    }
                    default:
                        goto error;
                }
                if (prefix == 0xfff)
                    instr->size--;
                break;
            }
            default: {
                if ((opcode & 0xf8) == 0xb8){
                    uint8_t reg = opcode & 0x7;
                    instr->size = 1;
                    if (prefix != 0xfff){
                        reg = (B << 3)|reg;
                        instr->size += 1;
                    }
                    instr->opcode = MOVRI;
                    instr->op1 = reg;
                    uint64_t da;
                    if ((prefix == 0xfff)||(W == 0)){
                        da = *(uint32_t *)buffer;
                        buffer+=4;
                        instr->size += 4;
                    }else{
                        da = *(uint64_t *)buffer;
                        buffer += 8;
                        instr->size += 8;
                    }
                    instr->operand3val = da;
                    
                }else if ((opcode & 0xf8) == 0x50){
                    uint8_t reg = opcode & 0x7;
                    instr->size = 1;
                    if (prefix != 0xfff){
                        reg = (B << 3)|reg;
                        instr->size += 1;
                    }
                    instr->opcode = PUSHR;
                    instr->op1 = reg;
                    break;
                }else if ((opcode & 0xf8) == 0x58){
                    uint8_t reg = opcode & 0x7;
                    instr->size = 1;
                    if (prefix != 0xfff){
                        reg = (B << 3)|reg;
                        instr->size += 1;
                    }
                    instr->opcode = POPR;
                    instr->op1 = reg;
                    break;
                }else{
                    error:
                        return 1;
                }
            }
        }
        return 0;
    }
    return 1;
}


int add_mapping(Program *prog, uint64_t start, uint64_t size){
    Mapping *map = &prog->mapping;
    char *data = get_mem_ptr(map, start, 1);
    if (data){
        return 1;
    }
    while(map->next != NULL){
        map = map->next;
    }
    int result = 1;
    if (map){
        map->next = malloc(sizeof(Mapping));
        if (map->next != NULL){
            map->next->next = NULL;
            map->mem.data = malloc(size);
            if (map->mem.data != NULL){
                map->mem.start = start;
                map->mem.size = size;
                result = 0;
            }else{
                free(map->next);
                map->next = NULL;
            }
        }
    }
    
    return result;
}


Program *init_program(uint32_t size){
    Program *prog = malloc(sizeof(Program));
    if (prog == NULL)
        return prog;
    prog->mapping.next = NULL;
    prog->mapping.mem.data = NULL;    
    size = (size + 0xfff) & 0xfffff000;
    int res = add_mapping(prog, CODE_START, size);
    if (!res){
        res = add_mapping(prog, DATA_START, 0x10000);
        if (res)
            goto err;
    }else{
err:
        free(prog);
        prog = NULL;
    }
    return prog;
}   

int load_file(Program *p, uint64_t addr, uint64_t size, FILE *file){
    char *ptr_to_read = get_mem_ptr(&p->mapping, addr, size);
    int res = 1;
    if (ptr_to_read != NULL){
        int sz = fread(ptr_to_read, 1, size, file);
        if (sz == size)
            res = 0;
    }
    return res;
}


char * get_mem_op2(Program *p, Instruction *i){
    uint64_t base = p->cpu.regs[i->op2];
    if (base == 0x64){
        base = 0;
    }
    uint64_t index = p->cpu.regs[i->op3];
    if (index == 0x64){
        index = 0;
    }
    if (i->cached_op2_base != 0){
        return i->cached_op2_base + index *i->op3_m + i->operand2val;
    }
    uint64_t addr = base + index *i->op3_m + i->operand2val;
    char * data = get_mem_ptr(&p->mapping, addr, 8);    
    return data;
}

char * get_mem_op1(Program *p, Instruction *i){
    uint64_t base = p->cpu.regs[i->op1];
    if (base == 0x64){
        base = 0;
    }
    uint64_t index = p->cpu.regs[i->op2];
    if (index == 0x64){
        index = 0;
    }
    if (i->cached_op1_base != 0){
        return i->cached_op1_base + index *i->op2_m + i->operand1val;
    }
    uint64_t addr = base + index *i->op2_m + i->operand1val;
    char * data = get_mem_ptr(&p->mapping, addr, 8);    
    return data;
}

int execute_instruction(Program *p, Instruction *i){
    p->cpu.rip += i->size;
    switch(i->opcode){
        case MOVRI:{
            p->cpu.regs[i->op1] = i->operand3val;
            break;
        }
        case MOVRR:{
            p->cpu.regs[i->op1] = p->cpu.regs[i->op2];
            break;
        }
        case MOVRM:{
            char * data = get_mem_op2(p, i);
            if( data != NULL){
                p->cpu.regs[i->op1] = *(uint64_t *)data;
            }else{
                return 1;
            }
            break;
        }
        case MOVMR:{
            char *data = get_mem_op1(p, i);
            if (data != NULL){
                *(uint64_t *)data = p->cpu.regs[i->op3];
            }else{
                return 1;
            }
            break;
        }
        case MOVMI:{
            char *data = get_mem_op1(p, i);
            if (data != NULL){
                *(uint64_t *)data = i->operand3val;
            }else{
                return 1;
            }
            break;
        }
        case ADDRI:{
            uint64_t orig = p->cpu.regs[i->op1];
            p->cpu.regs[i->op1] += i->operand3val;
            uint8_t zf = (p->cpu.regs[i->op1] == 0);
            uint8_t cf = (p->cpu.regs[i->op1] < orig);
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case ADDRR:{
            uint64_t orig = p->cpu.regs[i->op1];
            p->cpu.regs[i->op1] += p->cpu.regs[i->op2];
            uint8_t zf = (p->cpu.regs[i->op1] == 0);
            uint8_t cf = (p->cpu.regs[i->op1] < orig);
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case ADDRM:{
            char * data = get_mem_op2(p, i);
            if (data){
                uint64_t orig = p->cpu.regs[i->op1];
                p->cpu.regs[i->op1] += *(uint64_t *)data;
                uint8_t zf = (p->cpu.regs[i->op1] == 0);
                uint8_t cf = (p->cpu.regs[i->op1] < orig);
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case ADDMR:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                *(uint64_t *)data += p->cpu.regs[i->op3];
                uint8_t zf = (*(uint64_t *)data  == 0);
                uint8_t cf = (*(uint64_t *)data  < orig);
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case ADDMI:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                *(uint64_t *)data += i->operand3val;
                uint8_t zf = (*(uint64_t *)data  == 0);
                uint8_t cf = (*(uint64_t *)data  < orig);
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case SUBRI:{
            uint64_t orig = p->cpu.regs[i->op1];
            p->cpu.regs[i->op1] -= i->operand3val;
            uint8_t zf = (p->cpu.regs[i->op1] == 0);
            uint8_t cf = (p->cpu.regs[i->op1] > orig);
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case SUBRR:{
            uint64_t orig = p->cpu.regs[i->op1];
            p->cpu.regs[i->op1] -= p->cpu.regs[i->op2];
            uint8_t zf = (p->cpu.regs[i->op1] == 0);
            uint8_t cf = (p->cpu.regs[i->op1] > orig);
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case SUBRM:{
            char * data = get_mem_op2(p, i);
            if (data){
                uint64_t orig = p->cpu.regs[i->op1];
                p->cpu.regs[i->op1] -= *(uint64_t *)data;
                uint8_t zf = (p->cpu.regs[i->op1] == 0);
                uint8_t cf = (p->cpu.regs[i->op1] > orig);
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case SUBMR:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                *(uint64_t *)data -= p->cpu.regs[i->op3];
                uint8_t zf = (*(uint64_t *)data  == 0);
                uint8_t cf = (*(uint64_t *)data  > orig);
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case SUBMI:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                *(uint64_t *)data -= i->operand3val;
                uint8_t zf = (*(uint64_t *)data  == 0);
                uint8_t cf = (*(uint64_t *)data  > orig);
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case ANDRI:{
            uint64_t orig = p->cpu.regs[i->op1];
            p->cpu.regs[i->op1] &= i->operand3val;
            uint8_t zf = (p->cpu.regs[i->op1] == 0);
            uint8_t cf = 0;
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case ANDRR:{
            uint64_t orig = p->cpu.regs[i->op1];
            p->cpu.regs[i->op1] &= p->cpu.regs[i->op2];
            uint8_t zf = (p->cpu.regs[i->op1] == 0);
            uint8_t cf = 0;
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case ANDRM:{
            char * data = get_mem_op2(p, i);
            if (data){
                uint64_t orig = p->cpu.regs[i->op1];
                p->cpu.regs[i->op1] &= *(uint64_t *)data;
                uint8_t zf = (p->cpu.regs[i->op1] == 0);
                uint8_t cf = 0;
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case ANDMR:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                *(uint64_t *)data &= p->cpu.regs[i->op3];
                uint8_t zf = (*(uint64_t *)data  == 0);
                uint8_t cf = 0;
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case ANDMI:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                *(uint64_t *)data &= i->operand3val;
                uint8_t zf = (*(uint64_t *)data  == 0);
                uint8_t cf = 0;
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case XORRI:{
            uint64_t orig = p->cpu.regs[i->op1];
            p->cpu.regs[i->op1] ^= i->operand3val;
            uint8_t zf = (p->cpu.regs[i->op1] == 0);
            uint8_t cf = 0;
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case XORRR:{
            uint64_t orig = p->cpu.regs[i->op1];
            p->cpu.regs[i->op1] ^= p->cpu.regs[i->op2];
            uint8_t zf = (p->cpu.regs[i->op1] == 0);
            uint8_t cf = 0;
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case XORRM:{
            char * data = get_mem_op2(p, i);
            if (data){
                uint64_t orig = p->cpu.regs[i->op1];
                p->cpu.regs[i->op1] ^= *(uint64_t *)data;
                uint8_t zf = (p->cpu.regs[i->op1] == 0);
                uint8_t cf = 0;
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case XORMR:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                *(uint64_t *)data ^= p->cpu.regs[i->op3];
                uint8_t zf = (*(uint64_t *)data  == 0);
                uint8_t cf = 0;
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case XORMI:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                *(uint64_t *)data ^= i->operand3val;
                uint8_t zf = (*(uint64_t *)data  == 0);
                uint8_t cf = 0;
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case CMPRI:{
            uint8_t zf = p->cpu.regs[i->op1] == i->operand3val;
            uint8_t cf = p->cpu.regs[i->op1] < i->operand3val;
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case CMPRR:{
            uint8_t zf = p->cpu.regs[i->op1] == p->cpu.regs[i->op2];
            uint8_t cf = p->cpu.regs[i->op1] < p->cpu.regs[i->op2];
            p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            break;
        }
        case CMPRM:{
            char * data = get_mem_op2(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                uint8_t zf = p->cpu.regs[i->op1] == orig;
                uint8_t cf = p->cpu.regs[i->op1] < orig;
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case CMPMR:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                uint8_t zf = orig == p->cpu.regs[i->op3];
                uint8_t cf = orig < p->cpu.regs[i->op3];
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case CMPMI:{
            char * data = get_mem_op1(p, i);
            if (data){
                uint64_t orig = *(uint64_t *)data;
                uint8_t zf = orig == i->operand3val;
                uint8_t cf = orig < i->operand3val;
                p->cpu.rflags = ((p->cpu.rflags & 0xfffffffffffffc) | (cf<<1)| zf);
            }else{
                return 1;
            }
            break;
        }
        case JMPI: {
            p->cpu.rip += i->operand1val;
            break;
        }
        case JMPR: {
            p->cpu.rip = p->cpu.regs[i->op1];
            break;
        }
        case JMPM: {
            char *data = get_mem_op1(p, i);
            if (data){
                p->cpu.rip = *(uint64_t *)data;
            }else{
                return 1;
            }
            break;
        }
        case PUSHI: {
            p->cpu.regs[4] -= 4;
            char *data = get_mem_ptr(&p->mapping, p->cpu.regs[4], 4);
            if (data != NULL){
                *(uint32_t *)data = i->operand1val;
            }else{
                return 1;
            }
            break;
        }
        case PUSHR: {
            p->cpu.regs[4] -= 8;
            char *data = get_mem_ptr(&p->mapping, p->cpu.regs[4], 4);
            if (data != NULL){
                *(uint64_t *)data = p->cpu.regs[i->op1];
            }else{
                return 1;
            }
            break;
        }
        case PUSHM: {
            p->cpu.regs[4] -= 8;
            char *data = get_mem_ptr(&p->mapping, p->cpu.regs[4], 4);
            if (data != NULL){
                char *data2 = get_mem_op1(p,i);
                if(data2){
                    *(uint64_t *)data = *(uint64_t *)data2;    
                }else{
                    return 1;
                }
            }else{
                return 1;
            }
            break;
        }
        case POPR:{
            char *data = get_mem_ptr(&p->mapping, p->cpu.regs[4], 8);
            if (data){
                p->cpu.regs[i->op1] = *(uint64_t *)data;
                p->cpu.regs[4] += 8;
            }else{
                return 1;
            }
            break;
        }
        case POPM:{
            char *data = get_mem_ptr(&p->mapping, p->cpu.regs[4], 8);
            if (data){
                char *data2 = get_mem_op1(p, i);
                if (data2){
                    *(uint64_t *)data2 = *(uint64_t *)data;
                    p->cpu.regs[4] += 8;
                }else{
                    return 1;
                }
            }else{
                return 1;
            }
            break;
        }
        case JZ: {
            if (p->cpu.rflags & 1){
                p->cpu.rip += i->operand1val;
            }
            break;
        }
        case JNZ: {
            if (!(p->cpu.rflags & 1)){
                p->cpu.rip += i->operand1val;
            }
            break;
        }
        case CALLI: {
            p->cpu.regs[4] -= 8;
            char *data = get_mem_ptr(&p->mapping, p->cpu.regs[4], 4);
            if (data != NULL){
                *(uint64_t *)data = p->cpu.rip;
            }else{
                return 1;
            }
            p->cpu.rip = p->cpu.rip + i->operand1val;
            break;
        }
        case CALLR: {
            p->cpu.regs[4] -= 8;
            char *data = get_mem_ptr(&p->mapping, p->cpu.regs[4], 4);
            if (data != NULL){
                *(uint64_t *)data = p->cpu.rip;
            }else{
                return 1;
            }
            p->cpu.rip = p->cpu.regs[i->op1];
            break;
        }
        case CALLM:{
            p->cpu.regs[4] -= 8;
            char *data = get_mem_ptr(&p->mapping, p->cpu.regs[4], 4);
            if (data != NULL){
                *(uint64_t *)data = p->cpu.rip;
            }else{
                return 1;
            }
            char *data2 = get_mem_op1(p, i);
            if (data2){
                p->cpu.rip = *(uint64_t *)data2;
            }else{
                return 1;
            }
            break;
        }
        case MULR: {
            unsigned __int128 res = (unsigned __int128)p->cpu.regs[i->op1] * (unsigned __int128)p->cpu.regs[0];
            p->cpu.regs[0] = res & 0xffffffffffffffff;
            p->cpu.regs[2] = res >> 64;
            p->cpu.rflags = 0;
            break;
        }
        case MULM: {
            char * data = get_mem_op1(p, i);
            if(data){
                uint64_t mult = *(uint64_t *)data;
                unsigned __int128 res = (unsigned __int128)mult * (unsigned __int128)p->cpu.regs[0];
                p->cpu.regs[0] = res & 0xffffffffffffffff;
                p->cpu.regs[2] = res >> 64;
                p->cpu.rflags = 0;
            }else{
                return 1;
            }
            break;
        }
        case DIVR:{
            unsigned __int128 divident = (((unsigned __int128)p->cpu.regs[2]) << 64)| (p->cpu.regs[0]);
            uint64_t divisor = p->cpu.regs[i->op1];
            p->cpu.regs[0] = divident / divisor;
            p->cpu.regs[2] = divident % divisor;
            break;
        }
        case DIVM:{
            unsigned __int128 divident = (((unsigned __int128)p->cpu.regs[2]) << 64)| (p->cpu.regs[0]);
            char *data = get_mem_op1(p, i);
            if (data){
                uint64_t divisor = *(uint64_t *)data;
                p->cpu.regs[0] = divident / divisor;
                p->cpu.regs[2] = divident % divisor;
            }else{
                return 1;
            }
            break;
        }
        case SYSCALL: {
            uint64_t sysnum = p->cpu.regs[0];
            switch(sysnum){
                case 0: {
                    uint64_t addr = p->cpu.regs[7];
                    uint64_t size = p->cpu.regs[6];
                    int res = add_mapping(p, addr, size);
                    if (!res){
                        p->cpu.regs[0] = addr;
                    }else{
                        p->cpu.regs[0] = -1;
                    }
                    break;
                }
                case 1: {
                    uint64_t addr = p->cpu.regs[7];
                    uint64_t size = p->cpu.regs[6];
                    char *data = get_mem_ptr(&p->mapping, addr, size);
                    if (data){
                        write(1, data, size);
                    }else{
                       return 1;
                    }   
                    break;
                }
                default: {
                    p->cpu.regs[0] = -1;
                }
            }
            break;
        }
        case RET: {
            char *data = get_mem_ptr(&p->mapping, p->cpu.regs[4], 8);
            if (data){
                p->cpu.rip = *(uint64_t *)data;
                p->cpu.regs[4] += 8;
            }else{
                return 1;
            }
            break;
        }
        default:{
            printf("Unknown instruction!\n");
            return 1;
        }
    }
    return 0;
}


int execute_block(Program *prog){
    uint8_t rinstr;
    prog->pipe.queued_size = 0;
    int offset = 0;
    for(int i=0; i < 32; ++i){
        rinstr = fetch_instruction(prog, prog->cpu.rip + offset, &prog->pipe.queued[i]);
        if (rinstr == 0){
            prog->pipe.queued_size++;
            switch(prog->pipe.queued[i].opcode){
                case CALLR:
                case CALLI:
                case CALLM:
                case JMPI:
                case JMPM:
                case JZ:
                case JNZ:
                case JMPR:{
                    goto _next;
                    break;
                }
                default:{
                    offset += prog->pipe.queued[i].size;
                }
            }
        }else{
            break;
        }
    }

    uint64_t cached_regs[32];
_next:
    if (prog->pipe.queued_size == 0){
        return 1;
    }
    for(int i=0; i < 16; ++i){
        cached_regs[i] = prog->cpu.regs[i];
        cached_regs[16+i] = 1;
    }
    for(int idx=0; idx < prog->pipe.queued_size; ++idx){
        Instruction *i = &prog->pipe.queued[idx];
        switch(i->opcode){
            case MOVMI:
            case MOVMR:
            case ADDMI:
            case ADDMR:
            case SUBMR:
            case SUBMI:
            case XORMI:
            case XORMR:
            case CMPMI:
            case CMPMR:
            case JMPM:
            case CALLM:{
                if (cached_regs[16+i->op1] == 1){
                    i->cached_op1_base = get_mem_ptr(&prog->mapping, cached_regs[i->op1], 1);
                }
                break;
            }
            case MOVRR:{
                if (cached_regs[16+i->op2] == 1){
                    cached_regs[i->op1] = cached_regs[i->op2];
                }else{
                    cached_regs[i->op1] = 0;
                }
                break;
            }
            case SUBRM:
            case MOVRM:
            case XORRM:
            case ANDRM:
            case CMPRM:
            case ADDRM:{
                if (cached_regs[16+i->op2] == 1){
                    i->cached_op2_base = get_mem_ptr(&prog->mapping, cached_regs[i->op2], 1);
                }
                cached_regs[16+i->op1] = 0;
                break;
            }
            case XORRI:
            case ANDRI:
            case MOVRI:
            case ADDRI:{
                cached_regs[16 + i->op1] = 0;
                break;
            }
        }
    }
    uint8_t got_error = 0;
    for(int i=0; i < prog->pipe.queued_size; ++i){
        int res = execute_instruction(prog, &prog->pipe.queued[i]);
        if(res){
            got_error = 1;
            break;
        }
    }
    return got_error;
}

int main(int argc, char **argv){
    if (argc < 2){
        puts("Usage: CCPU <code>");
        return -1;
    }
    FILE *input = fopen(argv[1], "rb");
    if (input == NULL){
        perror("Can't open code file");
        exit(-2);
    }

    struct stat st;
    stat(argv[1], &st);
    uint32_t size = st.st_size;
    Program *prog = init_program(size);
    int res = load_file(prog, CODE_START, size, input);
    fclose(input);
    prog->cpu.rip = CODE_START;
    prog->cpu.regs[4] = DATA_START + 0x10000;
    if (!res){
        while(!execute_block(prog)){
        }
    }else{
        printf("[LOAD_FILE] = %x\n", res);
    }
    free(prog);
    return 0;
};
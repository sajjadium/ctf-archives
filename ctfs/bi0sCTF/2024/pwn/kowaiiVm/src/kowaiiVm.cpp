#include "kowaiiVm.h"

using namespace std;

class kowaiiCtx
{
    private:
        void *genAddr()
        {
            u64 r = 0;
            do r = (u64)rand();
            while((int)r < 0);

            return (void *)(r << 12);
        }

    public:
        kowaiiBin *bin;
        kowaiiRegisters *regs;
        kowaiiFuncEntry **callStack;
        kowaiiFuncEntry **callStackBase;
        u8 *bss;
        u8 *jitBase;
        u8 *jitEnd;

        kowaiiCtx()
        {
            this->bin = (kowaiiBin *)mmap(this->genAddr(), MAX_BIN_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
            this->regs = (kowaiiRegisters *)calloc(1,sizeof(kowaiiRegisters));
            if(this->bin == (void *)-1 || this->regs == NULL) error("Memory error!");
        }

        void readBin()
        {
            u8 *ptr = (u8 *)this->bin;
            u8 chr = 0xa;
            u8 eof = 0x0;
            u32 i = 0;

            cout << "Send your kowaii binary" << endl;
            cout << "> " << flush;
            while(i < MAX_BIN_SIZE)
            {
                if(read(0,&chr,1) < 0) error("Read error!");
                if(chr == 0xa)
                {
                    if(eof)
                    {
                        ptr[i-1] = 0x0;
                        break;
                    }
                    ptr[i++] = chr;
                    eof = 1;
                }
                else
                {
                    ptr[i++] = chr;
                    eof = 0;
                }
            }
        }

        void checkBin()
        {
            if(memcmp(this->bin->kowaii,"KOWAII",6)) error("Invalid file format!");
            if(this->bin->entry < CODE_START_ADDR || this->bin->entry > this->bin->bss) error("Invalid entry point!");
            if(this->bin->magic != 0xdeadc0de) error("Corrupted file!");
            if(this->bin->bss < MAX_BIN_SIZE-BSS_SIZE) error("Invalid .bss!");
            if(this->bin->no_funcs > MAX_FUNC_ENTRIES) error("Invalid function table!");
        }

        void prepareFuncTable()
        {
            for(int i = 0; i < this->bin->no_funcs; i++)
            {
                u64 addr = (u64)(this->bin->funct[i].addr);
                
                if(addr > this->bin->bss || addr < CODE_START_ADDR) error("Invalid function table!");

                this->bin->funct[i].addr = (u64)(this->bin)+addr;
                this->bin->funct[i].callCount = 0;
            }
        }

        void prepareCtx()
        {
            this->prepareFuncTable();

            this->regs->bp = (u64 *)mmap(this->genAddr(), STACK_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
            if(this->regs->bp == (void *)(-1)) error("Unable to map stack!");
            this->regs->bp += (STACK_SIZE)/sizeof(u64);
            this->regs->sp = this->regs->bp;

            this->jitBase = (u8 *)mmap(this->genAddr(), JIT_SIZE, PROT_READ | PROT_EXEC, MAP_PRIVATE | MAP_ANON, -1, 0);
            if(this->jitBase == (void *)(-1)) error("Unable to allocate executable memory!");
            this->jitEnd = this->jitBase + JIT_SIZE;

            this->callStackBase = (kowaiiFuncEntry **)mmap(this->genAddr(), STACK_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
            if(this->callStackBase == (void *)(-1)) error("Unable to map call stack!");
            this->callStack = this->callStackBase;

            this->regs->pc = (u8 *)(this->bin)+this->bin->entry;
            this->bss = ((u8 *)(this->bin)+this->bin->bss);
            mprotect((void *)((u64)this->bin+CODE_START_ADDR), this->bin->bss-CODE_START_ADDR, PROT_READ);
        }
};

class kowaiiVm
{
    protected:
        kowaiiCtx ctx;
        u8 stepSize, dst, src1, src2;
        u64 imm;

        void initVm()
        {
            this->ctx = kowaiiCtx();
            this->ctx.readBin();
            this->ctx.checkBin();
            this->ctx.prepareCtx();
        }

        void virtual callFunc()
        {
            u16 hash = *(u16 *)(this->ctx.regs->pc+1);
            kowaiiFuncEntry *fe = NULL;

            for(int i = 0; i < this->ctx.bin->no_funcs; i++)
            {
                if(hash == this->ctx.bin->funct[i].hash)
                {
                    fe = &this->ctx.bin->funct[i];
                    break;
                }
            }
            if(!fe) error("Invalid function call!");

            *(--this->ctx.regs->sp) = (u64)(this->ctx.regs->pc+3);
            this->ctx.regs->pc = (u8 *)fe->addr;
            *(++this->ctx.callStack) = fe;
            return;
        }

        void virtual retFunc()
        {
            this->ctx.regs->pc = (u8 *)(*this->ctx.regs->sp++);
            *(this->ctx.callStack--) = NULL; 
            return;
        }

        void checkState()
        {
            switch(*this->ctx.regs->pc)
            {
                case ADD:
                case SUB:
                case MUL:
                    this->dst = *(this->ctx.regs->pc+1);
                    this->src1 = *(this->ctx.regs->pc+2);
                    this->src2 = *(this->ctx.regs->pc+3);
                    if(this->dst >= MAX_REGS || this->src1 >= MAX_REGS | this->src2 >= MAX_REGS) error("Invalid register!");
                    this->stepSize = 4;
                    break;

                case SHR:
                case SHL:
                    this->dst = *(this->ctx.regs->pc+1);
                    this->imm = *(this->ctx.regs->pc+2);
                    if(this->dst >= MAX_REGS) error("Invalid register!");
                    this->stepSize = 3;
                    break;

                case PUSH:
                    this->src1 = *(this->ctx.regs->pc+1);
                    if(this->src1 >= MAX_REGS) error("Invalid register!");
                    if((u64)(this->ctx.regs->bp - this->ctx.regs->sp) >= STACK_SIZE) error("Stack Overflow (┛ಠ_ಠ)┛彡┻━┻");
                    this->stepSize = 2;
                    break;

                case POP:
                    this->dst = *(this->ctx.regs->pc+1);
                    if(this->dst >= MAX_REGS) error("Invalid register!");
                    if(this->ctx.regs->bp <= this->ctx.regs->sp) error("Stack Underflow ┳━┳ ヽ(ಠل͜ಠ)ﾉ");
                    this->stepSize = 2;
                    break;

                case GET:
                case SET:
                    this->src1 = *(this->ctx.regs->pc+1);
                    if(this->src1 >= MAX_REGS) error("Invalid register!");
                    this->imm = *(u32 *)(this->ctx.regs->pc+2);
                    if(this->imm >= (((u64)this->ctx.bin+MAX_BIN_SIZE)-(u64)this->ctx.bss)) error("Out Of Bounds on .bss ヽ(°ロ°)ﾉ");
                    this->stepSize = 6;
                    break;

                case MOV:
                    this->dst = *(this->ctx.regs->pc+1);
                    if(this->dst >= MAX_REGS) error("Invalid register!");
                    this->imm = *(u32 *)(this->ctx.regs->pc+2);
                    this->stepSize = 6;
                    break;

                case CALL:
                    if((u64)(this->ctx.callStack - this->ctx.callStackBase + 1) >= STACK_SIZE/sizeof(kowaiiFuncEntry*)) error("Call stack Overflow (┛ಠ_ಠ)┛彡┻━┻");
                    if((u64)(this->ctx.regs->bp - this->ctx.regs->sp + 1) >= STACK_SIZE/sizeof(u64)) error("Stack Overflow (┛ಠ_ಠ)┛彡┻━┻");
                    this->stepSize = 0;
                    break;

                case RET:
                    if(this->ctx.callStack <= this->ctx.callStackBase) error("Callstack Underflow ┳━┳ ヽ(ಠل͜ಠ)ﾉ");
                    if(this->ctx.regs->bp <= this->ctx.regs->sp) error("Stack Underflow ┳━┳ ヽ(ಠل͜ಠ)ﾉ");
                    this->stepSize = 0;
                    break;
                
                case NOP:
                    this->stepSize = 1;
                    break;

                default:
                    error("segfault T_T");
                    break;
            }
        }

        void executeIns()
        {
            switch(*this->ctx.regs->pc)
            {
                case ADD:
                    this->ctx.regs->x[this->dst] = this->ctx.regs->x[this->src1] + this->ctx.regs->x[this->src2];
                    break;

                case SUB:
                    this->ctx.regs->x[this->dst] = this->ctx.regs->x[this->src1] - this->ctx.regs->x[this->src2];
                    break;

                case MUL:
                    this->ctx.regs->x[this->dst] = this->ctx.regs->x[this->src1] * this->ctx.regs->x[this->src2];
                    break;

                case SHR:
                    this->ctx.regs->x[this->dst] = this->ctx.regs->x[this->dst] >> (u8)(this->imm);
                    break;

                case SHL:
                    this->ctx.regs->x[this->dst] = this->ctx.regs->x[this->dst] << (u8)(this->imm);
                    break;

                case PUSH:
                    *(--this->ctx.regs->sp) = this->ctx.regs->x[this->src1];
                    break;

                case POP:
                    this->ctx.regs->x[this->dst] = *(this->ctx.regs->sp++);
                    break;

                case GET:
                    this->ctx.regs->x[this->src1] = *(u64 *)(this->ctx.bss + this->imm);
                    break;

                case SET:
                    *(u64 *)(this->ctx.bss + this->imm) = this->ctx.regs->x[this->src1];
                    break;

                case MOV:
                    this->ctx.regs->x[this->dst] = (u32)this->imm;
                    break;

                case CALL:
                    this->callFunc();
                    break;

                case RET:
                    this->retFunc();
                    break;

                default:
                    break;
            }
        }

    public:
        kowaiiVm()
        {
            this->initVm();
        }

        void runVm()
        {
            while(*this->ctx.regs->pc != HLT)
            {
                this->checkState();
                this->executeIns();

                this->ctx.regs->pc += this->stepSize;
            }
            cout << "[*] Execution complete!" << endl;
        }
};

void error(const char *msg)
{
    cout << "[-] " << msg << endl;
    exit(ERROR_CODE);
}
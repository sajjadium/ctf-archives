#include "kowaiiVm.cpp"

class kowaiiJitVm: public kowaiiVm
{   
    private:

        void jitEmitIns(u64 INS, u16 reg1, u16 reg2, u16 reg3)
        {
            u8 insSize = 0;
            if(INS < (1<<8)) insSize = 0x1;
            else if(INS < (1<<16)) insSize = 0x2;
            else if(INS < (1<<24)) insSize = 0x3;
            else insSize = 0x4;

            *(u64 *)(this->ctx.jitBase) = INS;
            if(reg1 != x64_NOREG)
            {
                if(reg1 < MAX_REGS) reg1 = x64_REG+reg1;
                else reg1 = reg1 & 0x3;
                *(this->ctx.jitBase+insSize-1) += reg1;
            }
            if(reg2 != x64_NOREG)
            {
                if(reg2 < MAX_REGS) reg2 = x64_REG+reg2;
                else reg2 = reg2 & 0x3;
                *(this->ctx.jitBase+insSize-1) += reg2 << 3;
            }
            if(reg3 != x64_NOREG)
            {
                if(reg3 < MAX_REGS) reg3 = x64_REG+reg3;
                else reg3 = reg3 & 0x3;
                *(this->ctx.jitBase+insSize-2) += reg3 << 3;
            }
            this->ctx.jitBase += insSize;
        }

        void jitGen(kowaiiFuncEntry *fe)
        {
            u8 *code = (u8 *)fe->addr;
            u8 reg1, reg2, reg3;
            u64 imm;
            int i = 0;
            u16 hash;
            kowaiiFuncEntry *kfe;
            vector<char> stackBalance;

            mprotect(this->ctx.jitEnd-JIT_SIZE, JIT_SIZE, PROT_READ | PROT_WRITE);

            fe->addr = (u64)this->ctx.jitBase;
            while(i < fe->size)
            {
                if(this->ctx.jitBase >= this->ctx.jitEnd) error("Out of executable memory!");
                kfe = NULL;
                reg1 = code[i+1];
                reg2 = code[i+2];
                reg3 = code[i+3];
                imm = *(u64 *)(code+i+2);
                hash = *(u16 *)(code+i+1);

                switch(code[i])
                {
                    case ADD:

                        if(reg1 != reg2 && reg1 != reg3)
                        {
                            this->jitEmitIns(x64_MOVNN, reg1, reg2, x64_NOREG);
                            this->jitEmitIns(x64_ADD, reg1, reg3, x64_NOREG);
                        }
                        else
                        {
                            if(reg1 == reg2) this->jitEmitIns(x64_ADD, reg1, reg3, x64_NOREG);   
                            else this->jitEmitIns(x64_ADD, reg1, reg2, x64_NOREG);
                        }
                        i += 4;
                        break;

                    case SUB:

                        if(reg1 != reg2 && reg1 != reg3)
                        {
                            this->jitEmitIns(x64_MOVNN, reg1, reg2, x64_NOREG);
                            this->jitEmitIns(x64_ADD, reg1, reg3, x64_NOREG);
                        }
                        else
                        {
                            if(reg1 == reg2) this->jitEmitIns(x64_ADD, reg1, reg3, x64_NOREG);   
                            else this->jitEmitIns(x64_SUB, reg1, reg2, x64_NOREG);
                        }
                        i += 4;
                        break;

                    case MUL:

                        this->jitEmitIns(x64_MOVAN, x64_RAX, reg2, x64_NOREG);
                        this->jitEmitIns(x64_MUL, reg3, x64_NOREG, x64_NOREG);
                        this->jitEmitIns(x64_XCHGAN, reg1, x64_NOREG, x64_NOREG);
                        i += 4;
                        break;

                    case SHR:

                        this->jitEmitIns(x64_MOVALI, x64_RCX, x64_NOREG, x64_NOREG);
                        *this->ctx.jitBase++ = (u8)imm; 
                        this->jitEmitIns(x64_SHR, reg1, x64_NOREG, x64_NOREG);
                        i += 3;
                        break;

                    case SHL:

                        this->jitEmitIns(x64_MOVALI, x64_RCX, x64_NOREG, x64_NOREG);
                        *this->ctx.jitBase++ = (u8)imm; 
                        this->jitEmitIns(x64_SHL, reg1, x64_NOREG, x64_NOREG);
                        i += 3;
                        break;

                    case PUSH:

                        this->jitEmitIns(x64_PUSH, reg1, x64_NOREG, x64_NOREG);
                        stackBalance.push_back('x');
                        i += 2;
                        break;

                    case POP:

                        this->jitEmitIns(x64_POP, reg1, x64_NOREG, x64_NOREG);
                        stackBalance.pop_back();
                        i += 2;
                        break;

                    case GET:

                        this->jitEmitIns(x64_MOVNP, x64_RDX, reg1, x64_NOREG);
                        *(u32 *)this->ctx.jitBase = (u32)imm;
                        this->ctx.jitBase += 4;
                        i += 6;
                        break;

                    case SET:

                        this->jitEmitIns(x64_MOVPN, x64_RDX, reg1, x64_NOREG);
                        *(u32 *)this->ctx.jitBase = (u32)imm;
                        this->ctx.jitBase += 4;
                        i += 6;
                        break;

                    case MOV:

                        this->jitEmitIns(x64_MOVNI, reg1, x64_NOREG, x64_NOREG);
                        *(u32 *)this->ctx.jitBase = imm;
                        this->ctx.jitBase += 4;
                        i += 6;
                        break;

                    case CALL:

                        for(int i = 0; i < this->ctx.bin->no_funcs; i++)
                        {
                            if(hash == this->ctx.bin->funct[i].hash)
                            {
                                kfe = &this->ctx.bin->funct[i];
                                break;
                            }
                        }
                        
                        if(!kfe) error("Invalid function call!");
                        if(kfe->addr >= (u64)this->ctx.jitEnd || kfe->addr < (u64)this->ctx.jitEnd - JIT_SIZE) error("This shouldn't happen O__O");

                        this->jitEmitIns(x64_MOVAI, x64_RAX, x64_NOREG, x64_NOREG);
                        *(u64 *)this->ctx.jitBase = kfe->addr;
                        this->ctx.jitBase += 8;
                        this->jitEmitIns(x64_CALLA, x64_RAX, x64_NOREG, x64_NOREG);
                        i += 3;
                        break;

                    case HLT: // too lazy to implement :)
                    case RET:
                        goto cleanup;

                    case NOP:
                        i++;
                        break;

                    default:
                        error("NANI?!");
                        break;
                }
            }
cleanup:
            *this->ctx.jitBase++ = x64_RET;
            mprotect(this->ctx.jitEnd-JIT_SIZE, JIT_SIZE, PROT_READ | PROT_EXEC);
        }


        __attribute__((noinline))
        __attribute__((naked))
        void jitCall(kowaiiFuncEntry *fe)
        {
            __asm__(
                "push rbp;"
                "push r8;"
                "push r9;"
                "push r10;"
                "push r11;"
                "push r12;"
                "push r13;"
                "push r14;"
                "push r15;"
                "push rdi;"
                "push rdx;"
                "push rcx;"
                "xor r8, r8;"
                "xor r9, r9;"
                "mov rbp, rsp;"
                "mov rdx, qword ptr [rdi+0x28];"
                "mov rdi, qword ptr [rdi+0x10];"
                "mov r10, qword ptr [rdi];"
                "mov r11, qword ptr [rdi+0x8];"
                "mov r12, qword ptr [rdi+0x10];"
                "mov r13, qword ptr [rdi+0x18];"
                "mov r14, qword ptr [rdi+0x20];"
                "mov r15, qword ptr [rdi+0x28];"
                "mov rsp, qword ptr [rdi+0x38];"
                "call qword ptr [rsi+0x2];"
                "mov qword ptr [rdi], r10;"
                "mov qword ptr [rdi+0x8], r11;"
                "mov qword ptr [rdi+0x10], r12;"
                "mov qword ptr [rdi+0x18], r13;"
                "mov qword ptr [rdi+0x20], r14;"
                "mov qword ptr [rdi+0x28], r15;"
                "mov rsp, rbp;"
                "pop rcx;"
                "pop rdx;"
                "pop rdi;"
                "pop r15;"
                "pop r14;"
                "pop r13;"
                "pop r12;"
                "pop r11;"
                "pop r10;"
                "pop r9;"
                "pop r8;"
                "pop rbp;"
                "ret"
            );
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

            if(fe->callCount >= JIT_CC && fe->size >= JIT_MS)
            {
                this->jitCall(fe);
                this->ctx.regs->pc += 3;
                return;
            }

            *(--this->ctx.regs->sp) = (u64)(this->ctx.regs->pc+3);
            this->ctx.regs->pc = (u8 *)fe->addr;
            *(++this->ctx.callStack) = fe;
            return;
        }

        void virtual retFunc()
        {
            this->ctx.regs->pc = (u8 *)(*this->ctx.regs->sp++);
            (*this->ctx.callStack)->callCount++;
            if((*this->ctx.callStack)->callCount >= JIT_CC && (*this->ctx.callStack)->size >= JIT_MS ) this->jitGen(*this->ctx.callStack);
            *(this->ctx.callStack--) = NULL; 
            return;
        }
};

void initialize()
{
    u32 seed;

    int urf = open("/dev/urandom", O_RDONLY);
    if(urf < 0 ) error("Can't open urandom");
    if(read(urf, &seed, sizeof(seed)) < sizeof(seed)) error("Unable to read from urandom");
    close(urf);
    srand(seed);
    
    setbuf(stdout, nullptr);
    alarm(30);
}

void printWelcomeMsg()
{
    cout << endl;
    cout << ",  ,                      .   , .   , " << endl;
    cout << "| /                 o o   |  /  |\\ /| " << endl;
    cout << "|<   ,-,  , , , ,-: . .   | /   | V | " << endl;
    cout << "| \\ (   ) |/|/  | | | |   |/    |   | " << endl;
    cout << "'  ` `-`  ' '   `-` ' '   '     '   ' " << endl;
    cout << "                                     " << endl;
    cout << "      .      ,-.          .       " << endl;
    cout << "      |   o /  /\\         |    ,- " << endl;
    cout << "      |-. . | / | ,-. ,-. |-   |  " << endl;
    cout << "      | | | \\/  / `-. |   |    |- " << endl;
    cout << "      `-' '  `-'  `-' `-' `-'  |  " << endl;
    cout << "                              -'  " << endl;
    cout << endl;
}

#ifdef SECCOMP
void kowaiiSeccomp()
{
    scmp_filter_ctx sctx;

    sctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(sctx, SCMP_ACT_ALLOW, SCMP_SYS(mprotect), 0);
    seccomp_rule_add(sctx, SCMP_ACT_ALLOW, SCMP_SYS(lseek), 0);
    seccomp_rule_add(sctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(sctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);
    seccomp_rule_add(sctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(sctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(sctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(sctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

    cout << "[*] Applying seccomp filetrs, no escape ;)" << endl;
    close(STDIN_FILENO);
    if(seccomp_load(sctx)) error("Seccomp error :^(");
}
#endif

int main()
{
    char opt;

    initialize();
    printWelcomeMsg();
    kowaiiJitVm kvm = kowaiiJitVm();
    cout << "Activate superfast™ mode?" << endl;
    cout << "> " << flush;
    cin >> opt;
    if(opt == 'y') 
    { 
        kowaiiSeccomp();
        kvm.runVm();
    }
    else
    {
        kowaiiSeccomp();
        ((kowaiiVm)kvm).runVm();
    }
}
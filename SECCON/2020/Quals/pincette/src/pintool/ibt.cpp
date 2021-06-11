#include <sys/resource.h>
#include "pin.H"

using namespace std;

ADDRINT entrypoint;
vector<pair<ADDRINT, ADDRINT>> code_regions;
BOOL entrypoint_reached = FALSE;

VOID check_pc(ADDRINT pc)
{
    struct rlimit rlim_nproc = {0, 0}, rlim_cpu = {1, 1};
    if(pc == entrypoint){
        entrypoint_reached = TRUE;
        setrlimit(RLIMIT_NPROC, &rlim_nproc);
        setrlimit(RLIMIT_CPU, &rlim_cpu);
    }
    if(entrypoint_reached){
        for(unsigned int i = 0; i < code_regions.size(); i++){
            if(code_regions[i].first <= pc && pc <= code_regions[i].second){
                return;
            }
        }
        PIN_ERROR("Invalid PC!\n");
    }
}

VOID check_target(ADDRINT target, ADDRINT pc)
{
    UINT8 buf[4];
    if(entrypoint_reached == FALSE){
        return;
    }
    if(PIN_SafeCopy(&buf, (VOID*)target, sizeof(buf)) == sizeof(buf)
    && (buf[0] == 0xf3 && buf[1] == 0x0f && buf[2] == 0x1e && buf[3] == 0xfa)){
        return;
    }
    PIN_ERROR("Invalid branch target!\n");
}

VOID imgload_callback(IMG img, VOID *v)
{
    if(IMG_IsInterpreter(img) || IMG_IsVDSO(img)){
        return;
    }
    if(IMG_IsMainExecutable(img)){
        entrypoint = IMG_EntryAddress(img);
    }
    for(SEC sec = IMG_SecHead(img); SEC_Valid(sec); sec = SEC_Next(sec)){
        if(SEC_IsExecutable(sec) == TRUE){
            code_regions.push_back(make_pair(
                SEC_Address(sec), SEC_Address(sec) + SEC_Size(sec) - 1));
        }
    }
}

VOID ins_callback(INS ins, VOID *v)
{
    INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)check_pc,IARG_INST_PTR,
        IARG_END);
    if(INS_IsIndirectControlFlow(ins) && INS_IsRet(ins) == FALSE){
        INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)check_target,
            IARG_BRANCH_TARGET_ADDR, IARG_INST_PTR, IARG_END);
    }
}

int main(int argc, char *argv[])
{
    PIN_Init(argc,argv);
    IMG_AddInstrumentFunction(imgload_callback, 0);
    INS_AddInstrumentFunction(ins_callback, 0);
    PIN_StartProgram();
    return 0;
}

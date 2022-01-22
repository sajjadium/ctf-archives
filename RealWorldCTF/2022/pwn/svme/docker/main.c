#include <stdbool.h>
#include <unistd.h>
#include "vm.h"

int main(int argc, char *argv[]) {
    int code[128], nread = 0;
    while (nread < sizeof(code)) {
        int ret = read(0, code+nread, sizeof(code)-nread);
        if (ret <= 0) break;
        nread += ret;
    }
    VM *vm = vm_create(code, nread/4, 0);
    vm_exec(vm, 0, true);
    vm_free(vm);
    return 0;
}


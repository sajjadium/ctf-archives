#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <dlfcn.h>

typedef void*(*func_t)(uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t, uintptr_t);

bool security_check() {
    FILE* f = fopen("/proc/self/maps", "rb");
    if (f == NULL)
        return false;
    
    unsigned long long from, to;
    char buf[1024];
    while (fgets(buf, sizeof(buf), f)) {
        sscanf(buf, "%llx-%llx", &from, &to);
        if (from < 0x100000000LLu || to < 0x100000000LLu) {
            fclose(f);
            return false;
        }
    }
    
    fclose(f);
    return true;
}

int main() {
    char lib_and_symbol[65];
    char lib_name[128];
    char* sep;
    unsigned int arg1, arg2, arg3, arg4, arg5, arg6;
    int i;
    
    void* lib = NULL;
    
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    puts("[debug] RPC ready");

    while (true) {
        // Ensure that the process is secure.
        if (!security_check()) {
            fprintf(stderr, "security error!\n");
            exit(1);
        }
        
        // Read the lib and symbol name and 6 parameters.
        scanf(" %64[^ ]", lib_and_symbol);
        scanf("%u %u %u %u %u %u", &arg1, &arg2, &arg3, &arg4, &arg5, &arg6);
        
        // Ensure the input is safe.
        for (i = 0; lib_and_symbol[i]; i++) {
            if ((lib_and_symbol[i] >= '0' && lib_and_symbol[i] <= '9') ||
                (lib_and_symbol[i] >= 'a' && lib_and_symbol[i] <= 'z') ||
                lib_and_symbol[i] == '_' || lib_and_symbol[i] == ':')
                continue;
            fprintf(stderr, "rpc service name or symbol name contains illegal characters\n");
            exit(1);
        }
        
        // Split the lib and symbol name.
        sep = strchr(lib_and_symbol, ':');
        if (sep == NULL) {
            fprintf(stderr, "missing rpc service name\n");
            exit(1);
        }
        *sep = 0;
        
        // Open the lib.
        sprintf(lib_name, "rpc_%s.so", lib_and_symbol);
        lib = dlopen(lib_name, RTLD_LAZY);
        
        // Check if the symbol is valid.
        func_t func = (func_t) dlsym(lib, sep + 1);
        if ((sep + 1)[0] == '_' || func == NULL) {
            fprintf(stderr, "symbol not found: %s\n", sep + 1);
            exit(1);
        }
        
        // Call the function.
        func(arg1, arg2, arg3, arg4, arg5, arg6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

	printf("[debug] finished %s:%s(%#x, %#x, %#x, %#x, %#x, %#x) RPC\n",
	       lib_name, sep+1, arg1, arg2, arg3, arg4, arg5, arg6);
    }
}

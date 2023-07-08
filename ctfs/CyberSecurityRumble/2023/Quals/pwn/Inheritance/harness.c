
#include <stddef.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/resource.h>
#include <string.h>

#define PARENT_PATH "./parent"

unsigned long long read_limit() {
    fflush(stdout);
    char line[256];
    unsigned long long i = 0;
    if (fgets(line, sizeof(line), stdin)) {
        if (1 == sscanf(line, "%llu", &i)) {
            return i;
        }
        else {
            return -1;
        }
    }
    return -1;
}

int main() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
    
    struct rlimit limit, old_limit;
    unsigned long long tmp_limit = 0;

    char file_name[256];

    puts("[+] Getting old limits:");
    getrlimit(RLIMIT_DATA, &old_limit);
    printf("[*] Old soft limit: %lu\n", old_limit.rlim_cur);
    printf("[*] Old hard limit: %lu\n", old_limit.rlim_max);

    puts("[+] Please enter a new limit:");    
    fflush(stdout);
    tmp_limit = read_limit();
    
    puts("[+] Setting the new limit");
    limit.rlim_cur = tmp_limit;
    limit.rlim_max = tmp_limit;
    if(setrlimit(RLIMIT_DATA ,&limit) != 0) {
        puts("[-] setrlimit failed");
    }

    puts("[+] Please enter a file name:");
    fflush(stdout);
    fgets(file_name, 256, stdin);
    file_name[strcspn(file_name, "\n")] = 0;

    puts("[+] Executing target");
    fflush(stdout);
    execl(PARENT_PATH, "parent", file_name, NULL);
}


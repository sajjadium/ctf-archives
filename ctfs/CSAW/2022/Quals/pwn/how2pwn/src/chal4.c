#include <linux/seccomp.h>
#include <unistd.h>
#include <syscall.h>
#include <sys/prctl.h>
#include <linux/filter.h>
#include <string.h>
#include <sys/ioctl.h>
#include <stddef.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <sys/mman.h>
void panic(char *s){
    puts(s);
    _exit(1);
}
void checkin(){ 
    // Solved the previous challenge, and find the ticket in "/flag"
    char real_ticket[0x30] = {0};
    char your_ticket[0x30] = {0};
    int f = open("./ticket",0);
    if(f<0)
        panic("[-] Fail to open tickect");
    read(f,real_ticket,0x20);
    read(0,your_ticket,0x20);
    close(f);
    if(strncmp(real_ticket,your_ticket,0x20))
        panic("[-] Wrong Ticket");
    return ; 
}
void init(){
    fclose(stderr);
    setvbuf(stdin,  0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    checkin();
}
void sandbox(){
    // challenge setting
    // This sandbox only allows __NR_seccomp __NR_fork __NR_ioctl __NR_exit
    // and it would trace all other syscalls
    struct sock_filter strict_filter[] = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS,offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_seccomp, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
		BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_fork, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
		BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_ioctl, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
		BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_exit, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_TRACE),
    };
    struct sock_fprog prog = {
        .len = sizeof(strict_filter) / sizeof(strict_filter[0]),
        .filter = strict_filter,
    };
    int ret = 0 ; 
    ret = syscall(__NR_prctl,PR_SET_NO_NEW_PRIVS, 1,0,0,0);
    if(ret!=0)
        panic("[-] PR_SET_NO_NEW_PRIVS FAIL");
    // Apply the filter. 
    ret = syscall(__NR_seccomp,SECCOMP_SET_MODE_FILTER,0,&prog);
    if(ret!=0)
        panic("[-] SECCOMP_SET_MODE_FILTER FAIL");
    puts("[+] Sandbox On");

}
int main(){
    init();
    // To make exploit script easier, our shellcode would be on 0xcafe000
    char *buf = mmap((void *)0xcafe000,0x1000,7,0x21,0,0);
    if((size_t)buf!=0xcafe000)
        panic("Fail to mmap");
    puts("Enter your shellcode: ");
    read(0, buf, 0x1000);
    void (* p )(); 
    p = (void (*)())buf;
    sandbox();
    p();
    return 1;
}

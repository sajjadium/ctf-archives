/*gcc -z lazy -z noexecstack -fstack-protector robot.c -o robot*/

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <fcntl.h>
#include <signal.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "SECCOMP.h"
//#include<seccomp.h>

struct sock_filter seccompfilter[] = {
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, ArchField),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, SyscallNum),
    Allow(read),
    Allow(write),
    Allow(rt_sigreturn),
    Allow(exit),
    Allow(exit_group),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
};

struct sock_fprog filterprog = {
    .len = sizeof(seccompfilter) / sizeof(struct sock_filter),
    .filter = seccompfilter};

void apply_seccomp()
{
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0))
    {
        perror("Seccomp Error");
        exit(1);
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &filterprog) == -1)
    {
        perror("Seccomp Error");
        exit(1);
    }
    return;
}

void initproc()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    return;
}

int move(unsigned int *pos, unsigned int x, unsigned int y)
{
    int newx = pos[0] + x;
    int newy = pos[1] + y;
    if (newx < 0 || newx >= 100 || newy < 0 || newy >= 100)
        return -1;
    else
    {
        pos[0] = newx;
        pos[1] = newy;
        return 1;
    }
}

_Noreturn main()
{
    initproc();
    int pipefd[4];
    if (pipe2(pipefd, O_CLOEXEC | O_DIRECT) == -1 || pipe2(&(pipefd[2]), O_CLOEXEC | O_DIRECT) == -1)
    {
        puts("Cannot establish connection to robot");
        exit(1);
    }
    int pid = fork();
    if (pid < 0)
    {
        puts("Robot bootup failed");
        exit(1);
    }
    if (pid != 0)
    {
        close(pipefd[0]);
        close(pipefd[3]);
        char *buf = mmap(NULL, 0x100, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        int randfd = open("/dev/urandom", O_RDONLY);
        if (buf == (void *)-1 || randfd == -1)
        {
            puts("Monitor crashed");
            exit(1);
        }
        int seed;
        read(randfd, &seed, 4);
        srand(seed);
        close(randfd);
        unsigned int robot[2] = {((unsigned int)rand()) % 20, ((unsigned int)rand()) % 20};
        unsigned int outlaw[2] = {80U + (unsigned int)rand() % 20, 80U + ((unsigned int)rand()) % 20};
        for (int i = 0; i < 1000; i++)
        {
            read(pipefd[2], buf, 0x1000);
            siginfo_t status = {0, 0, 0, 0, 0};
            int waitres = waitid(P_PID, pid, &status, WNOHANG | WEXITED);
            if (waitres == -1)
            {
                kill(pid, SIGKILL);
                puts("Monitor malfunctioning");
                exit(1);
            }
            else if (status.si_pid == pid)
            {
                if (status.si_code == CLD_EXITED && status.si_status == 0)
                    puts("AI halted");
                else
                    puts("AI crashed");
                exit(0);
            }
            if (buf[0] == 'S')
            {
                buf[0] = robot[0] + 1;
                buf[1] = robot[1] + 1;
                buf[2] = outlaw[0] + 1;
                buf[3] = outlaw[1] + 1;
                buf[4] = '\0';
            }
            else if (buf[0] == 'M')
            {
                int moveres = 0;
                if (buf[1] == 'A')
                    moveres = move(robot, -1, 0);
                else if (buf[1] == 'D')
                    moveres = move(robot, 1, 0);
                else if (buf[1] == 'W')
                    moveres = move(robot, 0, 1);
                else if (buf[1] == 'S')
                    moveres = move(robot, 0, -1);
                if (moveres == -1)
                    strcpy(buf, "Failed");
                else if (moveres == 1)
                    strcpy(buf, "Success");
            }
            else if (buf[0] == 'G')
            {
                puts("Mission failed :(");
                puts("Only quitters giveup");
                kill(pid, SIGKILL);
                exit(0);
            }
            else
            {
                buf[0] = '\0';
            }
            if (robot[0] == outlaw[0] && robot[1] == outlaw[1])
            {
                puts("Mission cleared!");
                puts("Here is a token to show our gratitude : NOTFLAG{Super shellcoder}");
                exit(0);
            }
            move(outlaw, (((unsigned int)rand()) % 2) - 1, (((unsigned int)rand()) % 2) - 1);
            dprintf(pipefd[1], buf);
        }
        puts("Mission failed :(");
        puts("Robot ran out of fuel");
        kill(pid, SIGKILL);
    }
    else
    {
        close(pipefd[1]);
        close(pipefd[2]);
        void (*ropchain)() = mmap((void *)((((unsigned long long)(main)>>12)+0x10)<<12), 0x100, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        printf("Gift1: %p\n", ropchain);
        printf("Gift2: %p\n", main);
        //printf("Gift3: %p\n", printf);
        if (ropchain == (void *)-1)
        {
            puts("Robot initialisation failed");
            exit(1);
        }
        printf("Give me chain : ");
        fgets((char *)ropchain, 0x8e0, stdin);
        close(STDIN_FILENO);
        close(STDOUT_FILENO);
        close(STDERR_FILENO);
        apply_seccomp();
        asm("mov %0, %%rsp\n"
            "xor %%rdx, %%rdx\n"
            "xor %%rax, %%rax\n"
            "xor %%rbx, %%rbx\n"
            "xor %%rcx, %%rcx\n"
            "xor %%rsi, %%rsi\n"
            "xor %%rdi, %%rdi\n"
            "xor %%rbp, %%rbp\n"
            "xor %%r8, %%r8\n"
            "xor %%r9, %%r9\n"
            "xor %%r10, %%r10\n"
            "xor %%r11, %%r11\n"
            "xor %%r12, %%r12\n"
            "xor %%r13, %%r13\n"
            "xor %%r14, %%r14\n"
            "xor %%r15, %%r15\n"
            "ret\n"
            "pop %%rax\n"
            "ret\n"
            "pop %%rcx\n"
            "ret\n"
            "pop %%rdx\n"
            "ret\n" ::"r"(*ropchain));
    }
    exit(0);
}

#define _GNU_SOURCE
#include <sys/ioctl.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/klog.h>
#include <unistd.h>
#include <time.h>
#include <sys/shm.h>
#include <sys/timerfd.h>
#include <poll.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/syscall.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <time.h>
#include <errno.h>
#include <sys/msg.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "base64.h"
#include "../kernel_module/includes/ioctls.h"

#define u64 uint64_t
#define u32 uint32_t
#define u16 uint16_t
#define u8 uint8_t

#define NUMBUS 0x100

typedef struct mapping {
    void *vaddr;
    int vm;
    u64 size;
} mapping_t;

int vms[NUMBUS];
mapping_t mappings[NUMBUS];
pid_t pids[NUMBUS];
static int *return_codes;

void setup(void)
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
    memset(vms, 0xff, sizeof(vms));
    memset(pids, 0xff, sizeof(vms));
    memset(mappings, 0x0, sizeof(vms));
}

void readline(char *ptr, u64 size) {
    read(0, ptr, size);
}

u64 readnum() {
    char buf[0x10];
    readline(buf, sizeof(buf));
    return strtouq(buf, 0, 0);
}

void create(void) {
    printf("index: ");
    u64 num = readnum();
    if (num >= NUMBUS){
        puts("index out of bound");
        exit(0);
    }
    if (vms[num] != -1)
    {
        puts("vm already exists");
        exit(0);
    }
    vms[num] = open("/dev/hyper-k", O_RDWR);    
    puts("vm created");
}

int get_vm(void) {
    printf("vm index: ");
    u64 num = readnum();
    if (num >= NUMBUS){
        puts("index out of bound");
        exit(0);
    }
    if (vms[num] == -1) {
        puts("vm do not exist");
        exit(0);
    }
    return vms[num];
}

mapping_t *get_map(void) {
    printf("mapping index: ");
    u64 num = readnum();
    if (num >= NUMBUS){
        puts("index out of bound");
        exit(0);
    }
    mapping_t *map = &mappings[num];
    return map;
}

void map(void) {
    int vm = get_vm();
    mapping_t *map = get_map();
    if (map->vm != 0) {
        puts("mapping already exist");
        exit(0);
    }
    printf("vm physical addr: ");
    u64 phys = readnum();
    printf("map size: ");
    u64 size = readnum();
    map->vaddr = mmap((void *)0, size, PROT_WRITE | PROT_READ, MAP_SHARED, vm, phys);
    map->vm = vm;
    map->size = size;
    puts("mapping created");
}

void unmap(void) {
    mapping_t *map = get_map();
    if (map->vm == 0) {
        puts("mapping do not exist");
        exit(0);
    }
    munmap(map->vaddr, map->size);
    memset(map, 0, sizeof(mapping_t));
    puts("mapping removed");
}

void read_from_vm(void) {
    mapping_t *map = get_map();
    if (map->vm == 0) {
        puts("mapping do not exist");
        exit(0);
    }
    printf("size: ");
    u64 size = readnum();
    printf("offset: ");
    u64 offset = readnum();
    if (size > 0x10000)
    {
        puts("no more data");
        exit(0);
    }
    if (offset + size > map->size)
    {
        puts("no overflow");
        exit(0);
    }
    u8 *data = base64_encode(map->vaddr + offset, size, &size);
    printf("data: %s\n", data);
    free(data);
}

void write_to_vm(void) {
    mapping_t *map = get_map();
    if (map->vm == 0) {
        puts("mapping do not exist");
        exit(0);
    }
    printf("size: ");
    u64 size = readnum();
    if (size > 0x10000)
    {
        puts("no more data");
        exit(0);
    }
    printf("offset: ");
    u64 offset = readnum();
    u8 *buf = malloc(size);
    printf("data: ");
    read(0, buf, size);
    while(getchar() != '\n');
    u8 *data = base64_decode(buf, size, &size);
    if (!data)
    {
        puts("decode error");
        exit(0);
    }
    if (offset + size > map->size)
    {
        puts("no overflow");
        exit(0);
    }
    memcpy(map->vaddr + offset, data, size);
    free(buf);
    free(data);
}

void get_regs(void) {
    u64 size;
    userspace_regs_t regs;
    int vm = get_vm();
    ioctl(vm, IOCTL_GET, &regs);
    u8 *data = base64_encode((u8 *)&regs, sizeof(regs), &size);
    printf("regs: %s\n", data);
    free(data);
}

void set_regs(void) {
    int vm = get_vm();
    printf("size: ");
    u64 size = readnum();
    if (size > 0x1000)
    {
        puts("no more data");
        exit(0);
    }
    u8 *buf = malloc(size);
    printf("regs: ");
    read(0, buf, size);
    while(getchar() != '\n');
    u8 *data = base64_decode(buf, size, &size);
    if (!data)
    {
        puts("decode error");
        exit(0);
    }
    if (size != sizeof(userspace_regs_t))
    {
        puts("wrong registes size");
        exit(0);
    }
    ioctl(vm, IOCTL_PUT, data);
    puts("regs set");
    free(buf);
    free(data);
}

void delete(void) {
    printf("vm index: ");
    u64 num = readnum();
    if (num >= NUMBUS){
        puts("index out of bound");
        exit(0);
    }
    if (vms[num] == -1) {
        puts("vm do not exist");
        exit(0);
    }
    int vm = vms[num];
    for (int i = 0; i < NUMBUS; i++) {
        mapping_t *map = &mappings[i];
        if (map->vm != vm)
            continue;
        munmap(map->vaddr, map->size);
        memset(map, 0, sizeof(mapping_t));
    }
    close(vm);
    vms[num] = -1;
    puts("vm deleted");
}

void run(void) {
    printf("vm index: ");
    u64 num = readnum();
    if (num >= NUMBUS){
        puts("index out of bound");
        exit(0);
    }
    if (vms[num] == -1) {
        puts("vm do not exist");
        exit(0);
    }
    int vm = vms[num];
    puts("running vm");
    int pi = fork();
    if (!pi) {
        int ret = ioctl(vm, IOCTL_RUN);
        return_codes[num] = ret;
        exit(0);
    }
    pids[num] = pi;
}

void wait_for_vm(void) {
    printf("vm index: ");
    u64 num = readnum();
    if (num >= NUMBUS){
        puts("index out of bound");
        exit(0);
    }
    if (pids[num] == -1) {
        puts("vm not running");
        exit(0);
    }
    waitpid(pids[num], 0, 0);
    printf("return status: %d\n", return_codes[num]);
}

void menu(void) {
    printf("\n1) create\n2) mmap\n3) munmap\n4) read\n5) write\n6) get registers\n7) set registers\n8) delete\n9) run\n10) wait\noption: ");
}

void banner(void) {
    printf( "\nWelcome to hyper-k here you can run you x86 code in our cloud hypervisor.\n"
            "You can set registers and system registers as you like but if left untouched before running vm will boot in realmode.\n"
            "If CS and rip is left untouced the vm will beging executing at address 0.\n" ); 
}

int main(void)
{
    setup();
    return_codes = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    banner();
    while(1) {
        menu();
        u8 choice = (u8)readnum();
        switch(choice) {
            case 1:
                create();
                break;
            case 2:
                map();
                break;
            case 3:
                unmap();
                break;
            case 4:
                read_from_vm();
                break;
            case 5:
                write_to_vm();
                break;
            case 6:
                get_regs();
                break;
            case 7:
                set_regs();
                break;
            case 8:
                delete();
                break;
            case 9:
                run();
                break;
            case 10:
                wait_for_vm();
                break;
            default:
                return 0;
        }
    }
    return 0;
}


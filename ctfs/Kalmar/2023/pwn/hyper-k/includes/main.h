#pragma once
#include <asm-generic/int-ll64.h>
#include <linux/mutex.h>
#include "../includes/ioctls.h"
#include "../includes/vmcs.h"
#include "../includes/memory.h"

typedef struct vm_t vm_t;

#define VMEXIT_HANDLED -1

typedef struct vcpu_t
{
    __u8 msr_bitmap[0x4000];
    struct __vmcs_t vmcs;
    __u64 vmcs_pa;
    state_t state;
    vm_t *vm;

    __u8 host_cpu_id;
    __u8 initialized;
    __u8 launched;

} __attribute__((packed)) vcpu_t;


typedef struct vm_t
{
        vcpu_t vcpu;
        memory_t *memory;
        struct mutex vm_mutex;
} vm_t;


void vmx_on(void);
void vmx_off(void);
vm_t *vm_alloc(void);
int vm_destroy(vm_t *vm);
int vcpu_run(vcpu_t *vcpu);
void init_sregs(sregs_t *sregs);
void clearvm(vcpu_t *vcpu);

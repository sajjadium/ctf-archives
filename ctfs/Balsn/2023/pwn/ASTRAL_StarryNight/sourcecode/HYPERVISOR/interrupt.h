#ifndef __INTERRUPT_HEADER__
#define __INTERRUPT_HEADER__

#include <stddef.h>
#include "hypervisor.h"
#include "device.h"
#include "hypercall.h"

#define APPLET_INVOKE_INTERRUPT 0x01
#define APPLET_RES_INTERRUPT 0x02

void injectInterrupt(VM *vm, uint64_t interruptEntry, uint64_t kernelInterruptStackAddr);

#endif

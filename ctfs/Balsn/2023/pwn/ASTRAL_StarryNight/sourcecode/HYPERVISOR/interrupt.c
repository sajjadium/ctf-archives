#include "interrupt.h"

void runInterruptHandler(VM *vm, uint8_t type, uint64_t interruptEntry, uint64_t kernelInterruptStackAddr, uint8_t *data) {
  struct kvm_regs origRegs;
  struct kvm_regs newRegs;
  uint64_t stackOffset = KERNEL_STACK_SIZE - PAGE_UPALIGN(DV_INTERRUPT_DATA_SIZE_MAX);
  if (ioctl(vm->vcpufd, KVM_GET_REGS, &origRegs) < 0) printError("runInterruptHandler::KVM_GET_REGS failed");
  memset(&newRegs, '\0', sizeof(struct kvm_regs));
  newRegs.rip = interruptEntry;
  newRegs.rsp = kernelInterruptStackAddr + stackOffset;
  newRegs.rsi = kernelInterruptStackAddr + stackOffset;
  newRegs.rflags = 0x2;
  if (type == DV_APPLET_RES_INTERRUPT) {
    newRegs.rdi = APPLET_RES_INTERRUPT;
    setMem(vm, KERNEL_INTERRUPT_STACK_PADDR + stackOffset, sizeof(HYPER_APPLET_RES), data);
    newRegs.rdi = APPLET_RES_INTERRUPT;
  } else if (type == DV_APPLET_INVOKE_INTERRUPT) {
    newRegs.rdi = APPLET_INVOKE_INTERRUPT;
    setMem(vm, KERNEL_INTERRUPT_STACK_PADDR + stackOffset, sizeof(HYPER_APPLET_CONTEXT), data);
  } else {
    printError("runInterruptHandler::unknown interrupt");
  }
  if (ioctl(vm->vcpufd, KVM_SET_REGS, &newRegs) < 0) printError("runInterruptHandler::KVM_SET_REGS failed");
  execute(vm, interruptEntry, kernelInterruptStackAddr);
  if (ioctl(vm->vcpufd, KVM_SET_REGS, &origRegs) < 0) printError("runInterruptHandler::KVM_SET_REGS failed");
  return;
}

void injectInterrupt(VM *vm, uint64_t interruptEntry, uint64_t kernelInterruptStackAddr) {
  if (vm->withinInterrupt || vm->run->io.direction == KVM_EXIT_IO_OUT) return;
  vm->withinInterrupt = true;
  uint8_t req[DV_INTERRUPT_DATA_SIZE_MAX];
  uint8_t type = dv_recvInterrupt(req);
  if (type == DV_NO_INTERRUPT) {
    vm->withinInterrupt = false;
    return;
  } else if (type == DV_APPLET_RES_INTERRUPT || type == DV_APPLET_INVOKE_INTERRUPT) {
    runInterruptHandler(vm, type, interruptEntry, kernelInterruptStackAddr, req);
  } else if (type == DV_APPLET_PROCESSOR_FLAG_INTERRUPT) {
    printFlag(PROCESSORSPACE_FLAG_FNAME);
  } else {
    printError("injectInterrupt::unknown interrupt");
  }
  vm->withinInterrupt = false;
  return;
}

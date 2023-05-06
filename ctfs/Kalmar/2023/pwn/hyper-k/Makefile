ifeq ($(KERNELRELEASE),)
                PWD := $(shell pwd)
                KERNELDIR ?= $(PWD)/../linux

modules:
		$(MAKE) -C $(KERNELDIR) M=$(PWD) modules CC=clang
clean:
		rm -rf *.o *~ core .depend .*.cmd *.ko *.mod.c .tmp_versions hyperk.mod Module.symvers modules.order

.PHONY: modules clean

else
        # called from kernel build system: just declare what our modules are
		obj-m := hyperk.o
		hyperk-objs := src/asm_functions.o src/vmx.o src/memory.o src/main.o
endif

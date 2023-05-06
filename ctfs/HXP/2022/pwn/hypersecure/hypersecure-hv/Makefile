obj-m += hypersecure.o
hypersecure-objs := \
	hypersecure-asm.o \
	hypersecure-main.o \
	hypersecure-mm.o \
	hypersecure-debug.o \
	hypersecure-user.o

all:
	make -B -C $(KERNEL_DIR) M=$(PWD) modules

clean:
	make -C $(KERNEL_DIR) M=$(PWD) clean

.FORCE:

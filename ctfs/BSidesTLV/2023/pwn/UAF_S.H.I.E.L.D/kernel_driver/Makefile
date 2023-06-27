#Tested with kernel v5.14 
KVERSION		= ${KERNEL_VERSION}
LKM             = uaf_shield
PWD            := $(shell pwd)

obj-m          += $(LKM).o

all:
	make -C /lib/modules/${KVERSION}/build M=$(PWD) modules
clean:
	make -C /lib/modules/${KVERSION}/build M=$(PWD) clean

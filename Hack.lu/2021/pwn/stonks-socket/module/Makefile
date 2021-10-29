M ?= $(shell basename $(PWD))

ifneq ($(KERNELRELEASE),)

obj-m := stonks_socket.o

else
UNAME ?= $(shell uname -r)
# UNAME ?=$(uname -r)
PWD             ?= $(shell pwd)
#KDIR ?= /lib/modules/$(UNAME)/build
KDIR ?= /lib/modules/5.11.0-38-generic/build

MY_CFLAGS += -g -DDEBUG
ccflags-y += ${MY_CFLAGS}
CC += ${MY_CFLAGS}

default:
	$(MAKE) -C $(KDIR) M=$(shell pwd) modules
test:
	$(CC) -static -o test_$(M) test_$(M).c

endif

clean:
	rm -rf *.ko *.o *.mod.c .*.cmd .tmp_versions *.symvers *.order *.mod
	rm -f "test_$(M)"

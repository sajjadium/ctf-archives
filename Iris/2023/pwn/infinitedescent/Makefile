MACHINE := lm3s6965evb
CMSIS := ./CMSIS_5

SRC_ASM = $(CMSIS)/Device/ARM/ARMCM3/Source/GCC/startup_ARMCM3.S
SRC_C = $(CMSIS)/Device/ARM/ARMCM3/Source/system_ARMCM3.c \
        chal.c

INCLUDE_FLAGS = \
  -I$(CMSIS)/Device/ARM/ARMCM3/Include \
  -I$(CMSIS)/CMSIS/Core/Include

CFLAGS = \
  -mcpu=cortex-m3 \
  -specs=nano.specs \
  -specs=nosys.specs \
  -specs=rdimon.specs \
  -Wall \
  -g3 \
  $(INCLUDE_FLAGS) \
  -mthumb \
  -nostartfiles \
  -fdata-sections \
  -ffunction-sections \
  -Wl,--gc-sections \
  -DARMCM3 \
  -D__CORTEX_M3

all: $(SRC_C) $(SRC_ASM)
	arm-none-eabi-gcc $^ $(CFLAGS) -T gcc_arm.ld -o chal.elf

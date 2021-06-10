# apt install gcc-avr binutils-avr srecord
NAME = avr_main

MMCU = attiny2313
F_CPU = 8000000

CFLAGS:=${CFLAGS} -Wall -Os -mmcu=${MMCU} -DF_CPU=${F_CPU}
LDFLAGS:=${LDFLAGS} -Wl,--defsym,boot=0x400

all: ${NAME}.elf ${NAME}.hex eeprom.hex

# Compilation
%.o: %.c
	avr-gcc -c ${CFLAGS} ${^} -o ${@}

# Linking
%.elf: %.o
	avr-gcc ${LDFLAGS} ${CFLAGS} ${^} -o ${@}
	avr-size -C --mcu=${MMCU} ${@}

# Conversion to ihex
%.hex: %.elf
	avr-objcopy -O ihex -j .text ${^} ${@}

eeprom.hex: ${NAME}.elf
	avr-objcopy --dump-section .eeprom=eeprom.bin ${^}
	srec_cat eeprom.bin -Binary -Output ${@} -Intel
	rm eeprom.bin

clean:
	rm -f ${NAME}.o ${NAME}.elf ${NAME}.hex eeprom.hex

.PHONY: all clean

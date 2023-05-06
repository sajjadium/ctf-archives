CC := clang
AS := riscv32-elf-as
OBJCOPY := riscv32-elf-objcopy

CFLAGS := -Wall -Wextra -Wunused -Wnull-dereference -Wdouble-promotion -Wconversion \
	-Wsign-conversion -Wmissing-prototypes \
	-Og -ggdb3
LDFLAGS := $(CFLAGS)

BUILD := build

OBJECTS := $(patsubst src/%.c,%.o,$(shell find src -type f -name '*.c'))
HEADERS := $(shell find src -type f -name '*.h')

.PHONY: all
all: riscv-jit example

.PHONY: clean
clean:
	rm -rf $(BUILD)

.PHONY: riscv-jit
riscv-jit: $(BUILD)/riscv-jit

# Compile main binary from all objects
$(BUILD)/riscv-jit: $(patsubst %,$(BUILD)/%,$(OBJECTS))
	$(CC) $(LDFLAGS) -o $@ $^

# Define prerequisites for objects: Source and all headers
define prereq
$(BUILD)/$(1): $(patsubst %.o,src/%.c,$(1)) $(HEADERS)
endef
$(foreach o,$(OBJECTS),$(eval $(call prereq,$(o))))

# Compile single object
$(BUILD)/%.o:
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c -o $@ $<

# Build example code
.PHONY: example
example: $(BUILD)/example.bin

$(BUILD)/example.elf: example.asm
	@mkdir -p $(dir $@)
	$(AS) -march=rv32i -mabi=ilp32 -mlittle-endian -fpic -o $@ $<

$(BUILD)/example.bin: $(BUILD)/example.elf
	$(OBJCOPY) -O binary $< $@

.PHONY: default run clean
default: compile

BIN  := grhealth
SRC  := main.c
HDR  := glacier_resilience.h
PMR := 0 10

# Compile flags, pass PMC standards
CFLAGS += -O2 -Werror -Wall -Wextra -Wformat=2 -Wno-unused-parameter           \
-Wformat-overflow=2 -Wformat-truncation=2 -Wformat-security -Wnull-dereference \
-Wstack-protector -Wtrampolines -Walloca -Wvla -Warray-bounds=2                \
-Wimplicit-fallthrough=3 -Wshift-overflow=2 -Wcast-qual -Wstringop-overflow=4  \
-Wconversion -Warith-conversion -Wlogical-op -Wduplicated-cond                 \
-Wduplicated-branches -Wformat-signedness -Wshadow -Wstrict-overflow=4 -Wundef \
-Wstrict-prototypes -Wswitch-default -Wswitch-enum -Wstack-usage=1000000       \
-Wcast-align=strict -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=3                      \
-fstack-protector-strong -fstack-clash-protection -fPIE -fsanitize=bounds      \
-fsanitize-undefined-trap-on-error -Wl,-z,relro -Wl,-z,now -Wl,-z,noexecstack  \
-Wl,-z,separate-code # src: https://github.com/airbus-seclab/c-compiler-security

compile: $(BIN)
$(BIN): $(SRC) $(HDR)
	$(CC) $(CFLAGS) $(SRC) -o $(BIN)
	strip $(BIN)

run: $(BIN)
	./$< $(PMR)
	
clean:
	rm -f $(BIN)

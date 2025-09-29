# EAR Essential Architecture Reference v3

The EARv3 architecture uses 8-bit bytes. It uses a 16-bit virtual address space, with 24-bit
physical addressing. Byte ordering for memory operations is little-endian. There are 16
general purpose 16-bit registers, explained in the table below. In addition to that, there
are bit flags for conditional execution.

## EAR Instruction Set Architecture

### General Purpose Registers

| Register | Aliases     | Description
|----------|-------------|-------------
| `R0`     | `ZERO`      | Always holds the value 0. Writes are ignored
| `R1-R6`  | `A0-A5`     | General purpose temporary and parameters (caller-saved)
| `R7-R9`  | `S0-S2`     | General purpose permanent (callee-saved)
| `R10`    | `FP`        | Frame Pointer (callee-saved)
| `R11`    | `SP`        | Stack Pointer
| `R12`    | `RA`        | Return Address
| `R13`    | `RD`        | Return Delta
| `R14`    | `PC`        | Program Counter
| `R15`    | `DPC`       | Delta PC: After reading each code byte, `PC := PC + 1 + DPC`. Default value is 0


### CPU Flags

Flags are updated by default by unconditional instructions, whereas conditional instructions
(instructions where `cc` is not `AL`) do not update `FLAGS` normally. This is done to enable running
multiple instructions in a row in a conditional block without clobbering the condition flags. There
is an instruction prefix byte, `TF` aka Toggle Flags, which inverts this behavior, causing
unconditional instructions to not update `FLAGS` and for conditional instructions to write back the
new value of `FLAGS`. To use this instruction modifier in assembler syntax, add the `F` suffix to an
instruction such as `MOVF`, `ADDF.EQ`, or `DECF.PS`.

| Name | Description
|------|-------------
| `ZF` | Zero Flag, set when the computation result is zero
| `SF` | Sign Flag, set when the computation result's high bit is set
| `PF` | Parity Flag, set when the computation result has an odd number of bits set
| `CF` | Carry Flag, set when the computation result would have bit 16 set
| `VF` | Overflow Flag, set when the signed computation overflowed


### Conditions

Each instruction's opcode byte has two parts: a 3-bit condition code and a 5-bit opcode.
Condition codes with encoding values between 8-F may be used when an instruction has the
`XC` (Extended Condition) prefix.

| Encoding   | Name       | Description                                | Condition calculation
|------------|------------|--------------------------------------------|-----------------------
| `0`        | EQ/ZR      | Equal (Zero)                               | `COND := ZF`
| `1`        | NE/NZ      | Not Equal (Nonzero)                        | `COND := !ZF`
| `2`        | GT         | Unsigned Greater Than                      | `COND := CF and !ZF`
| `3`        | LE         | Unsigned Less Than or Equal                | `COND := !CF or ZF`
| `4`        | LT/CC      | Unsigned Less Than (Carry Clear)           | `COND := !CF`
| `5`        | GE/CS      | Unsigned Greater Than or Equal (Carry Set) | `COND := CF`
| `6`        | N/A        | Instruction Prefix, more info later        | N/A
| `7`        | omitted/AL | Unconditional (Always)                     | `COND := true`
| `8 (XF;0)` | NG         | Negative                                   | `COND := SF`
| `9 (XF;1)` | PS         | Positive or Zero                           | `COND := !SF`
| `A (XF;2)` | BG         | Signed Greater Than                        | `COND := !ZF and (SF == VF)`
| `B (XF;3)` | SE         | Signed Less Than or Equal                  | `COND := ZF or (SF != VF)`
| `C (XF;4)` | SM         | Signed Less Than                           | `COND := SF != VF`
| `D (XF;5)` | BE         | Signed Greater Than or Equal               | `COND := SF == VF`
| `E (XF;6)` | OD         | Odd Parity                                 | `COND := PF`
| `F (XF;7)` | EV         | Even Parity                                | `COND := !PF`


### Calling Convention

When calling a function, parameters are passed in registers `A0`-`A5`. Any additional arguments
are pushed to the stack in reverse order directly before calling the target function. When the
target function returns, it stores the return value in `A0` aka `R1`. For functions that return a
value that's larger than 16-bit and no bigger than 64-bit, the low word is stored in `A0` and the
subsequent words are stored in `A1`-`A3`. Functions that return values that are larger than 64-bit
do so by accepting an additional parameter at the beginning in `A0`, which is a pointer to where
the callee function should write the return value. The caller function is responsible for making
space on the stack (or elsewhere) for this return value and then passing its address as the first
parameter to the target function. The target function is responsible for ensuring that all
callee-saved registers have the same value upon return as they did when the target function was
called initially. Upon calling a function, the address of the instruction directly after the call
instruction is stored into `RA`, the current `DPC` is stored into `RD`, then both `DPC` and `PC`
are updated by the call instruction (`FCR`/`FCA`). The target function is responsible for
returning to `RA` and setting `DPC` back to `RD` when it finishes.


### Instruction Encoding

> Throughout this document there may be breakdowns which detail what the individual bits mean in a
> byte or 16-bit word. For words, the format will look like `AAAAAAAA BBBBBBBB`. Note that this
> means that `AAAAAAAA` are the upper 8 bits in the word and `BBBBBBBB` are the lower 8 bits of the
> word. When stored in memory in little-endian byte ordering, the byte `BBBBBBBB` will come first.

Instructions consist of an optional set of instruction prefix bytes followed by an opcode byte.
Depending on the opcode, there may be additional bytes, such as a regpair byte (to encode `Rx` and
`Vy`), an `Imm16` immediate value, a `Regs16` bitset of registers, etc. Here is a description of
the various encodings for these values:

* Instruction prefix: `110PPPPP`, where `P` is the specific instruction prefix.
* Opcode byte: `CCCIIIII`, where `C` is the condition code, and `I` is the instruction's opcode.
* Regpair byte: `XXXXYYYY`, where `X` is the register number `Rx`, and `Y` is the register number
  for `Ry`, `Vy`, `CReg`, `Imm4`, or `SImm4`, depending on the instruction. When `Vy` == 0xF aka
  `DPC`, then there will be an `Imm16` immediately following the regpair byte to set `Vy`'s value.
* `Imm16`: `LLLLLLLL HHHHHHHH`, where `L` is the lower 8 bits and `H` is the upper 8 bits.
* `CReg`: `CCCC`, where `C` is the 4-bit number selecting the control register to be used.
* `Imm4`: `XXXX`, where `X` is the 4-bit immediate value.
* `SImm4`: `SXXX`, where `S` is the sign bit (1 = negative), and `X` is the rest of the value bits.
  The value is interpreted as a 2s-complement integer. When `S` is 0, however, the resulting value
  is increased by 1. This is done because it's more important to encode the value 8 than 0. Some
  examples: `0000` = 1, `0001` = 2, `0111` = 8, `1111` = -1, `1110` = -2, `1000` = -8.
* `Regs16`: `HGFEDCBA PONMLKJI`, where bits `A`-`P` can be 1 to indicate that the corresponding
  register from `R0-R15` should be pushed/popped.


Other important notes:

* By default, `Rd` (the destination register) is the same as `Rx`. However, with the `DR` instruction
  prefix, `Rd` may be changed to a different register.
* During instruction execution, `PC` points to the instruction after the current one.
* The term `Rdx` is defined as the corresponding paired register to `Rd`, which is calculated by
  taking the register number and XOR-ing it with 1. So when `Rd` == `R4`, then `Rdx` == `R5`, and when
  `Rd` == `R5`, then `Rdx` == `R4`.

| Opcode | Assembler&nbsp;Syntax | Name                    | FLAGS | Description
|--------|-----------------------|-------------------------|-------|-------------
| 00     | `ADD Rx, Vy`          | Add                     | ZSPCV | `Rd := Rx + Vy`
| 01     | `SUB Rx, Vy`          | Subtract                | ZSPCV | `Rd := Rx - Vy`
| 02     | `MLU Rx, Vy`          | Multiply Unsigned       | ZSPC* | Treat `Rx` and `Vy` as unsigned<br>`Rdx:Rd := Rx * Vy`
| 03     | `MLS Rx, Vy`          | Multiply Signed         | ZSPC* | Treat `Rx` and `Vy` as signed<br>`Rdx:Rd := Rx * Vy`
| 04     | `DVU Rx, Vy`          | Divide Unsigned         | ZSP   | Treat `Rx` and `Vy` as unsigned<br>`Rd, Rdx := Rx // Vy, Rx % Vy`
| 05     | `DVS Rx, Vy`          | Divide Signed           | ZSP   | Treat `Rx` and `Vy` as signed<br>`Rd, Rdx := Rx // Vy, Rx % Vy`
| 06     | `XOR Rx, Vy`          | Bitwise XOR             | ZSP   | `Rd := Rx ^ Vy`
| 07     | `AND Rx, Vy`          | Bitwise AND             | ZSP   | `Rd := Rx & Vy`
| 08     | `ORR Rx, Vy`          | Bitwise OR              | ZSP   | `Rd := Rx \| Vy`
| 09     | `SHL Rx, Vy`          | Shift Left              | ZSPC  | `Rd := Rx << Vy`
| 0A     | `SRU Rx, Vy`          | Shift Right Unsigned    | ZSPC  | Treat `Rx` as unsigned<br>`Rd := Rx >> Vy`
| 0B     | `SRS Rx, Vy`          | Shift Right Signed      | ZSPC  | Treat `Rx` as signed<br>`Rd := Rx >> Vy`
| 0C     | `MOV Rx, Vy`          | Move                    | ZSP   | `Rx := Vy`
| 0D     | `CMP Rx, Vy`          | Compare                 | ZSPCV | Subtracts `Vy` from `Rx`, discarding the result. Used to update `FLAGS`<br>`(void)(Rx - Vy)`
| 0E     | `RDC Rx, CReg`        | Read Control Register   | ZSPC  | Reads control register `CReg` into `Rx`. Sets `CF` on read failure
| 0F     | `WRC CReg, Ry`        | Write Control Register  | ZSPC  | Writes `Ry` to control register `CReg`. Sets `CF` on write failure
| 10     | `LDW Rx, [Vy]`        | Load Word               | ZSP   | Load into `Rx` the 16-bit value from `MEM[Rd + Vy]` (little-endian)<br>The memory address must be 16-bit aligned
| 11     | `STW [Vy], Rx`        | Store Word              |       | Store into `MEM[Rd + Vy]` the 16-bit value of `Rx` (little-endian)<br>The memory address must be 16-bit aligned
| 12     | `LDB Rx, [Vy]`        | Load Byte               | ZSP   | Load into `Rx` the byte from `MEM[Rd + Vy]`
| 13     | `STB [Vy], Rx`        | Store Byte              |       | Store into `MEM[Rd + Vy]` the byte value of `Rx`
| 14     | `BRA Rx, Vy`          | Branch Absolute         |       | Sets `DPC` to `Rx`, then branches to the absolute address specified by `Vy`
| 15     | `BRR Imm16`           | Branch Relative         |       | Branches to the relative address specified by `PC + Imm16 * (DPC + 1)`
| 16     | `FCA Rx, Vy`          | Function Call Absolute  |       | Stores `DPC` in `RD`, stores next `PC` to `RA`, then acts like `BRA`
| 17     | `FCR Imm16`           | Function Call Relative  |       | Stores `DPC` in `RD`, stores next `PC` to `RA`, then acts like `BRR`
| 18     | `RDB Rx, (Imm4)`      | Input Byte              | ZSPC  | Reads byte from `PORT[Imm4]` into `Rx`. `CF` is updated, will be 1 on read failure
| 19     | `WRB (Imm4), V8`      | Output Byte             |    C  | Writes byte to `PORT[Imm4]` from `V8`. `CF` is updated, will be 1 on write failure
| 1A     | `PSH {Regs16}`        | Push Registers          |       | Pushes registers from `Regs16` bitset to `Rd` (default `SP`), which must be 16-bit aligned.<br>Registers are pushed in order from highest to lowest (by number).<br>Each push operation works by first decrementing `Rd` by 2, then writing the next register's value to the memory address pointed to by `Rd`.
| 1B     | `POP {Regs16}`        | Pop Registers           |       | Pops registers from `Regs16` bitset from `Rd` (default `SP`), which must be 16-bit aligned.<br>Registers are popped in order from lowest to highest (by number).<br>Each pop operation works by first reading the next register's value from the memory address pointed to by `Rd`, then incrementing `Rd` by 2.
| 1C     | `INC Rx, SImm4`       | Increment               | ZSPCV | Increment or decrement `Rx` by a small nonzero value `SImm4` in range `-8 <= N <= 8`<br>`Rd := Rx + SImm4;`
| 1D     | `BPT`                 | Breakpoint              |       | Trigger a software breakpoint, or `NOP` when there's no debugger attached
| 1E     | `HLT`                 | High Level Transfer     |       | Swap active thread state context
| 1F     | `NOP`                 | No-op                   |       | No operation


### Instruction Prefixes

| Byte (opcode) | Bits        | Name | Description
|---------------|-------------|------|-------------
| C0 (00)       | `110 00000` | `XC` | Extended Condition. Add 8 to the next instruction's condition code. Must be last.
| C1 (01)       | `110 00001` | `TF` | Toggle Flags. Toggles whether the instruction should update the `FLAGS` register.
| C2 (02)       | `110 00010` | `XX` | Cross-Rx. `Rx` refers to the inactive thread state's register bank.
| C3 (03)       | `110 00011` | `XY` | Cross-Ry. `Ry` refers to the inactive thread state's register bank.
| C4 (04)       | `110 00100` | `XZ` | Cross-Rd. `Rd` refers to the inactive thread state's register bank.
| C5-CF (05-0F) | `110 0XXXX` | N/A  | Reserved for future use.
| Dx (1x)       | `110 1DDDD` | `DR` | Destination Register. Sets `Rd` to `D`, or `Rdx` if `Rd` has already been set.


### Control Registers

| Number | Name            | Description
|--------|-----------------|-------------
| `CR0`  | `CREG_DENY_R`   | Bitmask of which control registers may be accessed with `RDC`. Raises `EXC_DENIED_CREG` on denial.
| `CR1`  | `CREG_DENY_W`   | Bitmask of which control registers may be accessed with `WRC`. Raises `EXC_DENIED_CREG` on denial.
| `CR2`  | `INSN_DENY_0`   | For each instruction executed, if the bit `1 << OPCODE` is set in `INSN_DENY_0`, raise `EXC_DENIED_INSN`.
| `CR3`  | `INSN_DENY_1`   | For each instruction executed, if the bit `1 << (OPCODE - 16)` is set in `INSN_DENY_1`, raise `EXC_DENIED_INSN`.
| `CR4`  | `INSN_COUNT_LO` | Increments after each successfully executed instruction (lower half of 32-bit value)
| `CR5`  | `INSN_COUNT_HI` | Increments after each successfully executed instruction (upper half of 32-bit value)
| `CR6`  | `EXEC_STATE_0`  | Holds state information about the currently executing instruction
| `CR7`  | `EXEC_STATE_1`  | Holds state information about the currently executing instruction
| `CR8`  | `MEMBASE_R`     | See [`MEMBASE`](#membase_rwx) section
| `CR9`  | `MEMBASE_W`     | See [`MEMBASE`](#membase_rwx) section
| `CR10` | `MEMBASE_X`     | See [`MEMBASE`](#membase_rwx) section
| `CR11` | `EXC_INFO`      | See [`EXC_INFO`](#exc_info) section
| `CR12` | `EXC_ADDR`      | Address of the exception (if applicable)
| `CR13` | `TIMER`         | When set to a nonzero value, decrements after each successfully executed instruction. When decremented to zero, raise `EXC_TIMER`.
| `CR14` | `INSN_ADDR`     | Holds the address of the beginning of the currently executing instruction
| `CR15` | `FLAGS`         | See [`FLAGS`](#flags) section


#### `EXC_INFO`

* Bit 0: Set whenever an exception is raised
* Bits 1-3: Identify the type of exception that was raised
* Bits 4-13: Reserved for future use
* Bits 14-15: (Only for `EXC_MMU`, `EXC_BUS`, `EXC_UNALIGNED`) Memory access mode: `01`=read, `10`=write, `11`=execute


#### `MEMBASE_[R/W/X]`

* Bit 0: `ENABLE_MMU` - set to enable the MMU
* When `ENABLE_MMU = 0`:
  * Bits 1-7: Reserved for future use
  * Bits 8-15: `REGION` - Memory accesses for this access mode will have their 16-bit memory addresses prefixed with `REGION` to form a 24-bit physical memory address
* When `ENABLE_MMU = 1`:
  * Bits 1-15: `MEMBASE` - Physical page number where the page tables for this access mode are located


#### `FLAGS`

High-level description: [CPU Flags](#cpu-flags)

* Bit 0: `ZF`
* Bit 1: `SF`
* Bit 2: `PF`
* Bit 3: `CF`
* Bit 4: `VF`
* Bit 5: `FLAG_DENY_XREGS` - When set, attempts by this thread context to execute an instruction with an `XX`/`XY`/`XZ` prefix will raise `EXC_DENIED_INSN`
* Bits 6-31: Reserved for future use


## EAR Memory Model

In EAR v1 and v2, there was a 16-bit address space. EAR v3 expands the address space to be 24-bit.
For backwards compatiblity, all instructions still work with 16-bit virtual addresses, and
registers like `PC`, `SP`, etc are still 16-bit. So in effect, virtual addresses are 16-bit, and
physical addresses are 24-bit.

Each virtual page is 0x100 bytes in size and is aligned on a 0x100 byte boundary. Unlike most other
CPU architectures, EAR allows the same virtual memory page to be backed by different physical pages
based on the desired access to that page. For example, the virtual page 0x7A00 may be mapped to
the physical page 0x00_2C00 for read access, 0x00_2D00 for write access, and 0x00_2E00 for execute
access.

Each memory address holds a single byte, not a 16-bit word. Unaligned memory accesses, where an
instruction attempts to load a 16-bit word from an address which is not 16-bit aligned, cause an
exception to be raised.

When translating a virtual address to a physical address, the first step is to use the access mode
to lookup the `MEMBASE_(R|W|X)` control register. If the MMU enabled bit (low bit) is clear, then
the upper 8 bits of this register are used as the region number (highest 8 bits). This is combined
with the 16-bit address to build a 24-bit "full address", aka an "EAR full". This EAR full is then
used to access the physical memory bus.

If the MMU enabled bit is set, however, things get a bit more complicated. The remaining 15 bits
are shifted left by one (to form a 16-bit value whose LSB is 0) and then used as the physical page
number where the page tables to use are located. The page number of the virtual address indexes into
this page table to find the 16-bit physical page number for the backing physical page. Then, the low
8 bits of the virtual address are used as the offset into this physical page, thus finally building
a 24-bit EAR full. This EAR full is then used to access the physical memory bus.


### Context Swaps

The `HLT` (~~Halt~~ High Level Transfer) instruction swaps which of the two thread state
contexts is active.

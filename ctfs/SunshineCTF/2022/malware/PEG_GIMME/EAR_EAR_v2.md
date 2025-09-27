# EAR Essential Architecture Reference v2

The EAR architecture uses 8-bit bytes and supports a 16-bit address space. There are 16 general
purpose 16-bit registers, explained in the table below.

## EAR Instruction Set Architecture

### General Purpose Registers

| Register | Aliases | Description
|----------|---------|-------------
| R0       | ZERO    | Always holds the value 0. Writes are ignored
| R1       | A0      | First parameter (caller-saved)
| R2       | A1, RV  | Return Value and second parameter (caller-saved)
| R3       | A2, RVX | Return Value (extended) and third parameter (caller-saved)
| R4-R6    | A3-A5   | General purpose temporary and parameters (caller-saved)
| R7-R9    | S0-S2   | General purpose permanent (callee-saved)
| R10      | FP, S3  | Frame Pointer (callee-saved)
| R11      | SP      | Stack Pointer
| R12      | RA      | Return Address
| R13      | RD      | Return Delta
| R14      | PC      | Program Counter
| R15      | DPC     | Delta PC: After reading each code byte, `PC := PC + 1 + DPC`. Default value is 0


### Special Registers

| Register | Description
|----------|-------------
| FLAGS    | Bit flags used to represent CPU state.


### Flags

Flags are updated by default by unconditional instructions, whereas conditional instructions
(instructions where cc is neither `AL` nor `SP`) do not update `FLAGS` normally. This is done to
enable running multiple instructions in a row in a conditional block without clobbering the
condition flags. There is an instruction prefix byte, `TF` aka Toggle Flags, which inverts this
behavior, causing unconditional instructions to not update `FLAGS` and for conditional instructions
to write back the new value of `FLAGS`. To use this instruction modifier in assembler syntax, add
the `F` suffix to an instruction such as `MOVF`, `ADDF.EQ`, or `DECF.PS`.

| Name | Description
|------|-------------
| ZF   | Zero Flag, set when the computation result is zero
| SF   | Sign Flag, set when the computation result's high bit is set
| PF   | Parity Flag, set when the computation result has an odd number of bits set
| CF   | Carry Flag, set when the computation result would have bit 16 set
| VF   | Overflow Flag, set when the signed computation overflowed
| MF   | MMU-disable Flag, set when executing a page fault handler


### Conditions

| Value | Name       | Description                                | Condition calculation
|-------|------------|--------------------------------------------|-----------------------
| 0     | EQ/ZR      | Equal (Zero)                               | `COND := ZF`
| 1     | NE/NZ      | Not Equal (Nonzero)                        | `COND := !ZF`
| 2     | GT         | Unsigned Greater Than                      | `COND := CF and !ZF`
| 3     | LE         | Unsigned Less Than or Equal                | `COND := !CF or ZF`
| 4     | LT/CC      | Unsigned Less Than (Carry Clear)           | `COND := !CF`
| 5     | GE/CS      | Unsigned Greater Than or Equal (Carry Set) | `COND := CF`
| 6     | SP         | Unconditional Special (Instruction Prefix) | N/A
| 7     | omitted/AL | Unconditional (Always)                     | `COND := true`
| 8     | NG         | Negative                                   | `COND := SF`
| 9     | PS         | Positive or Zero                           | `COND := !SF`
| A     | BG         | Signed Greater Than                        | `COND := !ZF and (SF == VF)`
| B     | SE         | Signed Less Than or Equal                  | `COND := ZF or (SF != VF)`
| C     | SM         | Signed Less Than                           | `COND := SF != VF`
| D     | BE         | Signed Greater Than or Equal               | `COND := SF == VF`
| E     | OD         | Odd Parity                                 | `COND := PF`
| F     | EV         | Even Parity                                | `COND := !PF`

### Calling Convention

When calling a function, parameters are passed in registers `A0`-`A5`. Any additional arguments
are pushed to the stack in reverse order directly before calling the target function. When the
target function returns, it stores the return value in `RV` aka `R2`. For functions that return a
32-bit value, the low word is stored in `RV` and the high word is stored in `RVX`. Functions that
return structures do so by actually accepting an additional parameter at the end, which is a
pointer to the structure. The caller function is responsible for making space on the stack (or
elsewhere) for this returned structure and then passing its address as the final parameter to the
target function. The target function is responsible for ensuring that all callee-saved registers
have the same value upon return as they did when the target function was called initially. Upon
calling a function, the address of the code byte directly after the call instruction is stored
into `RA`, the current `DPC` is stored into `RD`, then both `DPC` and `PC` are updated by the
call instruction. The target function is responsible for returning to `RA` and setting `DPC` back
to `RD` when it finishes.


### Instructions

The first byte of each instruction contains two parts: the condition code and opcode. Each
instruction is conditional and may be treated as a `NOP` if the condition evaluates false. Many
instructions have two operands, referred to as `Rx` and `Ry` (or sometimes `Vy`). For these
instructions, there is a second byte after the opcode byte that is called the "regpair" byte. The
high nybble of the regpair byte is the `Rx` register number. The low nybble of the regpair byte is
the `Ry` register number. If `Ry` is `DPC`, then the value for the `Vy` operand is read after the
regpair byte and is encoded as an `Imm16`. Otherwise, `Vy` is the value stored in the `Ry` register.
For `SImm4`, if the immediate's value is >= 0, it has 1 added to it. The value 0 cannot be encoded as
an `SImm4`, as the `ZERO` register can be used for this purpose. If an instruction references `V8`,
this is `Ry` unless `Ry` is `DPC`, in which case it will be the next immediate byte (as an `Imm8`).
By default, `Rd` (the destination register) is the same as `Rx`. However, with the `DR` instruction
prefix, this allows changing `Rd` to a different register. During instruction execution, `PC` points
to the instruction after the current one. The term `Rdx` is defined as the corresponding paired
register to `Rd`, which is calculated by taking the register number and XOR-ing it with 1. So when
`Rd` == `R4`, then `Rdx` == `R5`, and when `Rd` == `R5`, then `Rdx` == `R4`.

| Opcode | Assembler&nbsp;Syntax | Name                    | FLAGS | Description
|--------|-----------------------|-------------------------|-------|-------------
| 00     | `ADD Rx, Vy`          | Add                     | ZSPCV | `Rd := Rx + Vy`
| 01     | `SUB Rx, Vy`          | Subtract                | ZSPCV | `Rd := Rx - Vy`
| 02     | `MLU Rx, Vy`          | Multiply Unsigned       | ZSP   | Treat `Rx` and `Vy` as unsigned<br>`Rdx:Rd := Rx * Vy`
| 03     | `MLS Rx, Vy`          | Multiply Signed         | ZSP   | Treat `Rx` and `Vy` as signed<br>`Rdx:Rd := Rx * Vy`
| 04     | `DVU Rx, Vy`          | Divide Unsigned         | ZSP   | Treat `Rx` and `Vy` as unsigned<br>`Rd, Rdx := Rx // Vy, Rx % Vy`
| 05     | `DVS Rx, Vy`          | Divide Signed           | ZSP   | Treat `Rx` and `Vy` as signed<br>`Rd, Rdx := Rx // Vy, Rx % Vy`
| 06     | `XOR Rx, Vy`          | Bitwise XOR             | ZSP   | `Rd := Rx ^ Vy`
| 07     | `AND Rx, Vy`          | Bitwise AND             | ZSP   | `Rd := Rx & Vy`
| 08     | `ORR Rx, Vy`          | Bitwise OR              | ZSP   | `Rd := Rx \| Vy`
| 09     | `SHL Rx, Vy`          | Shift Left              | ZSP   | `Rd := Rx << Vy`
| 0A     | `SRU Rx, Vy`          | Shift Right Unsigned    | ZSPC  | Treat `Rx` as unsigned<br>`Rd := Rx >> Vy`
| 0B     | `SRS Rx, Vy`          | Shift Right Signed      | ZSPC  | Treat `Rx` as signed<br>`Rd := Rx >> Vy`
| 0C     | `MOV Rx, Vy`          | Move                    | ZSP   | `Rx := Vy`
| 0D     | `CMP Rx, Vy`          | Compare                 | ZSPCV | Subtracts `Vy` from `Rx`, discarding the result. Used to update `FLAGS`<br>`(void)(Rx - Vy)`
| 0E-0F  | N/A                   | Reserved                | N/A   | Reserved for future use
| 10     | `LDW Rx, [Vy]`        | Load Word               | ZSP   | Load into `Rx` the 16-bit value from `MEM[Vy]`
| 11     | `STW [Rx], Vy`        | Store Word              |       | Store into `MEM[Rx]` the 16-bit value of `Vy`
| 12     | `LDB Rx, [Vy]`        | Load Byte               | ZSP   | Load into `Rx` the byte from `MEM[Vy]`
| 13     | `STB [Rx], V8`        | Store Byte              |       | Store into `MEM[Rx]` the byte value of `V8`
| 14     | `BRA Rx, Vy`          | Branch Absolute         |       | Sets `DPC` to `Rx`, then branches to the absolute address specified by `Vy`
| 15     | `BRR Imm16`           | Branch Relative         |       | Branches to the relative address specified by `PC + Imm16`
| 16     | `FCA Rx, Vy`          | Function Call Absolute  |       | Stores `DPC` in `RD`, stores next `PC` to `RA`, then acts like `BRA`
| 17     | `FCR Imm16`           | Function Call Relative  |       | Stores `DPC` in `RD`, stores next `PC` to `RA`, then acts like `BRR`
| 18     | `RDB Rx, (Imm4)`      | Input Byte              | ZSPC  | Reads byte from `PORT[Imm4]` into `Rx`. `CF` is updated, will be 1 on read failure
| 19     | `WRB (Imm4), V8`      | Output Byte             | ZSPC  | Writes byte to `PORT[Imm4]` from `V8`. `CF` is updated, will be 1 on write failure
| 1A     | `PSH {Regs16}`        | Push Registers          |       | Pushes registers from `Regs16` bitset to `Rd` (default `SP`)<br>`Rd -= popcnt(Regs16); MEM[Rd:Rd+popcnt(Regs16)] := REG[Regs16]`
| 1B     | `POP {Regs16}`        | Pop Registers           |       | Pops registers from `Regs16` bitset from `Rd` (default `SP`)<br>`REG[Regs16] := MEM[Rd:Rd+popcnt(Regs16)]; Rd += popcnt(Regs16)`
| 1C     | `INC Rx, SImm4`       | Increment               | ZSPCV | Increment or decrement `Rx` by a small nonzero value SImm4 in range [-8, 8]<br>`Rx += SImm4;`
| 1D     | `BPT`                 | Breakpoint              |       | Trigger a software breakpoint
| 1E     | `HLT`                 | Halt                    |       | Terminates the program
| 1F     | `NOP`                 | No-op                   |       | No operation


### Instruction Prefixes

| Byte (opcode) | Name | Description
|---------------|------|-------------
| C0 (00)       | `XC` | Extended Condition. Add 8 to the next instruction's condition code. Must be last.
| C1 (01)       | `TF` | Toggle Flags. Toggles whether the instruction should update the `FLAGS` register.
| C2 (02)       | `EM` | Enable MMU. Only useful in a page fault handler. This one instruction will use the MMU.
| C3-CF (0D-0F) | N/A  | Reserved for future use.
| Dx (1x)       | `DR` | Destination Register. The low 4 bits of this byte are the register number of `Rd`.


### Pseudo-instructions

| Assembler Syntax        | Bytes | Real Instruction Sequence
|-------------------------|-------|---------------------------
| `RET`                   | 2     | `BRA RD, RA`
| `INC Ra, 0`             | 1     | `NOP`
| `RDB Ra`                | 2     | `RDB Ra, (0)`
| `WRB V8`                | 2-3   | `WRB (0), V8`
| `INC Ra`                | 2     | `INC Ra, 1`
| `DEC Ra`                | 2     | `INC Ra, -1`
| `DEC Ra, imm4`          | 2     | `INC Ra, -imm4`
| `ADD Ra, Rb, imm4`      | 3     | `INC Ra, Rb, imm4`
| `SUB Ra, Rb, imm4`      | 3     | `DEC Ra, Rb, imm4`
| `NEG Ra`                | 3     | `SUB Ra, ZERO, Ra`
| `INV Ra`                | 3     | `XOR Ra, -1`
| `ADR Ra, <label>`       | 3-6   | `ADD Ra, PC, label-@`
| `BRA Va`                | 2-5   | `BRA DPC, Va`
| `FCA Va`                | 2-5   | `FCA DPC, Va`
| `SWP Ra, Rb`            | 6     | `XOR Ra, Rb; XOR Rb, Ra; XOR Ra, Rb`
| `ADC Rd, Vb`            | 4-6   | `INC.CS Rd; ADD Rd, Vb`
| `ADC Rd, Ra, Vb`        | 6-8   | `INC.CS Rd, ZERO, 1; ADD Rd, Ra; ADD Rd, Vb`
| `SBC Rd, Vb`            | 4-6   | `DEC.CS Rd; SUB Rd, Vb`
| `SBC Rd, Ra, Vb`        | 6-8   | `DEC.CS Rd, ZERO, 1; ADD Rd, Ra; SUB Rd, Vb`
| `LDWM Rx, [Vy]`         | 3-5   | `EM:LDW Rx, [Vy]`
| `STWM [Rx], Vy`         | 3-5   | `EM:STW [Rx], Vy`
| `LDBM Rx, [Vy]`         | 3-5   | `EM:LDB Rx, [Vy]`
| `STBM [Rx], V8`         | 3-5   | `EM:STB [Rx], V8`


## EAR Memory Model

The EAR memory model defines a 16-bit address space. This address space is supported by 64KiB of
total physical memory, and a page table system that maps pages of physical memory to different
virtual addresses and with different permissions to access them. Each virtual page is 0x100 bytes in
size and is aligned on a 0x100 byte boundary. Unlike most other CPU architectures, EAR allows the
same virtual memory page to be backed by different physical pages based on the desired access to
that page. For example, the virtual page 0x2C00 may be mapped to the physical page 0x2C00 for read
access, 0x2D00 for write access, and 0x2E00 for execute access. Additionally, accessing virtual
memory pages without a physical page associated will cause a page fault. Each page table entry
specifies its own page fault handler, which must be a function that starts at the beginning of a
page of physical memory. This page fault handler will be given the exact virtual address the
processor tried to access, the requested access (read, write, or execute), and a pointer to the
faulting thread state. Multiple virtual pages may be backed by the same underlying physical memory.
Any combination of memory access permissions is permitted for a virtual page.

Each memory address holds a single byte, not a 16-bit word. Unaligned memory accesses, where an
instruction attempts to load a 16-bit word from an address which is not 16-bit aligned, are allowed.
When this unaligned access straddles a page boundary, the bytes are read in order of ascending
memory addresses.

The first 256 bits of physical memory are used as a bitmap that marks physical pages as accessible
or not.


### Physical Allocation Table Layout

The page at physical address 0x0100 is the physical allocation table. Each byte stores flags for a
physical page. For example, the byte at address 0x0142 stores the flags for the physical page at
address 0x4200. The following flags are used:

* `PHYS_DIRTY = 1 << 0`: The physical page is dirty and must be zeroed before being allocated.
* `PHYS_IN_USE = 1 << 1`: The physical page is in use and should not be used to fulfill an allocation.
* `PHYS_ALLOW = 1 << 2`: The physical page is accessible and will not cause a fault on access.
* `PHYS_DENY = 0 << 2`: The physical page is not accessible, and accessing it will cause `HALT_DOUBLEFAULT`.
  * All other bits are reserved for future use.


### Virtual Page Table Layout

The page table is an array of page table entries. The page table begins at physical address 0xFC00
and extends until the end of the address space (last byte is 0xFFFF). There are exactly 256 pages in
EAR's address space and therefore 256 page table entries. Each page table entry contains 4 bytes:

* Read physical page number
* Write physical page number
* Execute physical page number
* Fault handler physical page number

Each of the physical page number bytes is the top byte of the physical address that backs the
relevant access permission for this virtual page. These can be set to any page except 0x00, which is
special and is used to mark that level of access to this virtual page as being disallowed (the page
is unmapped for that access type). Whenever the CPU attempts to access a virtual page whose
underlying physical page number for the requested access type is 0x00, a page fault is triggered. If
the fault handler physical page number is 0x00, the CPU is halted with `HALT_UNMAPPED` as the halt
reason. Otherwise, the CPU switches to a clean exception thread context and exception thread stack
(2.5KiB) and calls the page fault handler function. Note that the MMU will be disabled during the
execution of a page fault handler function, which means that all memory accesses will use physical
addresses. The prototype of the fault handler should be as follows:

```c
/*!
 * @brief Handle a page fault triggered by an instruction or during instruction execution.
 * 
 * @param tte_paddr Physical address of the page table entry corresponding to the faulting virtual
 *        address
 * @param fault_vmaddr Virtual address being accessed that caused the page fault
 * @param prot Attempted access mode. Read is 0, write is 1, execute is 2.
 * @param saved_regs Pointer to the saved registers area, holding all 16 general purpose registers.
 *        PC here is the value of PC before the instruction started executing, aka the first byte
 *        of the current instruction. If upon return from this fault handler ZERO contains a
 *        nonzero value, the current instruction is marked as complete. All registers besides ZERO
 *        will be written back to the faulting thread's context upon return.
 * @param next_pc Holds the address of the next instruction byte after the current instruction, or
 *        if the fault occurred during instruction decoding, it should be exactly fault_vmaddr.
 * 
 * @return Physical address to be used in place of fault_vmaddr for accesses. This is ignored when
 *         the instruction is marked as complete by writing a nonzero value to saved_regs[ZERO].
 */
void* handle_fault(
	uint16_t    tte_paddr,
	void*       fault_vmaddr,
	uint8_t     prot,
	uint16_t*   saved_regs,
	void*       next_pc
) {
	// Handle fault
}
```

The fault handler function is expected to do one of the following:

1. Fill in the page table entry (at physical address `tte_paddr + prot`) with a physical page to
back this virtual address and return the specific physical address that corresponds to the requested
virtual address.
2. Leave the page table entry blank but return a one-time physical address for this memory access to
use.
3. Fully handle the page fault access by modifying the saved thread state as necessary.

In option 3 above, the current operation must be marked as completed by writing some nonzero value
into `saved_regs[ZERO]`. Alternatively, if the value stored in `saved_regs[PC]` is modified, this
also marks the operation as completed. Either of these actions instruct the CPU upon return from
the exception handler to mark the current instruction as completed and to stop its execution. Note
that care must be taken as a page fault can occur while fetching an instruction.

If, during the execution of a page fault handler, an inaccessible physical page is accessed, the CPU
will halt with `HALT_DOUBLEFAULT` as the reason.

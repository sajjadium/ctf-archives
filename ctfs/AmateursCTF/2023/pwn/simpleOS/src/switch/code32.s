    .intel_syntax noprefix

    .section .boot32, "awx"
    .code32


    .include "src/switch/macros.s"


    .extern __page_table_memory_start
    .extern _code_64


    .global _code_32
    .global gdt64_offset_code
    .global gdt64_offset_data
    .global mapped_memory
    .global page_table_unused


_code_32:
    cli
    mov   ax,    0x10
    mov   ds,    ax
    mov   es,    ax
    mov   fs,    ax
    mov   gs,    ax
    mov   ss,    ax

    mov   esi,   offset enter_code32
    call  serial_send32

    call  check_cpuid
    call  check_longmode

setup_paging64:
    mov   eax,   cr0
    and   eax,   ~(1 << 31)
    mov   cr0,   eax

    mov   edi,   offset __page_table_memory_start     # page map level 4
    mov   cr3,   edi
    xor   eax,   eax
    mov   ecx,   4096
    rep   stosd
    mov   edi,   cr3

    # bits 51:12 hold the 4KiB aligned address
    # bit 1 | 0 -> read         | 1 -> write
    # bit 0 | 0 -> not present  | 1 -> present

    # pml4 entry - 51:12 -> pdpt address, 1 -> read/write, 0 -> present
    lea   eax,   [edi + 0x1003]
    mov   long ptr [edi], eax      # pml4[0] = pml4 entry
    add   edi,   0x1000
    # pdpt entry - 51:12 -> pdt  address, 7 -> 1gb pages or 2mb pages, 1 -> read/write, 0 -> present
    lea   eax,   [edi + 0x1003]
    mov   long ptr [edi], eax      # pdpt[0] = pdpt entry
    add   edi,   0x1000
    # pdt entry  - 51:12 -> pt   address, 7 -> 2mb pages or 4kb pages, 1 -> read/write, 0 -> present
    lea   eax,   [edi + 0x1003]
    mov   long ptr [edi], eax      # pdt[0] = pdt entry
    add   edi,   0x1000

    # pt entry   - 51:12 -> phys address, 1 -> read/write, 0 -> present
    mov   ebx,   0x03
    .equ  pages, 512
    mov   ecx,   pages
    mov   long ptr [mapped_memory], pages * 0x1000

set_entries:
    mov   long ptr [edi], ebx        # pt[i]   (0x4000 + i * 8) = pt entry
    add   ebx,   0x1000
    add   edi,   8
    loop  set_entries

    mov   long ptr [page_table_unused], edi

    mov   esi,   offset leave_code32
    call  serial_send32

enable_PAE_paging:
    mov   eax,   cr4
    or    eax,   1 << 5
    mov   cr4,   eax

enable_longmode:
    mov   ecx,   0xc0000080
    rdmsr
    or    eax,   1 << 8
    wrmsr

enable_paging:
    mov   eax,   cr0
    or    eax,   1 << 31
    mov   cr0,   eax

    lgdt  [gdt64_desc]
    .att_syntax prefix
    jmpl $gdt64_offset_code, $_code_64
    .intel_syntax noprefix
    ; push  offset gdt64_offset_code
    ; mov   eax,   offset _code_64
    ; push  eax
    ; retf

mapped_memory: .8byte 0
page_table_unused: .8byte 0

gdt64:
gdt64_null:
    .8byte 0
gdt64_code:
    .4byte 0xffff
    .byte  0
    .byte  0b10011010
    .byte  0b10101111
    .byte  0
gdt64_data:
    .4byte 0xffff
    .byte  0
    .byte  0b10010010
    .byte  0b11001111
    .byte  0
gdt64_tss:
    .4byte 0x00000068
    .4byte 0x00cf8900
gdt64_end:
    
gdt64_desc:
    .2byte gdt64_end - gdt64 - 1
    .8byte gdt64

    .equ gdt64_offset_code, gdt64_code - gdt64
    .equ gdt64_offset_data, gdt64_data - gdt64

check_cpuid:
    pushfd               # push flags register onto stack
    pop   eax            # pop into eax

    mov   ecx, eax       # save eax into ecx
    xor   eax, 1 << 21   # flip the ID bit

    push  eax            # push eax onto stack
    popfd                # pop off stack and copy into flags register

    pushfd               # push flags register onto stack
    pop   eax            # pop into eax, eax will contain flipped bit if cpuid is supported

    push  ecx            # push ecx onto stack
    popfd                # restore flags register

    xor   eax, ecx
    jz    no_cpuid
    ret

no_cpuid:
    mov   esi, offset _no_cpuid
    call  serial_send32
1:  jmp   1b

_no_cpuid: .asciz "cpuid not detected"

check_longmode:
    mov   eax, 0x80000000
    cpuid
    cmp   eax, 0x80000001
    jb    no_longmode

    mov   eax, 0x80000001
    cpuid
    test  edx, 1 << 29
    jz    no_longmode
    ret

no_longmode:
    mov   esi, offset _no_longmode
    call  serial_send32
1:  jmp   1b

_no_longmode: .asciz "longmode not detected"

    .equ COM1, 0x3F8

serial_send32:
    pushad
2:
    inb   COM1+5
    test  al,    0x20
    jz    2b

    lodsb
    test  al,    al
    jz    1f
    mov   dx,    COM1+0
    out   dx,    al
    jmp   2b
1:
    popad
    ret


enter_code32: .asciz "enter code32\n"
leave_code32: .asciz "leave code32\n"


    .att_syntax prefix

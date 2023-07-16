ENTRY(_code_32)

SECTIONS
{    
    /* bootstrap start */
    __font_map = 0x1000;
    __e820_memory_map = 0x2000;
    __e820_memory_map_len = 0x3000;
    __partition_offset = 0x3008;
    /* bootstrap end */

    . = 0x100000;

    .boot32 : {
        KEEP(*(.boot32))
    }
    .boot64 : {
        KEEP(*(.boot64))
    }

    . = ALIGN(4K);
    __page_table_memory_start = .;
    . = . + 64 * 0x1000;
    __page_table_memory_end = .;

    .text : ALIGN(4K) {
        KEEP(*(.text.*))
    }

    .rodata : ALIGN(4K) {
        KEEP(*(.rodata.*))

    .data : ALIGN(4K) {
        *(.data.*)
    }

    .bss : ALIGN(4K) {
        *(COMMON)
        *(.bss.*)
    }

    __gnu_h2f_ieee = .;
    __gnu_f2h_ieee = .;

    . = ALIGN(4K);

    __end_of_bootloader = .;
}
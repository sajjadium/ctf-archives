ENTRY(_extended_entry)

SECTIONS {
    /* bootstrap start */
    __font_map = 0x1000;
    __e820_memory_map = 0x2000;
    __e820_memory_map_len = 0x3000;
    __partition_offset = 0x3008;
    /* bootstrap end */

    . = 0x7E00;
    .entry : { KEEP(*(.entry.*)) }

    .text   : { KEEP(*(.text)) }
    .rodata : { KEEP(*(.rodata)) }
    .data   : { KEEP(*(.data)) }
    .bss    : { KEEP(*(.bss)) }

    .boot16 : { KEEP(*(.boot16)) }
}
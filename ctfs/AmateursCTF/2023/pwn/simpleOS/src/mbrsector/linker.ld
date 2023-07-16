ENTRY(_entry)

SECTIONS
{
    . = 0x600;
    _entry_base = .;
    .mbrsector : { KEEP(*(.mbrsector)) }

    .text   : { KEEP(*(.text.*)) }
    .rodata : { KEEP(*(.rodata.*)) }
    .data   : { KEEP(*(.data.*)) }
    .bss    : { KEEP(*(.bss.*)) }

    . = 0x600 + 446;
    __partition_table = .;
    .table : {
        . = 0x600 + 446 + 16 * 4;
    }

    . = 0x600 + 510;
    .magic : { SHORT(0xAA55) }
}
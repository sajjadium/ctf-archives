ENTRY(_entry)

SECTIONS {
    . = 0x7C00;
    .stub : {
        KEEP(*(.stub))
        . = 0x7C00 + 3;
    }

    /* This is where the boot parameter block would be located.
     * mformat will fill out the necessary values for the bootsector
     * to read, and the rest will be filled with nops.
     * The nop sled is necessary because FAT12/16 have different
     * extended paramter block sizes from FAT32.
     */
    .fill : {
        FILL(0x90909090);

        __parameters = .;

        . = 0x7C00 + 14;
        __reserved_sectors = .;

        __extended_parameters = .;
        . = 0x7C00 + 90;
    }

    .bootsector : { KEEP(*(.bootsector)) }

    .text   : { KEEP(*(.text.*)) }
    .rodata : { KEEP(*(.rodata.*)) }
    .data   : { KEEP(*(.data.*)) }
    .bss    : { KEEP(*(.bss.*)) }

    . = 0x7C00 + 510;
    .magic : { SHORT(0xAA55) }
}
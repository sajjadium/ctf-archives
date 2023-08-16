OUTPUT_FORMAT("elf32-littlearm", "elf32-littlearm", "elf32-littlearm")

MEMORY {
    FLASH (RWX) :  ORIGIN = 0x0, LENGTH = 64K
    RAM (RWX) : ORIGIN = 0x20000, LENGTH = 64K
}

__stack = ORIGIN(RAM) + LENGTH(RAM);

SECTIONS {
    .vectors :
    {
        *(vectors)
    } > FLASH

    .text : 
    {
        *(.text)
    } > FLASH

    .rodata :
    {
        *(.rodata)
    } > FLASH

    .data :
    {
        *(.data)
    } > FLASH

    .bss :
    {
        __bss_start__ = .;
        *(.bss .bss.*)
        __bss_end__ = .;
    } > RAM

    .heap :
    {
        end = .;
    } > RAM

}
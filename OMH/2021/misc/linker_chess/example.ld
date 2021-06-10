ENTRY(main)
SECTIONS
{
  . = 0x1337000;
  .text : { *(.text); }
  .rodata : { *(.rodata); }

  . = 0x31337000;
  .data : { *(.data); }
  .bss : { *(.bss); }
}

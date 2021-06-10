FORCE_COMMON_ALLOCATION

SECTIONS
{
  .text.gatekey : ALIGN(0x1000) {
    _gatekey_text_begin = .;
    *(.text);
    _gatekey_text_end = ALIGN(0x1000);
    BYTE(1); /*hack*/
  }
  .data.gatekey : ALIGN(0x1000) {
    _gatekey_data_begin = .;
    *(.data);
    _gatekey_data_end = ALIGN(0x1000);
    BYTE(1); /*hack*/
  }
  .bss.gatekey : ALIGN(0x1000) {
    _gatekey_bss_begin = .;
    *(.bss);
    *(COMMON);
    _gatekey_bss_end = ALIGN(0x1000);
    BYTE(1); /*hack*/
  }
}

; Copyright (C) 2014-2020 Joonas Javanainen <joonas.javanainen@gmail.com>
;
; Permission is hereby granted, free of charge, to any person obtaining a copy
; of this software and associated documentation files (the "Software"), to deal
; in the Software without restriction, including without limitation the rights
; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
; copies of the Software, and to permit persons to whom the Software is
; furnished to do so, subject to the following conditions:
;
; The above copyright notice and this permission notice shall be included in
; all copies or substantial portions of the Software.
;
; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
; SOFTWARE.

.include "hardware.s"
.include "macros.s"

; --- Cartridge configuration ---

.ifndef CART_TYPE
  .define CART_TYPE 0
.endif
.ifndef CART_ROM_BANKS
  .define CART_ROM_BANKS 2
.endif
.ifndef CART_RAM_SIZE
  .define CART_RAM_SIZE 0
.endif

.rombanks CART_ROM_BANKS

.emptyfill $ff

.define DEFAULT_SP $e000
.ifdef CART_CGB
  .romgbc
.else
  .ifdef CART_SGB
    .romsgb
  .else
    .romdmg
  .endif
.endif

.ifndef CART_NO_TITLE
  .name "mooneye-gb test"
.endif

.licenseecodenew "ZZ"
.cartridgetype CART_TYPE
.ramsize CART_RAM_SIZE
.countrycode $01
.nintendologo
.version $00

.ifndef CART_NO_GLOBAL_CHECKSUM
  .computegbchecksum
.endif
.computegbcomplementcheck

; --- Library functions ---

.struct reg_dump
  reg_f db
  reg_a db
  reg_c db
  reg_b db
  reg_e db
  reg_d db
  reg_l db
  reg_h db
.endst

.bank 1 slot 1
.include "lib/check_asserts_cb.s"
.include "lib/clear_oam.s"
.include "lib/clear_vram.s"
.include "lib/clear_wram.s"
.include "lib/disable_lcd_safe.s"
.include "lib/memcmp.s"
.include "lib/memcpy.s"
.include "lib/memset.s"
.include "lib/print_bin1.s"
.include "lib/print_bin4.s"
.include "lib/print_bin8.s"
.include "lib/print_hex4.s"
.include "lib/print_hex8.s"
.include "lib/print_inline_string.s"
.include "lib/print_load_font.s"
.include "lib/print_newline.s"
.include "lib/print_reg_dump.s"
.include "lib/print_string.s"
.include "lib/quit.s"
.include "lib/quit_dump_mem.s"
.include "lib/reset_screen.s"
.include "lib/serial_send_byte.s"

; --- Cartridge header ---

.bank 0 slot 0
.org $100
.section "Header" force
  nop
  jp $150
.ends

; --- Runtime ---

.bank 1 slot 1
.section "Font" free
font:
  ; 8x8 ASCII bitmap font by Darkrose
  ; http://opengameart.org/content/8x8-ascii-bitmap-font-with-c-source
  .incbin "font.bin" fsize FONT_SIZE
.ends

.bank 0 slot 0
.org $150
main:

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

; *Manual test* for sprite priority
; See sprite_priority-expected.png for a reference image

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ld sp, DEFAULT_SP

  call disable_lcd_safe
  call reset_screen
  call print_load_font

  ; OBP palette 0 should use only black
  ld a, $ff
  ld (OBP0), a
  ; OBP palette 1 should use only light grey
  ld a, $55
  ld (OBP1), a

  call clear_oam

  ; Copy data to OAM
  ld hl, OAM
  ld de, data
  ld bc, data_end - data
  call memcpy

  ; Enable sprites
  ld hl, LCDC
  set 1, (HL)

  enable_lcd
  wait_vblank
  wait_vblank
  halt_execution

data:
  ;    Y   X  CH   Flags: $00 uses OBP0, $10 uses OBP1
  ; Priority with same X coordinate
  .db  32  8  'O'  $10 ; Light grey should be on top
  .db  32  8  'O'  $00
  .db  32  8  'O'  $00
  .db  32  8  'O'  $00
  .db  32  8  'O'  $00
  .db  32  8  'O'  $00
  .db  32  8  'O'  $00
  .db  32  8  'O'  $00
  .db  32  8  'O'  $00
  .db  32  8  'O'  $00
  .db  32  8  $10  $00 ; 11th sprite should not be displayed

  ; Priority with different X coordinate
  .db  48  96 '9'  $00
  .db  48  88 '8'  $00
  .db  48  80 '7'  $00
  .db  48  72 '6'  $00
  .db  48  64 '5'  $00
  .db  48  56 '4'  $00
  .db  48  48 '3'  $00
  .db  48  40 '2'  $00
  .db  48  32 '1'  $00
  .db  48  24 '0'  $00
  .db  48  16 $10  $00 ; 11th sprite should not be displayed

  ; These overlap slightly with the earlier higher priority sprites,
  ; so in overlapping areas these sprites should not be drawn
  .db  52  96 '9'  $10
  .db  52  88 '8'  $10
  .db  52  80 '7'  $10
  .db  52  72 '6'  $10
  .db  52  64 '5'  $10
  .db  52  56 '4'  $10
  .db  52  48 '3'  $10
  .db  52  40 '2'  $10
  .db  52  32 '1'  $10
  .db  52  24 '0'  $10
  .db  52  16 $10  $10 ; 11th sprite should not be displayed

  ;           $10 = unprintable character = solid rectangle in the font
  ; Draw order is based on X coordinate, so in both following groups
  ; the black area should be bigger than the light grey
  .db  64  12 $10  $10
  .db  64  8  $10  $00
  .db  80  8  $10  $00
  .db  80  12 $10  $10
data_end:
  nop

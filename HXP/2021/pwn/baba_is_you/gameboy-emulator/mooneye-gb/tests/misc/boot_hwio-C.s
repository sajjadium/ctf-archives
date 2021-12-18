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

; Tests the initial values of hardware IO registers that are not
; affected by the test itself, timing, or random factors.
; Therefore, we skip $FF04 (DIV), $FF30-$FF3F (wave ram),
; $FF40 (LCDC) and $FF41 (STAT)

; Verified results:
;   pass: CGB, AGB, AGS
;   fail: DMG, MGB, SGB, SGB2

.include "common.s"

  ld hl, $FF00
  ld de, hwio_data

--
  ld a, (de)
  ld c, a
  inc de

.repeat 8 INDEX i
  ld a, (hl)
  ld b, a

  bit 7 - i, c
  jr z, +

  ld a, (de)
  cp b
  jp nz, mismatch
+ inc de
  inc hl
.endr

  ld a, l
  cp $80
  jp nz, --

  quit_ok

mismatch:
  ld (mismatch_data), a
  ld a, b
  ld (mismatch_mem), a
  ld a, l
  ld (mismatch_addr), a
  ld a, h
  ld (mismatch_addr + 1), a

  quit_inline
  print_string_literal "MISMATCH AT $"
  ld a, (mismatch_addr + 1)
  call print_hex8
  ld a, (mismatch_addr)
  call print_hex8
  call print_newline
  call print_newline

  print_string_literal "EXPECTED "
  ld a, (mismatch_data)
  call print_hex8
  call print_newline

  print_string_literal "GOT      "
  ld a, (mismatch_mem)
  call print_hex8

  ld d, $42
  ret

hwio_data:
;   mask bits  values                                   address of first byte
;   |          |                                        |
.db %11110111, $FF, $00, $7E, $FF, $FF, $00, $00, $F8 ; $FF00
.db %11111111, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $E1 ; $FF08
.db %11111111, $80, $BF, $F3, $FF, $BF, $FF, $3F, $00 ; $FF10
.db %11111111, $FF, $BF, $7F, $FF, $9F, $FF, $BF, $FF ; $FF18
.db %11111111, $FF, $00, $00, $BF, $77, $F3, $F1, $FF ; $FF20
.db %11111111, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF ; $FF28
.db %00000000, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF ; $FF30
.db %00000000, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF ; $FF38
.db %00110101, $FF, $FF, $00, $00, $FF, $00, $00, $FC ; $FF40
.db %00111111, $00, $00, $00, $00, $FF, $FF, $FF, $FE ; $FF48
.db %11111111, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF ; $FF50
.db %11111111, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF ; $FF58
.db %11111111, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF ; $FF60
.db %11111111, $C8, $FF, $D0, $FF, $FF, $FF, $FF, $FF ; $FF68
.db %11111111, $FF, $FF, $00, $00, $FF, $8F, $00, $00 ; $FF70
.db %11111111, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF ; $FF78

.ramsection "Test-State" slot HRAM_SLOT
  mismatch_addr dw
  mismatch_data db
  mismatch_mem db
.ends

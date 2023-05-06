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

; This test checks that OAM DMA copies all bytes correctly.

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ld sp, DEFAULT_SP

  call disable_lcd_safe
  call clear_oam

  ld hl, hram.dma_proc
  ld de, dma_proc
  ld bc, _sizeof_dma_proc
  call memcpy

  ld a, >random_data
  call hram.dma_proc

  ld hl, random_data
  ld de, OAM
  ld bc, OAM_LEN
  call memcmp

  jp nc, finish

fail:
  ld a, l
  ldh (<fail_offset), a

  quit_inline
  print_string_literal "Fail: $FE"
  ldh a, (<fail_offset)
  call print_hex8
  ld d, $42
  ret

finish:
  quit_ok

dma_proc:
  ldh (<DMA), a
  ld b, 40
- dec b
  jr nz, -
  ret

_end_dma_proc:

.org $1200
random_data:
.db $d0, $25, $3d, $5b, $d2, $60, $63, $c3, $2e, $7e, $52, $32, $e5, $93, $c5, $09
.db $53, $38, $0a, $a8, $c0, $35, $ac, $e3, $66, $69, $9e, $a3, $b0, $48, $50, $2e
.db $b2, $de, $16, $81, $ca, $af, $0c, $f3, $92, $8f, $c7, $1a, $35, $57, $8d, $5b
.db $45, $86, $d1, $f6, $5f, $2c, $c2, $a6, $ce, $8b, $6f, $4e, $f7, $e8, $be, $c3
.db $ce, $6e, $62, $05, $e8, $70, $b5, $d7, $72, $ac, $b9, $45, $4c, $ca, $b8, $73
.db $71, $5a, $04, $36, $52, $1c, $9e, $3d, $43, $c7, $09, $fb, $09, $17, $09, $87
.db $4c, $00, $6d, $d1, $e2, $62, $d2, $81, $40, $8f, $dc, $12, $38, $af, $d4, $f6
.db $53, $ea, $45, $8c, $84, $e1, $4b, $b2, $5c, $03, $26, $b3, $39, $fa, $02, $b6
.db $32, $d5, $9c, $c3, $16, $d0, $49, $29, $ad, $78, $7d, $8b, $7a, $03, $31, $34
.db $19, $77, $3d, $70, $86, $b4, $a2, $96, $90, $1d, $e2, $dd, $6b, $01, $9c, $94

.ramsection "Test-HRAM" slot HRAM_SLOT
  hram.dma_proc dsb 16
  fail_offset db
.ends

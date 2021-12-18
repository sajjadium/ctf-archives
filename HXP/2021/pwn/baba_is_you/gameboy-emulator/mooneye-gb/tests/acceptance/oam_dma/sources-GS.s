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

; This test checks that OAM DMA source memory areas work as expected,
; including the area past $DFFF.

; Verified results:
;   pass: DMG, MGB, SGB, SGB2
;   fail: CGB, AGB, AGS

.define CART_TYPE $1B ; MBC5, ram, battery
.define CART_RAM_SIZE 2

.include "common.s"

  ld sp, $ffff

  call disable_lcd_safe
  call clear_oam
  call clear_vram
  call clear_wram

prepare_part1:
  ld hl, hram.dma_proc
  ld de, dma_proc
  ld bc, _sizeof_dma_proc
  call memcpy

test_0000:
  ld a, $00
  call hram.dma_proc

  ld hl, $0000
  call check_oam

  jp nc, test_3f00

  quit_failure_string "Fail: $0000"

test_3f00:
  ld a, $3f
  call hram.dma_proc

  ld hl, $3f00
  call check_oam

  jp nc, test_4000

  quit_failure_string "Fail: $3F00"

test_4000:
  ld a, $40
  call hram.dma_proc

  ld hl, $4000
  call check_oam

  jp nc, test_7f00

  quit_failure_string "Fail: $4000"

test_7f00:
  ld a, $7f
  call hram.dma_proc

  ld hl, $7f00
  call check_oam

  jp nc, prepare_part2

  quit_failure_string "Fail: $7F00"

prepare_part2:
  ld hl, $8000
  call copy_ram_pattern_1
  ld hl, $9f00
  call copy_ram_pattern_2

test_8000:
  ld a, $80
  call hram.dma_proc

  ld hl, ram_pattern_1
  call check_oam

  jp nc, test_9f00

  quit_failure_string "Fail: $8000"

test_9f00:
  ld a, $9f
  call hram.dma_proc

  ld hl, ram_pattern_2
  call check_oam

  jp nc, prepare_part3

  quit_failure_string "Fail: $9F00"

prepare_part3:
  call clear_vram

  ld a, $0a
  ld ($0000), a

  ld hl, $a000
  ld bc, $2000
  xor a
  call memset

  ld hl, $a000
  call copy_ram_pattern_1
  ld hl, $bf00
  call copy_ram_pattern_2

test_a000:
  ld a, $a0
  call hram.dma_proc

  ld hl, ram_pattern_1
  call check_oam

  jp nc, test_bf00

  quit_failure_string "Fail: $A000"

test_bf00:
  ld a, $bf
  call hram.dma_proc

  ld hl, ram_pattern_2
  call check_oam

  jp nc, prepare_part4

  quit_failure_string "Fail: $BF00"

prepare_part4:
  xor a
  ld ($0000), a

  ld hl, $c000
  call copy_ram_pattern_1
  ld hl, $de00
  call copy_ram_pattern_1
  ld hl, $df00
  call copy_ram_pattern_2

test_c000:
  ld a, $c0
  call hram.dma_proc

  ld hl, ram_pattern_1
  call check_oam

  jp nc, test_df00

  quit_failure_string "Fail: $C000"

test_df00:
  ld a, $df
  call hram.dma_proc

  ld hl, ram_pattern_2
  call check_oam

  jp nc, test_e000

  quit_failure_string "Fail: $DF00"

test_e000:
  ld a, $e0
  call hram.dma_proc

  ld hl, ram_pattern_1
  call check_oam

  jp nc, test_fe00

  quit_failure_string "Fail: $E000"

test_fe00:
  call clear_oam
  ld a, $fe
  call hram.dma_proc

  ld hl, ram_pattern_1
  call check_oam

  jp nc, test_ff00

  quit_failure_string "Fail: $FE00"

test_ff00:
  ld a, $ff
  call hram.dma_proc

  ld hl, ram_pattern_2
  call check_oam

  jp nc, test_finish

  quit_failure_string "Fail: $FF00"

test_finish:
  quit_ok

check_oam:
  ld de, OAM
  ld bc, OAM_LEN
  jp memcmp

dma_proc:
  ldh (<DMA), a
  ld a, 40
- dec a
  jr nz, -
  ret

copy_ram_pattern_1:
  ld de, ram_pattern_1
  ld bc, OAM_LEN
  jp memcpy

ram_pattern_1:
.db $c2, $d5, $1a, $e9, $fb, $0c, $80, $87, $45, $a9, $06, $d3, $bf, $0e, $38, $43
.db $32, $70, $7e, $44, $58, $0d, $4c, $3d, $1e, $4c, $17, $c4, $50, $e8, $6e, $b8
.db $f2, $a4, $a0, $5c, $e4, $7a, $87, $3f, $ee, $44, $82, $ef, $ed, $63, $49, $43
.db $da, $2e, $23, $7d, $de, $5a, $1b, $47, $b4, $28, $0f, $5c, $08, $90, $2c, $b1
.db $67, $48, $87, $e9, $10, $e6, $a4, $13, $ff, $2c, $62, $72, $a9, $08, $08, $9c
.db $f8, $77, $8e, $b8, $5a, $db, $31, $3e, $3f, $41, $ae, $1a, $b8, $33, $67, $96
.db $2d, $0b, $ae, $e3, $70, $69, $fe, $64, $b5, $1d, $e4, $65, $de, $c5, $64, $7a
.db $5c, $0e, $76, $cb, $2f, $79, $a6, $a8, $64, $99, $55, $5a, $63, $e7, $af, $06
.db $bb, $88, $e9, $15, $e2, $d3, $aa, $fc, $f0, $91, $99, $d6, $11, $b6, $07, $ee
.db $b2, $59, $3d, $ed, $46, $cd, $83, $e5, $aa, $ad, $5a, $1f, $60, $31, $3e, $88

copy_ram_pattern_2:
  ld de, ram_pattern_2
  ld bc, OAM_LEN
  jp memcpy

ram_pattern_2:
.db $db, $16, $e1, $18, $00, $39, $6b, $e5, $21, $a2, $ab, $fa, $da, $e9, $1b, $8d
.db $98, $14, $77, $c7, $92, $8c, $16, $1e, $30, $fe, $e6, $70, $46, $7f, $2d, $f1
.db $7c, $e4, $c4, $e3, $b2, $ef, $e2, $2e, $cf, $16, $1e, $b2, $c6, $b6, $ec, $31
.db $85, $c9, $8f, $33, $d9, $a8, $80, $2d, $c1, $99, $56, $3d, $b5, $13, $8e, $69
.db $85, $bf, $10, $57, $1c, $8e, $b2, $c4, $62, $97, $9f, $d4, $ab, $5d, $76, $21
.db $a0, $ae, $59, $50, $80, $09, $33, $65, $24, $54, $a9, $6e, $f1, $6c, $50, $e7
.db $d1, $04, $c2, $e7, $9c, $8c, $1f, $43, $38, $5b, $a9, $55, $5e, $41, $98, $0c
.db $7d, $42, $99, $ac, $49, $27, $e7, $a8, $f1, $09, $f4, $8e, $94, $75, $b2, $16
.db $2a, $49, $c0, $c9, $2f, $bd, $f8, $e6, $53, $98, $e8, $60, $f7, $03, $87, $6b
.db $59, $0f, $b0, $f6, $07, $18, $ef, $92, $d8, $fd, $50, $9e, $61, $b6, $14, $46

.org $0000
.db $1d, $de, $f9, $11, $5f, $11, $6f, $3a, $65, $ea, $d7, $48, $e8, $3a, $d7, $6e
.db $be, $45, $5d, $f2, $29, $2a, $cb, $a2, $bb, $19, $8f, $0d, $47, $86, $60, $81
.db $1e, $b3, $42, $97, $18, $05, $22, $e5, $21, $49, $05, $49, $2f, $07, $7f, $27
.db $b3, $e0, $22, $35, $a7, $fb, $20, $18, $b8, $cb, $6f, $cc, $27, $6f, $7b, $f5
.db $28, $48, $24, $34, $31, $bb, $3e, $48, $67, $8c, $cd, $14, $58, $8b, $05, $31
.db $95, $12, $95, $1f, $62, $30, $c4, $2a, $0e, $0e, $81, $74, $d8, $ec, $68, $39
.db $8a, $83, $c9, $8c, $49, $85, $18, $bd, $3c, $ca, $4c, $bc, $e2, $52, $dc, $d8
.db $61, $e0, $65, $32, $b7, $b9, $a5, $94, $35, $65, $dd, $44, $93, $d5, $ce, $a0
.db $d5, $7f, $ef, $ef, $e2, $78, $c6, $61, $66, $f2, $f0, $23, $f9, $be, $2e, $bb
.db $7b, $94, $d9, $35, $56, $0d, $69, $1a, $d5, $f5, $f0, $89, $8d, $93, $20, $68

.org $3F00
.db $c1, $cc, $59, $fd, $44, $4f, $72, $53, $81, $8c, $a2, $4a, $6f, $d3, $2b, $6f
.db $12, $c5, $be, $5c, $cf, $55, $07, $49, $68, $79, $fc, $5b, $21, $27, $0d, $fe
.db $5f, $67, $bf, $23, $c0, $a6, $b2, $7e, $f7, $65, $27, $c0, $ae, $a2, $7a, $35
.db $7d, $5f, $da, $f6, $e3, $ef, $35, $1a, $9a, $df, $c8, $80, $a6, $bd, $e7, $55
.db $5f, $4d, $31, $87, $81, $2c, $9e, $46, $6e, $11, $4d, $9b, $30, $3c, $e0, $36
.db $9c, $a5, $35, $a3, $72, $da, $6e, $a3, $b6, $fa, $7f, $55, $f6, $23, $8c, $6e
.db $78, $e5, $c7, $ae, $ce, $84, $36, $9f, $77, $16, $29, $9e, $91, $08, $45, $f5
.db $ec, $56, $e9, $92, $61, $a3, $7f, $0d, $07, $85, $75, $2d, $43, $88, $f9, $85
.db $cd, $8a, $5b, $aa, $d8, $12, $bd, $e2, $12, $df, $16, $fd, $d2, $5b, $38, $63
.db $b9, $fc, $53, $20, $ec, $a3, $c4, $97, $a9, $72, $f3, $b1, $37, $ab, $9d, $fe

.bank 1 slot 1

.org $0000
.db $56, $44, $c8, $f8, $be, $29, $7a, $9c, $87, $38, $96, $ef, $05, $92, $43, $4f
.db $fb, $09, $33, $ae, $40, $48, $06, $e5, $d1, $56, $26, $d0, $73, $8b, $86, $b0
.db $20, $88, $08, $f5, $10, $aa, $e6, $79, $06, $6a, $3b, $28, $a4, $67, $22, $1f
.db $27, $34, $76, $84, $7a, $dc, $30, $16, $06, $fd, $cf, $98, $c5, $74, $a7, $7c
.db $37, $87, $f7, $db, $30, $23, $54, $09, $57, $ea, $91, $6d, $0c, $48, $4c, $10
.db $87, $03, $3c, $83, $f2, $5a, $86, $e6, $4a, $c6, $d4, $7d, $f1, $9f, $b3, $23
.db $a9, $20, $9a, $5f, $7c, $98, $44, $9c, $7f, $7f, $61, $dd, $75, $3e, $27, $36
.db $16, $50, $fb, $ee, $9f, $49, $05, $82, $5a, $61, $14, $6b, $9d, $69, $01, $be
.db $73, $6b, $e5, $0a, $a7, $12, $e7, $c1, $6e, $2b, $01, $2c, $97, $de, $a3, $be
.db $1f, $df, $7c, $5c, $02, $0f, $43, $bb, $cb, $74, $a2, $9f, $32, $c1, $08, $72

.org $3F00
.db $51, $7b, $1a, $54, $7c, $0e, $15, $5b, $96, $a9, $4e, $3f, $04, $60, $c9, $cf
.db $6c, $a4, $1e, $e7, $6e, $03, $c7, $a2, $12, $e9, $78, $bb, $4b, $32, $94, $b4
.db $08, $43, $38, $f1, $6b, $27, $4e, $b2, $68, $43, $4d, $1a, $09, $68, $cb, $fc
.db $23, $bc, $be, $e2, $09, $c0, $39, $30, $aa, $4a, $5a, $e1, $3c, $53, $54, $6f
.db $b3, $3c, $25, $11, $b4, $12, $3a, $99, $1a, $b7, $8c, $81, $da, $97, $74, $2f
.db $03, $3b, $49, $99, $76, $89, $4c, $4c, $62, $26, $43, $12, $63, $7c, $b3, $c5
.db $bd, $0b, $3f, $81, $24, $43, $72, $b2, $37, $7a, $2e, $8d, $8e, $16, $88, $bb
.db $c3, $f0, $48, $00, $97, $06, $51, $78, $72, $5c, $20, $f1, $4d, $21, $bf, $5b
.db $81, $f0, $a7, $ba, $cf, $f2, $5c, $c2, $59, $eb, $4e, $7a, $1d, $16, $b9, $b5
.db $cc, $92, $9e, $60, $8f, $86, $6a, $dc, $e2, $26, $dc, $9f, $05, $00, $a2, $21

.ramsection "Test-HRAM" slot HRAM_SLOT
  hram.dma_proc dsb 16
.ends

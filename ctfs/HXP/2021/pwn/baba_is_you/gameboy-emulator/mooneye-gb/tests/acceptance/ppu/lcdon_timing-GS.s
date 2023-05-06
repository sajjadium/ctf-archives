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

; Tests the values of LY, STAT, and read accessibility of OAM and VRAM after
; the PPU is enabled by writing to LCDC.
; Expectations
;   - line 0 starts with mode 0 and goes straight to mode 3
;   - line 0 has different timings because the PPU is late by 2 T-cycles
;   - line 1 and line 2 have normal timings

; Verified results:
;   pass: DMG, MGB, SGB, SGB2
;   fail: CGB, AGB, AGS

; On real hardware, failures can be grouped into two categories:
;   CGB before D: failure
;   CGB D, E, AGB, AGS: different failure than pre-D CGBs

.include "common.s"

  ld sp, DEFAULT_SP

  call disable_lcd_safe
  call clear_vram
  call clear_oam

test_ly:
  ld de, LY
  call test_passes
  ld de, expect_ly
  call verify_results

test_stat_lyc0:
  xor a
  ldh (<LYC), a
  ld de, STAT
  call test_passes
  ld de, expect_stat_lyc0
  call verify_results

test_stat_lyc1:
  ld a, $01
  ldh (<LYC), a
  ld de, STAT
  call test_passes
  ld de, expect_stat_lyc1
  call verify_results

test_oam_access:
  ld de, OAM
  call test_passes
  ld de, expect_oam_access
  call verify_results

test_vram_access:
  ld de, VRAM
  call test_passes
  ld de, expect_vram_access
  call verify_results

test_finish:
  quit_ok

.bank 1 slot 1
.section "Test_expectations" FREE

; Each read in a test pass can be seen as equivalent to this:
;   ldh (<LCDC), a
;   nops XXX   <- cycle count goes here
;   ld a, (de)
cycle_counts:
.db 0   17  60  110 130 174 224 244
.db 1   18  61  111 131 175 225 245
.db 2   19  62  112 132 176 226 246

expect_ly:
.db $00 $00 $00 $00 $01 $01 $01 $02
.db $00 $00 $00 $01 $01 $01 $02 $02
.db $00 $00 $00 $01 $01 $01 $02 $02
.db "LY" $00

expect_stat_lyc0:
.db $84 $84 $87 $84 $82 $83 $80 $82
.db $84 $87 $84 $80 $82 $80 $80 $82
.db $84 $87 $84 $82 $83 $80 $82 $83
.db "STAT LYC=0" $00

expect_stat_lyc1:
.db $80 $80 $83 $80 $86 $87 $84 $82
.db $80 $83 $80 $80 $86 $84 $80 $82
.db $80 $83 $80 $86 $87 $84 $82 $83
.db "STAT LYC=1" $00

expect_oam_access:
.db $00 $00 $FF $00 $FF $FF $00 $FF
.db $00 $FF $00 $FF $FF $00 $FF $FF
.db $00 $FF $00 $FF $FF $00 $FF $FF
.db "OAM access" $00

expect_vram_access:
.db $00 $00 $FF $00 $00 $FF $00 $00
.db $00 $FF $00 $00 $FF $00 $00 $FF
.db $00 $FF $00 $00 $FF $00 $00 $FF
.db "VRAM access" $00

; Inputs:
;   DE: test expectations pointer
verify_results:
  push de

  ld c, $00
  ld hl, hram.pass1_results

- ld a, (hl)
  ld b, a
  ld a, (de)
  cp b
  jp nz, verify_fail
  inc de
  inc hl
  inc c
  ld a, c
  cp 24
  jr nz, -

  pop de
  ret

verify_fail:
  ld a, (hl)
  ld (hram.fail_actual), a
  ld a, (de)
  ld (hram.fail_expect), a
  ld a, c
  ld (hram.fail_round), a
  pop de
  ld h, $00
  ld l, 24
  add hl, de
  ld a, l
  ld (hram.fail_str_l), a
  ld a, h
  ld (hram.fail_str_h), a

  quit_inline
  print_string_literal "Test failed: "
  call print_newline
  ld a, (hram.fail_str_l)
  ld c, a
  ld a, (hram.fail_str_h)
  ld b, a
  call print_string
  call print_newline
  call print_newline

  print_string_literal "Cycle:    $"
  push hl
  ld hl, cycle_counts
  ld b, $00
  ld a, (hram.fail_round)
  ld c, a
  add hl, bc
  ld a, (hl)
  pop hl
  call print_hex8
  call print_newline

  print_string_literal "Expected: $"
  ld a, (hram.fail_expect)
  call print_hex8
  call print_newline

  print_string_literal "Actual:   $"
  ld a, (hram.fail_actual)
  call print_hex8

  ld d, $42
  ret

.ends

.ramsection "Test-State" slot HRAM_SLOT
  hram.pass1_results dsb 8
  hram.pass2_results dsb 8
  hram.pass3_results dsb 8
  hram.fail_round db
  hram.fail_expect db
  hram.fail_actual db
  hram.fail_str .dw
  hram.fail_str_l db
  hram.fail_str_h db
.ends

.bank 1 slot 1
.section "Test_passes" FREE

; Inputs:
;   DE address to read
; Preserved: -
test_passes:

.macro test_reads
  ld a, (de)  ; 0
  ld (hl+), a
  nops 13
  ld a, (de)  ; 17
  ld (hl+), a
  nops 39
  ld a, (de)  ; 60
  ld (hl+), a
  nops 46
  ld a, (de)  ; 110
  ld (hl+), a
  nops 16
  ld a, (de)  ; 130
  ld (hl+), a
  nops 40
  ld a, (de)  ; 174
  ld (hl+), a
  nops 46
  ld a, (de)  ; 224
  ld (hl+), a
  nops 16
  ld a, (de)  ; 244
  ld (hl+), a
.endm

test_pass1:
  ld hl, hram.pass1_results
  ld a, $81
  ldh (<LCDC), a
  test_reads
  call disable_lcd_safe

test_pass2:
  ld hl, hram.pass2_results
  ld a, $81
  ldh (<LCDC), a
  nops 1
  test_reads
  call disable_lcd_safe

test_pass3:
  ld hl, hram.pass3_results
  ld a, $81
  ldh (<LCDC), a
  nops 2
  test_reads
  jp disable_lcd_safe

.ends

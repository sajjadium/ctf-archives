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

; Tests whether writes to OAM and VRAM pass after the PPU is enabled by
; writing to LCDC.

; Verified results:
;   pass: DMG, MGB, SGB, SGB2
;   fail: CGB, AGB, AGS

.include "common.s"

  ld sp, DEFAULT_SP

  call disable_lcd_safe
  call clear_vram
  call clear_oam

test_oam_access:
  ld de, OAM
  call run_tests
  ld de, expect_oam_access
  call verify_results

test_vram_access:
  ld de, VRAM
  call run_tests
  ld de, expect_vram_access
  call verify_results

test_finish:
  quit_ok

.bank 1 slot 1
.section "Test_expectations" FREE

; Each write in a test pass can be seen as equivalent to this:
;   ldh (<LCDC), a <- PPU enabled
;   nops XXX       <- nop count goes here
;   ld (de), a
nop_counts:
.db 0   17  18  60  61  110 111
.db 112 130 131 132 174 175 224 225
.db 226 244 245 246

expect_oam_access:
.db $81 $81 $00 $00 $81 $81 $81
.db $00 $00 $81 $00 $00 $81 $81 $81
.db $00 $00 $81 $00
.db "OAM write" $00

expect_vram_access:
.db $81 $81 $00 $00 $81 $81 $81
.db $81 $81 $81 $00 $00 $81 $81 $81
.db $81 $81 $81 $00
.db "VRAM write" $00

; Inputs:
;   DE: test expectations pointer
verify_results:
  push de

  ld c, $00
  ld hl, wram.test_results

- ld a, (hl)
  ld b, a
  ld a, (de)
  cp b
  jp nz, verify_fail
  inc de
  inc hl
  inc c
  ld a, c
  cp 19
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
  ld l, 19
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
  ld hl, nop_counts
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

.ramsection "Test-WRAM" slot WRAM0_SLOT
  wram.test_code dsb 300
  wram.test_results dsb 19
.ends

.ramsection "Test-HRAM" slot HRAM_SLOT
  hram.fail_round db
  hram.fail_expect db
  hram.fail_actual db
  hram.fail_str .dw
  hram.fail_str_l db
  hram.fail_str_h db
.ends

.bank 1 slot 1
.section "Test_case" FREE

; Inputs:
;   DE address to read
; Preserved: -
run_tests:
  ld hl, nop_counts
  ld bc, wram.test_results
  xor a

- cp 19
  ret z

  push af
  ld a, (hl+)
  push hl
  ld h, b
  ld l, c

  call test_case

  ld b, h
  ld c, l
  pop hl
  pop af
  inc a

  jr -

; Inputs:
;   A number of nops
;   DE address to read
;   HL test result pointer
; Outputs:
;   DE address to read
;   HL test result pointer + 1
test_case:
  push hl
  push de
  push af
  xor a
  ld (OAM), a
  ld (VRAM), a

  ; Copy test case prologue code
  ld hl, wram.test_code
  ld de, test_case_prologue
  ld bc, test_case_epilogue - test_case_prologue
  call memcpy

  ; Add nops
  pop af
- and a
  jr z, +
  dec a
  ld (hl), $00
  inc hl
  jr -
+

  ; Copy test case epilogue code
  ld de, test_case_epilogue
  ld bc, test_case_end - test_case_epilogue
  call memcpy

  pop de
  call wram.test_code
  call disable_lcd_safe

  pop hl
  ld a, (de)
  ld (hl+), a
  ret

test_case_prologue:
  ld a, $81
  ldh (<LCDC), a
  ; nops will be added here
test_case_epilogue:
  ld (de), a
  ret
test_case_end:

.ends

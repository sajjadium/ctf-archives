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

; This test checks all unused bits in working $FFxx IO,
; and all unused $FFxx IO. Unused bits and unused IO all return 1s.
; A test looks like this:
;
;            mask      write     expected
; test REG   MASK      WRITE     EXPECTED
;
;   1. write WRITE to REG
;   2. read VALUE from REG
;   3. compare VALUE & MASK with EXPECTED & MASK

; Verified results:
;   pass: DMG, MGB, SGB, SGB2
;   fail: CGB, AGB, AGS

.include "common.s"

.macro test ARGS reg mask write expect
  ld hl, _test_data_\@
  ld a, l
  ld (test_addr), a
  ld a, h
  ld (test_addr + 1), a

  ld sp, DEFAULT_SP

  call run_testcase
  jr _finish_\@

_test_data_\@:
  .db <reg
  .db mask
  .db write
  .db expect

; String representing bits in "write"
.repeat 8 INDEX bit
  .db '0' + (write >> (7 - bit)) & 1
.endr
  .db $00

; String representing bits in "expect"
; Bits not present in mask are spaces
.repeat 8 INDEX bit
  .if mask >> (7 - bit) & 1 != 0
    .db '0' + (expect >> (7 - bit)) & 1
  .else
    .db ' '
  .endif
.endr
  .db $00

_finish_\@:
.endm

; Simple unmapped all $00 and $FF tests
.macro test_unmapped
  test \1 %11111111 %00000000 %11111111
  test \1 %11111111 %11111111 %11111111
.endm

  di

  ;          mask      write     expected
  ;          |         |         |
  test P1    %11000000 %11111111 %11000000
  test P1    %11000000 %00111111 %11000000
  test SC    %01111110 %01111110 %01111110
  test SC    %01111110 %00000000 %01111110
  test TAC   %11111000 %11111000 %11111000
  test TAC   %11111000 %00000000 %11111000
  test IF    %11100000 %11100000 %11100000
  test IF    %11100000 %00000000 %11100000
  test STAT  %10000000 %10000000 %10000000
  test STAT  %10000000 %00000000 %10000000
  test NR10  %10000000 %00000000 %10000000
  test NR10  %10000000 %10000000 %10000000
  test NR30  %01111111 %00000000 %01111111
  test NR30  %01111111 %01111111 %01111111
  test NR32  %10011111 %00000000 %10011111
  test NR32  %10011111 %10011111 %10011111
  test NR41  %11000000 %00000000 %11000000
  test NR41  %11000000 %11000000 %11000000
  test NR44  %00111111 %00000000 %00111111
  test NR44  %00111111 %00111111 %00111111
  test NR52  %01110000 %10000000 %01110000
  test NR52  %01110000 %11110000 %01110000
  test IE    %11100000 %00000000 %00000000
  test IE    %11100000 %11100000 %11100000

  test_unmapped $FF03
  test_unmapped $FF08
  test_unmapped $FF09
  test_unmapped $FF0A
  test_unmapped $FF0B
  test_unmapped $FF0C
  test_unmapped $FF0D
  test_unmapped $FF0E
  test_unmapped $FF15
  test_unmapped $FF1F
  test_unmapped $FF27
  test_unmapped $FF28
  test_unmapped $FF29

; $FF4C - $FF7F
.repeat $34 INDEX offset
  test_unmapped $FF4C + offset
.endr

  quit_ok

; Inputs:
;   HL: test data address
run_testcase:
  ; C = reg
  ld a, (hl)
  ld c, a

  inc hl
  ; B = mask
  ld a, (hl)
  ld b, a

  ; write value to reg
  inc hl
  ld a, (hl)
  ld ($FF00+C), a

  ; read value, apply mask
  ld a, ($FF00+C)
  and b

  ; check expectation
  ld d, a
  inc hl
  ld a, (hl)
  and b
  cp d
  ret z

  ld a, d
  ld (test_got), a

  call fetch_test_data

  quit_inline
  print_string_literal "TEST FAILED"
  call print_newline
  call print_newline
  print_string_literal "$FF"

  ld a, (test_reg)
  call print_hex8

  print_string_literal "       76543210"
  call print_newline
  call print_newline
  print_string_literal "WROTE       "

  ld bc, test_str_write
  call print_string

  call print_newline
  print_string_literal "EXPECTED    "

  ld bc, test_str_expect
  call print_string

  call print_newline
  print_string_literal "GOT         "

  call print_got

  ld d, $42
  ret

fetch_test_data:
  ld a, (test_addr)
  ld e, a
  ld a, (test_addr + 1)
  ld d, a

  ld hl, test_reg
  ; Copy reg
  ld a, (de)
  ld (hl+), a
  inc de
  ; Copy mask
  ld a, (de)
  ld (hl+), a
  inc de

  ; Skip write+expect
  inc de
  inc de

  ; Copy both strings
  ld bc, 18
  call memcpy

  ret

; Inputs:
;   HL: print pointer
print_got:
  ld a, (test_got)
  ld d, a
  ld a, (test_mask)
  ld e, a
  ld c, $80

--
  ; Skip bits not present in mask
  ld a, e
  and c
  jr z, _skip

  ld a, d
  and c
  jr nz, _print_one
_print_zero:
  ld b, 0
  jr _print_bit
_print_one:
  ld b, 1

_print_bit:
  push bc
  push de
  call print_hex4
  pop de
  pop bc
  jr _next

_skip:
  inc hl
_next:
  rrc c
  jr nc, --

  ret

.ramsection "Test-State" slot HRAM_SLOT
  test_addr dw
  test_got db
  test_reg db
  test_mask db
  test_str_write dsb 9
  test_str_expect dsb 9
.ends

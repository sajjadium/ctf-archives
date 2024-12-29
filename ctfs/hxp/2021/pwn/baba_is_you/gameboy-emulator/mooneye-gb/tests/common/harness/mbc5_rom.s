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

.define CART_TYPE $19 ; MBC5

.include "common.s"

.define wram.functions $c000

.macro call_wram ARGS target
  call target - wram_functions_start + wram.functions
.endm

.macro jp_wram ARGS target
  jp target - wram_functions_start + wram.functions
.endm

  ld sp, DEFAULT_SP

  ld hl, wram.functions
  ld de, wram_functions_start
  ld bc, wram_functions_end - wram_functions_start
  call memcpy

  ld hl, wram.expected_banks
  ld de, expected_banks
  ld bc, _sizeof_wram.expected_banks
  call memcpy

  jp_wram run_test_suite

fail:
  quit_inline
  print_string_literal "TEST FAILED"
  call print_newline
  ldh a, (<hram.lower_upper)
  and a
  jr nz, +

  print_string_literal "$0000-$3FFF"
  jr ++

+ print_string_literal "$4000-$7FFF"

++
  call print_newline

  print_string_literal "BANK NUMBER "
  ldh a, (<hram.bank_number_h)
  call print_hex8
  ldh a, (<hram.bank_number_l)
  call print_hex8
  call print_newline

  print_string_literal "EXPECTED    "
  ldh a, (<hram.expected_value_h)
  call print_hex8
  ldh a, (<hram.expected_value_l)
  call print_hex8
  call print_newline

  print_string_literal "ACTUAL      "
  ldh a, (<hram.actual_value_h)
  call print_hex8
  ldh a, (<hram.actual_value_l)
  call print_hex8
  call print_newline
  ld d, $42
  ret


wram_functions_start:

run_test_suite:
  call_wram run_tests

  call_wram restore_mbc5
  quit_ok

run_tests:
  ld bc, $0000
--
  ld a, c
  ldh (<hram.bank_number_l), a
  ld a, b
  ldh (<hram.bank_number_h), a

  call_wram test_case

  ldh a, (<hram.bank_number_l)
  ld c, a
  ldh a, (<hram.bank_number_h)
  ld b, a
  inc bc
  ld a, b
  cp $01
  jr nz, --
  ld a, c
  cp $00
  jr nz, --

  ret

test_case:
  ldh a, (<hram.bank_number_l)
  ld c, a
  ldh a, (<hram.bank_number_h)
  ld b, a
  call_wram switch_bank

  xor a
  ldh (<hram.lower_upper), a
  ldh (<hram.expected_value_l), a
  ldh (<hram.expected_value_h), a

  ld a, ($0000)
  ld c, a
  ldh (<hram.actual_value_l), a
  ld a, ($0001)
  ldh (<hram.actual_value_h), a
  or c
  jr z, +

  call_wram restore_mbc5
  jp fail

+ ld a, $40
  ldh (<hram.lower_upper), a
  ldh a, (<hram.bank_number_l)
  ld c, a
  ldh a, (<hram.bank_number_h)
  ld b, a
  call_wram fetch_expected_value
  ld a, c
  ldh (<hram.expected_value_l), a
  ld a, b
  ldh (<hram.expected_value_h), a

  ld a, ($4000)
  ld c, a
  ldh (<hram.actual_value_l), a
  ld a, ($4001)
  ldh (<hram.actual_value_h), a
  ld b, a

  ldh a, (<hram.expected_value_l)
  cp c
  jr nz, ++
  ldh a, (<hram.expected_value_h)
  cp b
  ret z

++
  call_wram restore_mbc5
  jp fail

; Inputs: -
; Preserved: BC, DE, HL
restore_mbc5:
  ld bc, $0001
  jp_wram switch_bank

; Inputs:
;   BC: bank number
; Preserved: DE, HL
switch_bank:
  ld a, c
  ld (ROMB0), a
  ld a, b
  or %11111110 ; set high bits to expose bugs
  ld (ROMB1), a
  ret

; Inputs:
;   BC: bank number
; Preserved: DE
fetch_expected_value:
  ld hl, wram.expected_banks
  add hl, bc
  add hl, bc

  ld a, (hl+)
  ld c, a
  ld a, (hl)
  ld b, a
  ret

wram_functions_end:

.ramsection "Harness-WRAM" slot WRAM0_SLOT
  wram.expected_banks dsb 512
.ends

.ramsection "Harness-WRAM-functions" slot WRAM0_SLOT orga wram.functions force
  wram._functions dsb $200
.ends

.ramsection "Harness-HRAM" slot HRAM_SLOT
  hram.bank_number .dw
  hram.bank_number_l db
  hram.bank_number_h db
  hram.actual_value .dw
  hram.actual_value_l db
  hram.actual_value_h db
  hram.expected_value .dw
  hram.expected_value_l db
  hram.expected_value_h db
  hram.lower_upper db
.ends

.repeat CART_ROM_BANKS INDEX bank

.bank bank
.org $0000
.dw bank

.endr

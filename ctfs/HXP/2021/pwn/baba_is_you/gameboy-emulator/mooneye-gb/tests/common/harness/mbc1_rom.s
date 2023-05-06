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

.define CART_TYPE $01 ; MBC1

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

  print_string_literal "MODE "
  ldh a, (<hram.mode)
  call print_hex8

  call print_newline
  call print_newline

  print_string_literal "BANK NUMBER "
  ldh a, (<hram.bank_number)
  call print_hex8
  call print_newline

  print_string_literal "EXPECTED    "
  ldh a, (<hram.expected_value)
  call print_hex8
  call print_newline

  print_string_literal "ACTUAL      "
  ldh a, (<hram.actual_value)
  call print_hex8
  call print_newline
  ld d, $42
  ret


wram_functions_start:

run_test_suite:
  xor a
  ld (MODE), a
  ldh (<hram.mode), a
  call_wram run_tests

  ld a, $01
  ld (MODE), a
  ldh (<hram.mode), a
  call_wram run_tests

  call_wram restore_mbc1
  quit_ok

run_tests:
  xor a
  ldh (<hram.lower_upper), a
  call_wram run_test_cases

  ld a, $40
  ldh (<hram.lower_upper), a
  call_wram run_test_cases

  ret

run_test_cases:
  xor a
--
  ldh (<hram.bank_number), a

  call_wram test_case
  ldh a, (<hram.bank_number)
  inc a
  cp 128
  jr nz, --

  ret

; Inputs:
;   DE: address to check ($0000 or $4000)
test_case:
  ldh a, (<hram.bank_number)
  call_wram switch_bank

  ldh a, (<hram.bank_number)
  call_wram fetch_expected_value
  ldh (<hram.expected_value), a
  ld b, a

  ldh a, (<hram.lower_upper)
  ld d, a
  ld e, $00
  ld a, (de)
  cp b
  ret z

  ldh (<hram.actual_value), a

  call_wram restore_mbc1
  jp fail

; Inputs: -
; Preserved: BC, DE, HL
restore_mbc1:
  xor a
  ld (MODE), a
  ld a, 1
  jp_wram switch_bank

; Inputs:
;   A: bank number
; Preserved: BC, DE, HL
switch_bank:
  push af
  or %11100000 ; set high bits to expose bugs
  ld (BANK1), a
  pop af
  swap a
  sra a
  or %11111100 ; set high bits to expose bugs
  ld (BANK2), a
  ret

; Inputs:
;   A: bank number
; Preserved: DE
fetch_expected_value:
  ld b, $00
  ld c, a
  ld hl, wram.expected_banks
  add hl, bc

  ldh a, (<hram.lower_upper)
  and a
  jr z, +

  ld bc, 256
  add hl, bc
  jr ++

+ ldh a, (<hram.mode)
  and a
  jr z, ++

  ld bc, 128
  add hl, bc
  jr ++

++
  ld a, (hl)
  ret

wram_functions_end:

.ramsection "Harness-WRAM" slot WRAM0_SLOT
  wram.expected_banks dsb $180
.ends

.ramsection "Harness-WRAM-functions" slot WRAM0_SLOT orga wram.functions force
  wram._functions dsb $200
.ends

.ramsection "Harness-HRAM" slot HRAM_SLOT
  hram.bank_number db
  hram.actual_value db
  hram.expected_value db
  hram.lower_upper db
  hram.mode db
.ends

.repeat CART_ROM_BANKS INDEX bank

.bank bank
.org $0000
.db bank

.endr

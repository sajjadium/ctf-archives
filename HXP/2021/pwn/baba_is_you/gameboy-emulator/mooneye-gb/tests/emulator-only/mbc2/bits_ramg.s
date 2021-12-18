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

; Tests that RAMG is mapped to correct addresses, and RAM disable/enable
; happens with the right data values.

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC2A chip
; and support for configuring ROM/RAM sizes.

.define CART_TYPE $06 ; MBC2, ram, battery

.seed 340206
.include "common.s"

  ld sp, DEFAULT_SP

  ; Enable ram
  ld a, $0a
  ld (RAMG), a

  ; Copy RAM data
  ld hl, $a000
  ld bc, _sizeof_test_pattern
  ld de, test_pattern
  call memcpy

  ld hl, hram.memcmp
  ld de, memcmp
  ld bc, _sizeof_memcmp
  call memcpy

test_round1
  ld hl, $3fff

--
  ld a, h
  and %00000001
  jr nz, ++

  ld a, l
  ldh (<hram.test_address_l), a
  ld a, h
  ldh (<hram.test_address_h), a
  push hl

  ; Disable RAM
  ld (hl), $00

  ld de, all_ff
  call compare_ram_data
  jp c, fail_round1_disable

  pop hl
  push hl

  ; Enable RAM
  ld (hl), $0a

  ld de, test_pattern
  call compare_ram_data
  jp c, fail_round1_enable

  pop hl

++
  ld a, h
  or l
  dec hl
  jr nz, --

test_round2:
  xor a
  ldh (<hram.ramg), a

- ; Disable RAM
  xor a
  ld (RAMG), a

  ld de, all_ff
  call compare_ram_data
  jp c, fail_round2_disable

  ldh a, (<hram.ramg)

  ; Write RAMG
  ld (RAMG), a

  ld hl, ramg_expectations
  add l
  ld l, a
  ld a, (hl)
  and a

  jr z, @expect_disabled
@expect_enabled:
  ld de, test_pattern
  jr +
@expect_disabled:
  ld de, all_ff

+ call compare_ram_data
  jp c, fail_round2_expect

  ldh a, (<hram.ramg)
  inc a
  ldh (<hram.ramg), a
  jr nz, -

  quit_ok

test_pattern:
  .dbrnd 16, $f0, $ff

all_ff:
  .dsb 16, $ff

; Inputs:
;   DE: ram data address
; Outputs:
;   cf 0 if data matched
compare_ram_data:
  ld hl, $a000
  ld bc, _sizeof_test_pattern
  jp hram.memcmp

fail_round1_disable:
  quit_inline
  call print_newline
  print_string_literal "R1: Test failed"
  call print_newline
  call fail_round1_print_test_address
  call print_newline
  print_string_literal "RAM not disabled"
  ld d, $42
  ret

fail_round1_enable:
  quit_inline
  call print_newline
  print_string_literal "R1: Test failed"
  call print_newline
  call fail_round1_print_test_address
  call print_newline
  print_string_literal "RAM not enabled"
  ld d, $42
  ret

fail_round1_print_test_address:
  ldh a, (<hram.test_address_h)
  call print_hex8
  ldh a, (<hram.test_address_l)
  call print_hex8
  ret

fail_round2_disable:
  quit_failure_string "R2: RAM not disabled"

fail_round2_expect:
  quit_inline
  call print_newline
  print_string_literal "R2: Test failed"
  call print_newline
  print_string_literal "RAMG="
  ldh a, (<hram.ramg)
  call print_hex8

  ld d, $42
  ret

.bank 1 slot 1
.section "ramg_expectations" align $100
ramg_expectations:
.repeat 16
.db $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $ff $00 $00 $00 $00 $00
.endr
.ends

.ramsection "Test-HRAM" slot HRAM_SLOT
  hram.test_address .dw
  hram.test_address_l db
  hram.test_address_h db
  hram.ramg db
  hram.memcmp dsb 32
.ends

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

; Tests that ROMB is mapped to correct addresses and has the right initial
; value.

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC2A chip
; and support for configuring ROM/RAM sizes.

.define CART_TYPE $06 ; MBC2, ram, battery
.define CART_ROM_BANKS 4

.macro gen_bank1_pattern
  .db $24, $fe, $ca, $1e, $e4, $2c, $6a, $ec
  .db $7c, $af, $31, $be, $5c, $25, $c3, $7c
.endm

.macro gen_bank3_pattern
  .db $74, $86, $39, $37, $97, $0a, $83, $b2
  .db $8b, $77, $f0, $fa, $22, $81, $62, $69
.endm

.include "common.s"

  ld sp, DEFAULT_SP

  ld hl, hram.memcmp
  ld de, memcmp
  ld bc, _sizeof_memcmp
  call memcpy

test_round1:
  ld hl, $7f00
  ld de, bank1_pattern
  ld bc, 16
  call memcmp

  jr z, test_round2
  quit_failure_string "R1: initial ROMB"

test_round2:
  ld hl, $3fff

--
  ld a, h
  and %00000001
  jr z, ++

  ld a, l
  ldh (<hram.test_address_l), a
  ld a, h
  ldh (<hram.test_address_h), a
  push hl

  ld (hl), 3

  ld hl, $7f00
  ld de, bank3_pattern
  ld bc, 16
  call hram.memcmp

  ld a, 1
  ld (ROMB), a

  jp c, fail_round2

  pop hl
++
  ld a, h
  or l
  dec hl
  jr nz, --

  quit_ok

bank1_pattern:
  gen_bank1_pattern

bank3_pattern:
  gen_bank3_pattern

fail_round2:
  quit_inline
  call print_newline
  print_string_literal "R2: Test failed"
  call print_newline
  ldh a, (<hram.test_address_h)
  call print_hex8
  ldh a, (<hram.test_address_l)
  call print_hex8

  ld d, $42
  ret

.bank 1 slot 1
.org $3f00
  gen_bank1_pattern

.bank 3 slot 1
.org $3f00
  gen_bank3_pattern

.ramsection "Test-HRAM" slot HRAM_SLOT
  hram.test_address .dw
  hram.test_address_l db
  hram.test_address_h db
  hram.memcmp dsb 32
.ends

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

; Tests that BANK2 is mapped to correct addresses and has the right initial
; value.

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC1B1 chip
; and support for configuring ROM/RAM sizes.

.define CART_TYPE $03 ; MBC1, ram, battery
.define CART_RAM_SIZE 3

.include "common.s"

  ld sp, DEFAULT_SP

test_round1:
  ld a, $01
  ld (MODE), a
  ld a, $0a
  ld (RAMG), a

  ld hl, $a000
  ld de, bank0_pattern
  ld bc, 16
  call memcpy

  ld a, 1
  ld (BANK2), a

  ld hl, $a000
  ld de, bank1_pattern
  ld bc, 16
  call memcpy

  ld a, 2
  ld (BANK2), a

  ld hl, $a000
  ld de, bank2_pattern
  ld bc, 16
  call memcpy

  ld a, 3
  ld (BANK2), a

  ld hl, $a000
  ld de, bank3_pattern
  ld bc, 16
  call memcpy

  xor a
  ld (BANK2), a

  ld hl, $a000
  ld de, bank0_pattern
  ld bc, 16
  call memcmp

  jr z, test_round2
  quit_failure_string "R1: initial BANK2"

test_round2:
  ld hl, $5fff

- ld a, l
  ldh (<hram.test_address_l), a
  ld a, h
  ldh (<hram.test_address_h), a
  push hl

  ld (hl), 3

  ld hl, $a000
  ld de, bank3_pattern
  ld bc, 16
  call memcmp

  jp c, fail_round2

  pop hl
  dec hl
  ld a, h
  cp $3f
  jr nz, -

  quit_ok

bank0_pattern:
  .db $bd, $7f, $05, $2e, $21, $c7, $a6, $88
  .db $0e, $da, $05, $3a, $82, $19, $73, $71

bank1_pattern:
  .db $81, $dc, $07, $35, $9c, $4f, $48, $11
  .db $34, $f9, $47, $5e, $8a, $53, $80, $a1

bank2_pattern:
  .db $d7, $8d, $55, $7b, $b8, $d3, $81, $70
  .db $ec, $d6, $23, $6a, $84, $87, $7b, $49

bank3_pattern:
  .db $6e, $16, $1a, $58, $79, $0b, $19, $75
  .db $e2, $14, $2b, $3f, $4e, $37, $c4, $e4

fail_round2:
  call clear_ram
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

clear_ram:
  ld a, $0A
  ld (RAMG), a
  ld a, $01
  ld (MODE), a

  ld e, 4

- ld a, e
  ld (BANK2), a
  ld hl, $A000
  ld bc, $2000
  xor a
  call memset
  dec e
  jr nz, -

  xor a
  ld (RAMG), a

  ret

.ramsection "Test-HRAM" slot HRAM_SLOT
  hram.test_address .dw
  hram.test_address_l db
  hram.test_address_h db
.ends

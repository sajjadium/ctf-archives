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

; Tests that MODE is mapped to correct addresses and has the right initial
; value.

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC1B1 chip
; and support for configuring ROM/RAM sizes.

.define CART_TYPE $03 ; MBC1, ram, battery
.define CART_RAM_SIZE 3

.include "common.s"

  ld sp, DEFAULT_SP

test_round1:
  ld a, $0a
  ld (RAMG), a

  call copy_patterns

  xor a
  ld (BANK2), a
  ld a, 1
  ld (MODE), a

  ld hl, $a000
  ld de, bank3_pattern
  ld bc, 16
  call memcmp

  jr z, test_round2
  quit_failure_string "R1: initial MODE"

test_round2:
  call copy_patterns

  xor a
  ld (MODE), a

  ld hl, $7fff

- ld a, l
  ldh (<hram.test_address_l), a
  ld a, h
  ldh (<hram.test_address_h), a
  push hl

  ld (hl), 1

  ld hl, $a000
  ld de, bank3_pattern
  ld bc, 16
  call memcmp

  ld a, 0
  ld (MODE), a

  jp c, fail_round2

  pop hl
  dec hl
  ld a, h
  cp $5f
  jr nz, -

  quit_ok

copy_patterns:
  xor a
  ld (BANK2), a

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
  jp memcpy

bank0_pattern:
  .db $3b, $bd, $28, $75, $3e, $0a, $8e, $c4
  .db $26, $8c, $72, $80, $66, $bb, $86, $6f

bank1_pattern:
  .db $86, $3a, $5c, $b6, $96, $d8, $0e, $da
  .db $e9, $ad, $41, $f2, $df, $bd, $07, $41

bank2_pattern:
  .db $ee, $e1, $ea, $97, $10, $53, $4b, $b7
  .db $61, $64, $dd, $b6, $8c, $9c, $25, $3f

bank3_pattern:
  .db $4e, $d4, $da, $48, $5e, $3f, $fb, $3f
  .db $b9, $87, $71, $f9, $3b, $b7, $0b, $6e

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

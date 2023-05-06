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

; Tests RAM behaviour of an MBC2 cart
; Expected behaviour:
;   * RAM is disabled initially
;   * When RAM is disabled, writes have no effect
;   * There's only 512 RAM addresses, so they wrap around
;   * There's no "RAM bank register" at $4000
;   * Upper 4 bits of RAM data don't exist in the hardware

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC2A chip
; and support for configuring ROM/RAM sizes.

.define CART_TYPE $06 ; MBC2, ram, battery

.seed 661680
.include "common.s"

  ld sp, DEFAULT_SP

  ld hl, hram.ramcmp
  ld de, ramcmp
  ld bc, _sizeof_ramcmp
  call memcpy

test_round1:
  ld hl, all_ff
  ld de, $a000
  ld bc, 16
  call hram.ramcmp

  jp c, fail_round1

  ld hl, all_ff
  ld de, $b000
  ld bc, 16
  call hram.ramcmp

  jp c, fail_round1

; Let's clear the RAM, write to it while it's disabled, and check that the
; writes didn't have an effect
test_round2:
  call clear_ram
  call copy_test_pattern

  ld a, $0a
  ld (RAMG), a

  call check_test_pattern

  jp nc, fail_round2

; Now, if we copy data to the RAM, we should see the same data
test_round3:
  call copy_test_pattern
  call check_test_pattern
  jp c, fail_round3

; Writing to $4000 should have no effect since there's no RAM banking
test_round4:
  ld a, $01
  ld ($4000), a

  call check_test_pattern
  jp c, fail_round4

; RAM should wrap around so we should see the pattern repeated
test_round5:
  call check_test_pattern ; $A000 - $A1FF
  jp c, fail_round5
  ; $A200-$BFFF in $200 chunks
  .repeat 15
    ld hl, test_pattern
    ld bc, _sizeof_test_pattern
    call hram.ramcmp
    jp c, fail_round5
  .endr

; Upper 4 bits are undefined
test_round6:
  ld hl, hram.memcmp
  ld de, memcmp
  ld bc, _sizeof_memcmp
  call memcpy

  ld hl, wram.test_pattern
  ld de, test_pattern
  ld bc, _sizeof_test_pattern
  call memcpy

  ld bc, 512
  ld hl, wram.test_pattern
- ld a, (hl)
  or %11110000
  ld (hl+), a
  dec bc
  ld a, c
  or b
  jr nz, -

  ld hl, wram.test_pattern
  ld de, $a000
  ld bc, _sizeof_test_pattern
  call hram.memcmp

  jp c, fail_round6

test_finish:
  call clear_ram
  quit_ok

; Inputs:
;   HL source 1
;   DE source 2
;   BC length
; Outputs:
;   cf 0 if both were equal, 1 otherwise
; Preserved: -
ramcmp:
- ld a, b
  or c
  ret z

  push de
  ld a, (de)
  and %00001111
  ld e, a
  ld a, (hl+)
  and %00001111
  cp e
  pop de
  jr nz, +

  inc de
  dec bc
  jr -

+ scf
  ret

all_ff:
  .dsb 512, $ff

test_pattern:
  .dbrnd 512, $00, $ff

copy_test_pattern:
  ld hl, $a000
  ld de, test_pattern
  ld bc, _sizeof_test_pattern
  jp memcpy

check_test_pattern:
  ld hl, test_pattern
  ld de, $a000
  ld bc, _sizeof_test_pattern
  jp hram.ramcmp

clear_ram:
  ld a, $0a
  ld (RAMG), a

  ld hl, $a000
  ld bc, 512
  xor a
  call memset

  xor a
  ld (RAMG), a

  ret

fail_round1:
  call clear_ram
  quit_failure_string "FAIL: Round 1"

fail_round2:
  call clear_ram
  quit_failure_string "FAIL: Round 2"

fail_round3:
  call clear_ram
  quit_failure_string "FAIL: Round 3"

fail_round4:
  call clear_ram
  quit_failure_string "FAIL: Round 4"

fail_round5:
  call clear_ram
  quit_failure_string "FAIL: Round 5"

fail_round6:
  call clear_ram
  quit_failure_string "FAIL: Round 6"

.ramsection "Test-WRAM" slot WRAM0_SLOT
  wram.test_pattern dsb 512
.ends

.ramsection "Test-HRAM" slot HRAM_SLOT
  hram.ramcmp dsb 32
  hram.memcmp dsb 32
.ends

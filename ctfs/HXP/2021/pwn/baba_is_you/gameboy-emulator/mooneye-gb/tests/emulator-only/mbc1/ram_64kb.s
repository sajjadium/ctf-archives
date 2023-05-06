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

; Tests banking behaviour of a MBC1 cart with a 64 kbit RAM
; Expected behaviour:
;   * RAM is disabled initially
;   * When RAM is disabled, writes have no effect
;   * Since we have only one 8 kB bank, we always access it regardless of what
;      we do with $4000 and $6000

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC1B1 chip
; and support for configuring ROM/RAM sizes.

.define CART_TYPE $03 ; MBC1, ram, battery
.define CART_ROM_BANKS 4
.define CART_RAM_SIZE 2

.include "common.s"

  ld sp, DEFAULT_SP

  ld hl, memcmp_hram
  ld de, memcmp
  ld bc, _sizeof_memcmp
  call memcpy

; Initially the RAM should be disabled
test_round1:
  ld hl, all_ff
  ld de, $A000
  ld bc, 16
  call memcmp_hram

  jp c, fail_round1

  ld hl, all_ff
  ld de, $B000
  ld bc, 16
  call memcmp_hram

  jp c, fail_round1

; Let's clear the RAM, write to it while it's disabled, and check that the
; writes didn't have an effect
test_round2:
  call clear_ram

.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld ($4000), a
  call copy_bank_data
.endr

  ld a, $0A
  ld ($0000), a

.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld ($4000), a
  call check_bank_data
  jp nc, fail_round2
.endr

; Now, if we copy data to the RAM, we should see the same data
test_round3:
  call copy_bank_data
  call check_bank_data
  jp c, fail_round3

; Switching RAM banks shouldn't have an effect because we only have one bank in mode 1
test_round4:
  xor a
  ld ($6000), a

.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld ($4000), a
  call check_bank_data
  jp c, fail_round4
.endr

; Same thing in mode 1
test_round5:
  ld a, $01
  ld ($6000), a

.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld ($4000), a
  call check_bank_data
  jp c, fail_round5
.endr

test_finish:
  call clear_ram
  quit_ok

copy_bank_data:
  ld de, bank_data
  ld hl, $A000
  ld bc, 16
  call memcpy

  ld de, bank_data
  ld hl, $B000
  ld bc, 16
  jp memcpy

check_bank_data:
  ld de, bank_data
  ld hl, $A000
  ld bc, 16
  call memcmp_hram

  ret c

  ld de, bank_data
  ld hl, $B000
  ld bc, 16
  jp memcmp_hram

all_ff:
.dsb 16 $FF

all_00:
.dsb 16 $00

.org $1000
bank_data:
.db $19 $9D $91 $12 $F6 $12 $64 $4D $E4 $34 $3B $2E $FB $C7 $1F $3F

clear_ram:
  ld a, $0A
  ld ($0000), a
  ld a, $01
  ld ($6000), a

  ld e, 4

- ld a, e
  ld ($4000), a
  ld hl, $A000
  ld bc, $2000
  xor a
  call memset
  dec e
  jr nz, -

  xor a
  ld ($0000), a

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

.ramsection "Test-State" slot HRAM_SLOT
  memcmp_hram dsb 32
.ends

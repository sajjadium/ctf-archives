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

; Tests banking behaviour of a MBC1 cart with a 256 kbit RAM
; Expected behaviour:
;   * RAM is disabled initially
;   * When RAM is disabled, writes have no effect
;   * In mode 0 everything accesses bank 0
;   * In mode 1 access is done based on $4000 bank number
;   * If we switch back from mode 1, we once again access bank 0

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC1B1 chip
; and support for configuring ROM/RAM sizes.

.define CART_TYPE $03 ; MBC1, ram, battery
.define CART_ROM_BANKS 4
.define CART_RAM_SIZE 3

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
  ld (BANK2), a
  ld a, bank
  call copy_bank_data
.endr

  ld a, $0A
  ld (RAMG), a

.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld (BANK2), a
  ld a, bank
  call check_bank_data
  jp nc, fail_round2
.endr

; Now, mode is 0 so if we switch banks and copy data to RAM, we are actually writing to bank 0
test_round3:
  xor a
  ld ($6000), a

.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld (BANK2), a
  ld a, bank
  call copy_bank_data
.endr

; All "banks" should show the last written data because of mode 0
.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld (BANK2), a
  ld a, 3
  call check_bank_data
  jp c, fail_round3
.endr

; Now, if we enable mode 1, none of the previously inaccessible banks should have the data
test_round4:
  ld a, $01
  ld (MODE), a

.repeat 3 INDEX bank
  ld a, (bank + 1) | %11111100 ; set high bits to expose bugs
  ld (BANK2), a

  ld hl, all_00
  ld de, $A000
  ld bc, 16
  call memcmp_hram

  jp c, fail_round4

  ld hl, all_00
  ld de, $B000
  ld bc, 16
  call memcmp_hram

  jp c, fail_round4
.endr

; Let's actually write to all of the banks
test_round5:
.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld (BANK2), a
  ld a, bank
  call copy_bank_data
.endr

; All "banks" should show the last written data because of mode 0
.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld (BANK2), a
  ld a, bank
  call check_bank_data
  jp c, fail_round5
.endr

; And if we set mode 0, we should be back to bank 0
test_round6:
  xor a
  ld (MODE), a

.repeat 4 INDEX bank
  ld a, bank | %11111100 ; set high bits to expose bugs
  ld (BANK2), a
  xor a
  call check_bank_data
  jp c, fail_round6
.endr

test_finish:
  call clear_ram
  quit_ok

; Inputs:
;   A bank number
copy_bank_data:
  sla a
  sla a
  sla a
  sla a
  ld d, >bank_data
  ld e, a
  push de

  ld hl, $A000
  ld bc, 16
  call memcpy

  ld hl, $B000
  ld bc, 16
  pop de
  jp memcpy

; Inputs:
;   A bank number to compare to
check_bank_data:
  sla a
  sla a
  sla a
  sla a
  ld d, >bank_data
  ld e, a
  push de

  ld hl, $A000
  ld bc, 16
  call memcmp_hram

  pop de
  ret c

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
.db $00 $82 $20 $C7 $DD $05 $DE $D3 $73 $D9 $50 $82 $52 $B9 $A8 $E7
.db $66 $5C $6A $13 $F0 $E8 $5F $A9 $B9 $56 $AE $9B $1E $48 $4A $4C
.db $E5 $60 $1A $2B $D0 $FA $99 $54 $56 $6A $AE $AE $30 $E7 $C9 $07

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

.ramsection "Test-State" slot HRAM_SLOT
  memcmp_hram dsb 32
.ends

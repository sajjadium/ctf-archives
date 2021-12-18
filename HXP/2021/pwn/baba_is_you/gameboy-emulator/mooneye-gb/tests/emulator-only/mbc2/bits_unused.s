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

; Tests that writes to $4000-$7FFF have no effect.

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC2A chip
; and support for configuring ROM/RAM sizes.

.define CART_TYPE $06 ; MBC2, ram, battery
.define CART_ROM_BANKS 16

.seed 672873
.include "common.s"

  ld sp, DEFAULT_SP

  ; Enable ram
  ld a, $0a
  ld (RAMG), a

  ; Copy RAM data
  ld hl, $a000
  ld bc, _sizeof_ram_test_pattern
  ld de, ram_test_pattern
  call memcpy

  ld a, $01
  ld (ROMB), a

test_round1
  ld hl, $7fff

--
  ld a, l
  ldh (<hram.test_address_l), a
  ld a, h
  ldh (<hram.test_address_h), a
  push hl

  ld (hl), $00
  call check_patterns

  pop hl
  push hl

  ld (hl), $ff
  call check_patterns

  pop hl
  dec hl
  ld a, h
  cp $3f
  jr nz, --

  quit_ok

ram_test_pattern:
  .dbrnd 16, $f0, $ff

check_patterns:
  ld hl, $a000
  ld bc, _sizeof_ram_test_pattern
  call memcmp
  jr nc, fail_round1

  ld hl, rom_test_pattern
  ld bc, _sizeof_rom_test_pattern
  call memcmp
  jr nc, fail_round1

  ret

fail_round1:
  quit_inline
  call print_newline
  print_string_literal "R1: Test failed"
  call print_newline
  ldh a, (<hram.test_address_h)
  call print_hex8
  ldh a, (<hram.test_address_l)
  call print_hex8

  ld d, $42
  ret

.bank 1 slot 1
rom_test_pattern:
  .dbrnd 16, $f0, $ff
_end_rom_test_pattern:

.ramsection "Test-HRAM" slot HRAM_SLOT
  hram.test_address .dw
  hram.test_address_l db
  hram.test_address_h db
.ends

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

; JP cc, nn is expected to have the following timing:
; M = 0: instruction decoding
; M = 1: nn read: memory access for low byte
; M = 2: nn read: memory access for high byte
; M = 3: internal delay

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  di

  wait_vblank
  ; copy rest of wram_test to VRAM
  ld hl, VRAM
  ld de, (wram_test + 2)
  ld bc, $10
  call memcpy

  ; also copy wram_test to OAM
  ld hl, OAM - 2
  ld de, wram_test
  ld bc, $10
  call memcpy

  run_hiram_test

test_finish:
  quit_ok

; test procedure which will be copied to WRAM/OAM
; the first two bytes of JP cc, nn will be at $FDFE, so
; the high byte of nn is at the first byte of OAM during testing
wram_test:
  jp c, $1a00

fail_round1:
  quit_failure_string "FAIL: ROUND 1"

fail_round2:
  quit_failure_string "FAIL: ROUND 2"

; $1F80 - $1FE0 will be copied to $FF80 - $FFE0
.org $1f80
hiram_test:
  ; set low byte of nn to $ca
  ld a, $ca
  ld (OAM - 1), a

  ld b, 38
  start_oam_dma $80
- dec b
  jr nz, -
  nops 2
  ld hl, OAM - 2
  scf
  jp hl
  ; the memory read of nn is aligned to happen exactly one cycle
  ; before the OAM DMA end, so high byte of nn = $FF
  ; therefore the call becomes:
  ;   jp c, $ffca

test_round2:
  ; set low byte of nn to $da
  ld a, $da
  ld (OAM - 1), a

  ld b, 38
  start_oam_dma $80
- dec b
  jr nz, -
  nops 3
  ld hl, OAM - 2
  scf
  jp hl
  ; the memory read of nn is aligned to happen exactly after OAM DMA
  ; ends, so high byte of nn = $1a
  ; therefore the call becomes:
  ;   jp c, $1ada

; this will be copied to $FFCA
.org $1fca
finish_round1:
  nops 2
  jp $FF80 + (test_round2 - hiram_test)

; this will be copied to $FFDA
.org $1fda
  jp fail_round2

.org $1aca
  jp fail_round1

.org $1ada
finish_round2:
  nops 2
  jp test_finish

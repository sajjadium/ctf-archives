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

; RET is expected to have the following timing:
; M = 0: instruction decoding
; M = 1: PC pop: memory access for low byte
; M = 2: PC pop: memory access for high byte
; M = 3: internal delay

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ; Copy $FF80 callback
  ld hl, $FF80
  ld de, hiram_cb
  ld bc, $02
  call memcpy

test_round1:
  wait_vblank
  ld hl, OAM - 1
  ld a, $80
  ld (hl), a

  ld hl, VRAM
  ld a, $20
  ld (hl), a

  ld SP, OAM-1
  ld hl, finish_round1

  ld b, 39
  start_oam_dma $80  
- dec b
  jr nz, -
  nops 3

  ret

finish_round1:
  or a
  jr z, test_round2

  quit_failure_string "FAIL: ROUND 1"

test_round2:
  wait_vblank
  ld hl, OAM
  ld a, $FF
  ld (hl), a

  ld SP, OAM-1
  ld hl, finish_round2

  ld b, 39
  start_oam_dma $80
- dec b
  jr nz, -
  nops 4

  ret

finish_round2:
  or a
  jr nz, test_success

  quit_failure_string "FAIL: ROUND 2"

test_success:
  quit_ok

hiram_cb:
  xor a
  jp hl

.org $2080
  ld a, $01
  jp hl

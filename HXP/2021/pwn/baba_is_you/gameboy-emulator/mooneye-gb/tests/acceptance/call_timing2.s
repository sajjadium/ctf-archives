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

; CALL nn is expected to have the following timing:
; M = 0: instruction decoding
; M = 1: nn read: memory access for low byte
; M = 2: nn read: memory access for high byte
; M = 3: internal delay
; M = 4: PC push: memory access for high byte
; M = 5: PC push: memory access for low byte

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  di

  ; set first $20 bytes of VRAM to $81, so we
  ; have a known value when reading results
  wait_vblank
  ld hl, VRAM
  ld bc, $20
  ld a, $81
  call memset

  run_hiram_test

test_finish:
  setup_assertions
  assert_b $81
  assert_c $81
  assert_d $81
  assert_e $B9
  assert_h $FF
  assert_l $D6
  quit_check_asserts

hiram_test:
  ld sp, OAM+$20
  start_oam_dma $80
  ld a, 38
- dec a
  jr nz, -
  nops 2
  call $FF80 + (finish_round1 - hiram_test)
  ; OAM is accessible at M=6, so we expect to see
  ; incorrect low and high bytes (= $81 written by OAM DMA)

finish_round1:
  pop bc

  start_oam_dma $80
  ld a, 38
- dec a
  jr nz, -
  nops 3
  call $FF80 + (finish_round2 - hiram_test)
  ; OAM is accessible at M=5, so we expect to see
  ; incorrect (= $81 written by OAM DMA) high byte, but correct low byte

finish_round2:
  pop de

  start_oam_dma $80
  ld a, 38
- dec a
  jr nz, -
  nops 4
  call $FF80 + (finish_round3 - hiram_test)
  ; OAM is accessible at M=4, so we expect to see
  ; correct high byte and low byte

finish_round3:
  pop hl

  jp test_finish

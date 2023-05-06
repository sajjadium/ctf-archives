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

; LD HL, SP+e is expected to have the following timing:
; M = 0: instruction decoding
; M = 1: memory access for e
; M = 2: internal delay

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  di

  wait_vblank
  ; copy rest of wram_test to VRAM
  ld hl, VRAM
  ld de, (wram_test + 1)
  ld bc, $10
  call memcpy

  ; also copy wram_test to OAM
  ld hl, OAM - 1
  ld de, wram_test
  ld bc, $10
  call memcpy

  ld sp, $CFFF

  run_hiram_test

test_finish:
  setup_assertions
  assert_b $CF
  assert_c $FE
  assert_d $D0
  assert_e $3F
  quit_check_asserts

; test procedure which will be copied to WRAM/OAM
; the first byte of LD HL, SP+e will be at $FDFF, so
; the e parameter is at the first byte of OAM during testing
wram_test:
  ; if OAM DMA is still running $42 will be replaced with $FF
  ld hl, SP+$42
  ; save result to temporary storage
  push hl
  ; set HL = DE
  push de
  pop hl
  jp hl

hiram_test:
  ld b, 38
  start_oam_dma $80
- dec b
  jr nz, -
  nops 1
  ; set hl to address of finish_round1 in hiram
  ld de, $FF80 + (finish_round1 - hiram_test)
  ld hl, OAM - 1
  jp hl
  ; the memory read of LD HL, SP+e is aligned to happen exactly one cycle
  ; before the OAM DMA end, so e = $FF = -1

finish_round1:
  ld b, 38
  start_oam_dma $80
- dec b
  jr nz, -
  nops 2
  ; set hl to address of finish_round2 in hiram
  ld de, $FF80 + (finish_round2 - hiram_test)
  ld hl, OAM - 1
  jp hl
  ; the memory read of LD HL, SP+e is aligned to happen exactly one cycle
  ; before the OAM DMA end, so e = $42 = 42

finish_round2:
  pop de
  pop bc
  jp test_finish

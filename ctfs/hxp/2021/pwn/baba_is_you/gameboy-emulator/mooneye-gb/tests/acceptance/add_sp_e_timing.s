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

; ADD SP, e is expected to have the following timing:
; M = 0: instruction decoding
; M = 1: memory access for e
; M = 2: internal delay
; M = 3: internal delay

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  wait_vblank

  ; also first byte of wram_test to OAM
  ld a, (wram_test)
  ld (OAM - 1), a
  ; copy rest of wram_test to VRAM
  ld hl, VRAM
  ld de, (wram_test + 1)
  ld bc, $10
  call memcpy

  ld sp, $FFFE
  run_hiram_test

test_finish:
  setup_assertions
  ; Round 1 result
  assert_b $FF
  assert_c $FD
  ; Round 2 result
  assert_d $00
  assert_e $40
  quit_check_asserts

; test procedure which will be copied to WRAM/OAM
; the first byte of ADD SP, e will be at $FDFF, so
; the e parameter is at the first byte of OAM during testing
wram_test:
  ; if OAM DMA is still running $42 will be replaced with $FF
  add sp, $42
  ; save result to temporary storage
  ld hl, sp+$00
  ld a, h
  ld (result_tmp), a
  ld a, l
  ld (result_tmp+1), a
  ; set HL = DE
  ld h, d
  ld l, e
  jp hl

hiram_test:

; the memory read of ADD SP, e is aligned to happen exactly one cycle
; before the OAM DMA end, so e = $FF = -1
; So, we should actually execute the instruction ADD SP, -1
; and as a result SP = $FFFE - 1 = $FFFD
test_round1:
  ld b, 38
  start_oam_dma $80
- dec b
  jr nz, -
  nops 1
  ; set DE to address of finish_round1 in hiram
  ld de, $FF80 + (finish_round1 - hiram_test)
  ld hl, OAM - 1
  jp hl

finish_round1:
  ld a, (result_tmp)
  ld (result_round1), a
  ld a, (result_tmp + 1)
  ld (result_round1 + 1), a

  ld sp, $FFFE

; the memory read of ADD SP, e is aligned to happen exactly when the
; OAM DMA ends, so e = $42 = $42
; So, we should see execution of instruction ADD SP, $42
; and as a result SP = $FFFE + $42 = $0040
test_round2:
  ld b, 38
  start_oam_dma $80
- dec b
  jr nz, -
  nops 2
  ; set hl to address of finish_round2 in hiram
  ld de, $FF80 + (finish_round2 - hiram_test)
  ld hl, OAM - 1
  jp hl

finish_round2:
  ; Round 1 result -> BC
  ld a, (result_round1)
  ld b, a
  ld a, (result_round1 + 1)
  ld c, a

  ; Round 2 result -> DE
  ld a, (result_tmp)
  ld d, a
  ld a, (result_tmp + 1)
  ld e, a

  jp test_finish

.ramsection "Test-State" slot HRAM_SLOT
  result_tmp dw
  result_round1 dw
.ends

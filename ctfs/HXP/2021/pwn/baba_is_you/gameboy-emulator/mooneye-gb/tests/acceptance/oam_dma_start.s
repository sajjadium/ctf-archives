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

; This tests what happens in the first few cycles of OAM DMA.
; Also, when OAM DMA is restarted while a previous one is running, the previous one
; is not immediately stopped.

; Expected timing (fresh DMA):
; M = 0: write to $FF46 happens
; M = 1: nothing (OAM still accessible)
; M = 2: new DMA starts, OAM reads will return $FF

; Expected timing (restarted DMA):
; M = 0: write to $FF46 happens. Previous DMA is running (OAM *not* accessible)
; M = 1: previous DMA is running (OAM *not* accessible)
; M = 2: new DMA starts, OAM reads will return $FF

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

.macro wait_dma_finish
  ld a, 40
- dec a
  jr nz, -
.endm

  di
  call disable_lcd_safe

  ld hl, VRAM
  ld bc, OAM_LEN
  ld a, $D7   ; RST $10
  call memset

test_round1:
  ld hl, vector_10
  ld a, <fail_round1
  ld (hl-), a
  ld a, >fail_round1

  ld hl, vector_38
  ld a, <finish_round1
  ld (hl+), a
  ld a, >finish_round1
  ld (hl+), a

  ld hl, OAM
  ld bc, $A0
  ld a, $04   ; INC B
  call memset

  ld hl, OAM - 1
  ld a, $77   ; LD (HL), A
  ld (hl), a

  enable_lcd
  wait_vblank

  ld b, $00
  ld a, $80
  ld hl, DMA

  ; This is what we end up executing
  ; $FDFF: LD (HL), A
  ; $FE00: INC B
  ; $FE01: INC B <-- this will be replaced by RST $38
  jp OAM - 1

fail_round1:
  quit_failure_string "FAIL: ROUND 1 RST $10"

finish_round1:
  ld a, (OAM)
  ld (round1_oam), a
  ld a, b
  ld (round1_b), a
  ld sp, $FFFE

test_round2:
  call disable_lcd_safe

  ld hl, vector_10
  ld a, <fail_round2
  ld (hl-), a
  ld a, >fail_round2

  ld hl, vector_38
  ld a, <finish_round2
  ld (hl+), a
  ld a, >finish_round2
  ld (hl+), a

  ld hl, OAM
  ld bc, OAM_LEN
  ld a, $04   ; INC B
  call memset

  ld hl, OAM - 2
  ld a, $77   ; LD (HL), A
  ld (hl+), a
  ld a, $77   ; LD (HL), A
  ld (hl), a

  enable_lcd
  wait_vblank

  ld b, $00
  ld a, $80
  ld hl, DMA

  ; This is what we end up executing
  ; $FDFE: LD (HL), A
  ; $FDFF: LD (HL), A
  ; $FE00: INC B <-- this will be replaced by RST $38
  jp OAM - 2

fail_round2:
  quit_failure_string "FAIL: ROUND 2 RST $10"

finish_round2:
  ld a, (OAM)
  ld d, a
  ld e, b

test_finish:
  ld a, (round1_oam)
  ld b, a
  ld a, (round1_b)  
  ld c, a
  setup_assertions
  assert_b $D7
  assert_c $01
  assert_d $D7
  assert_e $00
  quit_check_asserts

.org $10
  wait_dma_finish
  ld hl, vector_10
  ld a, (hl+)
  ld e, a
  ld a, (hl+)
  ld h, a
  ld l, e
  jp hl

.org $38
  wait_dma_finish
  ld hl, vector_38
  ld a, (hl+)
  ld e, a
  ld a, (hl+)
  ld h, a
  ld l, e
  jp hl

.ramsection "Test-State" slot HRAM_SLOT
  vector_10 dw
  vector_38 dw
  round1_oam db
  round1_b db
.ends

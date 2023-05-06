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

; This tests how the internal STAT IRQ signal can block
; subsequent STAT interrupts if the signal is never cleared

; Verified results:
;   pass: DMG ABC, MGB, CGB, AGB, AGS
;   fail: DMG 0

.include "common.s"

  ld sp, DEFAULT_SP

test_round1:
  ld b, $00
  ld hl, test_round2
  wait_vblank

  ld a, $10 ; enable mode=1 interrupt
  ldh (<STAT), a
  ei
  ld a, INTR_STAT
  ldh (<IE), a

  ; We are already in vblank, but an interrupt should occur
fail_round1:
  di
  quit_failure_string "FAIL: MODE=1 INTR"

  ; The STAT mode=1 interrupt should throw us here
test_round2:
  ld hl, fail_round2
  ei

  ld a, $78; enable all stat interrupts
  ldh (<STAT), a

  ; Now that all stat interrupts are enabled, the only mode
  ; that can clear the internal interrupt line is mode 3
  ; However, if we arrange things so that LY=LYC coincidence
  ; is set before mode 3 and kept set, the interrupt line is not cleared
  ld b, $00
ly_iteration:
  ld a, b
  cp $90 ; exit if LY>=144
  jr nc, finish_round2

  ldh (<LYC), a

  ; Wait until LY = b
  ; In practice we are in mode=2 when this happens
- ldh a, (<STAT)
  and $04
  jr z, -

  ; Wait until mode = 0
  ; At this point we have gone past mode=3
  ; while having LY=LYC
- ldh a, (<STAT)
  and $03
  jr nz, -

  inc b
  jr ly_iteration

finish_round2:
  di
  quit_ok

fail_round2:
  setup_assertions
  quit_failure_dump

.org INTR_VEC_STAT
  jp hl

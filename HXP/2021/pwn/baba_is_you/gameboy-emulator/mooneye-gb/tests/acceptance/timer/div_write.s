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

; This test verifies that the timer is affected by resetting the DIV register
; by writing to it. The timer uses the same internal counter as the DIV
; register, so resetting DIV also resets the timer.
; The basic idea of this test is very simple:
;   1. start the timer
;   2. keep resetting DIV in a loop by writing to it
;   3. run N iterations of the loop
;   4. if an interrupt happened, test failed

; Common reasons for failing this test:
;   "FAIL: INTR"
;     Your emulator does not use the internal counter for the timer, so DIV
;     resets did not prevent the timer increase and interrupt from happening

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

test:
  ld a, INTR_TIMER
  ldh (<IE), a
  xor a
  ldh (<IF), a
  ldh (<DIV), a
  ld a, $FF
  ldh (<TIMA), a
  ld a, %00000100 ; Start 4096 Hz timer
  ldh (<TAC), a

  ld bc, $FFFF ; loop counter

  ei

- xor a
  ldh (<DIV), a
  dec bc
  ld a, c
  or b
  jr nz, -

  di
  quit_ok

quit_failure:
  quit_failure_string "FAIL: INTR"

.org INTR_VEC_TIMER
  jp quit_failure

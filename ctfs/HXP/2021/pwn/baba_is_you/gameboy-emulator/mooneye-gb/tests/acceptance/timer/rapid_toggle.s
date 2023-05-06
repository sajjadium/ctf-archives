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

; This test rapidly starts and stops the timer.
; There are two behaviours that affect the test:
;   1. starting or stopping the timer does *not* reset its internal counter,
;      so repeated starting and stopping does not prevent timer increments
;   2. the timer circuit design causes some unexpected timer increases

; Common reasons for failing this test:
;   "FAIL: NO INTR"
;     Your emulator starts counting the timer when it is started or stopped.
;     This is incorrect, because in real hardware starting/stopping the timer
;     simply flips a single bit, and the timer state is otherwise preserved.
;   BC < $FFF8
;     Your emulator does not emulate the unexpected timer increases, so the
;     interrupt happens too late.

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
  ld a, $F0
  ldh (<TIMA), a
  ld a, %00000100 ; Start 4096 Hz timer
  ldh (<TAC), a

  ld bc, $FFFF

  ei

- ld a, %00000100 ; Start 4096 Hz timer
  ldh (<TAC), a
  ld a, %00000000 ; Stop timer
  ldh (<TAC), a
  dec bc
  ld a, c
  or b
  jr nz, -

  quit_failure_string "FAIL: NO INTR"

test_finish:
  setup_assertions
  assert_b $FF
  assert_c $D9
  quit_check_asserts

.org INTR_VEC_TIMER
  jp test_finish

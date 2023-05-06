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

; If IME=1, HALT is expected to immediately service an interrupt.
; So, if the interrupt service routine doesn't return,
; the instruction after HALT should never get executed

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ei

  ; B = 0
  xor a
  ld b, a

  ; Enable timer interrupt
  ld a, INTR_TIMER
  ldh (<IE), a

  ; TIMA = $F0
  ld a, $F0
  ldh (<TIMA), a

  ; Start timer at 262144 Hz
  ld a, $05
  ldh (<TAC), a

  halt
  ; This should never get executed
  inc b

  quit_failure

test_finish:
  setup_assertions
  assert_b $00
  quit_check_asserts

.org INTR_VEC_TIMER
  jp test_finish

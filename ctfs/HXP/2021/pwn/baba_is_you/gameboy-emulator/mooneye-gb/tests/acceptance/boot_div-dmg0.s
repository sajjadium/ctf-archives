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

; Tests the value and relative phase of DIV after boot

; Verified results:
;   pass: DMG 0
;   fail: DMG ABC, MGB, SGB, SGB2, CGB, AGB, AGS

.include "common.s"

  nops 45
  ; This read should happen immediately after DIV has incremented
  ldh a, (<DIV)
  push af

  ; With 57 NOPs here, the next read should happen immediately after the next
  ; increment. So, the relative phase between the read and the increment
  ; remains the same
  nops 57
  ldh a, (<DIV)
  push af

  ; This time we have only 56 NOPs, so the next read should happen immediately
  ; *before* the increment because we're altering the relative phase and
  ; reading one M-cycle earlier.
  nops 56
  ldh a, (<DIV)
  push af

  ; Since we're back to 57 NOPs, the next read should happen once again
  ; immediately *before* the increment. Phase is not changed here, but the change
  ; in the earlier step remains.
  nops 57
  ldh a, (<DIV)
  push af

  ; Same thing here...
  nops 57
  ldh a, (<DIV)
  push af

  ; This time we have 58 NOPs, which alters the phase and the read should
  ; happen after the increment once again.
  nops 58
  ldh a, (<DIV)
  push af

  pop af
  ld l, a
  pop af
  ld h, a
  pop af
  ld e, a
  pop af
  ld d, a
  pop af
  ld c, a
  pop af
  ld b, a
  setup_assertions
  assert_b $19
  assert_c $1a
  assert_d $1a
  assert_e $1b
  assert_h $1c
  assert_l $1e
  quit_check_asserts


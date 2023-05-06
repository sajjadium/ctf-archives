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

; This tests RETI instruction interrupt enable timing

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  di
  ld a, INTR_VBLANK | INTR_SERIAL
  ld (IF), a
  ld (IE), a
  xor a
  ld b, a
  ld d, a
  ld e, a

  ; We're expecting to see the effect of exactly one INC B instruction
  ; before we get the vblank interrupt (handler at $40)
  ei
  inc b
  ; Handler $40 is supposed to be executed here
  ; We expect not to see the second inc b, because RETI causes us to
  ; jump to handler $58
  inc b

test_finish:
  setup_assertions
  assert_b $01
  assert_d $01
  assert_e $01
  quit_check_asserts

.org INTR_VEC_VBLANK
  inc d
  reti

.org INTR_VEC_SERIAL
  inc e
  jp test_finish

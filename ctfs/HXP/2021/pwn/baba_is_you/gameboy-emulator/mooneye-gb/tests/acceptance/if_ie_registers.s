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

; This tests the behaviour of IE and IF flags by forcing a serial
; interrupt with a write to IF. The interrupt handler increments
; E, so we can track how many times the interrupt has been
; triggered

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ; Make sure IE, IF, and E are all $00
  di
  xor a
  ld (IF), a
  ld (IE), a
  ld e, a
  ei

  ; Write serial interrupt bit to IF and wait
  ; Since IE is $00, we are *not* expecting an
  ; interrupt
  ld hl, IF
  ld a, INTR_SERIAL
  ld (hl), a
  nops 64
  ld b, e
  ld a, (hl)
  ld c, a
  ; B contains counter E value
  ; C contains register IF value

  ; Write serial interrupt bit to IE and wait
  ; We already wrote it to IF, so now we expect
  ; one interrupt trigger
  ld hl, IE
  ld a, INTR_SERIAL
  ld (hl), a
  nops 64
  ld d, e
  ld hl, IF
  ld a, (hl)
  ld e, a
  ; D contains counter E value
  ; E contains register IF value

test_finish:
  setup_assertions
  assert_b $00
  assert_c $E8
  assert_d $01
  assert_e $E0
  quit_check_asserts

.org INTR_VEC_SERIAL
  inc e
  reti

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

; Tests when a serial transfer completes if one is started after boot.
; Expectations:
;   - the transfer doesn't start immediately
;   - serial clock is divided from the main clock with a big counter, so
;     clock edges align based on the *reset time*, not the time when SC is
;     written to

; Verified results:
;   pass: DMG ABC, MGB
;   fail: DMG 0, SGB, SGB2, CGB, AGB, AGS

.include "common.s"

  ld a, INTR_SERIAL
  ldh (<IE), a

  xor a
  ldh (<IF), a

  xor a
  ld b, a
  ld c, a
  ld d, a
  ld e, a
  ld h, a
  ld l, a

  ; We request a serial transfer here
  ld a, $81
  ldh (<SC), a

  ei

.repeat 2000
  inc a
  inc b
  inc c
  inc d
  inc e
  inc h
  inc l
.endr

  di
  quit_failure_string "No serial intr"

test_finish:
  setup_assertions
  assert_a $12
  assert_b $91
  assert_c $90
  assert_d $90
  assert_e $90
  assert_h $90
  assert_l $90
  quit_check_asserts

.org INTR_VEC_SERIAL
  jp test_finish

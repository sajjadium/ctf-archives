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

; POP rr is expected to have the following timing:
; M = 0: instruction decoding
; M = 1: memory access for low byte
; M = 2: memory access for high byte

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ld hl, DIV

.macro reset_div
  xor a
  ld (hl), a
.endm

  ; --- low byte tests

  ld sp, hl
  reset_div
  nops 61
  ; DIV increment happens at M = 2, so the low byte has already
  ; been popped and we should see $00
  pop bc
  ld d, c

  ld sp, DIV
  reset_div
  nops 62
  ; DIV increment happens at M = 1, so the low byte should be popped
  ; at the same time and we should see $01
  pop bc
  ld e, c

  ; Save the first two results to temporary storage
  ld sp, $CFFF
  push de

  ; --- high byte tests

  ld sp, DIV - 1
  reset_div
  nops 60
  ; DIV increment happens at M = 3, so the high byte has already
  ; been popped and we should see $00
  pop bc
  ld d, b

  ld sp, DIV - 1
  reset_div
  nops 61
  ; DIV increment happens at M = 2, so the high byte should be popped
  ; at the same time and we should see $01
  pop bc
  ld e, b

  ld sp, DIV - 1
  reset_div
  nops 62
  ; DIV increment happens at M = 1, so the high byte popping
  ; should see the increment and we should see $01
  pop af

  ; Restore old results from temporary storage
  ld sp, $CFFD
  pop bc

test_finish:
  setup_assertions
  assert_a $01
  assert_b $00
  assert_c $01
  assert_d $00
  assert_e $01
  quit_check_asserts

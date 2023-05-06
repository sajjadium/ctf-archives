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

; DIV increments are supposed to happen every 64 cycles,
; and the "internal counter" is supposed to reset when DIV is reset
;
; ld a, (hl) is expected to have the following timing:
; M = 0: instruction decoding
; M = 1: memory access from (HL)

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ld hl, DIV

.macro reset_div
  xor a
  ld (hl), a
.endm

  ; --- Test: increment is too late

  reset_div
  nops 61
  ; DIV increment should happen at M = 2, so the memory read
  ; should not see the increment, and we should get A = $00
  ld a, (hl)
  ld b, a

  ; --- Test: internal counter reset

  ; padding so if the internal counter is not reset, the next
  ; test should incorrectly see the increment
  nops 27

  ; repeat earlier test
  reset_div
  nops 61
  ; DIV increment should happen at M = 2, so the memory read
  ; should not see the increment, and we should get A = $00
  ld a, (hl)
  ld c, a

  ; --- Test: increment is exactly on time

  reset_div
  nops 62
  ; DIV increment should happen at M = 1, so the memory read
  ; should see the increment, and we should get A = $01
  ld a, (hl)
  ld d, a

test_finish:
  setup_assertions
  assert_b $00
  assert_c $00
  assert_d $01
  quit_check_asserts

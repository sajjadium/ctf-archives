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

; This test verifies that the timer count changes are actually triggered
; by bit 3 going low when writing to the DIV register in 262144 Hz mode.
;
; 8 cycles after resetting the internal div counter, bit 3 of the
; internal div counter will have been set. Writing to the DIV register
; at this time will cause bit 3 to change from high to low which in
; turn triggers a timer increment.
;
; Since the timer runs quite fast in this mode, this test is executed 
; by issueing several ldh (<DIV),a instructions. These instructions take
; 12 cycles and also trigger the mentioned behaviour.

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

test:
  di
  xor a
  ld b,4
  ldh (<IE), a
  ldh (<IF), a
  ldh (<DIV), a
  ld a, b
  ldh (<TIMA), a
  ldh (<TMA),a
  ld a, %00000101 ; Start 262144 Hz timer (16 cycles)
  ldh (<TAC), a
  ld a,b
  ldh (<DIV),a
  ldh (<TIMA), a
  ldh (<DIV),a
  ldh (<DIV),a
  ldh (<DIV),a
  ldh (<DIV),a
  ldh (<DIV),a
  ldh a,(<TIMA)
  ld d,a

  ld a,b
  ldh (<TIMA), a
  ldh (<DIV),a
  ldh (<TIMA), a
  ldh (<DIV),a
  ldh (<DIV),a
  ldh (<DIV),a
  ldh (<DIV),a
  ldh (<DIV),a
  nop
  ldh a,(<TIMA)
  ld e,a

  setup_assertions
  assert_d $0A
  assert_e $0B
  quit_check_asserts


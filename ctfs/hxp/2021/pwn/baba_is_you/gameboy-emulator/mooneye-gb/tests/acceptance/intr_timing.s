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

; Serving an interrupt is supposed to take 5 M-cycles.
; We know from div_timing that this code should not see a div increment:
;   reset_div
;     nops 61
;   ld a, (hl)
; On the other hand, this code should see the increment:
;   reset_div
;     nops 62
;   ld a, (hl)
; We set up a similar scenario by triggering an interrupt using IE/IF flags.
; In total we have
;   reset_div
;     x nops               x cycles
;     trigger_intr 2 + 3 = 5 cycles
;     interrupt handling:  5 cycles
;     jp hl                1 cycle
;   ld a, (bc)
; So, x=50 is equivalent to the nops 61 case,
; and x=51 is equivalent to the nops 62 case

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ld bc, DIV

  ld a, INTR_SERIAL
  ldh (<IE), a

.macro reset_div
  xor a
  ld (bc), a
.endm

.macro trigger_intr
  ld a, $08
  ldh (<IF), a
.endm

test_round1:
  ei
  ld hl, finish_round1

  reset_div
  nops 50
  trigger_intr

  ; never executed
  quit_failure_string "FAIL: ROUND 1"

finish_round1:
  ld a, (bc)
  ld d, a

test_round2:
  ei
  ld hl, finish_round2

  reset_div
  nops 51
  trigger_intr

  ; never executed
  quit_failure_string "FAIL: ROUND 2"

finish_round2:
  ld a, (bc)
  ld e, a

  jp test_finish

test_finish:
  setup_assertions
  assert_d $00
  assert_e $01
  quit_check_asserts

.org INTR_VEC_SERIAL
  jp hl

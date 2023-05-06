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

; This tests whether HALT adds any kind of delay in the IME=0 case
;
; HALT is expected to immediately continue execution, with exactly
; same timing as if a long series of NOP instructions were used to wait
; for the interrupt

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

.macro clear_IF
  xor a
  ldh (<IF), a
.endm

.macro enable_IE_vblank
  ld a, INTR_VBLANK
  ldh (<IE), a
.endm

  di
  wait_ly 10
  enable_IE_vblank

  clear_IF
  ld hl, test_round1

  ei
  halt
  nop
  jp fail_halt

test_round1:
  ld hl, fail_intr
  clear_IF

  nops 13
  xor a
  ldh (<DIV), a

  halt
  nops 6 ; Equivalent to interrupt + JP HL in the IME=1 case

finish_round1:
  ldh a, (<DIV)
  ld d, a

  clear_IF
  ld hl, test_round2

  ei
  halt
  nop
  jp fail_halt

test_round2:
  ld hl, fail_intr
  clear_IF

  nops 12
  xor a
  ldh (<DIV), a

  halt
  nops 6 ; Equivalent to interrupt + JP HL in the IME=1 case

finish_round2:
  ldh a, (<DIV)
  ld e, a
  setup_assertions
  assert_d $11
  assert_e $12
  quit_check_asserts

fail_halt:
  quit_failure_string "FAIL: HALT"

fail_intr:
  quit_failure_string "FAIL: INTERRUPT"

.org INTR_VEC_VBLANK
  jp hl

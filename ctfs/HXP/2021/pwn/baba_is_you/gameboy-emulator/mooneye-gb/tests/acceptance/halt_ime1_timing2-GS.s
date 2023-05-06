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

; This tests whether HALT adds any kind of delay in the IME=1 case
;
; HALT is expected to immediately service the interrupt, with exactly
; same timing as if a long series of NOP instructions were used to wait
; for the interrupt

; Verified results:
;   pass: DMG, MGB, SGB, SGB2
;   fail: CGB, AGB, AGS

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
  ld hl, finish_round1
  clear_IF
  ei

  nops 12
  xor a
  ldh (<DIV), a

  delay_long_time 2502
  nops 7

  di
  jp fail_round1

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
  ld hl, finish_round2
  clear_IF
  ei

  nops 11
  xor a
  ldh (<DIV), a

  delay_long_time 2502
  nops 8

  di
  jp fail_round2

finish_round2:
  ldh a, (<DIV)
  ld e, a

  clear_IF
  ld hl, test_round3

  ei
  halt
  nop
  jp fail_halt

test_round3:
  ld hl, finish_round3
  clear_IF
  ei

  nops 12
  xor a
  ldh (<DIV), a

  halt
  nop
  jp fail_round3

finish_round3:
  ldh a, (<DIV)
  ld b, a

  clear_IF
  ld hl, test_round4

  ei
  halt
  nop
  jp fail_halt

test_round4:
  ld hl, finish_round4
  clear_IF
  ei

  nops 11
  xor a
  ldh (<DIV), a

  halt
  nop
  jp fail_round4

finish_round4:
  ldh a, (<DIV)
  ld c, a
  setup_assertions
  assert_b $11
  assert_c $12
  assert_d $11
  assert_e $12
  quit_check_asserts

fail_halt:
  quit_failure_string "FAIL: HALT"

fail_round1:
  quit_failure_string "FAIL: ROUND 1"

fail_round2:
  quit_failure_string "FAIL: ROUND 2"

fail_round3:
  quit_failure_string "FAIL: ROUND 3"

fail_round4:
  quit_failure_string "FAIL: ROUND 4"

.org INTR_VEC_VBLANK
  jp hl

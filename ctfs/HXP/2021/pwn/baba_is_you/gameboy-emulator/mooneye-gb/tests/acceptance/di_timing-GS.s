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

; This tests DI instruction timing by setting up a vblank interrupt
; interrupt with a write to IE.
;
; This test is for DMG/MGB, so DI is expected to disable interrupts
; immediately
; On CGB/GBA DI has a delay and this test fails in round 2!!

.include "common.s"

; Verified results:
;   pass: DMG, MGB, SGB, SGB2
;   fail: CGB, AGB, AGS

  di
  ld a, INTR_VBLANK
  ldh (<IE), a

  ld hl, test_round1
  wait_vblank
  xor a
  ldh (<IF), a
  ei

  halt
  nop
  jp fail_halt

test_round1:
  ld hl, finish_round1
  ei

  delay_long_time 2505
  nops 6

  ; This DI should never get executed
  di
  jp fail_round1

finish_round1:
  ld hl, test_round2
  wait_vblank
  xor a
  ldh (<IF), a
  ei

  halt
  nop
  jp fail_halt

test_round2:
  ld hl, fail_round2
  ei

  delay_long_time 2505
  nops 5

  ; This time we let DI execute, because there is one less NOP
  di
  ; If DI doesn't have an immediate effect, we would get an interrupt here and
  ; fail the test.
  nop

test_finish:
  quit_ok

fail_halt:
  quit_failure_string "FAIL: HALT"

fail_round1:
  quit_failure_string "FAIL: ROUND 1"

fail_round2:
  quit_failure_string "FAIL: ROUND 2"

.org INTR_VEC_VBLANK
  jp hl

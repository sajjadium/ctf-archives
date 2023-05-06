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

; If bit 5 (mode 2 OAM interrupt) is set, an interrupt is also triggered
; at line 144 when vblank starts.
; This test measures the cycles between vblank<->vblank and compares that to vblank<->stat_m2_144
; Expected behaviour: vblank and stat_m2_144 are triggered at the same time

; Verified results:
;   pass: DMG, MGB, SGB, SGB2
;   fail: CGB, AGB, AGS

.include "common.s"

.macro halt_until ARGS intr
  xor a
  ldh (<IF), a
  ld a, intr
  ldh (<IE), a

  ei
  halt
  nop

  jp fail_halt
.endm

  ld sp, DEFAULT_SP

  ld hl, intr_vec_vblank
  ld a, $C3
  ld (hl+), a ; JP nnnn
  ld a, <test_round1
  ld (hl+), a
  ld a, >test_round1
  ld (hl), a

  halt_until INTR_VBLANK

fail_halt:
  quit_failure_string "HALT"

test_round1:
  ld hl, intr_vec_vblank
  ld a, $C3
  ld (hl+), a ; JP nnnn
  ld a, <finish_round1
  ld (hl+), a
  ld a, >finish_round1
  ld (hl), a

  wait_ly 143

  nops 54
  ldh (<DIV), a

  halt_until INTR_VBLANK

finish_round1:
  ldh a, (<DIV)
  ld (round1), a

  ld hl, intr_vec_vblank
  ld a, $C3
  ld (hl+), a ; JP nnnn
  ld a, <test_round2
  ld (hl+), a
  ld a, >test_round2
  ld (hl), a

  halt_until INTR_VBLANK

test_round2:
  ld hl, intr_vec_vblank
  ld a, $C3
  ld (hl+), a ; JP nnnn
  ld a, <finish_round2
  ld (hl+), a
  ld a, >finish_round2
  ld (hl), a

  wait_ly 143

  nops 55
  ldh (<DIV), a

  halt_until INTR_VBLANK

finish_round2:
  ldh a, (<DIV)
  ld (round2), a

  ld hl, intr_vec_vblank
  ld a, $C3
  ld (hl+), a ; JP nnnn
  ld a, <test_round3
  ld (hl+), a
  ld a, >test_round3
  ld (hl), a

  ld a, $20
  ldh (<STAT), a

  halt_until INTR_VBLANK

test_round3:
  ld hl, intr_vec_stat
  ld a, $C3
  ld (hl+), a ; JP nnnn
  ld a, <finish_round3
  ld (hl+), a
  ld a, >finish_round3
  ld (hl), a

  wait_ly 143

  nops 54
  ldh (<DIV), a

  halt_until INTR_STAT

finish_round3:
  ldh a, (<DIV)
  ld (round3), a

  ld hl, intr_vec_vblank
  ld a, $C3
  ld (hl+), a ; JP nnnn
  ld a, <test_round4
  ld (hl+), a
  ld a, >test_round4
  ld (hl), a

  halt_until INTR_VBLANK

test_round4:
  ld hl, intr_vec_stat
  ld a, $C3
  ld (hl+), a ; JP nnnn
  ld a, <finish_round4
  ld (hl+), a
  ld a, >finish_round4
  ld (hl), a

  wait_ly 143

  nops 55
  ldh (<DIV), a

  halt_until INTR_STAT

finish_round4:
  ldh a, (<DIV)

test_finish:
  ld e, a
  ld a, (round3)
  ld d, a
  ld a, (round2)
  ld c, a
  ld a, (round1)
  ld b, a

  setup_assertions
  assert_b $01
  assert_c $00
  assert_d $01
  assert_e $00
  quit_check_asserts

.org INTR_VEC_VBLANK
  jp intr_vec_vblank

.org INTR_VEC_STAT
  jp intr_vec_stat

.ramsection "Test-State" slot HRAM_SLOT
  intr_vec_vblank dsb 3
  intr_vec_stat dsb 3
  round1 db
  round2 db
  round3 db
.ends

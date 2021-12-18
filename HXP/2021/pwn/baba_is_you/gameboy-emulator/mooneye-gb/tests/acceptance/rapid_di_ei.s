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

; This tests how sequential DI/EI instructions work by forcing a serial
; interrupt with a write to IE/IF. The interrupt handler increments
; E, so we can track how many times the interrupt has been
; triggered

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

.macro reset
  ld a, INTR_SERIAL
  ld (IF), a
  ld (IE), a
  xor a
  ld e, a
.endm

  di
  reset

  ; Rapid EI/DI should *not* result in any interrupts
  ei
  di
  ei
  di
  ld b, e

  reset

  ; EI followed by DI should *not* result in any interrupts
  ei
  di
  nop
  nop
  ld c, e

  reset

  ; A nop after EI should cause an interrupt
  ei
  nop
  di
  ld d, e

  reset

  ; Two nops after EI should cause an interrupt
  ei
  nop
  nop
  di

test_finish:
  setup_assertions
  assert_b $00
  assert_c $00
  assert_d $01
  assert_e $01
  quit_check_asserts

.org INTR_VEC_SERIAL
  inc e
  reti

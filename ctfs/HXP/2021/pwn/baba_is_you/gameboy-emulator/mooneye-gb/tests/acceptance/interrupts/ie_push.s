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

; Tests what happens if the IE register is the target for one of the
; PC pushes during interrupt dispatch.

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ld sp, DEFAULT_SP

  call disable_lcd_safe

  jp round1

.org $0200
; Round 1: IE is written during upper byte push
; 
; The written value is $02, which clears the INTR_TIMER bit and cancels the
; interrupt dispatch. PC is set to $0000 instead of the normal jump address.
round1:
  ld hl, finish_round1
  xor a
  ldh (<IF), a

  ld a, INTR_TIMER
  ldh (<IE), a

  ei
  nop

  ld sp, $0000
  ldh (<IF), a

  jp fail_round1_nointr

finish_round1:
  ldh a, (<IF)
  and %11111
  cp INTR_TIMER
  jp nz, fail_round1_if

; Round 2: IME should be 0 after a cancellation
round2:
  ld a, INTR_JOYPAD
  ldh (<IE), a
  ldh (<IF), a

  nop

; Round 3: IE is written during lower byte push
;
; The written value is $35, which clears the INTR_SERIAL bit, but is too
; late to cancel the interrupt dispatch.
round3:
  ld hl, fail_round3_cancel
  xor a
  ldh (<IF), a

  ld a, INTR_SERIAL
  ldh (<IE), a

  ei
  nop

  ld sp, $0001
  ldh (<IF), a

target:
  jp fail_round3_nointr

finish_round3:
  ldh a, (<IF)
  and %11111
  jp nz, fail_round3_if

; Round 4: two interrupts, IE is written during upper byte push
;
; The written value is $02, which clears the INTR_VBLANK bit but keeps the
; INTR_STAT bit. The STAT interrupt is dispatched normally.
round4:
  ld hl, fail_round4_cancel
  xor a
  ldh (<IF), a

  ld a, INTR_STAT | INTR_VBLANK
  ldh (<IE), a

  ei
  nop

  ld sp, $0000
  ldh (<IF), a

  jp fail_round4_nointr

finish_round4:
  ldh a, (<IF)
  and %11111
  cp INTR_VBLANK
  jp nz, fail_round4_if

  quit_ok

.org $1000
; Round 1: interrupt dispatching didn't happen
fail_round1_nointr:
  ld sp, $fffe
  quit_failure_string "R1: no interrupt"

; Round 1: interrupt was dispatched normally, which is wrong here
fail_round1_nocancel:
  ld sp, $fffe
  quit_failure_string "R1: not cancelled"

; Round 1: cancellation worked, but IF was still modified
fail_round1_if:
  ld sp, $fffe
  quit_failure_string "R1: IF modified"

; Round 2: IME should be 0 after round 1, but an interrupt happened
fail_round2_intr:
  ld sp, $fffe
  quit_failure_string "R2: unwanted intr"

; Round 3: interrupt dispatching didn't happen
fail_round3_nointr:
  ld sp, $fffe
  quit_failure_string "R3: no interrupt"

; Round 3: cancellation happened even though it wasn't supposed to
fail_round3_cancel:
  ld sp, $fffe
  quit_failure_string "R3: unwanted cancel"

; Round 3: IF wasn't cleared
fail_round3_if:
  ld sp, $fffe
  quit_failure_string "R3: no IF clear"

; Round 4: interrupt dispatching didn't happen
fail_round4_nointr:
  ld sp, $fffe
  quit_failure_string "R4: no interrupt"

; Round 4: cancellation happened even though it wasn't supposed to
fail_round4_cancel:
  ld sp, $fffe
  quit_failure_string "R4: unwanted cancel"

; Round 4: wrong IF value
fail_round4_if:
  ld sp, $fffe
  quit_failure_string "R4: wrong IF"

; Round 4: vblank was dispatched even though IE push disabled it
fail_round4_vblank:
  ld sp, $fffe
  quit_failure_string "R4: wrong intr"

.org INTR_VEC_TIMER
  jp fail_round1_nocancel

.org INTR_VEC_JOYPAD
  jp fail_round2_intr

.org INTR_VEC_SERIAL
  jp finish_round3

.org INTR_VEC_VBLANK
  jp fail_round4_vblank

.org INTR_VEC_STAT
  jp finish_round4

.org $0000
  jp hl

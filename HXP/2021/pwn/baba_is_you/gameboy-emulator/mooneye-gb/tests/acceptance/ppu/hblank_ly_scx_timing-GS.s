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

; Tests how SCX affects the duration between STAT mode=0 interrupt and LY increment.
; No sprites or window.
;
; Expected behaviour:
;   (SCX mod 8) = 0   => LY increments 51 cycles after STAT interrupt
;   (SCX mod 8) = 1-4 => LY increments 50 cycles after STAT interrupt
;   (SCX mod 8) = 5-7 => LY increments 49 cycles after STAT interrupt

; Verified results:
;   pass: DMG, MGB, SGB, SGB2
;   fail: CGB, AGB, AGS

.include "common.s"

.macro clear_interrupts
  xor a
  ldh (<IF), a
.endm

.macro scroll_x ARGS value
  ld a, value
  ldh (<SCX), a
.endm

  ld sp, DEFAULT_SP

  wait_vblank
  ld hl, LY
  ld a, $08
  ldh (<STAT), a
  ld a, INTR_STAT
  ldh (<IE), a

.macro perform_test ARGS scanline delay_a delay_b
  ld d, scanline - 1
  ld e, scanline
  test_iter scanline delay_a
  cp d
  jp nz, test_fail
  test_iter scanline delay_b
  cp e
  jp nz, test_fail
.endm

.macro test_iter ARGS scanline delay
  call setup_and_wait
  ; Interrupt processing: 5
  ; Interrupt vector: 4 + 4 = 8
  call standard_delay
  ; 6 + 23 + 4
  nops delay
  ; N cycles
  ld a, (hl)
  ; 1 cycle for decoding before memory read
  ; 5 + 4 + 4 + 6 + 23 + 4 + N + 1
  ; = 47 + N cycles before memory read
.endm

  perform_test $42 2 3
  perform_test $43 2 3
  scroll_x $01
  perform_test $42 1 2
  perform_test $43 1 2
  scroll_x $02
  perform_test $42 1 2
  perform_test $43 1 2
  scroll_x $03
  perform_test $42 1 2
  perform_test $43 1 2
  scroll_x $04
  perform_test $42 1 2
  perform_test $43 1 2
  scroll_x $05
  perform_test $42 0 1
  perform_test $43 0 1
  scroll_x $06
  perform_test $42 0 1
  perform_test $43 0 1
  scroll_x $07
  perform_test $42 0 1
  perform_test $43 0 1
  scroll_x $08
  perform_test $42 2 3
  perform_test $43 2 3

  quit_ok

test_fail:
  ld b, a
  ldh a, (<SCX)
  setup_assertions
  ; A = SCX
  ; B = LY value
  ; D = scanline - 1
  ; E = scanline
  quit_failure_dump

standard_delay:
  nops 23
  ret

setup_and_wait:
  wait_vblank
- ldh a, (<LY)
  cp d
  jr nz, -
  clear_interrupts
  ei

  halt
  nop
  jp fail_halt

fail_halt:
  quit_failure_string "FAIL: HALT"

.org INTR_VEC_STAT
  add sp,+2
  ret

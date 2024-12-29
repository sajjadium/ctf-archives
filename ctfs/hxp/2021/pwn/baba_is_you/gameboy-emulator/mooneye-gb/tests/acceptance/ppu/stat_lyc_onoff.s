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

; This test checks how the STAT register LY=LYC comparison bit and the
; corresponding interrupt behave when turning off and starting the PPU

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ld sp, DEFAULT_SP

  ld a, %01000000
  ldh (<STAT), a
  ld a, INTR_STAT
  ldh (<IE), a

; In this round we turn off the PPU while the comparison bit is true,
; and run tests where comparison bit changes
round1:
  ld hl, fail_intr_round1
  wait_vblank
  ld a, $90
  ldh (<LYC), a
  xor a
  ldh (<LCDC), a
  ldh (<IF), a
  ei
  nop

; The bit should be retained and not reset to 0
  ldh a, (<STAT)
  cp $c4
  jr z, +
  quit_failure_string "Fail: r1 step 1"

; Changing LYC should not have an effect, because the comparison
; clock is not running
+ ld a, $01
  ldh (<LYC), a
  ldh a, (<STAT)
  cp $c4
  jr z, +
  quit_failure_string "Fail: r1 step 2"

; Enabling the PPU starts the comparison clock again.
; The bit should go to 0, because LY=0
+ ld a, $80
  ldh (<LCDC), a
  ldh a, (<STAT)
  cp $c0
  jr z, round2
  quit_failure_string "Fail: r1 step 3"

; In this round we turn off the PPU while the comparison bit is true,
; and run tests where comparison bit doesn't change
round2:
  di
  ld hl, fail_intr_round2
  wait_vblank
  ld a, $90
  ldh (<LYC), a
  xor a
  ldh (<LCDC), a
  ldh (<IF), a
  ei
  nop

; The bit should be retained and not reset to 0
  ldh a, (<STAT)
  cp $c4
  jr z, +
  quit_failure_string "Fail: r2 step 1"

; Changing LYC should not have an effect, but this should supress
; the interrupt in the next step since the comparison flag just
; stays set
+ ld a, $00
  ldh (<LYC), a
  ldh a, (<STAT)
  cp $c4
  jr z, +
  quit_failure_string "Fail: r2 step 2"

; Enabling the PPU should have no effect, because we simply
; update the comparison from LY=$90 vs LYC=$90 to LY=0 vs LYC=0, and
; the comparison result doesn't change
+ ld a, $80
  ldh (<LCDC), a
  ldh a, (<STAT)
  cp $c4
  jr z, round3
  quit_failure_string "Fail: r2 step 3"

; In this round we turn off the PPU while the comparison bit is false,
; and run tests where comparison bit doesn't change
round3:
  di
  ld hl, fail_intr_round3
  wait_vblank
  xor a
  ldh (<LYC), a
  ldh (<IF), a
  ldh (<LCDC), a
  ei
  nop

; The bit should not be set at this point
  ldh a, (<STAT)
  cp $c0
  jr z, +
  quit_failure_string "Fail: r3 step 1"

; Changing LYC should not have an effect, but this should also guarantee that
; we don't get a true bit from LY=00 comparison in the next step
+ ld a, $01
  ldh (<LYC), a
  ldh a, (<STAT)
  cp $c0
  jr z, +
  quit_failure_string "Fail: r3 step 2"

; Enabling the PPU should have no effect, because we are now comparing
; LY=00 to LYC=01
+ ld a, $80
  ldh (<LCDC), a
  ldh a, (<STAT)
  cp $c0
  jr z, round4
  quit_failure_string "Fail: r3 step 3"

; In this round we turn off the PPU while the comparison bit is false,
; and run tests where comparison bit changes and we get an interrupt
round4:
  di
  wait_vblank
  xor a
  ldh (<LYC), a
  ldh (<IF), a
  ldh (<LCDC), a
  ei
  nop

; The bit should not be set at this point
  ldh a, (<STAT)
  cp $c0
  jr z, +
  quit_failure_string "Fail: round 4"

; This time we are expecting an interrupt, because the comparison
; clock starts running and the comparison bit gets set
+ ld a, $80
  ld hl, finish
  ldh (<LCDC), a
  di
  quit_failure_string "Fail: r4 no intr"

finish:
  quit_ok

fail_intr_round1:
  quit_failure_string "Fail: r1 intr"
fail_intr_round2:
  quit_failure_string "Fail: r2 intr"
fail_intr_round3:
  quit_failure_string "Fail: r3 intr"

.org INTR_VEC_STAT
  jp hl

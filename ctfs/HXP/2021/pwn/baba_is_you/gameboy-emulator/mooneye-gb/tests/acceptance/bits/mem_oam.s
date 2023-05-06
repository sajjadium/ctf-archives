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

; This test checks that the OAM area has no unused bits
; On DMG the sprite flags have unused bits, but they are still
; writable and readable normally

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  ld sp, DEFAULT_SP

  call disable_lcd_safe

  ld hl, OAM
  ld b, OAM_LEN

-
; Write all 1s (= $FF) and expect the same value back
  ld a, $FF
  ld (hl), a
  ld a, (hl)
  cp $FF
  jp nz, fail_1

; Write all 0s (= $00) and expect the same value back
  ld a, $00
  ld (hl), a
  ld a, (hl)
  cp $00
  jp nz, fail_0
  
  inc hl
  dec b
  jr nz, -

test_finish:
  quit_ok

fail_1:
  quit_failure_string "FAIL: ALL 1s"
fail_0:
  quit_failure_string "FAIL: ALL 0s"

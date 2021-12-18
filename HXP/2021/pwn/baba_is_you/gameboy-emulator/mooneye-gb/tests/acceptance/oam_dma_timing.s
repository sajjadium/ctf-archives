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

; This tests the duration of OAM DMA

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

  di

  ; set $8000 to $01
  wait_vblank
  ld a, $01
  ld (VRAM), a

  run_hiram_test

test_finish:
  setup_assertions
  assert_c $FF
  assert_d $01
  quit_check_asserts

hiram_test:
  ld hl, OAM
  ld b, 40
  start_oam_dma $80
- dec b
  jr nz, -

  ; the memory read is aligned to happen exactly one cycle before the OAM DMA end,
  ; so we should still see $FF
  ld a, (hl)
  ld c, a

  ld b, 40
  start_oam_dma $80
- dec b
  jr nz, -
  nops 1

  ; the memory read is aligned to happen exactly after the OAM DMA ends, so
  ; we should see $01
  ld a, (hl)
  ld d, a

  jp test_finish

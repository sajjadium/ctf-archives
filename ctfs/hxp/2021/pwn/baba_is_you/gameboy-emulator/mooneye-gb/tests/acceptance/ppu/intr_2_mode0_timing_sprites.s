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

; Tests how long does it take to get from STAT=mode2 interrupt to mode0
; Includes sprites in various configurations

; Verified results:
;   pass: DMG, MGB, SGB, SGB2, CGB, AGB, AGS
;   fail: -

.include "common.s"

.macro clear_interrupts
  xor a
  ldh (<IF), a
.endm

.macro wait_mode ARGS mode
- ldh a, (<STAT)
  and $03
  cp mode
  jr nz, -
.endm

  ld sp, DEFAULT_SP

  call disable_lcd_safe
  call reset_screen
  call print_load_font

  enable_lcd
  ld a, INTR_STAT
  ldh (<IE), a

.macro testcase
  ld a, \@
  ld (testcase_id), a
  ld hl, _testcase_data_\@
  ld d, 41 + \1
  ld e, 40 + \1
  call run_testcase
  jr _testcase_end_\@
_testcase_data_\@:
  .shift
  .db NARGS
  .repeat NARGS
    .db \1
    .shift
  .endr
_testcase_end_\@:
.endm

  ; extra \      / x coordinates for sprites
  ; cycles \     / (varargs)
  ;        |     |
  ; 1-N sprites at X=0
  testcase 2,    0
  testcase 4,    0,  0
  testcase 5,    0,  0,  0
  testcase 7,    0,  0,  0,  0
  testcase 8,    0,  0,  0,  0,  0
  testcase 10,   0,  0,  0,  0,  0,  0
  testcase 11,   0,  0,  0,  0,  0,  0,  0
  testcase 13,   0,  0,  0,  0,  0,  0,  0,  0
  testcase 14,   0,  0,  0,  0,  0,  0,  0,  0,  0
  testcase 16,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0
  ; ==> sprite count affects cycles

  ; 10 sprites at X=N
  testcase 16,   1,  1,  1,  1,  1,  1,  1,  1,  1,  1
  testcase 15,   2,  2,  2,  2,  2,  2,  2,  2,  2,  2
  testcase 15,   3,  3,  3,  3,  3,  3,  3,  3,  3,  3
  testcase 15,   4,  4,  4,  4,  4,  4,  4,  4,  4,  4
  testcase 15,   5,  5,  5,  5,  5,  5,  5,  5,  5,  5
  testcase 15,   6,  6,  6,  6,  6,  6,  6,  6,  6,  6
  testcase 15,   7,  7,  7,  7,  7,  7,  7,  7,  7,  7
  testcase 16,   8,  8,  8,  8,  8,  8,  8,  8,  8,  8
  testcase 16,   9,  9,  9,  9,  9,  9,  9,  9,  9,  9
  testcase 15,   10, 10, 10, 10, 10, 10, 10, 10, 10, 10
  testcase 15,   11, 11, 11, 11, 11, 11, 11, 11, 11, 11
  testcase 15,   12, 12, 12, 12, 12, 12, 12, 12, 12, 12
  testcase 15,   13, 13, 13, 13, 13, 13, 13, 13, 13, 13
  testcase 15,   14, 14, 14, 14, 14, 14, 14, 14, 14, 14
  testcase 15,   15, 15, 15, 15, 15, 15, 15, 15, 15, 15
  testcase 16,   16, 16, 16, 16, 16, 16, 16, 16, 16, 16
  testcase 16,   17, 17, 17, 17, 17, 17, 17, 17, 17, 17
  testcase 16,   32, 32, 32, 32, 32, 32, 32, 32, 32, 32
  testcase 16,   33, 33, 33, 33, 33, 33, 33, 33, 33, 33
  testcase 16,   160,160,160,160,160,160,160,160,160,160
  testcase 16,   161,161,161,161,161,161,161,161,161,161
  testcase 15,   162,162,162,162,162,162,162,162,162,162
  testcase 15,   167,167,167,167,167,167,167,167,167,167
  testcase 15,   167,167,167,167,167,167,167,167,167,167
  testcase 0,    168,168,168,168,168,168,168,168,168,168
  testcase 0,    169,169,169,169,169,169,169,169,169,169
  ; ==> sprite location affects cycles

  ; 10 sprites split to two groups, X=N and X=M
  testcase 17,   0,  0,  0,  0,  0,  160,160,160,160,160
  testcase 17,   1,  1,  1,  1,  1,  161,161,161,161,161
  testcase 16,   2,  2,  2,  2,  2,  162,162,162,162,162
  testcase 16,   3,  3,  3,  3,  3,  163,163,163,163,163
  testcase 15,   4,  4,  4,  4,  4,  164,164,164,164,164
  testcase 15,   5,  5,  5,  5,  5,  165,165,165,165,165
  testcase 15,   6,  6,  6,  6,  6,  166,166,166,166,166
  testcase 15,   7,  7,  7,  7,  7,  167,167,167,167,167
  testcase 17,   64, 64, 64, 64, 64, 160,160,160,160,160
  testcase 17,   65, 65, 65, 65, 65, 161,161,161,161,161
  testcase 16,   66, 66, 66, 66, 66, 162,162,162,162,162
  testcase 16,   67, 67, 67, 67, 67, 163,163,163,163,163
  testcase 15,   68, 68, 68, 68, 68, 164,164,164,164,164
  testcase 15,   69, 69, 69, 69, 69, 165,165,165,165,165
  testcase 15,   70, 70, 70, 70, 70, 166,166,166,166,166
  testcase 15,   71, 71, 71, 71, 71, 167,167,167,167,167
  ; ==> non-overlapping locations affect cycles

  ; 1 sprite at X=N
  testcase 2,    0
  testcase 2,    1
  testcase 2,    2
  testcase 2,    3
  testcase 1,    4
  testcase 1,    5
  testcase 1,    6
  testcase 1,    7
  testcase 2,    8
  testcase 2,    9
  testcase 2,    10
  testcase 2,    11
  testcase 1,    12
  testcase 1,    13
  testcase 1,    14
  testcase 1,    15
  testcase 2,    16
  testcase 2,    17
  testcase 2,    160
  testcase 2,    161
  testcase 2,    162
  testcase 2,    163
  testcase 1,    164
  testcase 1,    165
  testcase 1,    166
  testcase 1,    167

  ; 2 sprites 8 bytes apart starting from X0=N
  testcase 5,    0,  8
  testcase 5,    1,  9
  testcase 4,    2,  10
  testcase 4,    3,  11
  testcase 3,    4,  12
  testcase 3,    5,  13
  testcase 3,    6,  14
  testcase 3,    7,  15
  testcase 5,    8,  16
  testcase 5,    9,  17
  testcase 4,    10, 18
  testcase 4,    11, 19
  testcase 3,    12, 20
  testcase 3,    13, 21
  testcase 3,    14, 22
  testcase 3,    15, 23
  testcase 5,    16, 24

  ; 10 sprites 8 bytes apart starting from X0=N
  testcase 27,   0,  8,  16, 24, 32, 40, 48, 56, 64, 72
  testcase 25,   1,  9,  17, 25, 33, 41, 49, 57, 65, 73
  testcase 22,   2,  10, 18, 26, 34, 42, 50, 58, 66, 74
  testcase 20,   3,  11, 19, 27, 35, 43, 51, 59, 67, 75
  testcase 17,   4,  12, 20, 28, 36, 44, 52, 60, 68, 76
  testcase 15,   5,  13, 21, 29, 37, 45, 53, 61, 69, 77
  testcase 15,   6,  14, 22, 30, 38, 46, 54, 62, 70, 78
  testcase 15,   7,  15, 23, 31, 39, 47, 55, 63, 71, 79

  ; 10 sprites 8 bytes apart starting from X0=N, reverse
  testcase 27,   72, 64, 56, 48, 40, 32, 24, 16, 8,  0
  testcase 25,   73, 65, 57, 49, 41, 33, 25, 17, 9,  1
  ; ==> sprite order does not affect cycles

  quit_ok

run_testcase:
  push de
  push hl
  wait_vblank
  disable_lcd
  call clear_oam

  pop de
  call prepare_sprites
  pop de

  ld c, d
  ld hl, nop_area_a
  call prepare_nop_area
  ld c, e
  ld hl, nop_area_b
  call prepare_nop_area

  enable_lcd
  ; Enable sprites
  ld hl, LCDC
  set 1, (HL)

testcase_round_a:
  ld hl, testcase_round_a_ret
  push hl
  ld hl, nop_area_a
  push hl
  jp setup_and_wait_mode2

testcase_round_a_ret:
  ld b, $00
- inc b
  ldh a, (<STAT)
  and $03
  jr nz, -
  ld a, b
  ld c, $01
  cp c
  jp nz, test_fail

testcase_round_b:
  ld hl, testcase_round_b_ret
  push hl
  ld hl, nop_area_b
  push hl
  jp setup_and_wait_mode2

testcase_round_b_ret:
  ld b, $00
- inc b
  ldh a, (<STAT)
  and $03
  jr nz, -
  ld a, b
  ld c, $02
  cp c
  jp nz, test_fail
  ret

prepare_sprites:
  ld a, (de)
  ld c, a    ; amount of sprites
  ld b, $30  ; sprite tile
  ld hl, OAM

- inc de
  ; Sprite Y
  ld a, $52
  ld (hl+), a
  ; Sprite X
  ld a, (de)
  ld (hl+) ,a
  ; Sprite tile
  ld a, b
  ld (hl+), a
  inc b
  ; Sprite flags
  xor a
  ld (hl+), a

  dec c
  jr nz, -
  ret

prepare_nop_area:
  xor a
- ld (hl+), a
  dec c
  jr nz, -

  ld a, $C9 ; RET instruction
  ld (hl+), a
  ret

setup_and_wait_mode2:
  wait_ly $42
  wait_mode $00
  wait_mode $03
  ld a, %00100000
  ldh (<STAT), a
  clear_interrupts
  ei

  halt
  nop
  jp fail_halt

test_fail:
  quit_inline
  print_string_literal "TEST #"
  ld a, (testcase_id)
  call print_hex8
  print_string_literal " FAILED"
  ld d, $42
  ret

fail_halt:
  quit_failure_string "FAIL: HALT"

.org INTR_VEC_STAT
  add sp,+2
  ret

.ramsection "Test-WRAM" slot WRAM0_SLOT
  nop_area_a ds 96
  nop_area_b ds 96
.ends

.ramsection "Test-HRAM" slot HRAM_SLOT
  testcase_id dw
.ends

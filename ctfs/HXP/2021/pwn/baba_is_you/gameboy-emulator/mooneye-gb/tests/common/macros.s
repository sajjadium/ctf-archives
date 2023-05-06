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

; --- Macros ---

.macro c_string ARGS string
  .db string, $00
.endm

.macro nops ARGS count
  .repeat count
    nop
  .endr
.endm

.macro delay_long_time ARGS iterations
  ld a, >iterations
  ld b, a
  ld a, <iterations
  ld c, a
  ; = 6 cycles

_delay_long_time_\@:
  dec bc
  ld a,b
  or c
  jr nz, _delay_long_time_\@
  ; = iterations * 7 - 1 cycles

  ; total: iterations * 7 + 5 cycles
.endm

.macro magic_breakpoint
  ld b, b ; magic breakpoint
.endm

.macro halt_execution
  magic_breakpoint
@halt_execution_\@:
  nop
  jr @halt_execution_\@
.endm

.macro disable_lcd
  ld hl, LCDC
  res 7, (hl)
.endm

.macro enable_lcd
  ld hl, LCDC
  set 7, (hl)
.endm

.macro wait_ly ARGS value
@wait_ly_\@:
  ldh a, (<LY)
  cp value
  jr nz, @wait_ly_\@
.endm

.macro wait_vblank
  ; wait for LY=143 first to ensure we get a fresh v-blank
  wait_ly 143
  ; wait for LY=144
  wait_ly 144
.endm

; Copy test procedure to hiram $FF80 and jump to it.
; This is for tests that involve OAM DMA.
; During OAM DMA the CPU cannot access any other memory,
; so our code needs to be there
.macro run_hiram_test
  ld hl, HIRAM
  ld de, hiram_test
  ld bc, $60 ; 0x60 bytes should be enough
  call memcpy
  ; jump to test procedure in hiram
  jp HIRAM
.endm

.macro start_oam_dma ARGS address
  wait_vblank
  ld a, address
  ldh (<DMA), a
.endm

.macro print_string_literal ARGS string
  call print_inline_string
  c_string string
.endm

.macro quit_failure
  quit_failure_string "Test failed"
.endm

.macro quit_failure_dump ARGS string
  quit_inline
  ld de, hram.regs_save
  print_string_literal "REGISTERS"
  call print_newline
  call print_newline
  call print_reg_dump
  call print_newline
  print_string_literal "Test failed"
  ld d, $42
  ret
.endm

.macro quit_failure_string ARGS string
  quit_inline
  call print_newline
  print_string_literal string
  ld d, $42
  ret
.endm

.macro quit_ok
  quit_ok_string "Test OK"
.endm

.macro quit_ok_string ARGS string
  quit_inline
  call print_newline
  print_string_literal string
  ld d, $00
  ret
.endm

.macro quit_callback ARGS cb
  di
  ld hl, cb
  jp quit
.endm

.macro quit_check_asserts
  quit_callback check_asserts_cb
.endm

.macro quit_inline
  quit_callback  @quit_inline_\@
@quit_inline_\@:
.endm

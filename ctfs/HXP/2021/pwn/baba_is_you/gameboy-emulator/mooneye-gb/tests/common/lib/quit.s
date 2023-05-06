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

.section "quit"
; Inputs:
;   HL: pointer to callback
; Outputs: -
; Preserved: -
quit:
  ld sp, DEFAULT_SP
  ld bc, @cb_return
  push bc
  push hl
  call disable_lcd_safe
  call reset_screen
  call print_load_font

  ld hl, $9800
  ; this is basically "call cb" since callback pointer is on the stack,
  ; followed by the return address
  ret

  @cb_return:
    enable_lcd
    wait_vblank
    ; Extra vblank to account for initial (invisible) frame
    wait_vblank
    ld a, d
    and a
    jr nz, @failure

  @success:
    ; Magic numbers signal a successful test
    ld b, 3
    ld c, 5
    ld d, 8
    ld e, 13
    ld h, 21
    ld l, 34

    magic_breakpoint

    ld a, b
    call serial_send_byte
    ld a, c
    call serial_send_byte
    ld a, d
    call serial_send_byte
    ld a, e
    call serial_send_byte
    ld a, h
    call serial_send_byte
    ld a, l
    call serial_send_byte

    jr @halt

  @failure:
    magic_breakpoint

    ld a, $42
    call serial_send_byte
    ld a, $42
    call serial_send_byte
    ld a, $42
    call serial_send_byte
    ld a, $42
    call serial_send_byte
    ld a, $42
    call serial_send_byte
    ld a, $42
    call serial_send_byte

  @halt:
    halt_execution
.ends

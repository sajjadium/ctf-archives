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

.section "print_reg_dump"
; Inputs:
;   DE pointer to reg_dump
; Outputs: -
; Preserved: -
print_reg_dump:
  .macro __print_reg_pair ARGS reg_a reg_b
    inc de
    print_string_literal reg_a
    ld a, (de)
    call print_hex8

    dec de
    print_string_literal reg_b
    ld a, (de)
    call print_hex8

    inc de
    inc de
    call print_newline
  .endm

  __print_reg_pair "  A: " "  F: "
  __print_reg_pair "  B: " "  C: "
  __print_reg_pair "  D: " "  E: "
  __print_reg_pair "  H: " "  L: "

  ret
.ends

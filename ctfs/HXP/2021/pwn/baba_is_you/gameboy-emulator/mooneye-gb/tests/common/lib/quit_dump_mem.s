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

.section "quit_dump_mem"
; Inputs:
;   A: number of bytes
;   HL: source address
; Outputs: -
; Preserved: -
quit_dump_mem:
  ldh (<hram.memdump_len), a
  ld a, l
  ldh (<hram.memdump_l), a
  ld a, h
  ldh (<hram.memdump_h), a

  quit_inline
  ldh a, (<hram.memdump_h)
  ld d, a
  ldh a, (<hram.memdump_l)
  ld e, a
  ldh a, (<hram.memdump_len)
  ld b, a
@line:
  ld a, d
  call print_hex8
  ld a, e
  call print_hex8

- ld a, (de)
  call print_hex8
  inc de
  dec b
  jr z, ++

  ld a, l
  and $1f
  cp 20
  jr nz, -

  call print_newline
  jr @line

++
  ld d, $00
  ret
.ends

.ramsection "Runtime-Memdump" slot HRAM_SLOT
  hram.memdump_len db
  hram.memdump .dw
  hram.memdump_l db
  hram.memdump_h db
.ends

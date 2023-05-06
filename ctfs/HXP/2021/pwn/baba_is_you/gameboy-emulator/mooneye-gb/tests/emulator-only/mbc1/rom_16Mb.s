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

; Tests banking behaviour of a MBC1 cart with a 16 Mbit ROM

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC1B1 chip
; and support for configuring ROM/RAM sizes.

.define CART_ROM_BANKS 128

.include "harness/mbc1_rom.s"

.bank 0 slot 0
.section "expected banks" FREE

expected_banks:

; $0000-$3FFF area, mode 0
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0

; $0000-$3FFF area, mode 1
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
.db   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
.db  32  32  32  32  32  32  32  32  32  32  32  32  32  32  32  32
.db  32  32  32  32  32  32  32  32  32  32  32  32  32  32  32  32
.db  64  64  64  64  64  64  64  64  64  64  64  64  64  64  64  64
.db  64  64  64  64  64  64  64  64  64  64  64  64  64  64  64  64
.db  96  96  96  96  96  96  96  96  96  96  96  96  96  96  96  96
.db  96  96  96  96  96  96  96  96  96  96  96  96  96  96  96  96

; $4000-$7FFF area
.db   1   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
.db  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
.db  33  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47
.db  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63
.db  65  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79
.db  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95
.db  97  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111
.db 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127

.ends

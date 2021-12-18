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

; Tests banking behaviour of a MBC1 multicart with a 8 Mbit ROM
; No other ROM sizes exist and it's not clear how they would be wired,
; so this is the only MBC1 multicart test.
; MBC1 multicarts *cannot* be detected from the header alone, because MBC1
; 8Mbit multicarts and normal carts have similar header data.
; Therefore any emulator that wants to pass this test must have either
; heuristics or some configuration to trigger MBC1 multicart mode.

; See gb-ctr for details: https://github.com/Gekkio/gb-ctr

; Results have been verified using a flash cartridge with a genuine MBC1B1 chip
; and support for configuring ROM/RAM sizes.

.define CART_ROM_BANKS 64

; Uncomment the following if the tested system uses titles to trigger MBC1
; multicart mode. For example, MAME can pass this test ROM if we lie that
; we're BOMCOL (= Bomber Man Collection)

; .define CART_NO_TITLE
; .name "BOMCOL"

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
.db  16  16  16  16  16  16  16  16  16  16  16  16  16  16  16  16
.db  16  16  16  16  16  16  16  16  16  16  16  16  16  16  16  16
.db  32  32  32  32  32  32  32  32  32  32  32  32  32  32  32  32
.db  32  32  32  32  32  32  32  32  32  32  32  32  32  32  32  32
.db  48  48  48  48  48  48  48  48  48  48  48  48  48  48  48  48
.db  48  48  48  48  48  48  48  48  48  48  48  48  48  48  48  48

; $4000-$7FFF area
.db   1   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
.db   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
.db  17  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
.db  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
.db  33  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47
.db  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47
.db  49  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63
.db  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63

.ends

; Put Nintendo logos in all banks. This triggers heuristics in some emulators
; (e.g. mooneye-gb)

.repeat CART_ROM_BANKS INDEX bank
.bank bank
.org $0104
.db $CE $ED $66 $66 $CC $0D $00 $0B $03 $73 $00 $83 $00 $0C $00 $0D
.db $00 $08 $11 $1F $88 $89 $00 $0E $DC $CC $6E $E6 $DD $DD $D9 $99
.db $BB $BB $67 $63 $6E $0E $EC $CC $DD $DC $99 $9F $BB $B9 $33 $3E
.endr

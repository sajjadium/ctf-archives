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

.ifndef ROM_BANK_SIZE
  .define ROM_BANK_SIZE $4000
.endif

.ifdef CART_TYPE
  ; MBC1 registers
  .ifgreq CART_TYPE $01
    .ifleeq CART_TYPE $03
      .define RAMG $0000
      .define BANK1 $2000
      .define BANK2 $4000
      .define MODE $6000
    .endif
  .endif
  ; MBC2 registers
  .ifgreq CART_TYPE $05
    .ifleeq CART_TYPE $06
      .define RAMG $0000
      .define ROMB $2100
    .endif
  .endif
  ; MBC5 registers
  .ifgreq CART_TYPE $19
    .ifleeq CART_TYPE $1e
      .define RAMG $0000
      .define ROMB0 $2000
      .define ROMB1 $3000
      .define RAMB $4000
    .endif
  .endif
.endif

.rombanksize ROM_BANK_SIZE
.memorymap
  defaultslot 1
  slot 0 start $0000 size ROM_BANK_SIZE
  slot 1 start $4000 size ROM_BANK_SIZE
  slot 2 start $c000 size $2000
  slot 3 start $a000 size $2000
  slot 4 start $ff80 size $007f
.endme
.define WRAM0_SLOT 2
.define WRAMX_SLOT 2
.define XRAM_SLOT 3
.define HRAM_SLOT 4

.define INTR_VBLANK (1 << 0)
.define INTR_STAT   (1 << 1)
.define INTR_TIMER  (1 << 2)
.define INTR_SERIAL (1 << 3)
.define INTR_JOYPAD (1 << 4)

.define INTR_VEC_VBLANK $40
.define INTR_VEC_STAT   $48
.define INTR_VEC_TIMER  $50
.define INTR_VEC_SERIAL $58
.define INTR_VEC_JOYPAD $60

.define VRAM  $8000
.define WRAM  $C000
.define OAM   $fe00
.define HIRAM $ff80

.define VRAM_LEN  $2000
.define WRAM_LEN  $2000
.define OAM_LEN   $a0
.define HIRAM_LEN $7f

.define P1    $ff00
.define SB    $ff01
.define SC    $ff02
.define DIV   $ff04
.define TIMA  $ff05
.define TMA   $ff06
.define TAC   $ff07
.define IF    $ff0f
.define NR10  $ff10
.define NR11  $ff11
.define NR12  $ff12
.define NR13  $ff13
.define NR14  $ff14
.define NR21  $ff16
.define NR22  $ff17
.define NR23  $ff18
.define NR24  $ff19
.define NR30  $ff1a
.define NR31  $ff1b
.define NR32  $ff1c
.define NR33  $ff1d
.define NR34  $ff1e
.define NR41  $ff20
.define NR42  $ff21
.define NR43  $ff22
.define NR44  $ff23
.define NR50  $ff24
.define NR51  $ff25
.define NR52  $ff26
.define LCDC  $ff40
.define STAT  $ff41
.define SCY   $ff42
.define SCX   $ff43
.define LY    $ff44
.define LYC   $ff45
.define DMA   $ff46
.define BGP   $ff47
.define OBP0  $ff48
.define OBP1  $ff49
.define WY    $ff4a
.define WX    $ff4b
.define KEY1  $ff4d
.define VBK   $ff4f
.define BOOT  $ff50
.define HDMA1 $ff51
.define HDMA2 $ff52
.define HDMA3 $ff53
.define HDMA4 $ff54
.define HDMA5 $ff55
.define RP    $ff56
.define BCPS  $ff68
.define BCPD  $ff69
.define OCPS  $ff6a
.define OCPD  $ff6b
.define SVBK  $ff70
.define IE    $ffff

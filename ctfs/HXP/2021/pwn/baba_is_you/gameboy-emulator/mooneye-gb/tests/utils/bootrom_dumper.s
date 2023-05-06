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

.include "hardware.s"

.rombanksize $4000
.rombanks 4
.ramsize 1
.emptyfill $00

.gbheader
  name "DUMPER"
  licenseecodeold $42
  cartridgetype 3 ; MBC1/RAM/battery
  destinationcode $00
  nintendologo
  romdmg
.endgb

.bank 0 slot 0
.org $0100
  nop
  jp $7D00

.bank 1 slot 1
.org $3D00
  di

enable_cartridge_ram:
  ld a, $0a
  ld ($1000), a

copy_data:
  ld hl, $a000
  ld de, $0000
  ld bc, $100
  call memcpy

disable_cartridge_ram:
  xor a
  ld ($1000), a

compare_data:
  ld hl, $0000
  ld c, $00

- ld a, (hl+)
  dec c
  jr z, finish
  cp $00
  jr z, -

finish:
  ld sp, $ffff
  ld a, c
  ldh ($80), a

  @check_lcd:
    ldh a, (<LCDC)
    and %10000000
    jr z, @clear_tilemap

  @wait_vblank:
    ldh a, (<LY)
    cp 144
    jr nz, @wait_vblank

  @disable_lcd:
    ld a, %00000001
    ldh (<LCDC), a

  @clear_tilemap:
    xor a
    ld hl, $9800
    ld bc, $400
    call memset

  @choose_tilemap:
    ldh a, ($80)
    or a
    jr nz, +
    ld de, tilemap_sadface
    jr @setup_tilemap
+   ld de, tilemap_happyface

  @setup_tilemap:
    ld hl, $9880
    ld b, 10
-   push bc
    ld bc, 20
    call memcpy
    pop af
    dec a
    and a
    jr z, @clear_tiles
    ld bc, 12
    add hl, bc
    ld b, a
    jr -

  @clear_tiles:
    xor a
    ld hl, $8000
    ld bc, $1000
    call memset

  @setup_tile:
    ld a, $ff
    ld hl, $8ff0
    ld bc, 16
    call memset

  @setup_audio:
    ld a, $ff
    ldh (<NR50), a
    ldh (<NR51), a
    ldh (<NR52), a
    xor a
    ldh (<NR10), a
    ld a, $80
    ldh (<NR11), a
    ld a, $F8
    ldh (<NR12), a
    xor a
    ldh (<NR13), a

  @enable_lcd:
    ld hl, LCDC
    set 7, (hl)

  ldh a, ($80)
  or a
  jr nz, +
  ld a, $C0
  jr ++
+ ld a, $C7
++
  ldh (<NR14), a

- halt
  nop
  jr -

; Inputs:
;   HL target
;   DE source
;   BC length
; Outputs:
;   HL target + length
; Preserved: -
memcpy:
- ld a, b
  or c
  ret z
  ld a, (de)
  ld (hl+), a
  inc de
  dec bc
  jr -

; Inputs:
;   HL target
;   A value
;   BC length
; Outputs:
;   HL target + number of bytes
; Preserved: E
memset:
  ld d, a
- ld a, b
  or c
  ret z
  ld a, d
  ld (hl+), a
  dec bc
  jr -

tilemap_happyface:
  .db $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00
  .db $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00
  .db $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00
  .db $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $00 $FF $FF $FF $FF $FF $FF $00 $00 $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $00

tilemap_sadface:
  .db $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00
  .db $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $00 $FF $FF $FF $FF $FF $FF $00 $00 $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00
  .db $00 $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00 $00
  .db $00 $00 $00 $FF $FF $00 $00 $00 $00 $00 $00 $00 $00 $00 $00 $FF $FF $00 $00 $00

.org $4000 - 3
  jp $7D00

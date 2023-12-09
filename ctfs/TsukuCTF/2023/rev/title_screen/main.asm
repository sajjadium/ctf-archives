.setcpu		"6502"
.autoimport	on

PPU_ADDR1	=	$0001
PPU_ADDR2	=	$0002

PPU_STATUS	=	$2002

.segment "HEADER"
	.byte	$4E, $45, $53, $1A
	.byte	$02
	.byte	$01
	.byte	$01
	.byte	$00
	.byte	$00, $00, $00, $00
	.byte	$00, $00, $00, $00

.segment "STARTUP"
.proc	Reset
	sei
	ldx #$ff
	txs
	clc
	cld
	
	lda #$00
	sta $2000
	sta $2001
	sta $2005
	sta $2006
	
	lda $4015
	and #%11111110
	sta $4015

	lda PPU_STATUS
	lda #$00
	sta $2000
	sta $2001

	lda #$00
	ldx #$00

clear_memory:
	sta $0000, X
	sta $0100, X
	sta $0200, X
	sta $0300, X
	sta $0400, X
	sta $0500, X
	sta $0600, X
	sta $0700, X
	inx
	cpx #$00
	bne clear_memory

	lda #$20
	sta $2006
	lda #$00
	sta $2006
	lda #$00
	ldx #$00
	ldy #$04

clear_vram_loop:
	sta $2007
	inx
	bne clear_vram_loop
	dey
	bne clear_vram_loop

	lda	#$3F
	sta	$2006
	lda	#$00
	sta	$2006
	ldx	#$00
	ldy	#$10

setpal:
	lda	palettes, x
	sta	$2007
	inx
	dey
	bne	setpal
	
	lda	#$20
	sta	$2006
	lda	#$00
	sta	$2006

	ldy #0
	jsr set_row

	jmp mapping1

mapping1:
	ldy	#11
	ldx	#$00
	lda	#$8c
mapping1_y_loop:
	jsr set_row
	ldx #05
	jsr set_col
	ldx #$14
mapping1_x_loop:
	sta	$2007
	dex
	bne	mapping1_x_loop

	iny
	cpy #16
	bne mapping1_y_loop


mapping2:
	ldy	#13
	jsr set_row
	ldx #08
	jsr set_col
	ldx #00
	ldy #14
mapping2_x_loop:
	lda	data, x
	sta	$2007
	inx
	dey
	bne	mapping2_x_loop


screenend:
	lda	#$00
	sta	$2005
	sta	$2005

	lda	#$08
	sta	$2000
	lda	#$1e
	sta	$2001

loop:
	jmp	loop

set_row:
	pha

	tya
	lsr a
	lsr a
	lsr a
	clc
	adc #$20
	sta	PPU_ADDR1

	tya
	asl a
	asl a
	asl a
	asl a
	asl a
	sta	PPU_ADDR2

	lda	PPU_ADDR1
	sta	$2006
	lda	PPU_ADDR2
	sta	$2006

	pla
	rts

set_col:
	pha

	txa
	adc PPU_ADDR2
	sta	PPU_ADDR2

	lda	PPU_ADDR1
	sta	$2006
	lda	PPU_ADDR2
	sta	$2006

	pla
	rts

.endproc

palettes:
	.byte	$01, $18, $39, $30
	.byte	$0f, $06, $16, $26
	.byte	$0f, $08, $18, $28
	.byte	$0f, $0a, $1a, $2a

data:
	.byte	$22, $a4, $39, $26, $39
	.byte	$a4, $55, $79, $bb, $4c
	.byte	$39, $c7, $a4, $d1, $8c

.segment "VECINFO"
	.word	$0000
	.word	Reset
	.word	$0000

.segment "CHARS"
	.incbin "character.chr"
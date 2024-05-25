
shufPtr1 = $00
shufPtr2 = $01
shufMask = $02
shufTemp0 = $03
shufTemp1 = $04
input = $200
.org $8000

main:
		LDX	#$FF
		TXS
		JSR	shuffleInput
		JSR	checkInput
		BCC	noWinning
		.byte	$12
noWinning:
		JMP	$0000



shuffleInput:	LDY	#$AB
		STY	shufPtr1
		LDY	#$00
		STY	shufPtr2
shufLoop:	LDA	#$80
		STA	shufMask
shufLoop2:	
		.byte	$02
		AND	shufMask
		BEQ	shufSkip
		STY	shufTemp0
		LDA	shufPtr1
		AND	#$3F
		CMP	#$30
		BCC	shufOk1
		SBC	#$30	
shufOk1:
		TAY
		LDA	shufPtr2
		AND	#$3F
		CMP	#$30
		BCC	shufOk2
		SBC	#$30	
shufOk2:
		TAX
		LDA	input,X
		PHA
		LDA	input,Y
		STA	input,X
		PLA
		STA	input,Y
		LDA	shufMask
		ADC	#$E3
		STA	shufTemp1
		LDA	shufPtr1
		ROR
		EOR	shufTemp1
		TAX
		LDA	shufTable,X
		STA	shufPtr1
		LDA	shufPtr2
		ROR
		EOR	shufTemp1
		TAX
		LDA	shufTable,X
		STA	shufPtr2
		LDY	shufTemp0
shufSkip:	LSR	shufMask
		BCC	shufLoop2
		INY
		CPY	#$30
		BNE	shufLoop
		RTS
		
checkInput:
		LDY	#$30
checkLoop:	.byte	$02
		EOR	input-$30,Y
		TAX
		LDA	checkTable,X
		STA	input-$30,Y
		INY
		CPY	#$60
		BNE	checkLoop
		LDY	#$00
checkLoop2:	.byte	$02
		CMP	input,Y
		BEQ	checkOk
		CLC
		RTS	
checkOk:	INY
		CPY	#$30
		BNE	checkLoop2
		SEC
		RTS

shufTable:
		.byte $49, $bc, $1d, $5a, $1c, $47, $74, $99, $67, $34, $19, $2f, $cf, $9f, $93, $84
		.byte $6e, $b0, $aa, $3c, $78, $24, $ca, $88, $c1, $d5, $47, $82, $aa, $18, $45, $05
		.byte $cf, $3d, $4d, $12, $e8, $2d, $d5, $d5, $f3, $66, $d0, $78, $ad, $a5, $c3, $66
		.byte $fb, $80, $7c, $ff, $04, $cd, $6d, $38, $1d, $62, $80, $7f, $c3, $2b, $4e, $a1
		.byte $66, $0b, $cc, $3e, $51, $32, $68, $8d, $eb, $02, $f0, $f9, $ff, $18, $ce, $2f
		.byte $fa, $c6, $4e, $5b, $31, $a0, $f8, $b9, $79, $05, $3b, $7e, $ca, $8d, $db, $5a
		.byte $c2, $97, $21, $b4, $dd, $3c, $c8, $20, $20, $d2, $f1, $a8, $cb, $26, $4b, $0b
		.byte $da, $91, $43, $69, $57, $9a, $8c, $f4, $f6, $ab, $36, $54, $03, $45, $24, $ee
		.byte $64, $7a, $28, $dc, $50, $77, $bd, $8c, $c9, $38, $64, $3c, $6f, $a0, $ad, $82
		.byte $ef, $ad, $11, $3f, $89, $e0, $cb, $76, $b9, $fb, $9f, $bf, $cb, $a4, $23, $c6
		.byte $41, $92, $ef, $b0, $35, $45, $93, $e9, $2a, $43, $58, $cf, $6c, $bd, $ab, $a4
		.byte $72, $6a, $66, $ed, $e8, $77, $b3, $51, $3a, $33, $0f, $6d, $8d, $df, $54, $42
		.byte $c0, $54, $29, $80, $c3, $b3, $0b, $c2, $a9, $80, $ae, $88, $52, $4a, $1e, $d9
		.byte $5d, $a3, $64, $ab, $8e, $c9, $34, $29, $b5, $02, $69, $05, $ff, $fb, $ef, $02
		.byte $45, $76, $13, $e2, $62, $dc, $c2, $34, $5c, $b8, $96, $9a, $9b, $e6, $08, $41
		.byte $eb, $b9, $3e, $9f, $d4, $ac, $ec, $c8, $a0, $92, $54, $a0, $c7, $66, $da, $b7
checkTable:
		.byte $00, $00, $00, $00, $00, $a8, $00, $64, $00, $00, $cd, $00, $00, $00, $80, $00  
		.byte $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $30, $00, $00  
		.byte $f1, $00, $00, $00, $63, $00, $11, $20, $a2, $29, $d7, $00, $00, $49, $00, $f1  
		.byte $00, $46, $00, $00, $00, $00, $00, $8b, $00, $00, $00, $00, $00, $00, $00, $00  
		.byte $87, $00, $00, $00, $00, $f8, $49, $00, $00, $00, $00, $00, $00, $00, $00, $00  
		.byte $00, $00, $00, $0b, $00, $00, $00, $00, $4f, $00, $00, $00, $00, $00, $00, $00  
		.byte $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $a8, $00, $00, $00, $00  
		.byte $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $31, $00, $00, $00, $00, $00  
		.byte $00, $20, $00, $07, $6e, $00, $00, $a7, $00, $00, $00, $00, $c2, $3c, $00, $00  
		.byte $57, $00, $00, $00, $00, $00, $00, $00, $00, $00, $c4, $00, $00, $00, $00, $00  
		.byte $94, $00, $00, $00, $00, $00, $25, $00, $00, $00, $00, $f8, $00, $00, $00, $00  
		.byte $00, $00, $00, $00, $00, $9c, $00, $00, $00, $00, $00, $00, $00, $13, $00, $00  
		.byte $00, $00, $00, $00, $00, $00, $00, $00, $95, $00, $00, $00, $00, $00, $00, $00  
		.byte $22, $00, $29, $00, $00, $00, $00, $00, $00, $5a, $00, $00, $00, $00, $00, $41  
		.byte $00, $00, $00, $00, $00, $00, $9f, $00, $00, $00, $00, $00, $00, $00, $86, $64  
		.byte $00, $48, $00, $00, $00, $eb, $00, $00, $00, $1f, $00, $ed, $00, $00, $00, $00  

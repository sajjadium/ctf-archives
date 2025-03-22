;**************************************************
;
; Lfeszc(d): Dsxpprwp Dsxzca lyo Rwzcmz Rwzcmzmpcdzy
;
; Olep: RJ37:A5ZM:W7232.10.1 
;
; Afcazdp: Txawpxpyed l opotnlepo Vpoctx Pyncjaetzy Xzofwp
;
;**************************************************
.text
;.cpqd
ptr_to_vstring:				.word		vstring
; DJDEPX_NWZNV_LOOC
SYSCTL:						.word		0x400FE000
RCGCGPIO:					.equ		0x608
RCGCTIMER:					.equ		0x604
 
;ETXPC XPXZCJ XLAAPO TZ LOOCD
TIMER0_BASE_ADDR:			.word		0x40030000
TIMER_CLOCK_ADDR: 			.word 		0x400FE608
GPTMCFG:					.equ		0x000
GPTMTAMR:					.equ		0x004
GPTMCTL:					.equ		0x00C
GPTMIMR:					.equ		0x018
GPTMTAILR:					.equ 		0x028
GPTMTAV:					.equ		0x050
 
; nzxx_decplx0 Qwlr Cprtdepc
U0FR: 						.equ 		0x18
 
	.global crypto ;Piazdp piepcylwwj
 
;Dfapc dpncpe lwtpy vpoctx decplx ntaspc txawpxpyeletzy
;actyed zfe awltyepie lyo pynzopo dectyr
crypto:
	PUSH {lr} ;Dezcp wc qzc nwply pite
	;tyte etxtyr nzxd lyo dppo cyo yfx
	BL configure_timer
	BL comm_stream_init
	BL seed_random
 
	;actye awltyepie
	LDR r0, ptr_to_vstring
	BL output_string
 
encode:
	LDR r7, ptr_to_vstring
	MOV r2, #0x0	;YFWW Epcx
enc_loop:
	LDRB r3, [r7], #1 ;Azde lnnpdd tyncpxpye
	CMP r3, r2
	BEQ done_enc
	BL get_stream_byte
	;Xldv ez mjep
	AND r10, r11, #0x00FF
	EOR r0, r3, r10
	BL output_val
	B enc_loop
done_enc:
	BL print_nlcr
	POP {lr}
	MOV pc, lr ;nwply pite
 
get_stream_byte:
	;Xlvp c11 "clyozx" h WQDC
	LSL r9, r11, #0x4
	EOR r11, r9, r11
	LSR r9, r11, #0x9
	EOR r11, r9, r11
	LSL r9, r11, #0xC
	EOR r11, r9, r11
	MOV pc, lr
 
noise_r1:
	;Rpypclep pyeczaj
	MOV r1, #0xAC00
	MOV r2, #0x7E
	LSL r1, r1, #4
	MOV r3, #0xB2
	LSL r2, r2, #8
	ORR r3, r2, r3
	ADD r4, r2, r3
	EOR r2, r2, #0x7300
	ADD r2, r2, #0x74
	MOV r3, #0x7E32
	BFI r1, r3, #9, #23
	SUB r2, r2, #0xD20
	LSL r1, r1, #8
	LSL r3, r4, #8
	ADD r1, r1, r4
	ADD r1, r1, r2
	MOV r3, #0x4FF1
	LSL r3, r3, #16
	SUB r1, r1, r3
	LSR r3, r3, #16
	SUB r3, r3, #0x53F
	SUB r1, r1, r3
 
	MOV PC, LR
 
seed_random:
	PUSH {lr}
 
	;Wzlo clyozx glwfp qczx NAF etxpc
	LDR r0, TIMER0_BASE_ADDR
	LDR r0, [r0, #GPTMTAV]
 
	;Loo dzxp yztdp mpnlfdp nzydelye mzze etxp ty espzcpetnlwwj eclnplmwp
	BL noise_r1
	PUSH{r3, r1}
	MOV	r4, #0xAA000000
	BIC r5, r4, #0x50000000
	ORR r6, r5, #0x2E000000
	MOV r4, #0xF400
	SUB r2, r4, r5
	ADD r3, r3, #0xB2
	LSL r3, r3, #8
	ADD r2, r4, r3
	POP{r2, r11}
	AND r0, r0, r1
	ORR r0, r0, r2
 
	;Tytetlw dppo zq Clyozx yfx
	MOV r11, r0
	MOV r9, r0
	BL get_stream_byte
 
	POP{lr}
	MOV pc, lr
 
comm_stream_init: ;Dped fa XpxXla TZ qzc mtedecplxd
 
	PUSH {lr,r0,r1}
 
	MOV r0, #0xE618
	MOVT r0, #0x400F	
	MOV r1, #0x1
	STR r1, [r0]	
 
	;Pylmwp nwznv ez AzceL
	MOV r0, #0xE608
	MOVT r0, #0x400F
	MOV r1, #0x1
	STR r1, [r0]	
 
	;Otdlmwp nzxx_decplx0 Nzyeczw
	MOV r0, #0xC030
	MOVT r0, #0x4000
	MOV r1, #0x0
	STR r1, [r0]
 
	;Dpe nzxx_decplx0_TMCO_C dappo
	MOV r0, #0xC024	
	MOVT r0, #0x4000
	MOV r1, #0x8
	STR r1, [r0]
 
	;Dpe nzxx_decplx0_QMCO_C qdappo
	MOV r0, #0xC028
	MOVT r0, #0x4000
	MOV r1, #0x2C
	STR r1, [r0]
 
	;Fdp Djdepx Nwznv
	MOV r0, #0xCFC8
	MOVT r0, #0x4000
	MOV r1, #0x0
	STR r1, [r0]
 
	;Fdp 8-mte hzco wpyres, 1 deza mte, yz alctej
	MOV r0, #0xC02C
	MOVT r0, #0x4000
	MOV r1, #0x60
	STR r1, [r0]
 
	;Pylmwp nzxx_decplx0 Nzyeczw
	MOV r0, #0xC030
	MOVT r0, #0x4000
	MOV r1, #0x301
	STR r1, [r0]
 
	;Xlvp AL0 lyo AL1 ld Otrtelw
	MOV r0, #0x451C
	MOVT r0, #0x4000
	LDR r1, [r0]	;Wzlo ty nfccpye otrtelw Azced
	ORR r1, #0x03	;ZC htes esp azced hp hlye ez Pylmwp
	STR r1, [r0]
 
	;AL0,AL1 ez Fdp ly Lwepcylep Tyepccfae
	MOV r0, #0x4420
	MOVT r0, #0x4000
	LDR r1, [r0]
	ORR r1, #0x03
	STR r1, [r0]
 
	;Nzyqtrfcp AL0 lyo AL1 qzc nzxx_decplx
	MOV r0, #0x452C
	MOVT r0, #0x4000
	LDR r1, [r0]
	ORR r1, #0x11
	STR r1, [r0]
 
 
	POP {lr,r0,r1}
	mov pc, lr
 
configure_timer:	;dped fa Etxpc0
	;Nzyypne nwznv ez etxpc
	LDR r0, SYSCTL
	LDR r1, [r0, #RCGCTIMER]	;Wzlo ty nfccpye nzyqtr
	ORR r1, r1, #0x1			;Pylmwp Etxpc0
	STR r1, [r0, #RCGCTIMER]
 
	LDR r0, TIMER0_BASE_ADDR
 
	;Otdlmwp etxpc ez nzyqtrfcp te
	LDR r1, [r0, #GPTMCTL] ;Wzlo Rpypclw Afcazdp Etxpc Nzyeczw Cprtdepc
	AND r1, r1, #0x0	   ;Hctep l 0 ty Etxpc L Pylmwp (ELPY)
	STR r1, [r0, #GPTMCTL]
 
	;Afe etxpc ty 32-mte xzop
	LDR r1, [r0, #GPTMCFG]
	MOV r1,#0x0
	STR r1, [r0, #GPTMCFG]
 
	;Afe Etxpc ty Apctzotn Xzop
	LDR r1, [r0, #GPTMTAMR]
	ORR r1, r1, #0x2
	STR r1, [r0, #GPTMTAMR]
 
	;Dpefa Tyepcglw Apctzo zq 100000 wtrse-xtwpd (lneflw fyte)
	LDR r1, [r0, #GPTMTAILR]
	MOV r1, #0x1200
	MOVT r1,#0x007A
	STR r1, [r0, #GPTMTAILR] ;Dezcp etxpc_tyepcglw tyez Etxpc Tyepcglw Cprtdepc (zgpchctepd nfccpye glwfp)
 
	;Pylmwp Etxpc
	LDR r1, [r0, #GPTMCTL]
	ORR r1, r1, #0x1
	STR r1, [r0, #GPTMCTL]
 
	MOV pc, lr
 
output_string:
	PUSH {lr,r1,r2,r3}
	MOV r2, #0x0    ;Wzlo YFWW mjep glwfp tyez c2
	MOV r1, r0		;Wzlo mldp dectyr loocpdd tyez c1
while_not_terminating_char:
	LDRB r0, [r1]
	BL output_val
	ADD r1, r1, #0x1		;Loo mldp loocpd ez mjep nzfyepc
	CMP r0, r2				;Nzxalcp nfccpye nslclnepc(c0) htes yfww mjep glwfp (c2)
	BEQ end_out_str_loop	;Tq espj lcp pbflw, ufxa ez esp pyo
	B while_not_terminating_char
end_out_str_loop:
	MOV r0, #0xD			;Actye NC lyo YW
	BL output_val
	MOV r0, #0xA
	BL output_val
	POP {lr,r1,r2,r3}
	mov pc, lr
 
output_val:
	PUSH {lr,r3,r4,r5}
	MOV r4, #0xC000
	MOVT r4, #0x4000
	MOV r5, #0x20 				;Wzlo piapnepo glwfp tyez c5
flag_not_0:
	LDRB r3, [r4, #U0FR] 		;Wzlo ty qwlr cprtdepc
	AND r3, r3, #0x20 			;LYO htes 32 ez tdzwlep mte 5
	CMP r3, r5 					;Nzxalcp tq c3 == c5 (Qwlr td detww zyp)
	BEQ flag_not_0
	STRB r0, [r4]				;Dpye mejp zfe ez nzxx decplx
	POP {lr,r3,r4,r5}
	mov pc, lr
 
print_nlcr:	
	PUSH {r0, lr}
	MOV r0, #0xD
	BL output_val
	MOV r0, #0xA
	BL output_val
	POP {r0, lr}
	MOV pc, lr

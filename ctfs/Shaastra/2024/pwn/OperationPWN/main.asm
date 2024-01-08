;Problem file
.CSEG;

LDI ZL,LOW(NUM<<1); load byte addrss of LSB of word addrss
LDI ZH,HIGH(NUM<<1);load byte addrss of MSB of word addrss
LPM R3,Z+;
LDI R20 , 0x0A;
LDI R22 , 0x04;
main:
	RJMP op1;

op1:
	MOV R16 , R3
	MOV R0,R3
	LDI R17, 0x01;
	RJMP loop1
loop1:
	MUL R3,R0
	MOV R4,R0
	MOV R0,R17
	MOV R18,R16
	RJMP loop2
	MUL R18,R0
	MOV R17,R0
	MOV R0,R4
	DEC R16
	CPI R16 , 0x00
	BRNE loop1
	ADD R0,R17
	MOV R3,R0
	RJMP op2

loop2:
	LSR R18
	BRCC loop2
	LSL R18
	INC R18
	RJMP 16

op2:
	DEC R3
	INC R3
	MUL R3,R3
	ADD R0,R22
	DEC R3
	DEC R3
	DEC R3
	MUL R3,R0
	MOV R3,R20
	ADD R3,R0
	CP R3,R21
	BRNE op2
end:
	RJMP end; If code reaches here you have found the answer
	NOP
NUM: .db 0x00; Load the guessed hex number here

Easy DreadFog
Intro

    Dark Backdoor managed to hijack our latest satellite! They managed to revoke our login credentials, effectively locking us out! Let's embark on a journey to hack them back! To do so, we first need to understand the hybrid low-energy extra-low memory complexity achitecture the satellite's processor uses...

The blueprints

    Luckily, one of the developers has kept the manual referencing all the opcodes, plus a test program written in the language! Don't you think finding a way to run this program would be useful?

Here is the manual:

Version: 0.7.0

Introducing Dread-ASM, the all-in-one assembly language that can be natively executed on all modern satellites! It runs on an architeccture that has the following properties:
Registers:

the usual RIP to count instructions
R0 and R1 registers for calculus
LCT is the loop count register. It keeps the index of the current loop within the program
PTR is a register that keeps a pointer to one of the cells of the buffer

The holy buffer

This super duper cool architecture has a whole 32*8 bit buffer, capable of holding up to 32 8-bit integers! Some may argue that it isn't enough, but it's only because their code isn't optimized enough!

Basic operations:

ADD R1 R2 : R1 <- (R1 + R2) % 0xff
MOV R1 cst : R1 <- cst
XOR R1 R2 : R1 <- R1 ^ (R2 + 3) % 0xff and no, this is not a bug, it's a feature!
CMP R1 R2 : classic comparison between R1 and R2
CLP cst: classic comparison between LCT and cst

Flow control:

three flags : is_bigger, is_equal and is_smaller
JRA cst : rip <- rip + cst ; you can read this opcode "jump relative always"
JRG cst : rip <- rip + cst if is_bigger flag set ; it reads "jump relative greater"
JRE cst : rip <- rip + cst if is_equal flag set ; it reads "jump relative equal"
JRL cst : rip <- rip + cst if is_smaller flag set ; it reads "jump relative lower"
INL cst: LCT = cst
ICL : LCT += 1
SPL: PTR = LCT

pointers and data:

LDA : R0 <- buf[PTR]
IPT : PTR <- (PTR + 3) % 32 ; The boss Jeb really wanted this feature, so here it is --'
LPT RI : RI <- PTR
STD RI : buf[PTR] <- RI

Additional properties:

The buffer is initialized with only zeroes.
All registers are initialized with a value equal to 1, except rip which starts at 0.
The comparison flags are set to True by default

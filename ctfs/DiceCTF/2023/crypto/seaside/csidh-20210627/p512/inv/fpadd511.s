
# qhasm: int64 input_0

# qhasm: int64 input_1

# qhasm: int64 input_2

# qhasm: int64 input_3

# qhasm: int64 input_4

# qhasm: int64 input_5

# qhasm: stack64 input_6

# qhasm: stack64 input_7

# qhasm: int64 caller_r11

# qhasm: int64 caller_r12

# qhasm: int64 caller_r13

# qhasm: int64 caller_r14

# qhasm: int64 caller_r15

# qhasm: int64 caller_rbx

# qhasm: int64 caller_rbp

# qhasm: const64 M_0 =  1982068743014369403
.p2align 5
M_0: .quad 1982068743014369403

# qhasm: const64 M_1 = 14011292126959937589
.p2align 5
M_1: .quad 14011292126959937589

# qhasm: const64 M_2 =  5865710692925656869
.p2align 5
M_2: .quad 5865710692925656869

# qhasm: const64 M_3 = 12081687501529634055
.p2align 5
M_3: .quad 12081687501529634055

# qhasm: const64 M_4 =  6556111612370143693
.p2align 5
M_4: .quad 6556111612370143693

# qhasm: const64 M_5 = 12983042349969476674
.p2align 5
M_5: .quad 12983042349969476674

# qhasm: const64 M_6 = 18197551657619704906
.p2align 5
M_6: .quad 18197551657619704906

# qhasm: const64 M_7 =  7328639240417282495
.p2align 5
M_7: .quad 7328639240417282495

# qhasm: int64 r0

# qhasm: int64 r1

# qhasm: int64 r2

# qhasm: int64 r3

# qhasm: int64 r4

# qhasm: int64 r5

# qhasm: int64 r6

# qhasm: int64 r7

# qhasm: stack64 caller_r11_stack

# qhasm: stack64 caller_r12_stack

# qhasm: stack64 caller_r13_stack

# qhasm: stack64 caller_r14_stack

# qhasm: stack64 caller_r15_stack

# qhasm: stack64 caller_rbp_stack

# qhasm: stack64 caller_rbx_stack

# qhasm: stack64 input_0_save

# qhasm: stack64 input_1_save

# qhasm: stack64 input_2_save

# qhasm: enter fpadd511
.p2align 5
.global _fpadd511
.global fpadd511
_fpadd511:
fpadd511:
mov %rsp,%r11
and $31,%r11
add $64,%r11
sub %r11,%rsp

# qhasm: caller_r11_stack = caller_r11
# asm 1: movq <caller_r11=int64#9,>caller_r11_stack=stack64#1
# asm 2: movq <caller_r11=%r11,>caller_r11_stack=0(%rsp)
movq %r11,0(%rsp)

# qhasm: caller_r12_stack = caller_r12
# asm 1: movq <caller_r12=int64#10,>caller_r12_stack=stack64#2
# asm 2: movq <caller_r12=%r12,>caller_r12_stack=8(%rsp)
movq %r12,8(%rsp)

# qhasm: caller_r13_stack = caller_r13
# asm 1: movq <caller_r13=int64#11,>caller_r13_stack=stack64#3
# asm 2: movq <caller_r13=%r13,>caller_r13_stack=16(%rsp)
movq %r13,16(%rsp)

# qhasm: caller_r14_stack = caller_r14
# asm 1: movq <caller_r14=int64#12,>caller_r14_stack=stack64#4
# asm 2: movq <caller_r14=%r14,>caller_r14_stack=24(%rsp)
movq %r14,24(%rsp)

# qhasm: caller_r15_stack = caller_r15
# asm 1: movq <caller_r15=int64#13,>caller_r15_stack=stack64#5
# asm 2: movq <caller_r15=%r15,>caller_r15_stack=32(%rsp)
movq %r15,32(%rsp)

# qhasm: caller_rbx_stack = caller_rbx
# asm 1: movq <caller_rbx=int64#14,>caller_rbx_stack=stack64#6
# asm 2: movq <caller_rbx=%rbx,>caller_rbx_stack=40(%rsp)
movq %rbx,40(%rsp)

# qhasm: caller_rbp_stack = caller_rbp
# asm 1: movq <caller_rbp=int64#15,>caller_rbp_stack=stack64#7
# asm 2: movq <caller_rbp=%rbp,>caller_rbp_stack=48(%rsp)
movq %rbp,48(%rsp)

# qhasm: r0 = mem64[ input_0 + 0 ]
# asm 1: movq   0(<input_0=int64#1),>r0=int64#4
# asm 2: movq   0(<input_0=%rdi),>r0=%rcx
movq   0(%rdi),%rcx

# qhasm: r1 = mem64[ input_0 + 8 ]
# asm 1: movq   8(<input_0=int64#1),>r1=int64#5
# asm 2: movq   8(<input_0=%rdi),>r1=%r8
movq   8(%rdi),%r8

# qhasm: r2 = mem64[ input_0 +16 ]
# asm 1: movq   16(<input_0=int64#1),>r2=int64#6
# asm 2: movq   16(<input_0=%rdi),>r2=%r9
movq   16(%rdi),%r9

# qhasm: r3 = mem64[ input_0 +24 ]
# asm 1: movq   24(<input_0=int64#1),>r3=int64#7
# asm 2: movq   24(<input_0=%rdi),>r3=%rax
movq   24(%rdi),%rax

# qhasm: r4 = mem64[ input_0 +32 ]
# asm 1: movq   32(<input_0=int64#1),>r4=int64#8
# asm 2: movq   32(<input_0=%rdi),>r4=%r10
movq   32(%rdi),%r10

# qhasm: r5 = mem64[ input_0 +40 ]
# asm 1: movq   40(<input_0=int64#1),>r5=int64#9
# asm 2: movq   40(<input_0=%rdi),>r5=%r11
movq   40(%rdi),%r11

# qhasm: r6 = mem64[ input_0 +48 ]
# asm 1: movq   48(<input_0=int64#1),>r6=int64#10
# asm 2: movq   48(<input_0=%rdi),>r6=%r12
movq   48(%rdi),%r12

# qhasm: r7 = mem64[ input_0 +56 ]
# asm 1: movq   56(<input_0=int64#1),>r7=int64#1
# asm 2: movq   56(<input_0=%rdi),>r7=%rdi
movq   56(%rdi),%rdi

# qhasm: carry? r0 += mem64[ input_1 + 0]
# asm 1: addq 0(<input_1=int64#2),<r0=int64#4
# asm 2: addq 0(<input_1=%rsi),<r0=%rcx
addq 0(%rsi),%rcx

# qhasm: carry? r1 += mem64[ input_1 + 8] + carry
# asm 1: adcq 8(<input_1=int64#2),<r1=int64#5
# asm 2: adcq 8(<input_1=%rsi),<r1=%r8
adcq 8(%rsi),%r8

# qhasm: carry? r2 += mem64[ input_1 +16] + carry
# asm 1: adcq 16(<input_1=int64#2),<r2=int64#6
# asm 2: adcq 16(<input_1=%rsi),<r2=%r9
adcq 16(%rsi),%r9

# qhasm: carry? r3 += mem64[ input_1 +24] + carry
# asm 1: adcq 24(<input_1=int64#2),<r3=int64#7
# asm 2: adcq 24(<input_1=%rsi),<r3=%rax
adcq 24(%rsi),%rax

# qhasm: carry? r4 += mem64[ input_1 +32] + carry
# asm 1: adcq 32(<input_1=int64#2),<r4=int64#8
# asm 2: adcq 32(<input_1=%rsi),<r4=%r10
adcq 32(%rsi),%r10

# qhasm: carry? r5 += mem64[ input_1 +40] + carry
# asm 1: adcq 40(<input_1=int64#2),<r5=int64#9
# asm 2: adcq 40(<input_1=%rsi),<r5=%r11
adcq 40(%rsi),%r11

# qhasm: carry? r6 += mem64[ input_1 +48] + carry
# asm 1: adcq 48(<input_1=int64#2),<r6=int64#10
# asm 2: adcq 48(<input_1=%rsi),<r6=%r12
adcq 48(%rsi),%r12

# qhasm: r7 += mem64[ input_1 +56] + carry
# asm 1: adcq 56(<input_1=int64#2),<r7=int64#1
# asm 2: adcq 56(<input_1=%rsi),<r7=%rdi
adcq 56(%rsi),%rdi

# qhasm: *(uint64 *)(input_2 + 0) = r0
# asm 1: movq   <r0=int64#4,0(<input_2=int64#3)
# asm 2: movq   <r0=%rcx,0(<input_2=%rdx)
movq   %rcx,0(%rdx)

# qhasm: *(uint64 *)(input_2 + 8) = r1
# asm 1: movq   <r1=int64#5,8(<input_2=int64#3)
# asm 2: movq   <r1=%r8,8(<input_2=%rdx)
movq   %r8,8(%rdx)

# qhasm: *(uint64 *)(input_2 + 16) = r2
# asm 1: movq   <r2=int64#6,16(<input_2=int64#3)
# asm 2: movq   <r2=%r9,16(<input_2=%rdx)
movq   %r9,16(%rdx)

# qhasm: *(uint64 *)(input_2 + 24) = r3
# asm 1: movq   <r3=int64#7,24(<input_2=int64#3)
# asm 2: movq   <r3=%rax,24(<input_2=%rdx)
movq   %rax,24(%rdx)

# qhasm: *(uint64 *)(input_2 + 32) = r4
# asm 1: movq   <r4=int64#8,32(<input_2=int64#3)
# asm 2: movq   <r4=%r10,32(<input_2=%rdx)
movq   %r10,32(%rdx)

# qhasm: *(uint64 *)(input_2 + 40) = r5
# asm 1: movq   <r5=int64#9,40(<input_2=int64#3)
# asm 2: movq   <r5=%r11,40(<input_2=%rdx)
movq   %r11,40(%rdx)

# qhasm: *(uint64 *)(input_2 + 48) = r6
# asm 1: movq   <r6=int64#10,48(<input_2=int64#3)
# asm 2: movq   <r6=%r12,48(<input_2=%rdx)
movq   %r12,48(%rdx)

# qhasm: *(uint64 *)(input_2 + 56) = r7
# asm 1: movq   <r7=int64#1,56(<input_2=int64#3)
# asm 2: movq   <r7=%rdi,56(<input_2=%rdx)
movq   %rdi,56(%rdx)

# qhasm: carry? r0 -= mem64[M_0]
# asm 1: sub  M_0,<r0=int64#4
# asm 2: sub  M_0,<r0=%rcx
sub  M_0(%rip),%rcx

# qhasm: carry? r1 -= mem64[M_1] - carry
# asm 1: sbb  M_1,<r1=int64#5
# asm 2: sbb  M_1,<r1=%r8
sbb  M_1(%rip),%r8

# qhasm: carry? r2 -= mem64[M_2] - carry
# asm 1: sbb  M_2,<r2=int64#6
# asm 2: sbb  M_2,<r2=%r9
sbb  M_2(%rip),%r9

# qhasm: carry? r3 -= mem64[M_3] - carry
# asm 1: sbb  M_3,<r3=int64#7
# asm 2: sbb  M_3,<r3=%rax
sbb  M_3(%rip),%rax

# qhasm: carry? r4 -= mem64[M_4] - carry
# asm 1: sbb  M_4,<r4=int64#8
# asm 2: sbb  M_4,<r4=%r10
sbb  M_4(%rip),%r10

# qhasm: carry? r5 -= mem64[M_5] - carry
# asm 1: sbb  M_5,<r5=int64#9
# asm 2: sbb  M_5,<r5=%r11
sbb  M_5(%rip),%r11

# qhasm: carry? r6 -= mem64[M_6] - carry
# asm 1: sbb  M_6,<r6=int64#10
# asm 2: sbb  M_6,<r6=%r12
sbb  M_6(%rip),%r12

# qhasm: carry? r7 -= mem64[M_7] - carry
# asm 1: sbb  M_7,<r7=int64#1
# asm 2: sbb  M_7,<r7=%rdi
sbb  M_7(%rip),%rdi

# qhasm: r0 = mem64[ input_2 + 0 ] if carry
# asm 1: cmovc 0(<input_2=int64#3),<r0=int64#4
# asm 2: cmovc 0(<input_2=%rdx),<r0=%rcx
cmovc 0(%rdx),%rcx

# qhasm: r1 = mem64[ input_2 + 8 ] if carry
# asm 1: cmovc 8(<input_2=int64#3),<r1=int64#5
# asm 2: cmovc 8(<input_2=%rdx),<r1=%r8
cmovc 8(%rdx),%r8

# qhasm: r2 = mem64[ input_2 +16 ] if carry
# asm 1: cmovc 16(<input_2=int64#3),<r2=int64#6
# asm 2: cmovc 16(<input_2=%rdx),<r2=%r9
cmovc 16(%rdx),%r9

# qhasm: r3 = mem64[ input_2 +24 ] if carry
# asm 1: cmovc 24(<input_2=int64#3),<r3=int64#7
# asm 2: cmovc 24(<input_2=%rdx),<r3=%rax
cmovc 24(%rdx),%rax

# qhasm: r4 = mem64[ input_2 +32 ] if carry
# asm 1: cmovc 32(<input_2=int64#3),<r4=int64#8
# asm 2: cmovc 32(<input_2=%rdx),<r4=%r10
cmovc 32(%rdx),%r10

# qhasm: r5 = mem64[ input_2 +40 ] if carry
# asm 1: cmovc 40(<input_2=int64#3),<r5=int64#9
# asm 2: cmovc 40(<input_2=%rdx),<r5=%r11
cmovc 40(%rdx),%r11

# qhasm: r6 = mem64[ input_2 +48 ] if carry
# asm 1: cmovc 48(<input_2=int64#3),<r6=int64#10
# asm 2: cmovc 48(<input_2=%rdx),<r6=%r12
cmovc 48(%rdx),%r12

# qhasm: r7 = mem64[ input_2 +56 ] if carry
# asm 1: cmovc 56(<input_2=int64#3),<r7=int64#1
# asm 2: cmovc 56(<input_2=%rdx),<r7=%rdi
cmovc 56(%rdx),%rdi

# qhasm: *(uint64 *)(input_2 + 0) = r0
# asm 1: movq   <r0=int64#4,0(<input_2=int64#3)
# asm 2: movq   <r0=%rcx,0(<input_2=%rdx)
movq   %rcx,0(%rdx)

# qhasm: *(uint64 *)(input_2 + 8) = r1
# asm 1: movq   <r1=int64#5,8(<input_2=int64#3)
# asm 2: movq   <r1=%r8,8(<input_2=%rdx)
movq   %r8,8(%rdx)

# qhasm: *(uint64 *)(input_2 + 16) = r2
# asm 1: movq   <r2=int64#6,16(<input_2=int64#3)
# asm 2: movq   <r2=%r9,16(<input_2=%rdx)
movq   %r9,16(%rdx)

# qhasm: *(uint64 *)(input_2 + 24) = r3
# asm 1: movq   <r3=int64#7,24(<input_2=int64#3)
# asm 2: movq   <r3=%rax,24(<input_2=%rdx)
movq   %rax,24(%rdx)

# qhasm: *(uint64 *)(input_2 + 32) = r4
# asm 1: movq   <r4=int64#8,32(<input_2=int64#3)
# asm 2: movq   <r4=%r10,32(<input_2=%rdx)
movq   %r10,32(%rdx)

# qhasm: *(uint64 *)(input_2 + 40) = r5
# asm 1: movq   <r5=int64#9,40(<input_2=int64#3)
# asm 2: movq   <r5=%r11,40(<input_2=%rdx)
movq   %r11,40(%rdx)

# qhasm: *(uint64 *)(input_2 + 48) = r6
# asm 1: movq   <r6=int64#10,48(<input_2=int64#3)
# asm 2: movq   <r6=%r12,48(<input_2=%rdx)
movq   %r12,48(%rdx)

# qhasm: *(uint64 *)(input_2 + 56) = r7
# asm 1: movq   <r7=int64#1,56(<input_2=int64#3)
# asm 2: movq   <r7=%rdi,56(<input_2=%rdx)
movq   %rdi,56(%rdx)

# qhasm: caller_r11 = caller_r11_stack
# asm 1: movq <caller_r11_stack=stack64#1,>caller_r11=int64#9
# asm 2: movq <caller_r11_stack=0(%rsp),>caller_r11=%r11
movq 0(%rsp),%r11

# qhasm: caller_r12 = caller_r12_stack
# asm 1: movq <caller_r12_stack=stack64#2,>caller_r12=int64#10
# asm 2: movq <caller_r12_stack=8(%rsp),>caller_r12=%r12
movq 8(%rsp),%r12

# qhasm: caller_r13 = caller_r13_stack
# asm 1: movq <caller_r13_stack=stack64#3,>caller_r13=int64#11
# asm 2: movq <caller_r13_stack=16(%rsp),>caller_r13=%r13
movq 16(%rsp),%r13

# qhasm: caller_r14 = caller_r14_stack
# asm 1: movq <caller_r14_stack=stack64#4,>caller_r14=int64#12
# asm 2: movq <caller_r14_stack=24(%rsp),>caller_r14=%r14
movq 24(%rsp),%r14

# qhasm: caller_r15 = caller_r15_stack
# asm 1: movq <caller_r15_stack=stack64#5,>caller_r15=int64#13
# asm 2: movq <caller_r15_stack=32(%rsp),>caller_r15=%r15
movq 32(%rsp),%r15

# qhasm: caller_rbx = caller_rbx_stack
# asm 1: movq <caller_rbx_stack=stack64#6,>caller_rbx=int64#14
# asm 2: movq <caller_rbx_stack=40(%rsp),>caller_rbx=%rbx
movq 40(%rsp),%rbx

# qhasm: caller_rbp = caller_rbp_stack
# asm 1: movq <caller_rbp_stack=stack64#7,>caller_rbp=int64#15
# asm 2: movq <caller_rbp_stack=48(%rsp),>caller_rbp=%rbp
movq 48(%rsp),%rbp

# qhasm: return
add %r11,%rsp
ret

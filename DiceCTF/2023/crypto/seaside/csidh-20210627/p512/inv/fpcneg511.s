
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

# qhasm: int64 t0

# qhasm: int64 t1

# qhasm: int64 t2

# qhasm: int64 t3

# qhasm: int64 t4

# qhasm: int64 t5

# qhasm: int64 t6

# qhasm: int64 t7

# qhasm: stack64 caller_r11_stack

# qhasm: stack64 caller_r12_stack

# qhasm: stack64 caller_r13_stack

# qhasm: stack64 caller_r14_stack

# qhasm: stack64 caller_r15_stack

# qhasm: stack64 caller_rbp_stack

# qhasm: stack64 caller_rbx_stack

# qhasm: enter fpcneg511
.p2align 5
.global _fpcneg511
.global fpcneg511
_fpcneg511:
fpcneg511:
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

# qhasm: t0 = mem64[ M_0 ]
# asm 1: movq M_0,>t0=int64#3
# asm 2: movq M_0,>t0=%rdx
movq M_0(%rip),%rdx

# qhasm: t1 = mem64[ M_1 ]
# asm 1: movq M_1,>t1=int64#4
# asm 2: movq M_1,>t1=%rcx
movq M_1(%rip),%rcx

# qhasm: t2 = mem64[ M_2 ]
# asm 1: movq M_2,>t2=int64#5
# asm 2: movq M_2,>t2=%r8
movq M_2(%rip),%r8

# qhasm: t3 = mem64[ M_3 ]
# asm 1: movq M_3,>t3=int64#6
# asm 2: movq M_3,>t3=%r9
movq M_3(%rip),%r9

# qhasm: t4 = mem64[ M_4 ]
# asm 1: movq M_4,>t4=int64#7
# asm 2: movq M_4,>t4=%rax
movq M_4(%rip),%rax

# qhasm: t5 = mem64[ M_5 ]
# asm 1: movq M_5,>t5=int64#8
# asm 2: movq M_5,>t5=%r10
movq M_5(%rip),%r10

# qhasm: t6 = mem64[ M_6 ]
# asm 1: movq M_6,>t6=int64#9
# asm 2: movq M_6,>t6=%r11
movq M_6(%rip),%r11

# qhasm: t7 = mem64[ M_7 ]
# asm 1: movq M_7,>t7=int64#10
# asm 2: movq M_7,>t7=%r12
movq M_7(%rip),%r12

# qhasm: carry? t0 -= mem64[ input_0 + 0 ]
# asm 1: subq 0(<input_0=int64#1),<t0=int64#3
# asm 2: subq 0(<input_0=%rdi),<t0=%rdx
subq 0(%rdi),%rdx

# qhasm: carry? t1 -= mem64[ input_0 + 8 ] - carry
# asm 1: sbbq 8(<input_0=int64#1),<t1=int64#4
# asm 2: sbbq 8(<input_0=%rdi),<t1=%rcx
sbbq 8(%rdi),%rcx

# qhasm: carry? t2 -= mem64[ input_0 +16 ] - carry
# asm 1: sbbq 16(<input_0=int64#1),<t2=int64#5
# asm 2: sbbq 16(<input_0=%rdi),<t2=%r8
sbbq 16(%rdi),%r8

# qhasm: carry? t3 -= mem64[ input_0 +24 ] - carry
# asm 1: sbbq 24(<input_0=int64#1),<t3=int64#6
# asm 2: sbbq 24(<input_0=%rdi),<t3=%r9
sbbq 24(%rdi),%r9

# qhasm: carry? t4 -= mem64[ input_0 +32 ] - carry
# asm 1: sbbq 32(<input_0=int64#1),<t4=int64#7
# asm 2: sbbq 32(<input_0=%rdi),<t4=%rax
sbbq 32(%rdi),%rax

# qhasm: carry? t5 -= mem64[ input_0 +40 ] - carry
# asm 1: sbbq 40(<input_0=int64#1),<t5=int64#8
# asm 2: sbbq 40(<input_0=%rdi),<t5=%r10
sbbq 40(%rdi),%r10

# qhasm: carry? t6 -= mem64[ input_0 +48 ] - carry
# asm 1: sbbq 48(<input_0=int64#1),<t6=int64#9
# asm 2: sbbq 48(<input_0=%rdi),<t6=%r11
sbbq 48(%rdi),%r11

# qhasm: t7 -= mem64[ input_0 +56 ] - carry
# asm 1: sbbq 56(<input_0=int64#1),<t7=int64#10
# asm 2: sbbq 56(<input_0=%rdi),<t7=%r12
sbbq 56(%rdi),%r12

# qhasm: =? input_1 & 2
# asm 1: test  $2,<input_1=int64#2
# asm 2: test  $2,<input_1=%rsi
test  $2,%rsi

# qhasm: t0 = mem64[ input_0 + 0 ] if =
# asm 1: cmove 0(<input_0=int64#1),<t0=int64#3
# asm 2: cmove 0(<input_0=%rdi),<t0=%rdx
cmove 0(%rdi),%rdx

# qhasm: t1 = mem64[ input_0 + 8 ] if =
# asm 1: cmove 8(<input_0=int64#1),<t1=int64#4
# asm 2: cmove 8(<input_0=%rdi),<t1=%rcx
cmove 8(%rdi),%rcx

# qhasm: t2 = mem64[ input_0 +16 ] if =
# asm 1: cmove 16(<input_0=int64#1),<t2=int64#5
# asm 2: cmove 16(<input_0=%rdi),<t2=%r8
cmove 16(%rdi),%r8

# qhasm: t3 = mem64[ input_0 +24 ] if =
# asm 1: cmove 24(<input_0=int64#1),<t3=int64#6
# asm 2: cmove 24(<input_0=%rdi),<t3=%r9
cmove 24(%rdi),%r9

# qhasm: t4 = mem64[ input_0 +32 ] if =
# asm 1: cmove 32(<input_0=int64#1),<t4=int64#7
# asm 2: cmove 32(<input_0=%rdi),<t4=%rax
cmove 32(%rdi),%rax

# qhasm: t5 = mem64[ input_0 +40 ] if =
# asm 1: cmove 40(<input_0=int64#1),<t5=int64#8
# asm 2: cmove 40(<input_0=%rdi),<t5=%r10
cmove 40(%rdi),%r10

# qhasm: t6 = mem64[ input_0 +48 ] if =
# asm 1: cmove 48(<input_0=int64#1),<t6=int64#9
# asm 2: cmove 48(<input_0=%rdi),<t6=%r11
cmove 48(%rdi),%r11

# qhasm: t7 = mem64[ input_0 +56 ] if =
# asm 1: cmove 56(<input_0=int64#1),<t7=int64#10
# asm 2: cmove 56(<input_0=%rdi),<t7=%r12
cmove 56(%rdi),%r12

# qhasm: mem64[ input_0 + 0 ] = t0 
# asm 1: movq   <t0=int64#3,0(<input_0=int64#1)
# asm 2: movq   <t0=%rdx,0(<input_0=%rdi)
movq   %rdx,0(%rdi)

# qhasm: mem64[ input_0 + 8 ] = t1 
# asm 1: movq   <t1=int64#4,8(<input_0=int64#1)
# asm 2: movq   <t1=%rcx,8(<input_0=%rdi)
movq   %rcx,8(%rdi)

# qhasm: mem64[ input_0 +16 ] = t2 
# asm 1: movq   <t2=int64#5,16(<input_0=int64#1)
# asm 2: movq   <t2=%r8,16(<input_0=%rdi)
movq   %r8,16(%rdi)

# qhasm: mem64[ input_0 +24 ] = t3 
# asm 1: movq   <t3=int64#6,24(<input_0=int64#1)
# asm 2: movq   <t3=%r9,24(<input_0=%rdi)
movq   %r9,24(%rdi)

# qhasm: mem64[ input_0 +32 ] = t4 
# asm 1: movq   <t4=int64#7,32(<input_0=int64#1)
# asm 2: movq   <t4=%rax,32(<input_0=%rdi)
movq   %rax,32(%rdi)

# qhasm: mem64[ input_0 +40 ] = t5 
# asm 1: movq   <t5=int64#8,40(<input_0=int64#1)
# asm 2: movq   <t5=%r10,40(<input_0=%rdi)
movq   %r10,40(%rdi)

# qhasm: mem64[ input_0 +48 ] = t6 
# asm 1: movq   <t6=int64#9,48(<input_0=int64#1)
# asm 2: movq   <t6=%r11,48(<input_0=%rdi)
movq   %r11,48(%rdi)

# qhasm: mem64[ input_0 +56 ] = t7 
# asm 1: movq   <t7=int64#10,56(<input_0=int64#1)
# asm 2: movq   <t7=%r12,56(<input_0=%rdi)
movq   %r12,56(%rdi)

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

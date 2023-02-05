
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

# qhasm: const64 M_0 = 1982068743014369403
.p2align 5
M_0: .quad 1982068743014369403

# qhasm: const64 M_1 = 14011292126959937589
.p2align 5
M_1: .quad 14011292126959937589

# qhasm: const64 M_2 = 5865710692925656869
.p2align 5
M_2: .quad 5865710692925656869

# qhasm: const64 M_3 = 12081687501529634055
.p2align 5
M_3: .quad 12081687501529634055

# qhasm: const64 M_4 = 6556111612370143693
.p2align 5
M_4: .quad 6556111612370143693

# qhasm: const64 M_5 = 12983042349969476674
.p2align 5
M_5: .quad 12983042349969476674

# qhasm: const64 M_6 = 18197551657619704906
.p2align 5
M_6: .quad 18197551657619704906

# qhasm: const64 M_7 = 7328639240417282495
.p2align 5
M_7: .quad 7328639240417282495

# qhasm: const64 M1 = 7404252173739895117
.p2align 5
M1: .quad 7404252173739895117

# qhasm: int64 t0

# qhasm: int64 t1

# qhasm: int64 t2

# qhasm: int64 t3

# qhasm: int64 t4

# qhasm: int64 t5

# qhasm: int64 t6

# qhasm: int64 t7

# qhasm: int64 t8

# qhasm: int64 rax

# qhasm: int64 rdx

# qhasm: int64 mulc

# qhasm: int64 M

# qhasm: int64 L

# qhasm: int64 mulx0

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

# qhasm: stack64 input_3_save

# qhasm: stack64 M1_save

# qhasm: enter fpmul511
.p2align 5
.global _fpmul511
.global fpmul511
_fpmul511:
fpmul511:
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

# qhasm: input_2_save = input_2
# asm 1: movq <input_2=int64#3,>input_2_save=stack64#8
# asm 2: movq <input_2=%rdx,>input_2_save=56(%rsp)
movq %rdx,56(%rsp)

# qhasm: M = input_3
# asm 1: mov  <input_3=int64#4,>M=int64#4
# asm 2: mov  <input_3=%rcx,>M=%rcx
mov  %rcx,%rcx

# qhasm: t0 ^= t0
# asm 1: xor >t0=int64#5,>t0=int64#5
# asm 2: xor >t0=%r8,>t0=%r8
xor %r8,%r8

# qhasm: t1 ^= t1
# asm 1: xor >t1=int64#6,>t1=int64#6
# asm 2: xor >t1=%r9,>t1=%r9
xor %r9,%r9

# qhasm: t2 ^= t2
# asm 1: xor >t2=int64#8,>t2=int64#8
# asm 2: xor >t2=%r10,>t2=%r10
xor %r10,%r10

# qhasm: t3 ^= t3
# asm 1: xor >t3=int64#9,>t3=int64#9
# asm 2: xor >t3=%r11,>t3=%r11
xor %r11,%r11

# qhasm: t4 ^= t4
# asm 1: xor >t4=int64#10,>t4=int64#10
# asm 2: xor >t4=%r12,>t4=%r12
xor %r12,%r12

# qhasm: t5 ^= t5
# asm 1: xor >t5=int64#11,>t5=int64#11
# asm 2: xor >t5=%r13,>t5=%r13
xor %r13,%r13

# qhasm: t6 ^= t6
# asm 1: xor >t6=int64#12,>t6=int64#12
# asm 2: xor >t6=%r14,>t6=%r14
xor %r14,%r14

# qhasm: t7 ^= t7
# asm 1: xor >t7=int64#13,>t7=int64#13
# asm 2: xor >t7=%r15,>t7=%r15
xor %r15,%r15

# qhasm: mulc ^= mulc
# asm 1: xor >mulc=int64#14,>mulc=int64#14
# asm 2: xor >mulc=%rbx,>mulc=%rbx
xor %rbx,%rbx

# qhasm:   rax = mem64[input_1 + 0] 
# asm 1: movq   0(<input_1=int64#2),>rax=int64#7
# asm 2: movq   0(<input_1=%rsi),>rax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 0] 
# asm 1: mulq  0(<input_0=int64#1)
# asm 2: mulq  0(<input_0=%rdi)
mulq  0(%rdi)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#5
# asm 2: add  <rax=%rax,<t0=%r8
add  %rax,%r8

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#6
# asm 2: adc <rdx=%rdx,<t1=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#14
# asm 2: adc $0,<mulc=%rbx
adc $0,%rbx

# qhasm:   mulx0 = mem64[M1] 
# asm 1: movq M1,>mulx0=int64#15
# asm 2: movq M1,>mulx0=%rbp
movq M1(%rip),%rbp

# qhasm:   mulx0 *= t0 
# asm 1: imul  <t0=int64#5,<mulx0=int64#15
# asm 2: imul  <t0=%r8,<mulx0=%rbp
imul  %r8,%rbp

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 0] 
# asm 1: mulq  0(<M=int64#4)
# asm 2: mulq  0(<M=%rcx)
mulq  0(%rcx)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#5
# asm 2: add  <rax=%rax,<t0=%r8
add  %rax,%r8

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#6
# asm 2: adc <rdx=%rdx,<t1=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#14
# asm 2: adc $0,<mulc=%rbx
adc $0,%rbx

# qhasm:   carry? t2 += mulc 
# asm 1: add  <mulc=int64#14,<t2=int64#8
# asm 2: add  <mulc=%rbx,<t2=%r10
add  %rbx,%r10

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 0] 
# asm 1: movq   0(<input_1=int64#2),>rax=int64#7
# asm 2: movq   0(<input_1=%rsi),>rax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 8] 
# asm 1: mulq  8(<input_0=int64#1)
# asm 2: mulq  8(<input_0=%rdi)
mulq  8(%rdi)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#6
# asm 2: add  <rax=%rax,<t1=%r9
add  %rax,%r9

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#8
# asm 2: adc <rdx=%rdx,<t2=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 8] 
# asm 1: mulq  8(<M=int64#4)
# asm 2: mulq  8(<M=%rcx)
mulq  8(%rcx)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#6
# asm 2: add  <rax=%rax,<t1=%r9
add  %rax,%r9

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#8
# asm 2: adc <rdx=%rdx,<t2=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t3 += mulc 
# asm 1: add  <mulc=int64#5,<t3=int64#9
# asm 2: add  <mulc=%r8,<t3=%r11
add  %r8,%r11

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 0] 
# asm 1: movq   0(<input_1=int64#2),>rax=int64#7
# asm 2: movq   0(<input_1=%rsi),>rax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +16] 
# asm 1: mulq  16(<input_0=int64#1)
# asm 2: mulq  16(<input_0=%rdi)
mulq  16(%rdi)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#8
# asm 2: add  <rax=%rax,<t2=%r10
add  %rax,%r10

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#9
# asm 2: adc <rdx=%rdx,<t3=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +16] 
# asm 1: mulq  16(<M=int64#4)
# asm 2: mulq  16(<M=%rcx)
mulq  16(%rcx)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#8
# asm 2: add  <rax=%rax,<t2=%r10
add  %rax,%r10

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#9
# asm 2: adc <rdx=%rdx,<t3=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t4 += mulc 
# asm 1: add  <mulc=int64#5,<t4=int64#10
# asm 2: add  <mulc=%r8,<t4=%r12
add  %r8,%r12

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 0] 
# asm 1: movq   0(<input_1=int64#2),>rax=int64#7
# asm 2: movq   0(<input_1=%rsi),>rax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +24] 
# asm 1: mulq  24(<input_0=int64#1)
# asm 2: mulq  24(<input_0=%rdi)
mulq  24(%rdi)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#9
# asm 2: add  <rax=%rax,<t3=%r11
add  %rax,%r11

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#10
# asm 2: adc <rdx=%rdx,<t4=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +24] 
# asm 1: mulq  24(<M=int64#4)
# asm 2: mulq  24(<M=%rcx)
mulq  24(%rcx)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#9
# asm 2: add  <rax=%rax,<t3=%r11
add  %rax,%r11

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#10
# asm 2: adc <rdx=%rdx,<t4=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t5 += mulc 
# asm 1: add  <mulc=int64#5,<t5=int64#11
# asm 2: add  <mulc=%r8,<t5=%r13
add  %r8,%r13

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 0] 
# asm 1: movq   0(<input_1=int64#2),>rax=int64#7
# asm 2: movq   0(<input_1=%rsi),>rax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +32] 
# asm 1: mulq  32(<input_0=int64#1)
# asm 2: mulq  32(<input_0=%rdi)
mulq  32(%rdi)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +32] 
# asm 1: mulq  32(<M=int64#4)
# asm 2: mulq  32(<M=%rcx)
mulq  32(%rcx)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t6 += mulc 
# asm 1: add  <mulc=int64#5,<t6=int64#12
# asm 2: add  <mulc=%r8,<t6=%r14
add  %r8,%r14

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 0] 
# asm 1: movq   0(<input_1=int64#2),>rax=int64#7
# asm 2: movq   0(<input_1=%rsi),>rax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +40] 
# asm 1: mulq  40(<input_0=int64#1)
# asm 2: mulq  40(<input_0=%rdi)
mulq  40(%rdi)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +40] 
# asm 1: mulq  40(<M=int64#4)
# asm 2: mulq  40(<M=%rcx)
mulq  40(%rcx)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t7 += mulc 
# asm 1: add  <mulc=int64#5,<t7=int64#13
# asm 2: add  <mulc=%r8,<t7=%r15
add  %r8,%r15

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 0] 
# asm 1: movq   0(<input_1=int64#2),>rax=int64#7
# asm 2: movq   0(<input_1=%rsi),>rax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +48] 
# asm 1: mulq  48(<input_0=int64#1)
# asm 2: mulq  48(<input_0=%rdi)
mulq  48(%rdi)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +48] 
# asm 1: mulq  48(<M=int64#4)
# asm 2: mulq  48(<M=%rcx)
mulq  48(%rcx)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   t8 = 0 
# asm 1: mov  $0,>t8=int64#14
# asm 2: mov  $0,>t8=%rbx
mov  $0,%rbx

# qhasm:   carry? t8 += mulc 
# asm 1: add  <mulc=int64#5,<t8=int64#14
# asm 2: add  <mulc=%r8,<t8=%rbx
add  %r8,%rbx

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 0] 
# asm 1: movq   0(<input_1=int64#2),>rax=int64#7
# asm 2: movq   0(<input_1=%rsi),>rax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +56] 
# asm 1: mulq  56(<input_0=int64#1)
# asm 2: mulq  56(<input_0=%rdi)
mulq  56(%rdi)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +56] 
# asm 1: mulq  56(<M=int64#4)
# asm 2: mulq  56(<M=%rcx)
mulq  56(%rcx)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   t8 += mulc 
# asm 1: add  <mulc=int64#5,<t8=int64#14
# asm 2: add  <mulc=%r8,<t8=%rbx
add  %r8,%rbx

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   rax = mem64[input_1 + 8] 
# asm 1: movq   8(<input_1=int64#2),>rax=int64#7
# asm 2: movq   8(<input_1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 0] 
# asm 1: mulq  0(<input_0=int64#1)
# asm 2: mulq  0(<input_0=%rdi)
mulq  0(%rdi)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#6
# asm 2: add  <rax=%rax,<t1=%r9
add  %rax,%r9

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#8
# asm 2: adc <rdx=%rdx,<t2=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   mulx0 = mem64[M1] 
# asm 1: movq M1,>mulx0=int64#15
# asm 2: movq M1,>mulx0=%rbp
movq M1(%rip),%rbp

# qhasm:   mulx0 *= t1 
# asm 1: imul  <t1=int64#6,<mulx0=int64#15
# asm 2: imul  <t1=%r9,<mulx0=%rbp
imul  %r9,%rbp

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 0] 
# asm 1: mulq  0(<M=int64#4)
# asm 2: mulq  0(<M=%rcx)
mulq  0(%rcx)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#6
# asm 2: add  <rax=%rax,<t1=%r9
add  %rax,%r9

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#8
# asm 2: adc <rdx=%rdx,<t2=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t3 += mulc 
# asm 1: add  <mulc=int64#5,<t3=int64#9
# asm 2: add  <mulc=%r8,<t3=%r11
add  %r8,%r11

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 8] 
# asm 1: movq   8(<input_1=int64#2),>rax=int64#7
# asm 2: movq   8(<input_1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 8] 
# asm 1: mulq  8(<input_0=int64#1)
# asm 2: mulq  8(<input_0=%rdi)
mulq  8(%rdi)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#8
# asm 2: add  <rax=%rax,<t2=%r10
add  %rax,%r10

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#9
# asm 2: adc <rdx=%rdx,<t3=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 8] 
# asm 1: mulq  8(<M=int64#4)
# asm 2: mulq  8(<M=%rcx)
mulq  8(%rcx)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#8
# asm 2: add  <rax=%rax,<t2=%r10
add  %rax,%r10

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#9
# asm 2: adc <rdx=%rdx,<t3=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t4 += mulc 
# asm 1: add  <mulc=int64#5,<t4=int64#10
# asm 2: add  <mulc=%r8,<t4=%r12
add  %r8,%r12

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 8] 
# asm 1: movq   8(<input_1=int64#2),>rax=int64#7
# asm 2: movq   8(<input_1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +16] 
# asm 1: mulq  16(<input_0=int64#1)
# asm 2: mulq  16(<input_0=%rdi)
mulq  16(%rdi)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#9
# asm 2: add  <rax=%rax,<t3=%r11
add  %rax,%r11

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#10
# asm 2: adc <rdx=%rdx,<t4=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +16] 
# asm 1: mulq  16(<M=int64#4)
# asm 2: mulq  16(<M=%rcx)
mulq  16(%rcx)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#9
# asm 2: add  <rax=%rax,<t3=%r11
add  %rax,%r11

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#10
# asm 2: adc <rdx=%rdx,<t4=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t5 += mulc 
# asm 1: add  <mulc=int64#5,<t5=int64#11
# asm 2: add  <mulc=%r8,<t5=%r13
add  %r8,%r13

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 8] 
# asm 1: movq   8(<input_1=int64#2),>rax=int64#7
# asm 2: movq   8(<input_1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +24] 
# asm 1: mulq  24(<input_0=int64#1)
# asm 2: mulq  24(<input_0=%rdi)
mulq  24(%rdi)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +24] 
# asm 1: mulq  24(<M=int64#4)
# asm 2: mulq  24(<M=%rcx)
mulq  24(%rcx)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t6 += mulc 
# asm 1: add  <mulc=int64#5,<t6=int64#12
# asm 2: add  <mulc=%r8,<t6=%r14
add  %r8,%r14

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 8] 
# asm 1: movq   8(<input_1=int64#2),>rax=int64#7
# asm 2: movq   8(<input_1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +32] 
# asm 1: mulq  32(<input_0=int64#1)
# asm 2: mulq  32(<input_0=%rdi)
mulq  32(%rdi)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +32] 
# asm 1: mulq  32(<M=int64#4)
# asm 2: mulq  32(<M=%rcx)
mulq  32(%rcx)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t7 += mulc 
# asm 1: add  <mulc=int64#5,<t7=int64#13
# asm 2: add  <mulc=%r8,<t7=%r15
add  %r8,%r15

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 8] 
# asm 1: movq   8(<input_1=int64#2),>rax=int64#7
# asm 2: movq   8(<input_1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +40] 
# asm 1: mulq  40(<input_0=int64#1)
# asm 2: mulq  40(<input_0=%rdi)
mulq  40(%rdi)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +40] 
# asm 1: mulq  40(<M=int64#4)
# asm 2: mulq  40(<M=%rcx)
mulq  40(%rcx)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t8 += mulc 
# asm 1: add  <mulc=int64#5,<t8=int64#14
# asm 2: add  <mulc=%r8,<t8=%rbx
add  %r8,%rbx

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 8] 
# asm 1: movq   8(<input_1=int64#2),>rax=int64#7
# asm 2: movq   8(<input_1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +48] 
# asm 1: mulq  48(<input_0=int64#1)
# asm 2: mulq  48(<input_0=%rdi)
mulq  48(%rdi)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +48] 
# asm 1: mulq  48(<M=int64#4)
# asm 2: mulq  48(<M=%rcx)
mulq  48(%rcx)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   t0 = 0 
# asm 1: mov  $0,>t0=int64#6
# asm 2: mov  $0,>t0=%r9
mov  $0,%r9

# qhasm:   carry? t0 += mulc 
# asm 1: add  <mulc=int64#5,<t0=int64#6
# asm 2: add  <mulc=%r8,<t0=%r9
add  %r8,%r9

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 + 8] 
# asm 1: movq   8(<input_1=int64#2),>rax=int64#7
# asm 2: movq   8(<input_1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +56] 
# asm 1: mulq  56(<input_0=int64#1)
# asm 2: mulq  56(<input_0=%rdi)
mulq  56(%rdi)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +56] 
# asm 1: mulq  56(<M=int64#4)
# asm 2: mulq  56(<M=%rcx)
mulq  56(%rcx)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   t0 += mulc 
# asm 1: add  <mulc=int64#5,<t0=int64#6
# asm 2: add  <mulc=%r8,<t0=%r9
add  %r8,%r9

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   rax = mem64[input_1 +16] 
# asm 1: movq   16(<input_1=int64#2),>rax=int64#7
# asm 2: movq   16(<input_1=%rsi),>rax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 0] 
# asm 1: mulq  0(<input_0=int64#1)
# asm 2: mulq  0(<input_0=%rdi)
mulq  0(%rdi)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#8
# asm 2: add  <rax=%rax,<t2=%r10
add  %rax,%r10

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#9
# asm 2: adc <rdx=%rdx,<t3=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   mulx0 = mem64[M1] 
# asm 1: movq M1,>mulx0=int64#15
# asm 2: movq M1,>mulx0=%rbp
movq M1(%rip),%rbp

# qhasm:   mulx0 *= t2 
# asm 1: imul  <t2=int64#8,<mulx0=int64#15
# asm 2: imul  <t2=%r10,<mulx0=%rbp
imul  %r10,%rbp

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 0] 
# asm 1: mulq  0(<M=int64#4)
# asm 2: mulq  0(<M=%rcx)
mulq  0(%rcx)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#8
# asm 2: add  <rax=%rax,<t2=%r10
add  %rax,%r10

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#9
# asm 2: adc <rdx=%rdx,<t3=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t4 += mulc 
# asm 1: add  <mulc=int64#5,<t4=int64#10
# asm 2: add  <mulc=%r8,<t4=%r12
add  %r8,%r12

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +16] 
# asm 1: movq   16(<input_1=int64#2),>rax=int64#7
# asm 2: movq   16(<input_1=%rsi),>rax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 8] 
# asm 1: mulq  8(<input_0=int64#1)
# asm 2: mulq  8(<input_0=%rdi)
mulq  8(%rdi)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#9
# asm 2: add  <rax=%rax,<t3=%r11
add  %rax,%r11

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#10
# asm 2: adc <rdx=%rdx,<t4=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 8] 
# asm 1: mulq  8(<M=int64#4)
# asm 2: mulq  8(<M=%rcx)
mulq  8(%rcx)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#9
# asm 2: add  <rax=%rax,<t3=%r11
add  %rax,%r11

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#10
# asm 2: adc <rdx=%rdx,<t4=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t5 += mulc 
# asm 1: add  <mulc=int64#5,<t5=int64#11
# asm 2: add  <mulc=%r8,<t5=%r13
add  %r8,%r13

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +16] 
# asm 1: movq   16(<input_1=int64#2),>rax=int64#7
# asm 2: movq   16(<input_1=%rsi),>rax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +16] 
# asm 1: mulq  16(<input_0=int64#1)
# asm 2: mulq  16(<input_0=%rdi)
mulq  16(%rdi)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +16] 
# asm 1: mulq  16(<M=int64#4)
# asm 2: mulq  16(<M=%rcx)
mulq  16(%rcx)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t6 += mulc 
# asm 1: add  <mulc=int64#5,<t6=int64#12
# asm 2: add  <mulc=%r8,<t6=%r14
add  %r8,%r14

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +16] 
# asm 1: movq   16(<input_1=int64#2),>rax=int64#7
# asm 2: movq   16(<input_1=%rsi),>rax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +24] 
# asm 1: mulq  24(<input_0=int64#1)
# asm 2: mulq  24(<input_0=%rdi)
mulq  24(%rdi)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +24] 
# asm 1: mulq  24(<M=int64#4)
# asm 2: mulq  24(<M=%rcx)
mulq  24(%rcx)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t7 += mulc 
# asm 1: add  <mulc=int64#5,<t7=int64#13
# asm 2: add  <mulc=%r8,<t7=%r15
add  %r8,%r15

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +16] 
# asm 1: movq   16(<input_1=int64#2),>rax=int64#7
# asm 2: movq   16(<input_1=%rsi),>rax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +32] 
# asm 1: mulq  32(<input_0=int64#1)
# asm 2: mulq  32(<input_0=%rdi)
mulq  32(%rdi)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +32] 
# asm 1: mulq  32(<M=int64#4)
# asm 2: mulq  32(<M=%rcx)
mulq  32(%rcx)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t8 += mulc 
# asm 1: add  <mulc=int64#5,<t8=int64#14
# asm 2: add  <mulc=%r8,<t8=%rbx
add  %r8,%rbx

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +16] 
# asm 1: movq   16(<input_1=int64#2),>rax=int64#7
# asm 2: movq   16(<input_1=%rsi),>rax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +40] 
# asm 1: mulq  40(<input_0=int64#1)
# asm 2: mulq  40(<input_0=%rdi)
mulq  40(%rdi)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +40] 
# asm 1: mulq  40(<M=int64#4)
# asm 2: mulq  40(<M=%rcx)
mulq  40(%rcx)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t0 += mulc 
# asm 1: add  <mulc=int64#5,<t0=int64#6
# asm 2: add  <mulc=%r8,<t0=%r9
add  %r8,%r9

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +16] 
# asm 1: movq   16(<input_1=int64#2),>rax=int64#7
# asm 2: movq   16(<input_1=%rsi),>rax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +48] 
# asm 1: mulq  48(<input_0=int64#1)
# asm 2: mulq  48(<input_0=%rdi)
mulq  48(%rdi)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +48] 
# asm 1: mulq  48(<M=int64#4)
# asm 2: mulq  48(<M=%rcx)
mulq  48(%rcx)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   t1 = 0 
# asm 1: mov  $0,>t1=int64#8
# asm 2: mov  $0,>t1=%r10
mov  $0,%r10

# qhasm:   carry? t1 += mulc 
# asm 1: add  <mulc=int64#5,<t1=int64#8
# asm 2: add  <mulc=%r8,<t1=%r10
add  %r8,%r10

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +16] 
# asm 1: movq   16(<input_1=int64#2),>rax=int64#7
# asm 2: movq   16(<input_1=%rsi),>rax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +56] 
# asm 1: mulq  56(<input_0=int64#1)
# asm 2: mulq  56(<input_0=%rdi)
mulq  56(%rdi)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +56] 
# asm 1: mulq  56(<M=int64#4)
# asm 2: mulq  56(<M=%rcx)
mulq  56(%rcx)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   t1 += mulc 
# asm 1: add  <mulc=int64#5,<t1=int64#8
# asm 2: add  <mulc=%r8,<t1=%r10
add  %r8,%r10

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   rax = mem64[input_1 +24] 
# asm 1: movq   24(<input_1=int64#2),>rax=int64#7
# asm 2: movq   24(<input_1=%rsi),>rax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 0] 
# asm 1: mulq  0(<input_0=int64#1)
# asm 2: mulq  0(<input_0=%rdi)
mulq  0(%rdi)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#9
# asm 2: add  <rax=%rax,<t3=%r11
add  %rax,%r11

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#10
# asm 2: adc <rdx=%rdx,<t4=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   mulx0 = mem64[M1] 
# asm 1: movq M1,>mulx0=int64#15
# asm 2: movq M1,>mulx0=%rbp
movq M1(%rip),%rbp

# qhasm:   mulx0 *= t3 
# asm 1: imul  <t3=int64#9,<mulx0=int64#15
# asm 2: imul  <t3=%r11,<mulx0=%rbp
imul  %r11,%rbp

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 0] 
# asm 1: mulq  0(<M=int64#4)
# asm 2: mulq  0(<M=%rcx)
mulq  0(%rcx)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#9
# asm 2: add  <rax=%rax,<t3=%r11
add  %rax,%r11

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#10
# asm 2: adc <rdx=%rdx,<t4=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t5 += mulc 
# asm 1: add  <mulc=int64#5,<t5=int64#11
# asm 2: add  <mulc=%r8,<t5=%r13
add  %r8,%r13

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +24] 
# asm 1: movq   24(<input_1=int64#2),>rax=int64#7
# asm 2: movq   24(<input_1=%rsi),>rax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 8] 
# asm 1: mulq  8(<input_0=int64#1)
# asm 2: mulq  8(<input_0=%rdi)
mulq  8(%rdi)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 8] 
# asm 1: mulq  8(<M=int64#4)
# asm 2: mulq  8(<M=%rcx)
mulq  8(%rcx)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t6 += mulc 
# asm 1: add  <mulc=int64#5,<t6=int64#12
# asm 2: add  <mulc=%r8,<t6=%r14
add  %r8,%r14

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +24] 
# asm 1: movq   24(<input_1=int64#2),>rax=int64#7
# asm 2: movq   24(<input_1=%rsi),>rax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +16] 
# asm 1: mulq  16(<input_0=int64#1)
# asm 2: mulq  16(<input_0=%rdi)
mulq  16(%rdi)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +16] 
# asm 1: mulq  16(<M=int64#4)
# asm 2: mulq  16(<M=%rcx)
mulq  16(%rcx)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t7 += mulc 
# asm 1: add  <mulc=int64#5,<t7=int64#13
# asm 2: add  <mulc=%r8,<t7=%r15
add  %r8,%r15

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +24] 
# asm 1: movq   24(<input_1=int64#2),>rax=int64#7
# asm 2: movq   24(<input_1=%rsi),>rax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +24] 
# asm 1: mulq  24(<input_0=int64#1)
# asm 2: mulq  24(<input_0=%rdi)
mulq  24(%rdi)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +24] 
# asm 1: mulq  24(<M=int64#4)
# asm 2: mulq  24(<M=%rcx)
mulq  24(%rcx)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t8 += mulc 
# asm 1: add  <mulc=int64#5,<t8=int64#14
# asm 2: add  <mulc=%r8,<t8=%rbx
add  %r8,%rbx

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +24] 
# asm 1: movq   24(<input_1=int64#2),>rax=int64#7
# asm 2: movq   24(<input_1=%rsi),>rax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +32] 
# asm 1: mulq  32(<input_0=int64#1)
# asm 2: mulq  32(<input_0=%rdi)
mulq  32(%rdi)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +32] 
# asm 1: mulq  32(<M=int64#4)
# asm 2: mulq  32(<M=%rcx)
mulq  32(%rcx)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t0 += mulc 
# asm 1: add  <mulc=int64#5,<t0=int64#6
# asm 2: add  <mulc=%r8,<t0=%r9
add  %r8,%r9

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +24] 
# asm 1: movq   24(<input_1=int64#2),>rax=int64#7
# asm 2: movq   24(<input_1=%rsi),>rax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +40] 
# asm 1: mulq  40(<input_0=int64#1)
# asm 2: mulq  40(<input_0=%rdi)
mulq  40(%rdi)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +40] 
# asm 1: mulq  40(<M=int64#4)
# asm 2: mulq  40(<M=%rcx)
mulq  40(%rcx)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t1 += mulc 
# asm 1: add  <mulc=int64#5,<t1=int64#8
# asm 2: add  <mulc=%r8,<t1=%r10
add  %r8,%r10

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +24] 
# asm 1: movq   24(<input_1=int64#2),>rax=int64#7
# asm 2: movq   24(<input_1=%rsi),>rax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +48] 
# asm 1: mulq  48(<input_0=int64#1)
# asm 2: mulq  48(<input_0=%rdi)
mulq  48(%rdi)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +48] 
# asm 1: mulq  48(<M=int64#4)
# asm 2: mulq  48(<M=%rcx)
mulq  48(%rcx)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   t2 = 0 
# asm 1: mov  $0,>t2=int64#9
# asm 2: mov  $0,>t2=%r11
mov  $0,%r11

# qhasm:   carry? t2 += mulc 
# asm 1: add  <mulc=int64#5,<t2=int64#9
# asm 2: add  <mulc=%r8,<t2=%r11
add  %r8,%r11

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +24] 
# asm 1: movq   24(<input_1=int64#2),>rax=int64#7
# asm 2: movq   24(<input_1=%rsi),>rax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +56] 
# asm 1: mulq  56(<input_0=int64#1)
# asm 2: mulq  56(<input_0=%rdi)
mulq  56(%rdi)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +56] 
# asm 1: mulq  56(<M=int64#4)
# asm 2: mulq  56(<M=%rcx)
mulq  56(%rcx)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   t2 += mulc 
# asm 1: add  <mulc=int64#5,<t2=int64#9
# asm 2: add  <mulc=%r8,<t2=%r11
add  %r8,%r11

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   rax = mem64[input_1 +32] 
# asm 1: movq   32(<input_1=int64#2),>rax=int64#7
# asm 2: movq   32(<input_1=%rsi),>rax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 0] 
# asm 1: mulq  0(<input_0=int64#1)
# asm 2: mulq  0(<input_0=%rdi)
mulq  0(%rdi)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   mulx0 = mem64[M1] 
# asm 1: movq M1,>mulx0=int64#15
# asm 2: movq M1,>mulx0=%rbp
movq M1(%rip),%rbp

# qhasm:   mulx0 *= t4 
# asm 1: imul  <t4=int64#10,<mulx0=int64#15
# asm 2: imul  <t4=%r12,<mulx0=%rbp
imul  %r12,%rbp

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 0] 
# asm 1: mulq  0(<M=int64#4)
# asm 2: mulq  0(<M=%rcx)
mulq  0(%rcx)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#10
# asm 2: add  <rax=%rax,<t4=%r12
add  %rax,%r12

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#11
# asm 2: adc <rdx=%rdx,<t5=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t6 += mulc 
# asm 1: add  <mulc=int64#5,<t6=int64#12
# asm 2: add  <mulc=%r8,<t6=%r14
add  %r8,%r14

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +32] 
# asm 1: movq   32(<input_1=int64#2),>rax=int64#7
# asm 2: movq   32(<input_1=%rsi),>rax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 8] 
# asm 1: mulq  8(<input_0=int64#1)
# asm 2: mulq  8(<input_0=%rdi)
mulq  8(%rdi)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 8] 
# asm 1: mulq  8(<M=int64#4)
# asm 2: mulq  8(<M=%rcx)
mulq  8(%rcx)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t7 += mulc 
# asm 1: add  <mulc=int64#5,<t7=int64#13
# asm 2: add  <mulc=%r8,<t7=%r15
add  %r8,%r15

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +32] 
# asm 1: movq   32(<input_1=int64#2),>rax=int64#7
# asm 2: movq   32(<input_1=%rsi),>rax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +16] 
# asm 1: mulq  16(<input_0=int64#1)
# asm 2: mulq  16(<input_0=%rdi)
mulq  16(%rdi)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +16] 
# asm 1: mulq  16(<M=int64#4)
# asm 2: mulq  16(<M=%rcx)
mulq  16(%rcx)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t8 += mulc 
# asm 1: add  <mulc=int64#5,<t8=int64#14
# asm 2: add  <mulc=%r8,<t8=%rbx
add  %r8,%rbx

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +32] 
# asm 1: movq   32(<input_1=int64#2),>rax=int64#7
# asm 2: movq   32(<input_1=%rsi),>rax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +24] 
# asm 1: mulq  24(<input_0=int64#1)
# asm 2: mulq  24(<input_0=%rdi)
mulq  24(%rdi)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +24] 
# asm 1: mulq  24(<M=int64#4)
# asm 2: mulq  24(<M=%rcx)
mulq  24(%rcx)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t0 += mulc 
# asm 1: add  <mulc=int64#5,<t0=int64#6
# asm 2: add  <mulc=%r8,<t0=%r9
add  %r8,%r9

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +32] 
# asm 1: movq   32(<input_1=int64#2),>rax=int64#7
# asm 2: movq   32(<input_1=%rsi),>rax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +32] 
# asm 1: mulq  32(<input_0=int64#1)
# asm 2: mulq  32(<input_0=%rdi)
mulq  32(%rdi)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +32] 
# asm 1: mulq  32(<M=int64#4)
# asm 2: mulq  32(<M=%rcx)
mulq  32(%rcx)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t1 += mulc 
# asm 1: add  <mulc=int64#5,<t1=int64#8
# asm 2: add  <mulc=%r8,<t1=%r10
add  %r8,%r10

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +32] 
# asm 1: movq   32(<input_1=int64#2),>rax=int64#7
# asm 2: movq   32(<input_1=%rsi),>rax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +40] 
# asm 1: mulq  40(<input_0=int64#1)
# asm 2: mulq  40(<input_0=%rdi)
mulq  40(%rdi)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +40] 
# asm 1: mulq  40(<M=int64#4)
# asm 2: mulq  40(<M=%rcx)
mulq  40(%rcx)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t2 += mulc 
# asm 1: add  <mulc=int64#5,<t2=int64#9
# asm 2: add  <mulc=%r8,<t2=%r11
add  %r8,%r11

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +32] 
# asm 1: movq   32(<input_1=int64#2),>rax=int64#7
# asm 2: movq   32(<input_1=%rsi),>rax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +48] 
# asm 1: mulq  48(<input_0=int64#1)
# asm 2: mulq  48(<input_0=%rdi)
mulq  48(%rdi)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +48] 
# asm 1: mulq  48(<M=int64#4)
# asm 2: mulq  48(<M=%rcx)
mulq  48(%rcx)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   t3 = 0 
# asm 1: mov  $0,>t3=int64#10
# asm 2: mov  $0,>t3=%r12
mov  $0,%r12

# qhasm:   carry? t3 += mulc 
# asm 1: add  <mulc=int64#5,<t3=int64#10
# asm 2: add  <mulc=%r8,<t3=%r12
add  %r8,%r12

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +32] 
# asm 1: movq   32(<input_1=int64#2),>rax=int64#7
# asm 2: movq   32(<input_1=%rsi),>rax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +56] 
# asm 1: mulq  56(<input_0=int64#1)
# asm 2: mulq  56(<input_0=%rdi)
mulq  56(%rdi)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#9
# asm 2: add  <rax=%rax,<t2=%r11
add  %rax,%r11

# qhasm:   t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#10
# asm 2: adc <rdx=%rdx,<t3=%r12
adc %rdx,%r12

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +56] 
# asm 1: mulq  56(<M=int64#4)
# asm 2: mulq  56(<M=%rcx)
mulq  56(%rcx)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#9
# asm 2: add  <rax=%rax,<t2=%r11
add  %rax,%r11

# qhasm:   t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#10
# asm 2: adc <rdx=%rdx,<t3=%r12
adc %rdx,%r12

# qhasm:   t3 += mulc 
# asm 1: add  <mulc=int64#5,<t3=int64#10
# asm 2: add  <mulc=%r8,<t3=%r12
add  %r8,%r12

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   rax = mem64[input_1 +40] 
# asm 1: movq   40(<input_1=int64#2),>rax=int64#7
# asm 2: movq   40(<input_1=%rsi),>rax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 0] 
# asm 1: mulq  0(<input_0=int64#1)
# asm 2: mulq  0(<input_0=%rdi)
mulq  0(%rdi)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   mulx0 = mem64[M1] 
# asm 1: movq M1,>mulx0=int64#15
# asm 2: movq M1,>mulx0=%rbp
movq M1(%rip),%rbp

# qhasm:   mulx0 *= t5 
# asm 1: imul  <t5=int64#11,<mulx0=int64#15
# asm 2: imul  <t5=%r13,<mulx0=%rbp
imul  %r13,%rbp

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 0] 
# asm 1: mulq  0(<M=int64#4)
# asm 2: mulq  0(<M=%rcx)
mulq  0(%rcx)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#11
# asm 2: add  <rax=%rax,<t5=%r13
add  %rax,%r13

# qhasm:   carry? t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#12
# asm 2: adc <rdx=%rdx,<t6=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t7 += mulc 
# asm 1: add  <mulc=int64#5,<t7=int64#13
# asm 2: add  <mulc=%r8,<t7=%r15
add  %r8,%r15

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +40] 
# asm 1: movq   40(<input_1=int64#2),>rax=int64#7
# asm 2: movq   40(<input_1=%rsi),>rax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 8] 
# asm 1: mulq  8(<input_0=int64#1)
# asm 2: mulq  8(<input_0=%rdi)
mulq  8(%rdi)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 8] 
# asm 1: mulq  8(<M=int64#4)
# asm 2: mulq  8(<M=%rcx)
mulq  8(%rcx)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t8 += mulc 
# asm 1: add  <mulc=int64#5,<t8=int64#14
# asm 2: add  <mulc=%r8,<t8=%rbx
add  %r8,%rbx

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +40] 
# asm 1: movq   40(<input_1=int64#2),>rax=int64#7
# asm 2: movq   40(<input_1=%rsi),>rax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +16] 
# asm 1: mulq  16(<input_0=int64#1)
# asm 2: mulq  16(<input_0=%rdi)
mulq  16(%rdi)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +16] 
# asm 1: mulq  16(<M=int64#4)
# asm 2: mulq  16(<M=%rcx)
mulq  16(%rcx)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t0 += mulc 
# asm 1: add  <mulc=int64#5,<t0=int64#6
# asm 2: add  <mulc=%r8,<t0=%r9
add  %r8,%r9

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +40] 
# asm 1: movq   40(<input_1=int64#2),>rax=int64#7
# asm 2: movq   40(<input_1=%rsi),>rax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +24] 
# asm 1: mulq  24(<input_0=int64#1)
# asm 2: mulq  24(<input_0=%rdi)
mulq  24(%rdi)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +24] 
# asm 1: mulq  24(<M=int64#4)
# asm 2: mulq  24(<M=%rcx)
mulq  24(%rcx)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t1 += mulc 
# asm 1: add  <mulc=int64#5,<t1=int64#8
# asm 2: add  <mulc=%r8,<t1=%r10
add  %r8,%r10

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +40] 
# asm 1: movq   40(<input_1=int64#2),>rax=int64#7
# asm 2: movq   40(<input_1=%rsi),>rax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +32] 
# asm 1: mulq  32(<input_0=int64#1)
# asm 2: mulq  32(<input_0=%rdi)
mulq  32(%rdi)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +32] 
# asm 1: mulq  32(<M=int64#4)
# asm 2: mulq  32(<M=%rcx)
mulq  32(%rcx)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t2 += mulc 
# asm 1: add  <mulc=int64#5,<t2=int64#9
# asm 2: add  <mulc=%r8,<t2=%r11
add  %r8,%r11

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +40] 
# asm 1: movq   40(<input_1=int64#2),>rax=int64#7
# asm 2: movq   40(<input_1=%rsi),>rax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +40] 
# asm 1: mulq  40(<input_0=int64#1)
# asm 2: mulq  40(<input_0=%rdi)
mulq  40(%rdi)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +40] 
# asm 1: mulq  40(<M=int64#4)
# asm 2: mulq  40(<M=%rcx)
mulq  40(%rcx)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t3 += mulc 
# asm 1: add  <mulc=int64#5,<t3=int64#10
# asm 2: add  <mulc=%r8,<t3=%r12
add  %r8,%r12

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +40] 
# asm 1: movq   40(<input_1=int64#2),>rax=int64#7
# asm 2: movq   40(<input_1=%rsi),>rax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +48] 
# asm 1: mulq  48(<input_0=int64#1)
# asm 2: mulq  48(<input_0=%rdi)
mulq  48(%rdi)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#9
# asm 2: add  <rax=%rax,<t2=%r11
add  %rax,%r11

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#10
# asm 2: adc <rdx=%rdx,<t3=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +48] 
# asm 1: mulq  48(<M=int64#4)
# asm 2: mulq  48(<M=%rcx)
mulq  48(%rcx)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#9
# asm 2: add  <rax=%rax,<t2=%r11
add  %rax,%r11

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#10
# asm 2: adc <rdx=%rdx,<t3=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   t4 = 0 
# asm 1: mov  $0,>t4=int64#11
# asm 2: mov  $0,>t4=%r13
mov  $0,%r13

# qhasm:   carry? t4 += mulc 
# asm 1: add  <mulc=int64#5,<t4=int64#11
# asm 2: add  <mulc=%r8,<t4=%r13
add  %r8,%r13

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +40] 
# asm 1: movq   40(<input_1=int64#2),>rax=int64#7
# asm 2: movq   40(<input_1=%rsi),>rax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +56] 
# asm 1: mulq  56(<input_0=int64#1)
# asm 2: mulq  56(<input_0=%rdi)
mulq  56(%rdi)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#10
# asm 2: add  <rax=%rax,<t3=%r12
add  %rax,%r12

# qhasm:   t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#11
# asm 2: adc <rdx=%rdx,<t4=%r13
adc %rdx,%r13

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +56] 
# asm 1: mulq  56(<M=int64#4)
# asm 2: mulq  56(<M=%rcx)
mulq  56(%rcx)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#10
# asm 2: add  <rax=%rax,<t3=%r12
add  %rax,%r12

# qhasm:   t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#11
# asm 2: adc <rdx=%rdx,<t4=%r13
adc %rdx,%r13

# qhasm:   t4 += mulc 
# asm 1: add  <mulc=int64#5,<t4=int64#11
# asm 2: add  <mulc=%r8,<t4=%r13
add  %r8,%r13

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   rax = mem64[input_1 +48] 
# asm 1: movq   48(<input_1=int64#2),>rax=int64#7
# asm 2: movq   48(<input_1=%rsi),>rax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 0] 
# asm 1: mulq  0(<input_0=int64#1)
# asm 2: mulq  0(<input_0=%rdi)
mulq  0(%rdi)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   mulx0 = mem64[M1] 
# asm 1: movq M1,>mulx0=int64#15
# asm 2: movq M1,>mulx0=%rbp
movq M1(%rip),%rbp

# qhasm:   mulx0 *= t6 
# asm 1: imul  <t6=int64#12,<mulx0=int64#15
# asm 2: imul  <t6=%r14,<mulx0=%rbp
imul  %r14,%rbp

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 0] 
# asm 1: mulq  0(<M=int64#4)
# asm 2: mulq  0(<M=%rcx)
mulq  0(%rcx)

# qhasm:   carry? t6 += rax 
# asm 1: add  <rax=int64#7,<t6=int64#12
# asm 2: add  <rax=%rax,<t6=%r14
add  %rax,%r14

# qhasm:   carry? t7 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t7=int64#13
# asm 2: adc <rdx=%rdx,<t7=%r15
adc %rdx,%r15

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t8 += mulc 
# asm 1: add  <mulc=int64#5,<t8=int64#14
# asm 2: add  <mulc=%r8,<t8=%rbx
add  %r8,%rbx

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +48] 
# asm 1: movq   48(<input_1=int64#2),>rax=int64#7
# asm 2: movq   48(<input_1=%rsi),>rax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 8] 
# asm 1: mulq  8(<input_0=int64#1)
# asm 2: mulq  8(<input_0=%rdi)
mulq  8(%rdi)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 8] 
# asm 1: mulq  8(<M=int64#4)
# asm 2: mulq  8(<M=%rcx)
mulq  8(%rcx)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t0 += mulc 
# asm 1: add  <mulc=int64#5,<t0=int64#6
# asm 2: add  <mulc=%r8,<t0=%r9
add  %r8,%r9

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +48] 
# asm 1: movq   48(<input_1=int64#2),>rax=int64#7
# asm 2: movq   48(<input_1=%rsi),>rax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +16] 
# asm 1: mulq  16(<input_0=int64#1)
# asm 2: mulq  16(<input_0=%rdi)
mulq  16(%rdi)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +16] 
# asm 1: mulq  16(<M=int64#4)
# asm 2: mulq  16(<M=%rcx)
mulq  16(%rcx)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t1 += mulc 
# asm 1: add  <mulc=int64#5,<t1=int64#8
# asm 2: add  <mulc=%r8,<t1=%r10
add  %r8,%r10

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +48] 
# asm 1: movq   48(<input_1=int64#2),>rax=int64#7
# asm 2: movq   48(<input_1=%rsi),>rax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +24] 
# asm 1: mulq  24(<input_0=int64#1)
# asm 2: mulq  24(<input_0=%rdi)
mulq  24(%rdi)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +24] 
# asm 1: mulq  24(<M=int64#4)
# asm 2: mulq  24(<M=%rcx)
mulq  24(%rcx)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t2 += mulc 
# asm 1: add  <mulc=int64#5,<t2=int64#9
# asm 2: add  <mulc=%r8,<t2=%r11
add  %r8,%r11

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +48] 
# asm 1: movq   48(<input_1=int64#2),>rax=int64#7
# asm 2: movq   48(<input_1=%rsi),>rax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +32] 
# asm 1: mulq  32(<input_0=int64#1)
# asm 2: mulq  32(<input_0=%rdi)
mulq  32(%rdi)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +32] 
# asm 1: mulq  32(<M=int64#4)
# asm 2: mulq  32(<M=%rcx)
mulq  32(%rcx)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t3 += mulc 
# asm 1: add  <mulc=int64#5,<t3=int64#10
# asm 2: add  <mulc=%r8,<t3=%r12
add  %r8,%r12

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +48] 
# asm 1: movq   48(<input_1=int64#2),>rax=int64#7
# asm 2: movq   48(<input_1=%rsi),>rax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +40] 
# asm 1: mulq  40(<input_0=int64#1)
# asm 2: mulq  40(<input_0=%rdi)
mulq  40(%rdi)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#9
# asm 2: add  <rax=%rax,<t2=%r11
add  %rax,%r11

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#10
# asm 2: adc <rdx=%rdx,<t3=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +40] 
# asm 1: mulq  40(<M=int64#4)
# asm 2: mulq  40(<M=%rcx)
mulq  40(%rcx)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#9
# asm 2: add  <rax=%rax,<t2=%r11
add  %rax,%r11

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#10
# asm 2: adc <rdx=%rdx,<t3=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t4 += mulc 
# asm 1: add  <mulc=int64#5,<t4=int64#11
# asm 2: add  <mulc=%r8,<t4=%r13
add  %r8,%r13

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +48] 
# asm 1: movq   48(<input_1=int64#2),>rax=int64#7
# asm 2: movq   48(<input_1=%rsi),>rax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +48] 
# asm 1: mulq  48(<input_0=int64#1)
# asm 2: mulq  48(<input_0=%rdi)
mulq  48(%rdi)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#10
# asm 2: add  <rax=%rax,<t3=%r12
add  %rax,%r12

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#11
# asm 2: adc <rdx=%rdx,<t4=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +48] 
# asm 1: mulq  48(<M=int64#4)
# asm 2: mulq  48(<M=%rcx)
mulq  48(%rcx)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#10
# asm 2: add  <rax=%rax,<t3=%r12
add  %rax,%r12

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#11
# asm 2: adc <rdx=%rdx,<t4=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   t5 = 0 
# asm 1: mov  $0,>t5=int64#12
# asm 2: mov  $0,>t5=%r14
mov  $0,%r14

# qhasm:   carry? t5 += mulc 
# asm 1: add  <mulc=int64#5,<t5=int64#12
# asm 2: add  <mulc=%r8,<t5=%r14
add  %r8,%r14

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +48] 
# asm 1: movq   48(<input_1=int64#2),>rax=int64#7
# asm 2: movq   48(<input_1=%rsi),>rax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +56] 
# asm 1: mulq  56(<input_0=int64#1)
# asm 2: mulq  56(<input_0=%rdi)
mulq  56(%rdi)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#11
# asm 2: add  <rax=%rax,<t4=%r13
add  %rax,%r13

# qhasm:   t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#12
# asm 2: adc <rdx=%rdx,<t5=%r14
adc %rdx,%r14

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +56] 
# asm 1: mulq  56(<M=int64#4)
# asm 2: mulq  56(<M=%rcx)
mulq  56(%rcx)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#11
# asm 2: add  <rax=%rax,<t4=%r13
add  %rax,%r13

# qhasm:   t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#12
# asm 2: adc <rdx=%rdx,<t5=%r14
adc %rdx,%r14

# qhasm:   t5 += mulc 
# asm 1: add  <mulc=int64#5,<t5=int64#12
# asm 2: add  <mulc=%r8,<t5=%r14
add  %r8,%r14

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   rax = mem64[input_1 +56] 
# asm 1: movq   56(<input_1=int64#2),>rax=int64#7
# asm 2: movq   56(<input_1=%rsi),>rax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 0] 
# asm 1: mulq  0(<input_0=int64#1)
# asm 2: mulq  0(<input_0=%rdi)
mulq  0(%rdi)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   mulx0 = mem64[M1] 
# asm 1: movq M1,>mulx0=int64#15
# asm 2: movq M1,>mulx0=%rbp
movq M1(%rip),%rbp

# qhasm:   mulx0 *= t7 
# asm 1: imul  <t7=int64#13,<mulx0=int64#15
# asm 2: imul  <t7=%r15,<mulx0=%rbp
imul  %r15,%rbp

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 0] 
# asm 1: mulq  0(<M=int64#4)
# asm 2: mulq  0(<M=%rcx)
mulq  0(%rcx)

# qhasm:   carry? t7 += rax 
# asm 1: add  <rax=int64#7,<t7=int64#13
# asm 2: add  <rax=%rax,<t7=%r15
add  %rax,%r15

# qhasm:   carry? t8 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t8=int64#14
# asm 2: adc <rdx=%rdx,<t8=%rbx
adc %rdx,%rbx

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t0 += mulc 
# asm 1: add  <mulc=int64#5,<t0=int64#6
# asm 2: add  <mulc=%r8,<t0=%r9
add  %r8,%r9

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +56] 
# asm 1: movq   56(<input_1=int64#2),>rax=int64#7
# asm 2: movq   56(<input_1=%rsi),>rax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 + 8] 
# asm 1: mulq  8(<input_0=int64#1)
# asm 2: mulq  8(<input_0=%rdi)
mulq  8(%rdi)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M + 8] 
# asm 1: mulq  8(<M=int64#4)
# asm 2: mulq  8(<M=%rcx)
mulq  8(%rcx)

# qhasm:   carry? t8 += rax 
# asm 1: add  <rax=int64#7,<t8=int64#14
# asm 2: add  <rax=%rax,<t8=%rbx
add  %rax,%rbx

# qhasm:   carry? t0 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t0=int64#6
# asm 2: adc <rdx=%rdx,<t0=%r9
adc %rdx,%r9

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t1 += mulc 
# asm 1: add  <mulc=int64#5,<t1=int64#8
# asm 2: add  <mulc=%r8,<t1=%r10
add  %r8,%r10

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +56] 
# asm 1: movq   56(<input_1=int64#2),>rax=int64#7
# asm 2: movq   56(<input_1=%rsi),>rax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +16] 
# asm 1: mulq  16(<input_0=int64#1)
# asm 2: mulq  16(<input_0=%rdi)
mulq  16(%rdi)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +16] 
# asm 1: mulq  16(<M=int64#4)
# asm 2: mulq  16(<M=%rcx)
mulq  16(%rcx)

# qhasm:   carry? t0 += rax 
# asm 1: add  <rax=int64#7,<t0=int64#6
# asm 2: add  <rax=%rax,<t0=%r9
add  %rax,%r9

# qhasm:   carry? t1 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t1=int64#8
# asm 2: adc <rdx=%rdx,<t1=%r10
adc %rdx,%r10

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t2 += mulc 
# asm 1: add  <mulc=int64#5,<t2=int64#9
# asm 2: add  <mulc=%r8,<t2=%r11
add  %r8,%r11

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +56] 
# asm 1: movq   56(<input_1=int64#2),>rax=int64#7
# asm 2: movq   56(<input_1=%rsi),>rax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +24] 
# asm 1: mulq  24(<input_0=int64#1)
# asm 2: mulq  24(<input_0=%rdi)
mulq  24(%rdi)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +24] 
# asm 1: mulq  24(<M=int64#4)
# asm 2: mulq  24(<M=%rcx)
mulq  24(%rcx)

# qhasm:   carry? t1 += rax 
# asm 1: add  <rax=int64#7,<t1=int64#8
# asm 2: add  <rax=%rax,<t1=%r10
add  %rax,%r10

# qhasm:   carry? t2 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t2=int64#9
# asm 2: adc <rdx=%rdx,<t2=%r11
adc %rdx,%r11

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t3 += mulc 
# asm 1: add  <mulc=int64#5,<t3=int64#10
# asm 2: add  <mulc=%r8,<t3=%r12
add  %r8,%r12

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +56] 
# asm 1: movq   56(<input_1=int64#2),>rax=int64#7
# asm 2: movq   56(<input_1=%rsi),>rax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +32] 
# asm 1: mulq  32(<input_0=int64#1)
# asm 2: mulq  32(<input_0=%rdi)
mulq  32(%rdi)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#9
# asm 2: add  <rax=%rax,<t2=%r11
add  %rax,%r11

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#10
# asm 2: adc <rdx=%rdx,<t3=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +32] 
# asm 1: mulq  32(<M=int64#4)
# asm 2: mulq  32(<M=%rcx)
mulq  32(%rcx)

# qhasm:   carry? t2 += rax 
# asm 1: add  <rax=int64#7,<t2=int64#9
# asm 2: add  <rax=%rax,<t2=%r11
add  %rax,%r11

# qhasm:   carry? t3 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t3=int64#10
# asm 2: adc <rdx=%rdx,<t3=%r12
adc %rdx,%r12

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t4 += mulc 
# asm 1: add  <mulc=int64#5,<t4=int64#11
# asm 2: add  <mulc=%r8,<t4=%r13
add  %r8,%r13

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +56] 
# asm 1: movq   56(<input_1=int64#2),>rax=int64#7
# asm 2: movq   56(<input_1=%rsi),>rax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +40] 
# asm 1: mulq  40(<input_0=int64#1)
# asm 2: mulq  40(<input_0=%rdi)
mulq  40(%rdi)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#10
# asm 2: add  <rax=%rax,<t3=%r12
add  %rax,%r12

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#11
# asm 2: adc <rdx=%rdx,<t4=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +40] 
# asm 1: mulq  40(<M=int64#4)
# asm 2: mulq  40(<M=%rcx)
mulq  40(%rcx)

# qhasm:   carry? t3 += rax 
# asm 1: add  <rax=int64#7,<t3=int64#10
# asm 2: add  <rax=%rax,<t3=%r12
add  %rax,%r12

# qhasm:   carry? t4 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t4=int64#11
# asm 2: adc <rdx=%rdx,<t4=%r13
adc %rdx,%r13

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   carry? t5 += mulc 
# asm 1: add  <mulc=int64#5,<t5=int64#12
# asm 2: add  <mulc=%r8,<t5=%r14
add  %r8,%r14

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +56] 
# asm 1: movq   56(<input_1=int64#2),>rax=int64#7
# asm 2: movq   56(<input_1=%rsi),>rax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +48] 
# asm 1: mulq  48(<input_0=int64#1)
# asm 2: mulq  48(<input_0=%rdi)
mulq  48(%rdi)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#11
# asm 2: add  <rax=%rax,<t4=%r13
add  %rax,%r13

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#12
# asm 2: adc <rdx=%rdx,<t5=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +48] 
# asm 1: mulq  48(<M=int64#4)
# asm 2: mulq  48(<M=%rcx)
mulq  48(%rcx)

# qhasm:   carry? t4 += rax 
# asm 1: add  <rax=int64#7,<t4=int64#11
# asm 2: add  <rax=%rax,<t4=%r13
add  %rax,%r13

# qhasm:   carry? t5 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t5=int64#12
# asm 2: adc <rdx=%rdx,<t5=%r14
adc %rdx,%r14

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   t6 = 0 
# asm 1: mov  $0,>t6=int64#13
# asm 2: mov  $0,>t6=%r15
mov  $0,%r15

# qhasm:   carry? t6 += mulc 
# asm 1: add  <mulc=int64#5,<t6=int64#13
# asm 2: add  <mulc=%r8,<t6=%r15
add  %r8,%r15

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#5
# asm 2: mov  $0,>mulc=%r8
mov  $0,%r8

# qhasm:   mulc += 0 + carry 
# asm 1: adc $0,<mulc=int64#5
# asm 2: adc $0,<mulc=%r8
adc $0,%r8

# qhasm:   rax = mem64[input_1 +56] 
# asm 1: movq   56(<input_1=int64#2),>rax=int64#7
# asm 2: movq   56(<input_1=%rsi),>rax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) rdx rax = rax * mem64[input_0 +56] 
# asm 1: mulq  56(<input_0=int64#1)
# asm 2: mulq  56(<input_0=%rdi)
mulq  56(%rdi)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#12
# asm 2: add  <rax=%rax,<t5=%r14
add  %rax,%r14

# qhasm:   t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#13
# asm 2: adc <rdx=%rdx,<t6=%r15
adc %rdx,%r15

# qhasm:   rax = mulx0 
# asm 1: mov  <mulx0=int64#15,>rax=int64#7
# asm 2: mov  <mulx0=%rbp,>rax=%rax
mov  %rbp,%rax

# qhasm:   (uint128) rdx rax = rax * mem64[M +56] 
# asm 1: mulq  56(<M=int64#4)
# asm 2: mulq  56(<M=%rcx)
mulq  56(%rcx)

# qhasm:   carry? t5 += rax 
# asm 1: add  <rax=int64#7,<t5=int64#12
# asm 2: add  <rax=%rax,<t5=%r14
add  %rax,%r14

# qhasm:   t6 += rdx + carry 
# asm 1: adc <rdx=int64#3,<t6=int64#13
# asm 2: adc <rdx=%rdx,<t6=%r15
adc %rdx,%r15

# qhasm:   t6 += mulc 
# asm 1: add  <mulc=int64#5,<t6=int64#13
# asm 2: add  <mulc=%r8,<t6=%r15
add  %r8,%r15

# qhasm:   mulc = 0 
# asm 1: mov  $0,>mulc=int64#1
# asm 2: mov  $0,>mulc=%rdi
mov  $0,%rdi

# qhasm: input_2 = input_2_save
# asm 1: movq <input_2_save=stack64#8,>input_2=int64#2
# asm 2: movq <input_2_save=56(%rsp),>input_2=%rsi
movq 56(%rsp),%rsi

# qhasm: mem64[input_2 + 0] = t8
# asm 1: movq   <t8=int64#14,0(<input_2=int64#2)
# asm 2: movq   <t8=%rbx,0(<input_2=%rsi)
movq   %rbx,0(%rsi)

# qhasm: mem64[input_2 + 8] = t0
# asm 1: movq   <t0=int64#6,8(<input_2=int64#2)
# asm 2: movq   <t0=%r9,8(<input_2=%rsi)
movq   %r9,8(%rsi)

# qhasm: mem64[input_2 +16] = t1
# asm 1: movq   <t1=int64#8,16(<input_2=int64#2)
# asm 2: movq   <t1=%r10,16(<input_2=%rsi)
movq   %r10,16(%rsi)

# qhasm: mem64[input_2 +24] = t2
# asm 1: movq   <t2=int64#9,24(<input_2=int64#2)
# asm 2: movq   <t2=%r11,24(<input_2=%rsi)
movq   %r11,24(%rsi)

# qhasm: mem64[input_2 +32] = t3
# asm 1: movq   <t3=int64#10,32(<input_2=int64#2)
# asm 2: movq   <t3=%r12,32(<input_2=%rsi)
movq   %r12,32(%rsi)

# qhasm: mem64[input_2 +40] = t4
# asm 1: movq   <t4=int64#11,40(<input_2=int64#2)
# asm 2: movq   <t4=%r13,40(<input_2=%rsi)
movq   %r13,40(%rsi)

# qhasm: mem64[input_2 +48] = t5
# asm 1: movq   <t5=int64#12,48(<input_2=int64#2)
# asm 2: movq   <t5=%r14,48(<input_2=%rsi)
movq   %r14,48(%rsi)

# qhasm: mem64[input_2 +56] = t6
# asm 1: movq   <t6=int64#13,56(<input_2=int64#2)
# asm 2: movq   <t6=%r15,56(<input_2=%rsi)
movq   %r15,56(%rsi)

# qhasm: carry? t8 -= mem64[M + 0]
# asm 1: subq 0(<M=int64#4),<t8=int64#14
# asm 2: subq 0(<M=%rcx),<t8=%rbx
subq 0(%rcx),%rbx

# qhasm: carry? t0 -= mem64[M + 8] - carry
# asm 1: sbbq 8(<M=int64#4),<t0=int64#6
# asm 2: sbbq 8(<M=%rcx),<t0=%r9
sbbq 8(%rcx),%r9

# qhasm: carry? t1 -= mem64[M +16] - carry
# asm 1: sbbq 16(<M=int64#4),<t1=int64#8
# asm 2: sbbq 16(<M=%rcx),<t1=%r10
sbbq 16(%rcx),%r10

# qhasm: carry? t2 -= mem64[M +24] - carry
# asm 1: sbbq 24(<M=int64#4),<t2=int64#9
# asm 2: sbbq 24(<M=%rcx),<t2=%r11
sbbq 24(%rcx),%r11

# qhasm: carry? t3 -= mem64[M +32] - carry
# asm 1: sbbq 32(<M=int64#4),<t3=int64#10
# asm 2: sbbq 32(<M=%rcx),<t3=%r12
sbbq 32(%rcx),%r12

# qhasm: carry? t4 -= mem64[M +40] - carry
# asm 1: sbbq 40(<M=int64#4),<t4=int64#11
# asm 2: sbbq 40(<M=%rcx),<t4=%r13
sbbq 40(%rcx),%r13

# qhasm: carry? t5 -= mem64[M +48] - carry
# asm 1: sbbq 48(<M=int64#4),<t5=int64#12
# asm 2: sbbq 48(<M=%rcx),<t5=%r14
sbbq 48(%rcx),%r14

# qhasm: carry? t6 -= mem64[M +56] - carry
# asm 1: sbbq 56(<M=int64#4),<t6=int64#13
# asm 2: sbbq 56(<M=%rcx),<t6=%r15
sbbq 56(%rcx),%r15

# qhasm: t8 = mem64[input_2 + 0] if carry
# asm 1: cmovc 0(<input_2=int64#2),<t8=int64#14
# asm 2: cmovc 0(<input_2=%rsi),<t8=%rbx
cmovc 0(%rsi),%rbx

# qhasm: t0 = mem64[input_2 + 8] if carry
# asm 1: cmovc 8(<input_2=int64#2),<t0=int64#6
# asm 2: cmovc 8(<input_2=%rsi),<t0=%r9
cmovc 8(%rsi),%r9

# qhasm: t1 = mem64[input_2 +16] if carry
# asm 1: cmovc 16(<input_2=int64#2),<t1=int64#8
# asm 2: cmovc 16(<input_2=%rsi),<t1=%r10
cmovc 16(%rsi),%r10

# qhasm: t2 = mem64[input_2 +24] if carry
# asm 1: cmovc 24(<input_2=int64#2),<t2=int64#9
# asm 2: cmovc 24(<input_2=%rsi),<t2=%r11
cmovc 24(%rsi),%r11

# qhasm: t3 = mem64[input_2 +32] if carry
# asm 1: cmovc 32(<input_2=int64#2),<t3=int64#10
# asm 2: cmovc 32(<input_2=%rsi),<t3=%r12
cmovc 32(%rsi),%r12

# qhasm: t4 = mem64[input_2 +40] if carry
# asm 1: cmovc 40(<input_2=int64#2),<t4=int64#11
# asm 2: cmovc 40(<input_2=%rsi),<t4=%r13
cmovc 40(%rsi),%r13

# qhasm: t5 = mem64[input_2 +48] if carry
# asm 1: cmovc 48(<input_2=int64#2),<t5=int64#12
# asm 2: cmovc 48(<input_2=%rsi),<t5=%r14
cmovc 48(%rsi),%r14

# qhasm: t6 = mem64[input_2 +56] if carry
# asm 1: cmovc 56(<input_2=int64#2),<t6=int64#13
# asm 2: cmovc 56(<input_2=%rsi),<t6=%r15
cmovc 56(%rsi),%r15

# qhasm: mem64[input_2 + 0] = t8
# asm 1: movq   <t8=int64#14,0(<input_2=int64#2)
# asm 2: movq   <t8=%rbx,0(<input_2=%rsi)
movq   %rbx,0(%rsi)

# qhasm: mem64[input_2 + 8] = t0
# asm 1: movq   <t0=int64#6,8(<input_2=int64#2)
# asm 2: movq   <t0=%r9,8(<input_2=%rsi)
movq   %r9,8(%rsi)

# qhasm: mem64[input_2 +16] = t1
# asm 1: movq   <t1=int64#8,16(<input_2=int64#2)
# asm 2: movq   <t1=%r10,16(<input_2=%rsi)
movq   %r10,16(%rsi)

# qhasm: mem64[input_2 +24] = t2
# asm 1: movq   <t2=int64#9,24(<input_2=int64#2)
# asm 2: movq   <t2=%r11,24(<input_2=%rsi)
movq   %r11,24(%rsi)

# qhasm: mem64[input_2 +32] = t3
# asm 1: movq   <t3=int64#10,32(<input_2=int64#2)
# asm 2: movq   <t3=%r12,32(<input_2=%rsi)
movq   %r12,32(%rsi)

# qhasm: mem64[input_2 +40] = t4
# asm 1: movq   <t4=int64#11,40(<input_2=int64#2)
# asm 2: movq   <t4=%r13,40(<input_2=%rsi)
movq   %r13,40(%rsi)

# qhasm: mem64[input_2 +48] = t5
# asm 1: movq   <t5=int64#12,48(<input_2=int64#2)
# asm 2: movq   <t5=%r14,48(<input_2=%rsi)
movq   %r14,48(%rsi)

# qhasm: mem64[input_2 +56] = t6
# asm 1: movq   <t6=int64#13,56(<input_2=int64#2)
# asm 2: movq   <t6=%r15,56(<input_2=%rsi)
movq   %r15,56(%rsi)

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

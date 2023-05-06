
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

# qhasm: int64 p0

# qhasm: int64 p1

# qhasm: int64 p2

# qhasm: int64 s0

# qhasm: int64 t0

# qhasm: int64 t1

# qhasm: int64 t2

# qhasm: int64 t3

# qhasm: int64 a0

# qhasm: int64 a1

# qhasm: int64 a2

# qhasm: int64 a3

# qhasm: int64 rax

# qhasm: int64 rdx

# qhasm: int64 flag

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

# qhasm: enter muls128xs128
.p2align 5
.global _muls128xs128
.global muls128xs128
_muls128xs128:
muls128xs128:
mov %rsp,%r11
and $31,%r11
add $96,%r11
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

# qhasm: input_0_save = input_0
# asm 1: movq <input_0=int64#1,>input_0_save=stack64#8
# asm 2: movq <input_0=%rdi,>input_0_save=56(%rsp)
movq %rdi,56(%rsp)

# qhasm: input_1_save = input_1
# asm 1: movq <input_1=int64#2,>input_1_save=stack64#9
# asm 2: movq <input_1=%rsi,>input_1_save=64(%rsp)
movq %rsi,64(%rsp)

# qhasm: input_2_save = input_2
# asm 1: movq <input_2=int64#3,>input_2_save=stack64#10
# asm 2: movq <input_2=%rdx,>input_2_save=72(%rsp)
movq %rdx,72(%rsp)

# qhasm: p0 = input_0_save
# asm 1: movq <input_0_save=stack64#8,>p0=int64#1
# asm 2: movq <input_0_save=56(%rsp),>p0=%rdi
movq 56(%rsp),%rdi

# qhasm: p1 = input_1_save
# asm 1: movq <input_1_save=stack64#9,>p1=int64#2
# asm 2: movq <input_1_save=64(%rsp),>p1=%rsi
movq 64(%rsp),%rsi

# qhasm: rax = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>rax=int64#7
# asm 2: movq   0(<p0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (uint128) rdx rax = rax * mem64[ p1 + 0 ]
# asm 1: mulq  0(<p1=int64#2)
# asm 2: mulq  0(<p1=%rsi)
mulq  0(%rsi)

# qhasm: t0 = rax
# asm 1: mov  <rax=int64#7,>t0=int64#4
# asm 2: mov  <rax=%rax,>t0=%rcx
mov  %rax,%rcx

# qhasm: t1 = rdx
# asm 1: mov  <rdx=int64#3,>t1=int64#5
# asm 2: mov  <rdx=%rdx,>t1=%r8
mov  %rdx,%r8

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ p1 + 8 ]
# asm 1: imulq  8(<p1=int64#2)
# asm 2: imulq  8(<p1=%rsi)
imulq  8(%rsi)

# qhasm: t2 = rax
# asm 1: mov  <rax=int64#7,>t2=int64#6
# asm 2: mov  <rax=%rax,>t2=%r9
mov  %rax,%r9

# qhasm: t3 = rdx
# asm 1: mov  <rdx=int64#3,>t3=int64#8
# asm 2: mov  <rdx=%rdx,>t3=%r10
mov  %rdx,%r10

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#9
# asm 2: mov  <rax=%rax,>flag=%r11
mov  %rax,%r11

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#9
# asm 2: sar  $63,<flag=%r11
sar  $63,%r11

# qhasm: s0 = mem64[ p1 + 0 ]
# asm 1: movq   0(<p1=int64#2),>s0=int64#10
# asm 2: movq   0(<p1=%rsi),>s0=%r12
movq   0(%rsi),%r12

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#10
# asm 2: mul  <s0=%r12
mul  %r12

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#9,<s0=int64#10
# asm 2: and  <flag=%r11,<s0=%r12
and  %r11,%r12

# qhasm: carry? t1 += rax
# asm 1: add  <rax=int64#7,<t1=int64#5
# asm 2: add  <rax=%rax,<t1=%r8
add  %rax,%r8

# qhasm: carry? t2 += rdx + carry
# asm 1: adc <rdx=int64#3,<t2=int64#6
# asm 2: adc <rdx=%rdx,<t2=%r9
adc %rdx,%r9

# qhasm: t3 += 0 + carry
# asm 1: adc $0,<t3=int64#8
# asm 2: adc $0,<t3=%r10
adc $0,%r10

# qhasm: carry? t2 -= s0
# asm 1: sub  <s0=int64#10,<t2=int64#6
# asm 2: sub  <s0=%r12,<t2=%r9
sub  %r12,%r9

# qhasm: t3 -= 0 - carry
# asm 1: sbb  $0,<t3=int64#8
# asm 2: sbb  $0,<t3=%r10
sbb  $0,%r10

# qhasm: rax = mem64[ p1 + 8 ]
# asm 1: movq   8(<p1=int64#2),>rax=int64#7
# asm 2: movq   8(<p1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#2
# asm 2: mov  <rax=%rax,>flag=%rsi
mov  %rax,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: s0 = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>s0=int64#1
# asm 2: movq   0(<p0=%rdi),>s0=%rdi
movq   0(%rdi),%rdi

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#1
# asm 2: mul  <s0=%rdi
mul  %rdi

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#2,<s0=int64#1
# asm 2: and  <flag=%rsi,<s0=%rdi
and  %rsi,%rdi

# qhasm: carry? t1 += rax
# asm 1: add  <rax=int64#7,<t1=int64#5
# asm 2: add  <rax=%rax,<t1=%r8
add  %rax,%r8

# qhasm: carry? t2 += rdx + carry
# asm 1: adc <rdx=int64#3,<t2=int64#6
# asm 2: adc <rdx=%rdx,<t2=%r9
adc %rdx,%r9

# qhasm: t3 += 0 + carry
# asm 1: adc $0,<t3=int64#8
# asm 2: adc $0,<t3=%r10
adc $0,%r10

# qhasm: carry? t2 -= s0
# asm 1: sub  <s0=int64#1,<t2=int64#6
# asm 2: sub  <s0=%rdi,<t2=%r9
sub  %rdi,%r9

# qhasm: t3 -= 0 - carry
# asm 1: sbb  $0,<t3=int64#8
# asm 2: sbb  $0,<t3=%r10
sbb  $0,%r10

# qhasm: p0 = 16
# asm 1: mov  $16,>p0=int64#1
# asm 2: mov  $16,>p0=%rdi
mov  $16,%rdi

# qhasm: p1 = 32
# asm 1: mov  $32,>p1=int64#2
# asm 2: mov  $32,>p1=%rsi
mov  $32,%rsi

# qhasm: p0 += input_0_save
# asm 1: addq <input_0_save=stack64#8,<p0=int64#1
# asm 2: addq <input_0_save=56(%rsp),<p0=%rdi
addq 56(%rsp),%rdi

# qhasm: p1 += input_1_save
# asm 1: addq <input_1_save=stack64#9,<p1=int64#2
# asm 2: addq <input_1_save=64(%rsp),<p1=%rsi
addq 64(%rsp),%rsi

# qhasm: rax = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>rax=int64#7
# asm 2: movq   0(<p0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (uint128) rdx rax = rax * mem64[ p1 + 0 ]
# asm 1: mulq  0(<p1=int64#2)
# asm 2: mulq  0(<p1=%rsi)
mulq  0(%rsi)

# qhasm: a0 = rax
# asm 1: mov  <rax=int64#7,>a0=int64#9
# asm 2: mov  <rax=%rax,>a0=%r11
mov  %rax,%r11

# qhasm: a1 = rdx
# asm 1: mov  <rdx=int64#3,>a1=int64#10
# asm 2: mov  <rdx=%rdx,>a1=%r12
mov  %rdx,%r12

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ p1 + 8 ]
# asm 1: imulq  8(<p1=int64#2)
# asm 2: imulq  8(<p1=%rsi)
imulq  8(%rsi)

# qhasm: a2 = rax
# asm 1: mov  <rax=int64#7,>a2=int64#11
# asm 2: mov  <rax=%rax,>a2=%r13
mov  %rax,%r13

# qhasm: a3 = rdx
# asm 1: mov  <rdx=int64#3,>a3=int64#12
# asm 2: mov  <rdx=%rdx,>a3=%r14
mov  %rdx,%r14

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#13
# asm 2: mov  <rax=%rax,>flag=%r15
mov  %rax,%r15

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#13
# asm 2: sar  $63,<flag=%r15
sar  $63,%r15

# qhasm: s0 = mem64[ p1 + 0 ]
# asm 1: movq   0(<p1=int64#2),>s0=int64#14
# asm 2: movq   0(<p1=%rsi),>s0=%rbx
movq   0(%rsi),%rbx

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#14
# asm 2: mul  <s0=%rbx
mul  %rbx

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#13,<s0=int64#14
# asm 2: and  <flag=%r15,<s0=%rbx
and  %r15,%rbx

# qhasm: carry? a1 += rax
# asm 1: add  <rax=int64#7,<a1=int64#10
# asm 2: add  <rax=%rax,<a1=%r12
add  %rax,%r12

# qhasm: carry? a2 += rdx + carry
# asm 1: adc <rdx=int64#3,<a2=int64#11
# asm 2: adc <rdx=%rdx,<a2=%r13
adc %rdx,%r13

# qhasm: a3 += 0 + carry
# asm 1: adc $0,<a3=int64#12
# asm 2: adc $0,<a3=%r14
adc $0,%r14

# qhasm: carry? a2 -= s0
# asm 1: sub  <s0=int64#14,<a2=int64#11
# asm 2: sub  <s0=%rbx,<a2=%r13
sub  %rbx,%r13

# qhasm: a3 -= 0 - carry
# asm 1: sbb  $0,<a3=int64#12
# asm 2: sbb  $0,<a3=%r14
sbb  $0,%r14

# qhasm: rax = mem64[ p1 + 8 ]
# asm 1: movq   8(<p1=int64#2),>rax=int64#7
# asm 2: movq   8(<p1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#2
# asm 2: mov  <rax=%rax,>flag=%rsi
mov  %rax,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: s0 = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>s0=int64#1
# asm 2: movq   0(<p0=%rdi),>s0=%rdi
movq   0(%rdi),%rdi

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#1
# asm 2: mul  <s0=%rdi
mul  %rdi

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#2,<s0=int64#1
# asm 2: and  <flag=%rsi,<s0=%rdi
and  %rsi,%rdi

# qhasm: carry? a1 += rax
# asm 1: add  <rax=int64#7,<a1=int64#10
# asm 2: add  <rax=%rax,<a1=%r12
add  %rax,%r12

# qhasm: carry? a2 += rdx + carry
# asm 1: adc <rdx=int64#3,<a2=int64#11
# asm 2: adc <rdx=%rdx,<a2=%r13
adc %rdx,%r13

# qhasm: a3 += 0 + carry
# asm 1: adc $0,<a3=int64#12
# asm 2: adc $0,<a3=%r14
adc $0,%r14

# qhasm: carry? a2 -= s0
# asm 1: sub  <s0=int64#1,<a2=int64#11
# asm 2: sub  <s0=%rdi,<a2=%r13
sub  %rdi,%r13

# qhasm: a3 -= 0 - carry
# asm 1: sbb  $0,<a3=int64#12
# asm 2: sbb  $0,<a3=%r14
sbb  $0,%r14

# qhasm: carry? a0 += t0
# asm 1: add  <t0=int64#4,<a0=int64#9
# asm 2: add  <t0=%rcx,<a0=%r11
add  %rcx,%r11

# qhasm: carry? a1 += t1 + carry
# asm 1: adc <t1=int64#5,<a1=int64#10
# asm 2: adc <t1=%r8,<a1=%r12
adc %r8,%r12

# qhasm: carry? a2 += t2 + carry
# asm 1: adc <t2=int64#6,<a2=int64#11
# asm 2: adc <t2=%r9,<a2=%r13
adc %r9,%r13

# qhasm: a3 += t3 + carry
# asm 1: adc <t3=int64#8,<a3=int64#12
# asm 2: adc <t3=%r10,<a3=%r14
adc %r10,%r14

# qhasm: p2 = input_2_save
# asm 1: movq <input_2_save=stack64#10,>p2=int64#1
# asm 2: movq <input_2_save=72(%rsp),>p2=%rdi
movq 72(%rsp),%rdi

# qhasm: mem64[ p2 + 0 ] = a0
# asm 1: movq   <a0=int64#9,0(<p2=int64#1)
# asm 2: movq   <a0=%r11,0(<p2=%rdi)
movq   %r11,0(%rdi)

# qhasm: mem64[ p2 + 8 ] = a1
# asm 1: movq   <a1=int64#10,8(<p2=int64#1)
# asm 2: movq   <a1=%r12,8(<p2=%rdi)
movq   %r12,8(%rdi)

# qhasm: mem64[ p2 +16 ] = a2
# asm 1: movq   <a2=int64#11,16(<p2=int64#1)
# asm 2: movq   <a2=%r13,16(<p2=%rdi)
movq   %r13,16(%rdi)

# qhasm: mem64[ p2 +24 ] = a3
# asm 1: movq   <a3=int64#12,24(<p2=int64#1)
# asm 2: movq   <a3=%r14,24(<p2=%rdi)
movq   %r14,24(%rdi)

# qhasm: p2 += 32
# asm 1: add  $32,<p2=int64#1
# asm 2: add  $32,<p2=%rdi
add  $32,%rdi

# qhasm: input_2_save = p2
# asm 1: movq <p2=int64#1,>input_2_save=stack64#10
# asm 2: movq <p2=%rdi,>input_2_save=72(%rsp)
movq %rdi,72(%rsp)

# qhasm: p0 = input_0_save
# asm 1: movq <input_0_save=stack64#8,>p0=int64#1
# asm 2: movq <input_0_save=56(%rsp),>p0=%rdi
movq 56(%rsp),%rdi

# qhasm: p1 = 16
# asm 1: mov  $16,>p1=int64#2
# asm 2: mov  $16,>p1=%rsi
mov  $16,%rsi

# qhasm: p1 += input_1_save
# asm 1: addq <input_1_save=stack64#9,<p1=int64#2
# asm 2: addq <input_1_save=64(%rsp),<p1=%rsi
addq 64(%rsp),%rsi

# qhasm: rax = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>rax=int64#7
# asm 2: movq   0(<p0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (uint128) rdx rax = rax * mem64[ p1 + 0 ]
# asm 1: mulq  0(<p1=int64#2)
# asm 2: mulq  0(<p1=%rsi)
mulq  0(%rsi)

# qhasm: t0 = rax
# asm 1: mov  <rax=int64#7,>t0=int64#4
# asm 2: mov  <rax=%rax,>t0=%rcx
mov  %rax,%rcx

# qhasm: t1 = rdx
# asm 1: mov  <rdx=int64#3,>t1=int64#5
# asm 2: mov  <rdx=%rdx,>t1=%r8
mov  %rdx,%r8

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ p1 + 8 ]
# asm 1: imulq  8(<p1=int64#2)
# asm 2: imulq  8(<p1=%rsi)
imulq  8(%rsi)

# qhasm: t2 = rax
# asm 1: mov  <rax=int64#7,>t2=int64#6
# asm 2: mov  <rax=%rax,>t2=%r9
mov  %rax,%r9

# qhasm: t3 = rdx
# asm 1: mov  <rdx=int64#3,>t3=int64#8
# asm 2: mov  <rdx=%rdx,>t3=%r10
mov  %rdx,%r10

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#9
# asm 2: mov  <rax=%rax,>flag=%r11
mov  %rax,%r11

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#9
# asm 2: sar  $63,<flag=%r11
sar  $63,%r11

# qhasm: s0 = mem64[ p1 + 0 ]
# asm 1: movq   0(<p1=int64#2),>s0=int64#10
# asm 2: movq   0(<p1=%rsi),>s0=%r12
movq   0(%rsi),%r12

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#10
# asm 2: mul  <s0=%r12
mul  %r12

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#9,<s0=int64#10
# asm 2: and  <flag=%r11,<s0=%r12
and  %r11,%r12

# qhasm: carry? t1 += rax
# asm 1: add  <rax=int64#7,<t1=int64#5
# asm 2: add  <rax=%rax,<t1=%r8
add  %rax,%r8

# qhasm: carry? t2 += rdx + carry
# asm 1: adc <rdx=int64#3,<t2=int64#6
# asm 2: adc <rdx=%rdx,<t2=%r9
adc %rdx,%r9

# qhasm: t3 += 0 + carry
# asm 1: adc $0,<t3=int64#8
# asm 2: adc $0,<t3=%r10
adc $0,%r10

# qhasm: carry? t2 -= s0
# asm 1: sub  <s0=int64#10,<t2=int64#6
# asm 2: sub  <s0=%r12,<t2=%r9
sub  %r12,%r9

# qhasm: t3 -= 0 - carry
# asm 1: sbb  $0,<t3=int64#8
# asm 2: sbb  $0,<t3=%r10
sbb  $0,%r10

# qhasm: rax = mem64[ p1 + 8 ]
# asm 1: movq   8(<p1=int64#2),>rax=int64#7
# asm 2: movq   8(<p1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#2
# asm 2: mov  <rax=%rax,>flag=%rsi
mov  %rax,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: s0 = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>s0=int64#1
# asm 2: movq   0(<p0=%rdi),>s0=%rdi
movq   0(%rdi),%rdi

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#1
# asm 2: mul  <s0=%rdi
mul  %rdi

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#2,<s0=int64#1
# asm 2: and  <flag=%rsi,<s0=%rdi
and  %rsi,%rdi

# qhasm: carry? t1 += rax
# asm 1: add  <rax=int64#7,<t1=int64#5
# asm 2: add  <rax=%rax,<t1=%r8
add  %rax,%r8

# qhasm: carry? t2 += rdx + carry
# asm 1: adc <rdx=int64#3,<t2=int64#6
# asm 2: adc <rdx=%rdx,<t2=%r9
adc %rdx,%r9

# qhasm: t3 += 0 + carry
# asm 1: adc $0,<t3=int64#8
# asm 2: adc $0,<t3=%r10
adc $0,%r10

# qhasm: carry? t2 -= s0
# asm 1: sub  <s0=int64#1,<t2=int64#6
# asm 2: sub  <s0=%rdi,<t2=%r9
sub  %rdi,%r9

# qhasm: t3 -= 0 - carry
# asm 1: sbb  $0,<t3=int64#8
# asm 2: sbb  $0,<t3=%r10
sbb  $0,%r10

# qhasm: p0 = 16
# asm 1: mov  $16,>p0=int64#1
# asm 2: mov  $16,>p0=%rdi
mov  $16,%rdi

# qhasm: p1 = 48
# asm 1: mov  $48,>p1=int64#2
# asm 2: mov  $48,>p1=%rsi
mov  $48,%rsi

# qhasm: p0 += input_0_save
# asm 1: addq <input_0_save=stack64#8,<p0=int64#1
# asm 2: addq <input_0_save=56(%rsp),<p0=%rdi
addq 56(%rsp),%rdi

# qhasm: p1 += input_1_save
# asm 1: addq <input_1_save=stack64#9,<p1=int64#2
# asm 2: addq <input_1_save=64(%rsp),<p1=%rsi
addq 64(%rsp),%rsi

# qhasm: rax = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>rax=int64#7
# asm 2: movq   0(<p0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (uint128) rdx rax = rax * mem64[ p1 + 0 ]
# asm 1: mulq  0(<p1=int64#2)
# asm 2: mulq  0(<p1=%rsi)
mulq  0(%rsi)

# qhasm: a0 = rax
# asm 1: mov  <rax=int64#7,>a0=int64#9
# asm 2: mov  <rax=%rax,>a0=%r11
mov  %rax,%r11

# qhasm: a1 = rdx
# asm 1: mov  <rdx=int64#3,>a1=int64#10
# asm 2: mov  <rdx=%rdx,>a1=%r12
mov  %rdx,%r12

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ p1 + 8 ]
# asm 1: imulq  8(<p1=int64#2)
# asm 2: imulq  8(<p1=%rsi)
imulq  8(%rsi)

# qhasm: a2 = rax
# asm 1: mov  <rax=int64#7,>a2=int64#11
# asm 2: mov  <rax=%rax,>a2=%r13
mov  %rax,%r13

# qhasm: a3 = rdx
# asm 1: mov  <rdx=int64#3,>a3=int64#12
# asm 2: mov  <rdx=%rdx,>a3=%r14
mov  %rdx,%r14

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#13
# asm 2: mov  <rax=%rax,>flag=%r15
mov  %rax,%r15

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#13
# asm 2: sar  $63,<flag=%r15
sar  $63,%r15

# qhasm: s0 = mem64[ p1 + 0 ]
# asm 1: movq   0(<p1=int64#2),>s0=int64#14
# asm 2: movq   0(<p1=%rsi),>s0=%rbx
movq   0(%rsi),%rbx

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#14
# asm 2: mul  <s0=%rbx
mul  %rbx

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#13,<s0=int64#14
# asm 2: and  <flag=%r15,<s0=%rbx
and  %r15,%rbx

# qhasm: carry? a1 += rax
# asm 1: add  <rax=int64#7,<a1=int64#10
# asm 2: add  <rax=%rax,<a1=%r12
add  %rax,%r12

# qhasm: carry? a2 += rdx + carry
# asm 1: adc <rdx=int64#3,<a2=int64#11
# asm 2: adc <rdx=%rdx,<a2=%r13
adc %rdx,%r13

# qhasm: a3 += 0 + carry
# asm 1: adc $0,<a3=int64#12
# asm 2: adc $0,<a3=%r14
adc $0,%r14

# qhasm: carry? a2 -= s0
# asm 1: sub  <s0=int64#14,<a2=int64#11
# asm 2: sub  <s0=%rbx,<a2=%r13
sub  %rbx,%r13

# qhasm: a3 -= 0 - carry
# asm 1: sbb  $0,<a3=int64#12
# asm 2: sbb  $0,<a3=%r14
sbb  $0,%r14

# qhasm: rax = mem64[ p1 + 8 ]
# asm 1: movq   8(<p1=int64#2),>rax=int64#7
# asm 2: movq   8(<p1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#2
# asm 2: mov  <rax=%rax,>flag=%rsi
mov  %rax,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: s0 = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>s0=int64#1
# asm 2: movq   0(<p0=%rdi),>s0=%rdi
movq   0(%rdi),%rdi

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#1
# asm 2: mul  <s0=%rdi
mul  %rdi

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#2,<s0=int64#1
# asm 2: and  <flag=%rsi,<s0=%rdi
and  %rsi,%rdi

# qhasm: carry? a1 += rax
# asm 1: add  <rax=int64#7,<a1=int64#10
# asm 2: add  <rax=%rax,<a1=%r12
add  %rax,%r12

# qhasm: carry? a2 += rdx + carry
# asm 1: adc <rdx=int64#3,<a2=int64#11
# asm 2: adc <rdx=%rdx,<a2=%r13
adc %rdx,%r13

# qhasm: a3 += 0 + carry
# asm 1: adc $0,<a3=int64#12
# asm 2: adc $0,<a3=%r14
adc $0,%r14

# qhasm: carry? a2 -= s0
# asm 1: sub  <s0=int64#1,<a2=int64#11
# asm 2: sub  <s0=%rdi,<a2=%r13
sub  %rdi,%r13

# qhasm: a3 -= 0 - carry
# asm 1: sbb  $0,<a3=int64#12
# asm 2: sbb  $0,<a3=%r14
sbb  $0,%r14

# qhasm: carry? a0 += t0
# asm 1: add  <t0=int64#4,<a0=int64#9
# asm 2: add  <t0=%rcx,<a0=%r11
add  %rcx,%r11

# qhasm: carry? a1 += t1 + carry
# asm 1: adc <t1=int64#5,<a1=int64#10
# asm 2: adc <t1=%r8,<a1=%r12
adc %r8,%r12

# qhasm: carry? a2 += t2 + carry
# asm 1: adc <t2=int64#6,<a2=int64#11
# asm 2: adc <t2=%r9,<a2=%r13
adc %r9,%r13

# qhasm: a3 += t3 + carry
# asm 1: adc <t3=int64#8,<a3=int64#12
# asm 2: adc <t3=%r10,<a3=%r14
adc %r10,%r14

# qhasm: p2 = input_2_save
# asm 1: movq <input_2_save=stack64#10,>p2=int64#1
# asm 2: movq <input_2_save=72(%rsp),>p2=%rdi
movq 72(%rsp),%rdi

# qhasm: mem64[ p2 + 0 ] = a0
# asm 1: movq   <a0=int64#9,0(<p2=int64#1)
# asm 2: movq   <a0=%r11,0(<p2=%rdi)
movq   %r11,0(%rdi)

# qhasm: mem64[ p2 + 8 ] = a1
# asm 1: movq   <a1=int64#10,8(<p2=int64#1)
# asm 2: movq   <a1=%r12,8(<p2=%rdi)
movq   %r12,8(%rdi)

# qhasm: mem64[ p2 +16 ] = a2
# asm 1: movq   <a2=int64#11,16(<p2=int64#1)
# asm 2: movq   <a2=%r13,16(<p2=%rdi)
movq   %r13,16(%rdi)

# qhasm: mem64[ p2 +24 ] = a3
# asm 1: movq   <a3=int64#12,24(<p2=int64#1)
# asm 2: movq   <a3=%r14,24(<p2=%rdi)
movq   %r14,24(%rdi)

# qhasm: p2 += 32
# asm 1: add  $32,<p2=int64#1
# asm 2: add  $32,<p2=%rdi
add  $32,%rdi

# qhasm: input_2_save = p2
# asm 1: movq <p2=int64#1,>input_2_save=stack64#10
# asm 2: movq <p2=%rdi,>input_2_save=72(%rsp)
movq %rdi,72(%rsp)

# qhasm: p0 = 32
# asm 1: mov  $32,>p0=int64#1
# asm 2: mov  $32,>p0=%rdi
mov  $32,%rdi

# qhasm: p0 += input_0_save
# asm 1: addq <input_0_save=stack64#8,<p0=int64#1
# asm 2: addq <input_0_save=56(%rsp),<p0=%rdi
addq 56(%rsp),%rdi

# qhasm: p1 = input_1_save
# asm 1: movq <input_1_save=stack64#9,>p1=int64#2
# asm 2: movq <input_1_save=64(%rsp),>p1=%rsi
movq 64(%rsp),%rsi

# qhasm: rax = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>rax=int64#7
# asm 2: movq   0(<p0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (uint128) rdx rax = rax * mem64[ p1 + 0 ]
# asm 1: mulq  0(<p1=int64#2)
# asm 2: mulq  0(<p1=%rsi)
mulq  0(%rsi)

# qhasm: t0 = rax
# asm 1: mov  <rax=int64#7,>t0=int64#4
# asm 2: mov  <rax=%rax,>t0=%rcx
mov  %rax,%rcx

# qhasm: t1 = rdx
# asm 1: mov  <rdx=int64#3,>t1=int64#5
# asm 2: mov  <rdx=%rdx,>t1=%r8
mov  %rdx,%r8

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ p1 + 8 ]
# asm 1: imulq  8(<p1=int64#2)
# asm 2: imulq  8(<p1=%rsi)
imulq  8(%rsi)

# qhasm: t2 = rax
# asm 1: mov  <rax=int64#7,>t2=int64#6
# asm 2: mov  <rax=%rax,>t2=%r9
mov  %rax,%r9

# qhasm: t3 = rdx
# asm 1: mov  <rdx=int64#3,>t3=int64#8
# asm 2: mov  <rdx=%rdx,>t3=%r10
mov  %rdx,%r10

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#9
# asm 2: mov  <rax=%rax,>flag=%r11
mov  %rax,%r11

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#9
# asm 2: sar  $63,<flag=%r11
sar  $63,%r11

# qhasm: s0 = mem64[ p1 + 0 ]
# asm 1: movq   0(<p1=int64#2),>s0=int64#10
# asm 2: movq   0(<p1=%rsi),>s0=%r12
movq   0(%rsi),%r12

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#10
# asm 2: mul  <s0=%r12
mul  %r12

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#9,<s0=int64#10
# asm 2: and  <flag=%r11,<s0=%r12
and  %r11,%r12

# qhasm: carry? t1 += rax
# asm 1: add  <rax=int64#7,<t1=int64#5
# asm 2: add  <rax=%rax,<t1=%r8
add  %rax,%r8

# qhasm: carry? t2 += rdx + carry
# asm 1: adc <rdx=int64#3,<t2=int64#6
# asm 2: adc <rdx=%rdx,<t2=%r9
adc %rdx,%r9

# qhasm: t3 += 0 + carry
# asm 1: adc $0,<t3=int64#8
# asm 2: adc $0,<t3=%r10
adc $0,%r10

# qhasm: carry? t2 -= s0
# asm 1: sub  <s0=int64#10,<t2=int64#6
# asm 2: sub  <s0=%r12,<t2=%r9
sub  %r12,%r9

# qhasm: t3 -= 0 - carry
# asm 1: sbb  $0,<t3=int64#8
# asm 2: sbb  $0,<t3=%r10
sbb  $0,%r10

# qhasm: rax = mem64[ p1 + 8 ]
# asm 1: movq   8(<p1=int64#2),>rax=int64#7
# asm 2: movq   8(<p1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#2
# asm 2: mov  <rax=%rax,>flag=%rsi
mov  %rax,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: s0 = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>s0=int64#1
# asm 2: movq   0(<p0=%rdi),>s0=%rdi
movq   0(%rdi),%rdi

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#1
# asm 2: mul  <s0=%rdi
mul  %rdi

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#2,<s0=int64#1
# asm 2: and  <flag=%rsi,<s0=%rdi
and  %rsi,%rdi

# qhasm: carry? t1 += rax
# asm 1: add  <rax=int64#7,<t1=int64#5
# asm 2: add  <rax=%rax,<t1=%r8
add  %rax,%r8

# qhasm: carry? t2 += rdx + carry
# asm 1: adc <rdx=int64#3,<t2=int64#6
# asm 2: adc <rdx=%rdx,<t2=%r9
adc %rdx,%r9

# qhasm: t3 += 0 + carry
# asm 1: adc $0,<t3=int64#8
# asm 2: adc $0,<t3=%r10
adc $0,%r10

# qhasm: carry? t2 -= s0
# asm 1: sub  <s0=int64#1,<t2=int64#6
# asm 2: sub  <s0=%rdi,<t2=%r9
sub  %rdi,%r9

# qhasm: t3 -= 0 - carry
# asm 1: sbb  $0,<t3=int64#8
# asm 2: sbb  $0,<t3=%r10
sbb  $0,%r10

# qhasm: p0 = 48
# asm 1: mov  $48,>p0=int64#1
# asm 2: mov  $48,>p0=%rdi
mov  $48,%rdi

# qhasm: p1 = 32
# asm 1: mov  $32,>p1=int64#2
# asm 2: mov  $32,>p1=%rsi
mov  $32,%rsi

# qhasm: p0 += input_0_save
# asm 1: addq <input_0_save=stack64#8,<p0=int64#1
# asm 2: addq <input_0_save=56(%rsp),<p0=%rdi
addq 56(%rsp),%rdi

# qhasm: p1 += input_1_save
# asm 1: addq <input_1_save=stack64#9,<p1=int64#2
# asm 2: addq <input_1_save=64(%rsp),<p1=%rsi
addq 64(%rsp),%rsi

# qhasm: rax = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>rax=int64#7
# asm 2: movq   0(<p0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (uint128) rdx rax = rax * mem64[ p1 + 0 ]
# asm 1: mulq  0(<p1=int64#2)
# asm 2: mulq  0(<p1=%rsi)
mulq  0(%rsi)

# qhasm: a0 = rax
# asm 1: mov  <rax=int64#7,>a0=int64#9
# asm 2: mov  <rax=%rax,>a0=%r11
mov  %rax,%r11

# qhasm: a1 = rdx
# asm 1: mov  <rdx=int64#3,>a1=int64#10
# asm 2: mov  <rdx=%rdx,>a1=%r12
mov  %rdx,%r12

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ p1 + 8 ]
# asm 1: imulq  8(<p1=int64#2)
# asm 2: imulq  8(<p1=%rsi)
imulq  8(%rsi)

# qhasm: a2 = rax
# asm 1: mov  <rax=int64#7,>a2=int64#11
# asm 2: mov  <rax=%rax,>a2=%r13
mov  %rax,%r13

# qhasm: a3 = rdx
# asm 1: mov  <rdx=int64#3,>a3=int64#12
# asm 2: mov  <rdx=%rdx,>a3=%r14
mov  %rdx,%r14

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#13
# asm 2: mov  <rax=%rax,>flag=%r15
mov  %rax,%r15

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#13
# asm 2: sar  $63,<flag=%r15
sar  $63,%r15

# qhasm: s0 = mem64[ p1 + 0 ]
# asm 1: movq   0(<p1=int64#2),>s0=int64#14
# asm 2: movq   0(<p1=%rsi),>s0=%rbx
movq   0(%rsi),%rbx

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#14
# asm 2: mul  <s0=%rbx
mul  %rbx

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#13,<s0=int64#14
# asm 2: and  <flag=%r15,<s0=%rbx
and  %r15,%rbx

# qhasm: carry? a1 += rax
# asm 1: add  <rax=int64#7,<a1=int64#10
# asm 2: add  <rax=%rax,<a1=%r12
add  %rax,%r12

# qhasm: carry? a2 += rdx + carry
# asm 1: adc <rdx=int64#3,<a2=int64#11
# asm 2: adc <rdx=%rdx,<a2=%r13
adc %rdx,%r13

# qhasm: a3 += 0 + carry
# asm 1: adc $0,<a3=int64#12
# asm 2: adc $0,<a3=%r14
adc $0,%r14

# qhasm: carry? a2 -= s0
# asm 1: sub  <s0=int64#14,<a2=int64#11
# asm 2: sub  <s0=%rbx,<a2=%r13
sub  %rbx,%r13

# qhasm: a3 -= 0 - carry
# asm 1: sbb  $0,<a3=int64#12
# asm 2: sbb  $0,<a3=%r14
sbb  $0,%r14

# qhasm: rax = mem64[ p1 + 8 ]
# asm 1: movq   8(<p1=int64#2),>rax=int64#7
# asm 2: movq   8(<p1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#2
# asm 2: mov  <rax=%rax,>flag=%rsi
mov  %rax,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: s0 = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>s0=int64#1
# asm 2: movq   0(<p0=%rdi),>s0=%rdi
movq   0(%rdi),%rdi

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#1
# asm 2: mul  <s0=%rdi
mul  %rdi

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#2,<s0=int64#1
# asm 2: and  <flag=%rsi,<s0=%rdi
and  %rsi,%rdi

# qhasm: carry? a1 += rax
# asm 1: add  <rax=int64#7,<a1=int64#10
# asm 2: add  <rax=%rax,<a1=%r12
add  %rax,%r12

# qhasm: carry? a2 += rdx + carry
# asm 1: adc <rdx=int64#3,<a2=int64#11
# asm 2: adc <rdx=%rdx,<a2=%r13
adc %rdx,%r13

# qhasm: a3 += 0 + carry
# asm 1: adc $0,<a3=int64#12
# asm 2: adc $0,<a3=%r14
adc $0,%r14

# qhasm: carry? a2 -= s0
# asm 1: sub  <s0=int64#1,<a2=int64#11
# asm 2: sub  <s0=%rdi,<a2=%r13
sub  %rdi,%r13

# qhasm: a3 -= 0 - carry
# asm 1: sbb  $0,<a3=int64#12
# asm 2: sbb  $0,<a3=%r14
sbb  $0,%r14

# qhasm: carry? a0 += t0
# asm 1: add  <t0=int64#4,<a0=int64#9
# asm 2: add  <t0=%rcx,<a0=%r11
add  %rcx,%r11

# qhasm: carry? a1 += t1 + carry
# asm 1: adc <t1=int64#5,<a1=int64#10
# asm 2: adc <t1=%r8,<a1=%r12
adc %r8,%r12

# qhasm: carry? a2 += t2 + carry
# asm 1: adc <t2=int64#6,<a2=int64#11
# asm 2: adc <t2=%r9,<a2=%r13
adc %r9,%r13

# qhasm: a3 += t3 + carry
# asm 1: adc <t3=int64#8,<a3=int64#12
# asm 2: adc <t3=%r10,<a3=%r14
adc %r10,%r14

# qhasm: p2 = input_2_save
# asm 1: movq <input_2_save=stack64#10,>p2=int64#1
# asm 2: movq <input_2_save=72(%rsp),>p2=%rdi
movq 72(%rsp),%rdi

# qhasm: mem64[ p2 + 0 ] = a0
# asm 1: movq   <a0=int64#9,0(<p2=int64#1)
# asm 2: movq   <a0=%r11,0(<p2=%rdi)
movq   %r11,0(%rdi)

# qhasm: mem64[ p2 + 8 ] = a1
# asm 1: movq   <a1=int64#10,8(<p2=int64#1)
# asm 2: movq   <a1=%r12,8(<p2=%rdi)
movq   %r12,8(%rdi)

# qhasm: mem64[ p2 +16 ] = a2
# asm 1: movq   <a2=int64#11,16(<p2=int64#1)
# asm 2: movq   <a2=%r13,16(<p2=%rdi)
movq   %r13,16(%rdi)

# qhasm: mem64[ p2 +24 ] = a3
# asm 1: movq   <a3=int64#12,24(<p2=int64#1)
# asm 2: movq   <a3=%r14,24(<p2=%rdi)
movq   %r14,24(%rdi)

# qhasm: p2 += 32
# asm 1: add  $32,<p2=int64#1
# asm 2: add  $32,<p2=%rdi
add  $32,%rdi

# qhasm: input_2_save = p2
# asm 1: movq <p2=int64#1,>input_2_save=stack64#10
# asm 2: movq <p2=%rdi,>input_2_save=72(%rsp)
movq %rdi,72(%rsp)

# qhasm: p0 = 32
# asm 1: mov  $32,>p0=int64#1
# asm 2: mov  $32,>p0=%rdi
mov  $32,%rdi

# qhasm: p1 = 16
# asm 1: mov  $16,>p1=int64#2
# asm 2: mov  $16,>p1=%rsi
mov  $16,%rsi

# qhasm: p0 += input_0_save
# asm 1: addq <input_0_save=stack64#8,<p0=int64#1
# asm 2: addq <input_0_save=56(%rsp),<p0=%rdi
addq 56(%rsp),%rdi

# qhasm: p1 += input_1_save
# asm 1: addq <input_1_save=stack64#9,<p1=int64#2
# asm 2: addq <input_1_save=64(%rsp),<p1=%rsi
addq 64(%rsp),%rsi

# qhasm: rax = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>rax=int64#7
# asm 2: movq   0(<p0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (uint128) rdx rax = rax * mem64[ p1 + 0 ]
# asm 1: mulq  0(<p1=int64#2)
# asm 2: mulq  0(<p1=%rsi)
mulq  0(%rsi)

# qhasm: t0 = rax
# asm 1: mov  <rax=int64#7,>t0=int64#4
# asm 2: mov  <rax=%rax,>t0=%rcx
mov  %rax,%rcx

# qhasm: t1 = rdx
# asm 1: mov  <rdx=int64#3,>t1=int64#5
# asm 2: mov  <rdx=%rdx,>t1=%r8
mov  %rdx,%r8

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ p1 + 8 ]
# asm 1: imulq  8(<p1=int64#2)
# asm 2: imulq  8(<p1=%rsi)
imulq  8(%rsi)

# qhasm: t2 = rax
# asm 1: mov  <rax=int64#7,>t2=int64#6
# asm 2: mov  <rax=%rax,>t2=%r9
mov  %rax,%r9

# qhasm: t3 = rdx
# asm 1: mov  <rdx=int64#3,>t3=int64#8
# asm 2: mov  <rdx=%rdx,>t3=%r10
mov  %rdx,%r10

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#9
# asm 2: mov  <rax=%rax,>flag=%r11
mov  %rax,%r11

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#9
# asm 2: sar  $63,<flag=%r11
sar  $63,%r11

# qhasm: s0 = mem64[ p1 + 0 ]
# asm 1: movq   0(<p1=int64#2),>s0=int64#10
# asm 2: movq   0(<p1=%rsi),>s0=%r12
movq   0(%rsi),%r12

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#10
# asm 2: mul  <s0=%r12
mul  %r12

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#9,<s0=int64#10
# asm 2: and  <flag=%r11,<s0=%r12
and  %r11,%r12

# qhasm: carry? t1 += rax
# asm 1: add  <rax=int64#7,<t1=int64#5
# asm 2: add  <rax=%rax,<t1=%r8
add  %rax,%r8

# qhasm: carry? t2 += rdx + carry
# asm 1: adc <rdx=int64#3,<t2=int64#6
# asm 2: adc <rdx=%rdx,<t2=%r9
adc %rdx,%r9

# qhasm: t3 += 0 + carry
# asm 1: adc $0,<t3=int64#8
# asm 2: adc $0,<t3=%r10
adc $0,%r10

# qhasm: carry? t2 -= s0
# asm 1: sub  <s0=int64#10,<t2=int64#6
# asm 2: sub  <s0=%r12,<t2=%r9
sub  %r12,%r9

# qhasm: t3 -= 0 - carry
# asm 1: sbb  $0,<t3=int64#8
# asm 2: sbb  $0,<t3=%r10
sbb  $0,%r10

# qhasm: rax = mem64[ p1 + 8 ]
# asm 1: movq   8(<p1=int64#2),>rax=int64#7
# asm 2: movq   8(<p1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#2
# asm 2: mov  <rax=%rax,>flag=%rsi
mov  %rax,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: s0 = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>s0=int64#1
# asm 2: movq   0(<p0=%rdi),>s0=%rdi
movq   0(%rdi),%rdi

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#1
# asm 2: mul  <s0=%rdi
mul  %rdi

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#2,<s0=int64#1
# asm 2: and  <flag=%rsi,<s0=%rdi
and  %rsi,%rdi

# qhasm: carry? t1 += rax
# asm 1: add  <rax=int64#7,<t1=int64#5
# asm 2: add  <rax=%rax,<t1=%r8
add  %rax,%r8

# qhasm: carry? t2 += rdx + carry
# asm 1: adc <rdx=int64#3,<t2=int64#6
# asm 2: adc <rdx=%rdx,<t2=%r9
adc %rdx,%r9

# qhasm: t3 += 0 + carry
# asm 1: adc $0,<t3=int64#8
# asm 2: adc $0,<t3=%r10
adc $0,%r10

# qhasm: carry? t2 -= s0
# asm 1: sub  <s0=int64#1,<t2=int64#6
# asm 2: sub  <s0=%rdi,<t2=%r9
sub  %rdi,%r9

# qhasm: t3 -= 0 - carry
# asm 1: sbb  $0,<t3=int64#8
# asm 2: sbb  $0,<t3=%r10
sbb  $0,%r10

# qhasm: p0 = 48
# asm 1: mov  $48,>p0=int64#1
# asm 2: mov  $48,>p0=%rdi
mov  $48,%rdi

# qhasm: p1 = 48
# asm 1: mov  $48,>p1=int64#2
# asm 2: mov  $48,>p1=%rsi
mov  $48,%rsi

# qhasm: p0 += input_0_save
# asm 1: addq <input_0_save=stack64#8,<p0=int64#1
# asm 2: addq <input_0_save=56(%rsp),<p0=%rdi
addq 56(%rsp),%rdi

# qhasm: p1 += input_1_save
# asm 1: addq <input_1_save=stack64#9,<p1=int64#2
# asm 2: addq <input_1_save=64(%rsp),<p1=%rsi
addq 64(%rsp),%rsi

# qhasm: rax = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>rax=int64#7
# asm 2: movq   0(<p0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (uint128) rdx rax = rax * mem64[ p1 + 0 ]
# asm 1: mulq  0(<p1=int64#2)
# asm 2: mulq  0(<p1=%rsi)
mulq  0(%rsi)

# qhasm: a0 = rax
# asm 1: mov  <rax=int64#7,>a0=int64#9
# asm 2: mov  <rax=%rax,>a0=%r11
mov  %rax,%r11

# qhasm: a1 = rdx
# asm 1: mov  <rdx=int64#3,>a1=int64#10
# asm 2: mov  <rdx=%rdx,>a1=%r12
mov  %rdx,%r12

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ p1 + 8 ]
# asm 1: imulq  8(<p1=int64#2)
# asm 2: imulq  8(<p1=%rsi)
imulq  8(%rsi)

# qhasm: a2 = rax
# asm 1: mov  <rax=int64#7,>a2=int64#11
# asm 2: mov  <rax=%rax,>a2=%r13
mov  %rax,%r13

# qhasm: a3 = rdx
# asm 1: mov  <rdx=int64#3,>a3=int64#12
# asm 2: mov  <rdx=%rdx,>a3=%r14
mov  %rdx,%r14

# qhasm: rax = mem64[ p0 + 8 ]
# asm 1: movq   8(<p0=int64#1),>rax=int64#7
# asm 2: movq   8(<p0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#13
# asm 2: mov  <rax=%rax,>flag=%r15
mov  %rax,%r15

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#13
# asm 2: sar  $63,<flag=%r15
sar  $63,%r15

# qhasm: s0 = mem64[ p1 + 0 ]
# asm 1: movq   0(<p1=int64#2),>s0=int64#14
# asm 2: movq   0(<p1=%rsi),>s0=%rbx
movq   0(%rsi),%rbx

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#14
# asm 2: mul  <s0=%rbx
mul  %rbx

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#13,<s0=int64#14
# asm 2: and  <flag=%r15,<s0=%rbx
and  %r15,%rbx

# qhasm: carry? a1 += rax
# asm 1: add  <rax=int64#7,<a1=int64#10
# asm 2: add  <rax=%rax,<a1=%r12
add  %rax,%r12

# qhasm: carry? a2 += rdx + carry
# asm 1: adc <rdx=int64#3,<a2=int64#11
# asm 2: adc <rdx=%rdx,<a2=%r13
adc %rdx,%r13

# qhasm: a3 += 0 + carry
# asm 1: adc $0,<a3=int64#12
# asm 2: adc $0,<a3=%r14
adc $0,%r14

# qhasm: carry? a2 -= s0
# asm 1: sub  <s0=int64#14,<a2=int64#11
# asm 2: sub  <s0=%rbx,<a2=%r13
sub  %rbx,%r13

# qhasm: a3 -= 0 - carry
# asm 1: sbb  $0,<a3=int64#12
# asm 2: sbb  $0,<a3=%r14
sbb  $0,%r14

# qhasm: rax = mem64[ p1 + 8 ]
# asm 1: movq   8(<p1=int64#2),>rax=int64#7
# asm 2: movq   8(<p1=%rsi),>rax=%rax
movq   8(%rsi),%rax

# qhasm: flag = rax
# asm 1: mov  <rax=int64#7,>flag=int64#2
# asm 2: mov  <rax=%rax,>flag=%rsi
mov  %rax,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: s0 = mem64[ p0 + 0 ]
# asm 1: movq   0(<p0=int64#1),>s0=int64#1
# asm 2: movq   0(<p0=%rdi),>s0=%rdi
movq   0(%rdi),%rdi

# qhasm: (uint128) rdx rax = rax * s0
# asm 1: mul  <s0=int64#1
# asm 2: mul  <s0=%rdi
mul  %rdi

# qhasm: s0 &= flag
# asm 1: and  <flag=int64#2,<s0=int64#1
# asm 2: and  <flag=%rsi,<s0=%rdi
and  %rsi,%rdi

# qhasm: carry? a1 += rax
# asm 1: add  <rax=int64#7,<a1=int64#10
# asm 2: add  <rax=%rax,<a1=%r12
add  %rax,%r12

# qhasm: carry? a2 += rdx + carry
# asm 1: adc <rdx=int64#3,<a2=int64#11
# asm 2: adc <rdx=%rdx,<a2=%r13
adc %rdx,%r13

# qhasm: a3 += 0 + carry
# asm 1: adc $0,<a3=int64#12
# asm 2: adc $0,<a3=%r14
adc $0,%r14

# qhasm: carry? a2 -= s0
# asm 1: sub  <s0=int64#1,<a2=int64#11
# asm 2: sub  <s0=%rdi,<a2=%r13
sub  %rdi,%r13

# qhasm: a3 -= 0 - carry
# asm 1: sbb  $0,<a3=int64#12
# asm 2: sbb  $0,<a3=%r14
sbb  $0,%r14

# qhasm: carry? a0 += t0
# asm 1: add  <t0=int64#4,<a0=int64#9
# asm 2: add  <t0=%rcx,<a0=%r11
add  %rcx,%r11

# qhasm: carry? a1 += t1 + carry
# asm 1: adc <t1=int64#5,<a1=int64#10
# asm 2: adc <t1=%r8,<a1=%r12
adc %r8,%r12

# qhasm: carry? a2 += t2 + carry
# asm 1: adc <t2=int64#6,<a2=int64#11
# asm 2: adc <t2=%r9,<a2=%r13
adc %r9,%r13

# qhasm: a3 += t3 + carry
# asm 1: adc <t3=int64#8,<a3=int64#12
# asm 2: adc <t3=%r10,<a3=%r14
adc %r10,%r14

# qhasm: p2 = input_2_save
# asm 1: movq <input_2_save=stack64#10,>p2=int64#1
# asm 2: movq <input_2_save=72(%rsp),>p2=%rdi
movq 72(%rsp),%rdi

# qhasm: mem64[ p2 + 0 ] = a0
# asm 1: movq   <a0=int64#9,0(<p2=int64#1)
# asm 2: movq   <a0=%r11,0(<p2=%rdi)
movq   %r11,0(%rdi)

# qhasm: mem64[ p2 + 8 ] = a1
# asm 1: movq   <a1=int64#10,8(<p2=int64#1)
# asm 2: movq   <a1=%r12,8(<p2=%rdi)
movq   %r12,8(%rdi)

# qhasm: mem64[ p2 +16 ] = a2
# asm 1: movq   <a2=int64#11,16(<p2=int64#1)
# asm 2: movq   <a2=%r13,16(<p2=%rdi)
movq   %r13,16(%rdi)

# qhasm: mem64[ p2 +24 ] = a3
# asm 1: movq   <a3=int64#12,24(<p2=int64#1)
# asm 2: movq   <a3=%r14,24(<p2=%rdi)
movq   %r14,24(%rdi)

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

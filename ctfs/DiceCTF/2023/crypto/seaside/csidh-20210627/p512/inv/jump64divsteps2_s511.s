
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

# qhasm: const64 c_0=0
.p2align 5
c_0: .quad 0

# qhasm: const64 c_1=1
.p2align 5
c_1: .quad 1

# qhasm: const64 c_m1=-1
.p2align 5
c_m1: .quad -1

# qhasm: int64 r

# qhasm: int64 q

# qhasm: int64 u

# qhasm: int64 v

# qhasm: int64 f

# qhasm: int64 g

# qhasm: int64 delta

# qhasm: int64 count

# qhasm: int64 t0

# qhasm: int64 t1

# qhasm: int64 t2

# qhasm: int64 t3

# qhasm: int64 flag

# qhasm: int64 flag1

# qhasm: int64 g1

# qhasm: int64 q1

# qhasm: int64 r1

# qhasm: int64 t4

# qhasm: int64 t5

# qhasm: int64 t6

# qhasm: int64 t7

# qhasm: int64 t8

# qhasm: int64 a0

# qhasm: int64 a1

# qhasm: int64 a2

# qhasm: int64 a3

# qhasm: int64 a4

# qhasm: int64 a5

# qhasm: int64 a6

# qhasm: int64 a7

# qhasm: int64 a8

# qhasm: int64 b0

# qhasm: int64 b1

# qhasm: int64 b2

# qhasm: int64 b3

# qhasm: int64 b4

# qhasm: int64 b5

# qhasm: int64 b6

# qhasm: int64 b7

# qhasm: int64 b8

# qhasm: int64 rax

# qhasm: int64 rdx

# qhasm: stack64 caller_r11_stack

# qhasm: stack64 caller_r12_stack

# qhasm: stack64 caller_r13_stack

# qhasm: stack64 caller_r14_stack

# qhasm: stack64 caller_r15_stack

# qhasm: stack64 caller_rbp_stack

# qhasm: stack64 caller_rbx_stack

# qhasm: stack64 a0s

# qhasm: stack64 a1s

# qhasm: stack64 a2s

# qhasm: stack64 a3s

# qhasm: stack64 a4s

# qhasm: stack64 a5s

# qhasm: stack64 a6s

# qhasm: stack64 a7s

# qhasm: stack64 a8s

# qhasm: stack64 b0s

# qhasm: stack64 b1s

# qhasm: stack64 b2s

# qhasm: stack64 b3s

# qhasm: stack64 b4s

# qhasm: stack64 b5s

# qhasm: stack64 b6s

# qhasm: stack64 b7s

# qhasm: stack64 b8s

# qhasm: stack64 t0s

# qhasm: stack64 t1s

# qhasm: stack64 t2s

# qhasm: stack64 t3s

# qhasm: stack64 t4s

# qhasm: stack64 t5s

# qhasm: stack64 t6s

# qhasm: stack64 t7s

# qhasm: stack64 input_0_save

# qhasm: stack64 input_1_save

# qhasm: stack64 input_2_save

# qhasm: stack64 input_3_save

# qhasm: stack64 input_4_save

# qhasm: stack64 odd_count_save

# qhasm: enter jump64divsteps2_s511
.p2align 5
.global _jump64divsteps2_s511
.global jump64divsteps2_s511
_jump64divsteps2_s511:
jump64divsteps2_s511:
mov %rsp,%r11
and $31,%r11
add $256,%r11
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

# qhasm: count = input_0
# asm 1: mov  <input_0=int64#1,>count=int64#1
# asm 2: mov  <input_0=%rdi,>count=%rdi
mov  %rdi,%rdi

# qhasm: delta = input_1
# asm 1: mov  <input_1=int64#2,>delta=int64#2
# asm 2: mov  <input_1=%rsi,>delta=%rsi
mov  %rsi,%rsi

# qhasm: input_2_save = input_2
# asm 1: movq <input_2=int64#3,>input_2_save=stack64#9
# asm 2: movq <input_2=%rdx,>input_2_save=64(%rsp)
movq %rdx,64(%rsp)

# qhasm: input_3_save = input_3
# asm 1: movq <input_3=int64#4,>input_3_save=stack64#10
# asm 2: movq <input_3=%rcx,>input_3_save=72(%rsp)
movq %rcx,72(%rsp)

# qhasm: f = mem64[ input_2 + 0 ]
# asm 1: movq   0(<input_2=int64#3),>f=int64#3
# asm 2: movq   0(<input_2=%rdx),>f=%rdx
movq   0(%rdx),%rdx

# qhasm: g = mem64[ input_3 + 0 ]
# asm 1: movq   0(<input_3=int64#4),>g=int64#4
# asm 2: movq   0(<input_3=%rcx),>g=%rcx
movq   0(%rcx),%rcx

# qhasm: input_4_save = input_4
# asm 1: movq <input_4=int64#5,>input_4_save=stack64#11
# asm 2: movq <input_4=%r8,>input_4_save=80(%rsp)
movq %r8,80(%rsp)

# qhasm: r = 1
# asm 1: mov  $1,>r=int64#5
# asm 2: mov  $1,>r=%r8
mov  $1,%r8

# qhasm: u = r
# asm 1: mov  <r=int64#5,>u=int64#6
# asm 2: mov  <r=%r8,>u=%r9
mov  %r8,%r9

# qhasm: v = 0
# asm 1: mov  $0,>v=int64#7
# asm 2: mov  $0,>v=%rax
mov  $0,%rax

# qhasm: q = v
# asm 1: mov  <v=int64#7,>q=int64#8
# asm 2: mov  <v=%rax,>q=%r10
mov  %rax,%r10

# qhasm: t0 = 1
# asm 1: mov  $1,>t0=int64#9
# asm 2: mov  $1,>t0=%r11
mov  $1,%r11

# qhasm: t0 &= count
# asm 1: and  <count=int64#1,<t0=int64#9
# asm 2: and  <count=%rdi,<t0=%r11
and  %rdi,%r11

# qhasm: odd_count_save = t0
# asm 1: movq <t0=int64#9,>odd_count_save=stack64#12
# asm 2: movq <t0=%r11,>odd_count_save=88(%rsp)
movq %r11,88(%rsp)

# qhasm: (uint64) count >>= 1
# asm 1: shr  $1,<count=int64#1
# asm 2: shr  $1,<count=%rdi
shr  $1,%rdi

# qhasm: loop:
._loop:

# qhasm: t3 ^= t3
# asm 1: xor >t3=int64#9,>t3=int64#9
# asm 2: xor >t3=%r11,>t3=%r11
xor %r11,%r11

# qhasm: r1 ^= r1
# asm 1: xor >r1=int64#10,>r1=int64#10
# asm 2: xor >r1=%r12,>r1=%r12
xor %r12,%r12

# qhasm: t2 = mem64[c_m1]
# asm 1: movq c_m1,>t2=int64#11
# asm 2: movq c_m1,>t2=%r13
movq c_m1(%rip),%r13

# qhasm: t1 = mem64[c_1]
# asm 1: movq c_1,>t1=int64#12
# asm 2: movq c_1,>t1=%r14
movq c_1(%rip),%r14

# qhasm: signed<? t3 -= delta
# asm 1: sub  <delta=int64#2,<t3=int64#9
# asm 2: sub  <delta=%rsi,<t3=%r11
sub  %rsi,%r11

# qhasm: t2 = t1 if !signed<
# asm 1: cmovge <t1=int64#12,<t2=int64#11
# asm 2: cmovge <t1=%r14,<t2=%r13
cmovge %r14,%r13

# qhasm: t1 &= g
# asm 1: and  <g=int64#4,<t1=int64#12
# asm 2: and  <g=%rcx,<t1=%r14
and  %rcx,%r14

# qhasm: r1 -= t1
# asm 1: sub  <t1=int64#12,<r1=int64#10
# asm 2: sub  <t1=%r14,<r1=%r12
sub  %r14,%r12

# qhasm: g1 = f
# asm 1: mov  <f=int64#3,>g1=int64#13
# asm 2: mov  <f=%rdx,>g1=%r15
mov  %rdx,%r15

# qhasm: q1 = u
# asm 1: mov  <u=int64#6,>q1=int64#14
# asm 2: mov  <u=%r9,>q1=%rbx
mov  %r9,%rbx

# qhasm: r1 &= t2
# asm 1: and  <t2=int64#11,<r1=int64#10
# asm 2: and  <t2=%r13,<r1=%r12
and  %r13,%r12

# qhasm: g1 *= r1
# asm 1: imul  <r1=int64#10,<g1=int64#13
# asm 2: imul  <r1=%r12,<g1=%r15
imul  %r12,%r15

# qhasm: q1 *= r1
# asm 1: imul  <r1=int64#10,<q1=int64#14
# asm 2: imul  <r1=%r12,<q1=%rbx
imul  %r12,%rbx

# qhasm: r1 *= v
# asm 1: imul  <v=int64#7,<r1=int64#10
# asm 2: imul  <v=%rax,<r1=%r12
imul  %rax,%r12

# qhasm: g1 += g
# asm 1: add  <g=int64#4,<g1=int64#13
# asm 2: add  <g=%rcx,<g1=%r15
add  %rcx,%r15

# qhasm: =? t1 += t2
# asm 1: add  <t2=int64#11,<t1=int64#12
# asm 2: add  <t2=%r13,<t1=%r14
add  %r13,%r14

# qhasm: delta = t3 if =
# asm 1: cmove <t3=int64#9,<delta=int64#2
# asm 2: cmove <t3=%r11,<delta=%rsi
cmove %r11,%rsi

# qhasm: delta = delta + 1
# asm 1: lea  1(<delta=int64#2),>delta=int64#2
# asm 2: lea  1(<delta=%rsi),>delta=%rsi
lea  1(%rsi),%rsi

# qhasm: u = q if =
# asm 1: cmove <q=int64#8,<u=int64#6
# asm 2: cmove <q=%r10,<u=%r9
cmove %r10,%r9

# qhasm: v = r if =
# asm 1: cmove <r=int64#5,<v=int64#7
# asm 2: cmove <r=%r8,<v=%rax
cmove %r8,%rax

# qhasm: f = g if =
# asm 1: cmove <g=int64#4,<f=int64#3
# asm 2: cmove <g=%rcx,<f=%rdx
cmove %rcx,%rdx

# qhasm: u += u
# asm 1: add  <u=int64#6,<u=int64#6
# asm 2: add  <u=%r9,<u=%r9
add  %r9,%r9

# qhasm: v += v
# asm 1: add  <v=int64#7,<v=int64#7
# asm 2: add  <v=%rax,<v=%rax
add  %rax,%rax

# qhasm: (int64) g1 >>= 1
# asm 1: sar  $1,<g1=int64#13
# asm 2: sar  $1,<g1=%r15
sar  $1,%r15

# qhasm: q1 += q
# asm 1: add  <q=int64#8,<q1=int64#14
# asm 2: add  <q=%r10,<q1=%rbx
add  %r10,%rbx

# qhasm: r1 += r
# asm 1: add  <r=int64#5,<r1=int64#10
# asm 2: add  <r=%r8,<r1=%r12
add  %r8,%r12

# qhasm: t3 ^= t3
# asm 1: xor >t3=int64#9,>t3=int64#9
# asm 2: xor >t3=%r11,>t3=%r11
xor %r11,%r11

# qhasm: r ^= r
# asm 1: xor >r=int64#5,>r=int64#5
# asm 2: xor >r=%r8,>r=%r8
xor %r8,%r8

# qhasm: t2 = mem64[c_m1]
# asm 1: movq c_m1,>t2=int64#11
# asm 2: movq c_m1,>t2=%r13
movq c_m1(%rip),%r13

# qhasm: t1 = mem64[c_1]
# asm 1: movq c_1,>t1=int64#12
# asm 2: movq c_1,>t1=%r14
movq c_1(%rip),%r14

# qhasm: signed<? t3 -= delta
# asm 1: sub  <delta=int64#2,<t3=int64#9
# asm 2: sub  <delta=%rsi,<t3=%r11
sub  %rsi,%r11

# qhasm: t2 = t1 if !signed<
# asm 1: cmovge <t1=int64#12,<t2=int64#11
# asm 2: cmovge <t1=%r14,<t2=%r13
cmovge %r14,%r13

# qhasm: t1 &= g1
# asm 1: and  <g1=int64#13,<t1=int64#12
# asm 2: and  <g1=%r15,<t1=%r14
and  %r15,%r14

# qhasm: r -= t1
# asm 1: sub  <t1=int64#12,<r=int64#5
# asm 2: sub  <t1=%r14,<r=%r8
sub  %r14,%r8

# qhasm: g = f
# asm 1: mov  <f=int64#3,>g=int64#4
# asm 2: mov  <f=%rdx,>g=%rcx
mov  %rdx,%rcx

# qhasm: q = u
# asm 1: mov  <u=int64#6,>q=int64#8
# asm 2: mov  <u=%r9,>q=%r10
mov  %r9,%r10

# qhasm: r &= t2
# asm 1: and  <t2=int64#11,<r=int64#5
# asm 2: and  <t2=%r13,<r=%r8
and  %r13,%r8

# qhasm: g *= r
# asm 1: imul  <r=int64#5,<g=int64#4
# asm 2: imul  <r=%r8,<g=%rcx
imul  %r8,%rcx

# qhasm: q *= r
# asm 1: imul  <r=int64#5,<q=int64#8
# asm 2: imul  <r=%r8,<q=%r10
imul  %r8,%r10

# qhasm: r *= v
# asm 1: imul  <v=int64#7,<r=int64#5
# asm 2: imul  <v=%rax,<r=%r8
imul  %rax,%r8

# qhasm: g += g1
# asm 1: add  <g1=int64#13,<g=int64#4
# asm 2: add  <g1=%r15,<g=%rcx
add  %r15,%rcx

# qhasm: =? t1 += t2
# asm 1: add  <t2=int64#11,<t1=int64#12
# asm 2: add  <t2=%r13,<t1=%r14
add  %r13,%r14

# qhasm: delta = t3 if =
# asm 1: cmove <t3=int64#9,<delta=int64#2
# asm 2: cmove <t3=%r11,<delta=%rsi
cmove %r11,%rsi

# qhasm: delta = delta + 1
# asm 1: lea  1(<delta=int64#2),>delta=int64#2
# asm 2: lea  1(<delta=%rsi),>delta=%rsi
lea  1(%rsi),%rsi

# qhasm: u = q1 if =
# asm 1: cmove <q1=int64#14,<u=int64#6
# asm 2: cmove <q1=%rbx,<u=%r9
cmove %rbx,%r9

# qhasm: v = r1 if =
# asm 1: cmove <r1=int64#10,<v=int64#7
# asm 2: cmove <r1=%r12,<v=%rax
cmove %r12,%rax

# qhasm: f = g1 if =
# asm 1: cmove <g1=int64#13,<f=int64#3
# asm 2: cmove <g1=%r15,<f=%rdx
cmove %r15,%rdx

# qhasm: u += u
# asm 1: add  <u=int64#6,<u=int64#6
# asm 2: add  <u=%r9,<u=%r9
add  %r9,%r9

# qhasm: v += v
# asm 1: add  <v=int64#7,<v=int64#7
# asm 2: add  <v=%rax,<v=%rax
add  %rax,%rax

# qhasm: (int64) g >>= 1
# asm 1: sar  $1,<g=int64#4
# asm 2: sar  $1,<g=%rcx
sar  $1,%rcx

# qhasm: q += q1
# asm 1: add  <q1=int64#14,<q=int64#8
# asm 2: add  <q1=%rbx,<q=%r10
add  %rbx,%r10

# qhasm: r += r1
# asm 1: add  <r1=int64#10,<r=int64#5
# asm 2: add  <r1=%r12,<r=%r8
add  %r12,%r8

# qhasm: =? count -= 1
# asm 1: sub  $1,<count=int64#1
# asm 2: sub  $1,<count=%rdi
sub  $1,%rdi
# comment:fp stack unchanged by jump

# qhasm: goto loop if !=
jne ._loop

# qhasm: count =  odd_count_save
# asm 1: movq <odd_count_save=stack64#12,>count=int64#1
# asm 2: movq <odd_count_save=88(%rsp),>count=%rdi
movq 88(%rsp),%rdi

# qhasm: =? count & 1
# asm 1: test  $1,<count=int64#1
# asm 2: test  $1,<count=%rdi
test  $1,%rdi
# comment:fp stack unchanged by jump

# qhasm: goto loop_no_extra if =
je ._loop_no_extra

# qhasm: loop_extra:
._loop_extra:

# qhasm: t3 ^= t3
# asm 1: xor >t3=int64#1,>t3=int64#1
# asm 2: xor >t3=%rdi,>t3=%rdi
xor %rdi,%rdi

# qhasm: r1 ^= r1
# asm 1: xor >r1=int64#9,>r1=int64#9
# asm 2: xor >r1=%r11,>r1=%r11
xor %r11,%r11

# qhasm: t2 = mem64[c_m1]
# asm 1: movq c_m1,>t2=int64#10
# asm 2: movq c_m1,>t2=%r12
movq c_m1(%rip),%r12

# qhasm: t1 = mem64[c_1]
# asm 1: movq c_1,>t1=int64#11
# asm 2: movq c_1,>t1=%r13
movq c_1(%rip),%r13

# qhasm: signed<? t3 -= delta
# asm 1: sub  <delta=int64#2,<t3=int64#1
# asm 2: sub  <delta=%rsi,<t3=%rdi
sub  %rsi,%rdi

# qhasm: t2 = t1 if !signed<
# asm 1: cmovge <t1=int64#11,<t2=int64#10
# asm 2: cmovge <t1=%r13,<t2=%r12
cmovge %r13,%r12

# qhasm: t1 &= g
# asm 1: and  <g=int64#4,<t1=int64#11
# asm 2: and  <g=%rcx,<t1=%r13
and  %rcx,%r13

# qhasm: r1 -= t1
# asm 1: sub  <t1=int64#11,<r1=int64#9
# asm 2: sub  <t1=%r13,<r1=%r11
sub  %r13,%r11

# qhasm: g1 = f
# asm 1: mov  <f=int64#3,>g1=int64#12
# asm 2: mov  <f=%rdx,>g1=%r14
mov  %rdx,%r14

# qhasm: q1 = u
# asm 1: mov  <u=int64#6,>q1=int64#13
# asm 2: mov  <u=%r9,>q1=%r15
mov  %r9,%r15

# qhasm: r1 &= t2
# asm 1: and  <t2=int64#10,<r1=int64#9
# asm 2: and  <t2=%r12,<r1=%r11
and  %r12,%r11

# qhasm: g1 *= r1
# asm 1: imul  <r1=int64#9,<g1=int64#12
# asm 2: imul  <r1=%r11,<g1=%r14
imul  %r11,%r14

# qhasm: q1 *= r1
# asm 1: imul  <r1=int64#9,<q1=int64#13
# asm 2: imul  <r1=%r11,<q1=%r15
imul  %r11,%r15

# qhasm: r1 *= v
# asm 1: imul  <v=int64#7,<r1=int64#9
# asm 2: imul  <v=%rax,<r1=%r11
imul  %rax,%r11

# qhasm: g1 += g
# asm 1: add  <g=int64#4,<g1=int64#12
# asm 2: add  <g=%rcx,<g1=%r14
add  %rcx,%r14

# qhasm: =? t1 += t2
# asm 1: add  <t2=int64#10,<t1=int64#11
# asm 2: add  <t2=%r12,<t1=%r13
add  %r12,%r13

# qhasm: delta = t3 if =
# asm 1: cmove <t3=int64#1,<delta=int64#2
# asm 2: cmove <t3=%rdi,<delta=%rsi
cmove %rdi,%rsi

# qhasm: delta = delta + 1
# asm 1: lea  1(<delta=int64#2),>delta=int64#2
# asm 2: lea  1(<delta=%rsi),>delta=%rsi
lea  1(%rsi),%rsi

# qhasm: u = q if =
# asm 1: cmove <q=int64#8,<u=int64#6
# asm 2: cmove <q=%r10,<u=%r9
cmove %r10,%r9

# qhasm: v = r if =
# asm 1: cmove <r=int64#5,<v=int64#7
# asm 2: cmove <r=%r8,<v=%rax
cmove %r8,%rax

# qhasm: f = g if =
# asm 1: cmove <g=int64#4,<f=int64#3
# asm 2: cmove <g=%rcx,<f=%rdx
cmove %rcx,%rdx

# qhasm: u += u
# asm 1: add  <u=int64#6,<u=int64#6
# asm 2: add  <u=%r9,<u=%r9
add  %r9,%r9

# qhasm: v += v
# asm 1: add  <v=int64#7,<v=int64#7
# asm 2: add  <v=%rax,<v=%rax
add  %rax,%rax

# qhasm: (int64) g1 >>= 1
# asm 1: sar  $1,<g1=int64#12
# asm 2: sar  $1,<g1=%r14
sar  $1,%r14

# qhasm: q1 += q
# asm 1: add  <q=int64#8,<q1=int64#13
# asm 2: add  <q=%r10,<q1=%r15
add  %r10,%r15

# qhasm: r1 += r
# asm 1: add  <r=int64#5,<r1=int64#9
# asm 2: add  <r=%r8,<r1=%r11
add  %r8,%r11

# qhasm: g = g1
# asm 1: mov  <g1=int64#12,>g=int64#1
# asm 2: mov  <g1=%r14,>g=%rdi
mov  %r14,%rdi

# qhasm: q = q1
# asm 1: mov  <q1=int64#13,>q=int64#8
# asm 2: mov  <q1=%r15,>q=%r10
mov  %r15,%r10

# qhasm: r = r1
# asm 1: mov  <r1=int64#9,>r=int64#5
# asm 2: mov  <r1=%r11,>r=%r8
mov  %r11,%r8
# comment:fp stack unchanged by fallthrough

# qhasm: loop_no_extra:
._loop_no_extra:

# qhasm: input_4 = input_4_save
# asm 1: movq <input_4_save=stack64#11,>input_4=int64#1
# asm 2: movq <input_4_save=80(%rsp),>input_4=%rdi
movq 80(%rsp),%rdi

# qhasm: mem64[ input_4 + 0 ] = u
# asm 1: movq   <u=int64#6,0(<input_4=int64#1)
# asm 2: movq   <u=%r9,0(<input_4=%rdi)
movq   %r9,0(%rdi)

# qhasm: mem64[ input_4 + 8 ] = v
# asm 1: movq   <v=int64#7,8(<input_4=int64#1)
# asm 2: movq   <v=%rax,8(<input_4=%rdi)
movq   %rax,8(%rdi)

# qhasm: mem64[ input_4 +16 ] = q
# asm 1: movq   <q=int64#8,16(<input_4=int64#1)
# asm 2: movq   <q=%r10,16(<input_4=%rdi)
movq   %r10,16(%rdi)

# qhasm: mem64[ input_4 +24 ] = r
# asm 1: movq   <r=int64#5,24(<input_4=int64#1)
# asm 2: movq   <r=%r8,24(<input_4=%rdi)
movq   %r8,24(%rdi)

# qhasm: input_1_save = delta
# asm 1: movq <delta=int64#2,>input_1_save=stack64#12
# asm 2: movq <delta=%rsi,>input_1_save=88(%rsp)
movq %rsi,88(%rsp)

# qhasm: input_2 = input_2_save
# asm 1: movq <input_2_save=stack64#9,>input_2=int64#1
# asm 2: movq <input_2_save=64(%rsp),>input_2=%rdi
movq 64(%rsp),%rdi

# qhasm: flag = u
# asm 1: mov  <u=int64#6,>flag=int64#2
# asm 2: mov  <u=%r9,>flag=%rsi
mov  %r9,%rsi

# qhasm: (int64) flag >>= 63 
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: rax = u
# asm 1: mov  <u=int64#6,>rax=int64#7
# asm 2: mov  <u=%r9,>rax=%rax
mov  %r9,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 + 0 ]
# asm 1: mulq  0(<input_2=int64#1)
# asm 2: mulq  0(<input_2=%rdi)
mulq  0(%rdi)

# qhasm: a0s = rax
# asm 1: movq <rax=int64#7,>a0s=stack64#13
# asm 2: movq <rax=%rax,>a0s=96(%rsp)
movq %rax,96(%rsp)

# qhasm: a1s = rdx
# asm 1: movq <rdx=int64#3,>a1s=stack64#14
# asm 2: movq <rdx=%rdx,>a1s=104(%rsp)
movq %rdx,104(%rsp)

# qhasm: rax = u
# asm 1: mov  <u=int64#6,>rax=int64#7
# asm 2: mov  <u=%r9,>rax=%rax
mov  %r9,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +16 ]
# asm 1: mulq  16(<input_2=int64#1)
# asm 2: mulq  16(<input_2=%rdi)
mulq  16(%rdi)

# qhasm: a2s = rax
# asm 1: movq <rax=int64#7,>a2s=stack64#15
# asm 2: movq <rax=%rax,>a2s=112(%rsp)
movq %rax,112(%rsp)

# qhasm: a3s = rdx
# asm 1: movq <rdx=int64#3,>a3s=stack64#16
# asm 2: movq <rdx=%rdx,>a3s=120(%rsp)
movq %rdx,120(%rsp)

# qhasm: rax = u
# asm 1: mov  <u=int64#6,>rax=int64#7
# asm 2: mov  <u=%r9,>rax=%rax
mov  %r9,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +32 ]
# asm 1: mulq  32(<input_2=int64#1)
# asm 2: mulq  32(<input_2=%rdi)
mulq  32(%rdi)

# qhasm: a4 = rax
# asm 1: mov  <rax=int64#7,>a4=int64#4
# asm 2: mov  <rax=%rax,>a4=%rcx
mov  %rax,%rcx

# qhasm: a5 = rdx
# asm 1: mov  <rdx=int64#3,>a5=int64#5
# asm 2: mov  <rdx=%rdx,>a5=%r8
mov  %rdx,%r8

# qhasm: rax = u
# asm 1: mov  <u=int64#6,>rax=int64#7
# asm 2: mov  <u=%r9,>rax=%rax
mov  %r9,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +48 ]
# asm 1: mulq  48(<input_2=int64#1)
# asm 2: mulq  48(<input_2=%rdi)
mulq  48(%rdi)

# qhasm: a6 = rax
# asm 1: mov  <rax=int64#7,>a6=int64#8
# asm 2: mov  <rax=%rax,>a6=%r10
mov  %rax,%r10

# qhasm: a7 = rdx
# asm 1: mov  <rdx=int64#3,>a7=int64#9
# asm 2: mov  <rdx=%rdx,>a7=%r11
mov  %rdx,%r11

# qhasm: rax = u
# asm 1: mov  <u=int64#6,>rax=int64#7
# asm 2: mov  <u=%r9,>rax=%rax
mov  %r9,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 + 8 ]
# asm 1: mulq  8(<input_2=int64#1)
# asm 2: mulq  8(<input_2=%rdi)
mulq  8(%rdi)

# qhasm: a1 = rax
# asm 1: mov  <rax=int64#7,>a1=int64#10
# asm 2: mov  <rax=%rax,>a1=%r12
mov  %rax,%r12

# qhasm: a2 = rdx
# asm 1: mov  <rdx=int64#3,>a2=int64#11
# asm 2: mov  <rdx=%rdx,>a2=%r13
mov  %rdx,%r13

# qhasm: rax = u
# asm 1: mov  <u=int64#6,>rax=int64#7
# asm 2: mov  <u=%r9,>rax=%rax
mov  %r9,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +24 ]
# asm 1: mulq  24(<input_2=int64#1)
# asm 2: mulq  24(<input_2=%rdi)
mulq  24(%rdi)

# qhasm: a3 = rax
# asm 1: mov  <rax=int64#7,>a3=int64#12
# asm 2: mov  <rax=%rax,>a3=%r14
mov  %rax,%r14

# qhasm: t4 = rdx
# asm 1: mov  <rdx=int64#3,>t4=int64#13
# asm 2: mov  <rdx=%rdx,>t4=%r15
mov  %rdx,%r15

# qhasm: rax = u
# asm 1: mov  <u=int64#6,>rax=int64#7
# asm 2: mov  <u=%r9,>rax=%rax
mov  %r9,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +40 ]
# asm 1: mulq  40(<input_2=int64#1)
# asm 2: mulq  40(<input_2=%rdi)
mulq  40(%rdi)

# qhasm: t5 = rax
# asm 1: mov  <rax=int64#7,>t5=int64#14
# asm 2: mov  <rax=%rax,>t5=%rbx
mov  %rax,%rbx

# qhasm: t6 = rdx
# asm 1: mov  <rdx=int64#3,>t6=int64#15
# asm 2: mov  <rdx=%rdx,>t6=%rbp
mov  %rdx,%rbp

# qhasm: rax = u
# asm 1: mov  <u=int64#6,>rax=int64#7
# asm 2: mov  <u=%r9,>rax=%rax
mov  %r9,%rax

# qhasm:  (int128) rdx rax = rax * mem64[ input_2 +56 ]
# asm 1: imulq  56(<input_2=int64#1)
# asm 2: imulq  56(<input_2=%rdi)
imulq  56(%rdi)

# qhasm: carry? a1 += a1s
# asm 1: addq <a1s=stack64#14,<a1=int64#10
# asm 2: addq <a1s=104(%rsp),<a1=%r12
addq 104(%rsp),%r12

# qhasm: carry? a2 += a2s + carry
# asm 1: adcq <a2s=stack64#15,<a2=int64#11
# asm 2: adcq <a2s=112(%rsp),<a2=%r13
adcq 112(%rsp),%r13

# qhasm: carry? a3 += a3s + carry
# asm 1: adcq <a3s=stack64#16,<a3=int64#12
# asm 2: adcq <a3s=120(%rsp),<a3=%r14
adcq 120(%rsp),%r14

# qhasm: carry? a4 += t4 + carry
# asm 1: adc <t4=int64#13,<a4=int64#4
# asm 2: adc <t4=%r15,<a4=%rcx
adc %r15,%rcx

# qhasm: carry? a5 += t5 + carry
# asm 1: adc <t5=int64#14,<a5=int64#5
# asm 2: adc <t5=%rbx,<a5=%r8
adc %rbx,%r8

# qhasm: carry? a6 += t6 + carry
# asm 1: adc <t6=int64#15,<a6=int64#8
# asm 2: adc <t6=%rbp,<a6=%r10
adc %rbp,%r10

# qhasm: carry? a7 += rax + carry
# asm 1: adc <rax=int64#7,<a7=int64#9
# asm 2: adc <rax=%rax,<a7=%r11
adc %rax,%r11

# qhasm: rdx += 0 + carry
# asm 1: adc $0,<rdx=int64#3
# asm 2: adc $0,<rdx=%rdx
adc $0,%rdx

# qhasm: t1 = mem64[ input_2 + 0 ]
# asm 1: movq   0(<input_2=int64#1),>t1=int64#6
# asm 2: movq   0(<input_2=%rdi),>t1=%r9
movq   0(%rdi),%r9

# qhasm: t2 = mem64[ input_2 + 8 ]
# asm 1: movq   8(<input_2=int64#1),>t2=int64#7
# asm 2: movq   8(<input_2=%rdi),>t2=%rax
movq   8(%rdi),%rax

# qhasm: t3 = mem64[ input_2 +16 ]
# asm 1: movq   16(<input_2=int64#1),>t3=int64#13
# asm 2: movq   16(<input_2=%rdi),>t3=%r15
movq   16(%rdi),%r15

# qhasm: t4 = mem64[ input_2 +24 ]
# asm 1: movq   24(<input_2=int64#1),>t4=int64#14
# asm 2: movq   24(<input_2=%rdi),>t4=%rbx
movq   24(%rdi),%rbx

# qhasm: t1 &= flag
# asm 1: and  <flag=int64#2,<t1=int64#6
# asm 2: and  <flag=%rsi,<t1=%r9
and  %rsi,%r9

# qhasm: t2 &= flag
# asm 1: and  <flag=int64#2,<t2=int64#7
# asm 2: and  <flag=%rsi,<t2=%rax
and  %rsi,%rax

# qhasm: t3 &= flag
# asm 1: and  <flag=int64#2,<t3=int64#13
# asm 2: and  <flag=%rsi,<t3=%r15
and  %rsi,%r15

# qhasm: t4 &= flag
# asm 1: and  <flag=int64#2,<t4=int64#14
# asm 2: and  <flag=%rsi,<t4=%rbx
and  %rsi,%rbx

# qhasm: carry? a1 -= t1
# asm 1: sub  <t1=int64#6,<a1=int64#10
# asm 2: sub  <t1=%r9,<a1=%r12
sub  %r9,%r12

# qhasm: carry? a2 -= t2 - carry
# asm 1: sbb  <t2=int64#7,<a2=int64#11
# asm 2: sbb  <t2=%rax,<a2=%r13
sbb  %rax,%r13

# qhasm: carry? a3 -= t3 - carry
# asm 1: sbb  <t3=int64#13,<a3=int64#12
# asm 2: sbb  <t3=%r15,<a3=%r14
sbb  %r15,%r14

# qhasm: carry? a4 -= t4 - carry
# asm 1: sbb  <t4=int64#14,<a4=int64#4
# asm 2: sbb  <t4=%rbx,<a4=%rcx
sbb  %rbx,%rcx

# qhasm: t0 -= t0 - carry
# asm 1: sbb  >t0=int64#6,>t0=int64#6
# asm 2: sbb  >t0=%r9,>t0=%r9
sbb  %r9,%r9

# qhasm: t5 = mem64[ input_2 +32 ]
# asm 1: movq   32(<input_2=int64#1),>t5=int64#7
# asm 2: movq   32(<input_2=%rdi),>t5=%rax
movq   32(%rdi),%rax

# qhasm: t6 = mem64[ input_2 +40 ]
# asm 1: movq   40(<input_2=int64#1),>t6=int64#13
# asm 2: movq   40(<input_2=%rdi),>t6=%r15
movq   40(%rdi),%r15

# qhasm: t7 = mem64[ input_2 +48 ]
# asm 1: movq   48(<input_2=int64#1),>t7=int64#1
# asm 2: movq   48(<input_2=%rdi),>t7=%rdi
movq   48(%rdi),%rdi

# qhasm: t5 &= flag
# asm 1: and  <flag=int64#2,<t5=int64#7
# asm 2: and  <flag=%rsi,<t5=%rax
and  %rsi,%rax

# qhasm: t6 &= flag
# asm 1: and  <flag=int64#2,<t6=int64#13
# asm 2: and  <flag=%rsi,<t6=%r15
and  %rsi,%r15

# qhasm: t7 &= flag
# asm 1: and  <flag=int64#2,<t7=int64#1
# asm 2: and  <flag=%rsi,<t7=%rdi
and  %rsi,%rdi

# qhasm: carry? t0 += 1
# asm 1: add  $1,<t0=int64#6
# asm 2: add  $1,<t0=%r9
add  $1,%r9

# qhasm: carry? a5 -= t5 - carry
# asm 1: sbb  <t5=int64#7,<a5=int64#5
# asm 2: sbb  <t5=%rax,<a5=%r8
sbb  %rax,%r8

# qhasm: carry? a6 -= t6 - carry
# asm 1: sbb  <t6=int64#13,<a6=int64#8
# asm 2: sbb  <t6=%r15,<a6=%r10
sbb  %r15,%r10

# qhasm: carry? a7 -= t7 - carry
# asm 1: sbb  <t7=int64#1,<a7=int64#9
# asm 2: sbb  <t7=%rdi,<a7=%r11
sbb  %rdi,%r11

# qhasm: rdx -= 0 - carry
# asm 1: sbb  $0,<rdx=int64#3
# asm 2: sbb  $0,<rdx=%rdx
sbb  $0,%rdx

# qhasm: a1s = a1
# asm 1: movq <a1=int64#10,>a1s=stack64#14
# asm 2: movq <a1=%r12,>a1s=104(%rsp)
movq %r12,104(%rsp)

# qhasm: a2s = a2
# asm 1: movq <a2=int64#11,>a2s=stack64#15
# asm 2: movq <a2=%r13,>a2s=112(%rsp)
movq %r13,112(%rsp)

# qhasm: a3s = a3
# asm 1: movq <a3=int64#12,>a3s=stack64#16
# asm 2: movq <a3=%r14,>a3s=120(%rsp)
movq %r14,120(%rsp)

# qhasm: a4s = a4
# asm 1: movq <a4=int64#4,>a4s=stack64#17
# asm 2: movq <a4=%rcx,>a4s=128(%rsp)
movq %rcx,128(%rsp)

# qhasm: a5s = a5
# asm 1: movq <a5=int64#5,>a5s=stack64#18
# asm 2: movq <a5=%r8,>a5s=136(%rsp)
movq %r8,136(%rsp)

# qhasm: a6s = a6
# asm 1: movq <a6=int64#8,>a6s=stack64#19
# asm 2: movq <a6=%r10,>a6s=144(%rsp)
movq %r10,144(%rsp)

# qhasm: a7s = a7
# asm 1: movq <a7=int64#9,>a7s=stack64#20
# asm 2: movq <a7=%r11,>a7s=152(%rsp)
movq %r11,152(%rsp)

# qhasm: a8s = rdx
# asm 1: movq <rdx=int64#3,>a8s=stack64#21
# asm 2: movq <rdx=%rdx,>a8s=160(%rsp)
movq %rdx,160(%rsp)

# qhasm: input_4 = input_4_save
# asm 1: movq <input_4_save=stack64#11,>input_4=int64#1
# asm 2: movq <input_4_save=80(%rsp),>input_4=%rdi
movq 80(%rsp),%rdi

# qhasm: v = mem64[ input_4 + 8 ]
# asm 1: movq   8(<input_4=int64#1),>v=int64#1
# asm 2: movq   8(<input_4=%rdi),>v=%rdi
movq   8(%rdi),%rdi

# qhasm: flag = v
# asm 1: mov  <v=int64#1,>flag=int64#2
# asm 2: mov  <v=%rdi,>flag=%rsi
mov  %rdi,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: input_3 = input_3_save
# asm 1: movq <input_3_save=stack64#10,>input_3=int64#4
# asm 2: movq <input_3_save=72(%rsp),>input_3=%rcx
movq 72(%rsp),%rcx

# qhasm: rax = v
# asm 1: mov  <v=int64#1,>rax=int64#7
# asm 2: mov  <v=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 + 0 ]
# asm 1: mulq  0(<input_3=int64#4)
# asm 2: mulq  0(<input_3=%rcx)
mulq  0(%rcx)

# qhasm: b0s = rax
# asm 1: movq <rax=int64#7,>b0s=stack64#22
# asm 2: movq <rax=%rax,>b0s=168(%rsp)
movq %rax,168(%rsp)

# qhasm: b1s = rdx
# asm 1: movq <rdx=int64#3,>b1s=stack64#23
# asm 2: movq <rdx=%rdx,>b1s=176(%rsp)
movq %rdx,176(%rsp)

# qhasm: rax = v
# asm 1: mov  <v=int64#1,>rax=int64#7
# asm 2: mov  <v=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +16 ]
# asm 1: mulq  16(<input_3=int64#4)
# asm 2: mulq  16(<input_3=%rcx)
mulq  16(%rcx)

# qhasm: b2s = rax
# asm 1: movq <rax=int64#7,>b2s=stack64#24
# asm 2: movq <rax=%rax,>b2s=184(%rsp)
movq %rax,184(%rsp)

# qhasm: b3s = rdx
# asm 1: movq <rdx=int64#3,>b3s=stack64#25
# asm 2: movq <rdx=%rdx,>b3s=192(%rsp)
movq %rdx,192(%rsp)

# qhasm: rax = v
# asm 1: mov  <v=int64#1,>rax=int64#7
# asm 2: mov  <v=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +32 ]
# asm 1: mulq  32(<input_3=int64#4)
# asm 2: mulq  32(<input_3=%rcx)
mulq  32(%rcx)

# qhasm: b4 = rax
# asm 1: mov  <rax=int64#7,>b4=int64#5
# asm 2: mov  <rax=%rax,>b4=%r8
mov  %rax,%r8

# qhasm: b5 = rdx
# asm 1: mov  <rdx=int64#3,>b5=int64#6
# asm 2: mov  <rdx=%rdx,>b5=%r9
mov  %rdx,%r9

# qhasm: rax = v
# asm 1: mov  <v=int64#1,>rax=int64#7
# asm 2: mov  <v=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +48 ]
# asm 1: mulq  48(<input_3=int64#4)
# asm 2: mulq  48(<input_3=%rcx)
mulq  48(%rcx)

# qhasm: b6 = rax
# asm 1: mov  <rax=int64#7,>b6=int64#8
# asm 2: mov  <rax=%rax,>b6=%r10
mov  %rax,%r10

# qhasm: b7 = rdx
# asm 1: mov  <rdx=int64#3,>b7=int64#9
# asm 2: mov  <rdx=%rdx,>b7=%r11
mov  %rdx,%r11

# qhasm: rax = v
# asm 1: mov  <v=int64#1,>rax=int64#7
# asm 2: mov  <v=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 + 8 ]
# asm 1: mulq  8(<input_3=int64#4)
# asm 2: mulq  8(<input_3=%rcx)
mulq  8(%rcx)

# qhasm: b1 = rax
# asm 1: mov  <rax=int64#7,>b1=int64#10
# asm 2: mov  <rax=%rax,>b1=%r12
mov  %rax,%r12

# qhasm: b2 = rdx
# asm 1: mov  <rdx=int64#3,>b2=int64#11
# asm 2: mov  <rdx=%rdx,>b2=%r13
mov  %rdx,%r13

# qhasm: rax = v
# asm 1: mov  <v=int64#1,>rax=int64#7
# asm 2: mov  <v=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +24 ]
# asm 1: mulq  24(<input_3=int64#4)
# asm 2: mulq  24(<input_3=%rcx)
mulq  24(%rcx)

# qhasm: b3 = rax
# asm 1: mov  <rax=int64#7,>b3=int64#12
# asm 2: mov  <rax=%rax,>b3=%r14
mov  %rax,%r14

# qhasm: t4 = rdx
# asm 1: mov  <rdx=int64#3,>t4=int64#13
# asm 2: mov  <rdx=%rdx,>t4=%r15
mov  %rdx,%r15

# qhasm: rax = v
# asm 1: mov  <v=int64#1,>rax=int64#7
# asm 2: mov  <v=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +40 ]
# asm 1: mulq  40(<input_3=int64#4)
# asm 2: mulq  40(<input_3=%rcx)
mulq  40(%rcx)

# qhasm: t5 = rax
# asm 1: mov  <rax=int64#7,>t5=int64#14
# asm 2: mov  <rax=%rax,>t5=%rbx
mov  %rax,%rbx

# qhasm: t6 = rdx
# asm 1: mov  <rdx=int64#3,>t6=int64#15
# asm 2: mov  <rdx=%rdx,>t6=%rbp
mov  %rdx,%rbp

# qhasm: rax = v
# asm 1: mov  <v=int64#1,>rax=int64#7
# asm 2: mov  <v=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm:  (int128) rdx rax = rax * mem64[ input_3 +56 ]
# asm 1: imulq  56(<input_3=int64#4)
# asm 2: imulq  56(<input_3=%rcx)
imulq  56(%rcx)

# qhasm: carry? b1 += b1s
# asm 1: addq <b1s=stack64#23,<b1=int64#10
# asm 2: addq <b1s=176(%rsp),<b1=%r12
addq 176(%rsp),%r12

# qhasm: carry? b2 += b2s + carry
# asm 1: adcq <b2s=stack64#24,<b2=int64#11
# asm 2: adcq <b2s=184(%rsp),<b2=%r13
adcq 184(%rsp),%r13

# qhasm: carry? b3 += b3s + carry
# asm 1: adcq <b3s=stack64#25,<b3=int64#12
# asm 2: adcq <b3s=192(%rsp),<b3=%r14
adcq 192(%rsp),%r14

# qhasm: carry? b4 += t4 + carry
# asm 1: adc <t4=int64#13,<b4=int64#5
# asm 2: adc <t4=%r15,<b4=%r8
adc %r15,%r8

# qhasm: carry? b5 += t5 + carry
# asm 1: adc <t5=int64#14,<b5=int64#6
# asm 2: adc <t5=%rbx,<b5=%r9
adc %rbx,%r9

# qhasm: carry? b6 += t6 + carry
# asm 1: adc <t6=int64#15,<b6=int64#8
# asm 2: adc <t6=%rbp,<b6=%r10
adc %rbp,%r10

# qhasm: carry? b7 += rax + carry
# asm 1: adc <rax=int64#7,<b7=int64#9
# asm 2: adc <rax=%rax,<b7=%r11
adc %rax,%r11

# qhasm: rdx += 0 + carry
# asm 1: adc $0,<rdx=int64#3
# asm 2: adc $0,<rdx=%rdx
adc $0,%rdx

# qhasm: t1 = mem64[ input_3 + 0 ]
# asm 1: movq   0(<input_3=int64#4),>t1=int64#1
# asm 2: movq   0(<input_3=%rcx),>t1=%rdi
movq   0(%rcx),%rdi

# qhasm: t2 = mem64[ input_3 + 8 ]
# asm 1: movq   8(<input_3=int64#4),>t2=int64#7
# asm 2: movq   8(<input_3=%rcx),>t2=%rax
movq   8(%rcx),%rax

# qhasm: t3 = mem64[ input_3 +16 ]
# asm 1: movq   16(<input_3=int64#4),>t3=int64#13
# asm 2: movq   16(<input_3=%rcx),>t3=%r15
movq   16(%rcx),%r15

# qhasm: t4 = mem64[ input_3 +24 ]
# asm 1: movq   24(<input_3=int64#4),>t4=int64#14
# asm 2: movq   24(<input_3=%rcx),>t4=%rbx
movq   24(%rcx),%rbx

# qhasm: t1 &= flag
# asm 1: and  <flag=int64#2,<t1=int64#1
# asm 2: and  <flag=%rsi,<t1=%rdi
and  %rsi,%rdi

# qhasm: t2 &= flag
# asm 1: and  <flag=int64#2,<t2=int64#7
# asm 2: and  <flag=%rsi,<t2=%rax
and  %rsi,%rax

# qhasm: t3 &= flag
# asm 1: and  <flag=int64#2,<t3=int64#13
# asm 2: and  <flag=%rsi,<t3=%r15
and  %rsi,%r15

# qhasm: t4 &= flag
# asm 1: and  <flag=int64#2,<t4=int64#14
# asm 2: and  <flag=%rsi,<t4=%rbx
and  %rsi,%rbx

# qhasm: carry? b1 -= t1
# asm 1: sub  <t1=int64#1,<b1=int64#10
# asm 2: sub  <t1=%rdi,<b1=%r12
sub  %rdi,%r12

# qhasm: carry? b2 -= t2 - carry
# asm 1: sbb  <t2=int64#7,<b2=int64#11
# asm 2: sbb  <t2=%rax,<b2=%r13
sbb  %rax,%r13

# qhasm: carry? b3 -= t3 - carry
# asm 1: sbb  <t3=int64#13,<b3=int64#12
# asm 2: sbb  <t3=%r15,<b3=%r14
sbb  %r15,%r14

# qhasm: carry? b4 -= t4 - carry
# asm 1: sbb  <t4=int64#14,<b4=int64#5
# asm 2: sbb  <t4=%rbx,<b4=%r8
sbb  %rbx,%r8

# qhasm: t0 -= t0 - carry
# asm 1: sbb  >t0=int64#1,>t0=int64#1
# asm 2: sbb  >t0=%rdi,>t0=%rdi
sbb  %rdi,%rdi

# qhasm: t5 = mem64[ input_3 +32 ]
# asm 1: movq   32(<input_3=int64#4),>t5=int64#7
# asm 2: movq   32(<input_3=%rcx),>t5=%rax
movq   32(%rcx),%rax

# qhasm: t6 = mem64[ input_3 +40 ]
# asm 1: movq   40(<input_3=int64#4),>t6=int64#13
# asm 2: movq   40(<input_3=%rcx),>t6=%r15
movq   40(%rcx),%r15

# qhasm: t7 = mem64[ input_3 +48 ]
# asm 1: movq   48(<input_3=int64#4),>t7=int64#4
# asm 2: movq   48(<input_3=%rcx),>t7=%rcx
movq   48(%rcx),%rcx

# qhasm: t5 &= flag
# asm 1: and  <flag=int64#2,<t5=int64#7
# asm 2: and  <flag=%rsi,<t5=%rax
and  %rsi,%rax

# qhasm: t6 &= flag
# asm 1: and  <flag=int64#2,<t6=int64#13
# asm 2: and  <flag=%rsi,<t6=%r15
and  %rsi,%r15

# qhasm: t7 &= flag
# asm 1: and  <flag=int64#2,<t7=int64#4
# asm 2: and  <flag=%rsi,<t7=%rcx
and  %rsi,%rcx

# qhasm: carry? t0 += 1
# asm 1: add  $1,<t0=int64#1
# asm 2: add  $1,<t0=%rdi
add  $1,%rdi

# qhasm: carry? b5 -= t5 - carry
# asm 1: sbb  <t5=int64#7,<b5=int64#6
# asm 2: sbb  <t5=%rax,<b5=%r9
sbb  %rax,%r9

# qhasm: carry? b6 -= t6 - carry
# asm 1: sbb  <t6=int64#13,<b6=int64#8
# asm 2: sbb  <t6=%r15,<b6=%r10
sbb  %r15,%r10

# qhasm: carry? b7 -= t7 - carry
# asm 1: sbb  <t7=int64#4,<b7=int64#9
# asm 2: sbb  <t7=%rcx,<b7=%r11
sbb  %rcx,%r11

# qhasm: rdx -= 0 - carry
# asm 1: sbb  $0,<rdx=int64#3
# asm 2: sbb  $0,<rdx=%rdx
sbb  $0,%rdx

# qhasm: b0 = b0s
# asm 1: movq <b0s=stack64#22,>b0=int64#1
# asm 2: movq <b0s=168(%rsp),>b0=%rdi
movq 168(%rsp),%rdi

# qhasm: carry? b0 += a0s  
# asm 1: addq <a0s=stack64#13,<b0=int64#1
# asm 2: addq <a0s=96(%rsp),<b0=%rdi
addq 96(%rsp),%rdi

# qhasm: carry? b1 += a1s  + carry
# asm 1: adcq <a1s=stack64#14,<b1=int64#10
# asm 2: adcq <a1s=104(%rsp),<b1=%r12
adcq 104(%rsp),%r12

# qhasm: carry? b2 += a2s  + carry
# asm 1: adcq <a2s=stack64#15,<b2=int64#11
# asm 2: adcq <a2s=112(%rsp),<b2=%r13
adcq 112(%rsp),%r13

# qhasm: carry? b3 += a3s  + carry
# asm 1: adcq <a3s=stack64#16,<b3=int64#12
# asm 2: adcq <a3s=120(%rsp),<b3=%r14
adcq 120(%rsp),%r14

# qhasm: carry? b4 += a4s  + carry
# asm 1: adcq <a4s=stack64#17,<b4=int64#5
# asm 2: adcq <a4s=128(%rsp),<b4=%r8
adcq 128(%rsp),%r8

# qhasm: carry? b5 += a5s  + carry
# asm 1: adcq <a5s=stack64#18,<b5=int64#6
# asm 2: adcq <a5s=136(%rsp),<b5=%r9
adcq 136(%rsp),%r9

# qhasm: carry? b6 += a6s  + carry
# asm 1: adcq <a6s=stack64#19,<b6=int64#8
# asm 2: adcq <a6s=144(%rsp),<b6=%r10
adcq 144(%rsp),%r10

# qhasm: carry? b7 += a7s  + carry
# asm 1: adcq <a7s=stack64#20,<b7=int64#9
# asm 2: adcq <a7s=152(%rsp),<b7=%r11
adcq 152(%rsp),%r11

# qhasm: rdx += a8s + carry
# asm 1: adcq <a8s=stack64#21,<rdx=int64#3
# asm 2: adcq <a8s=160(%rsp),<rdx=%rdx
adcq 160(%rsp),%rdx

# qhasm: count = input_0_save
# asm 1: movq <input_0_save=stack64#8,>count=int64#4
# asm 2: movq <input_0_save=56(%rsp),>count=%rcx
movq 56(%rsp),%rcx

# qhasm: b0 = (b1 b0) >> count
# asm 1: shrd %cl,<b1=int64#10,<b0=int64#1
# asm 2: shrd %cl,<b1=%r12,<b0=%rdi
shrd %cl,%r12,%rdi

# qhasm: b1 = (b2 b1) >> count
# asm 1: shrd %cl,<b2=int64#11,<b1=int64#10
# asm 2: shrd %cl,<b2=%r13,<b1=%r12
shrd %cl,%r13,%r12

# qhasm: b2 = (b3 b2) >> count
# asm 1: shrd %cl,<b3=int64#12,<b2=int64#11
# asm 2: shrd %cl,<b3=%r14,<b2=%r13
shrd %cl,%r14,%r13

# qhasm: b3 = (b4 b3) >> count
# asm 1: shrd %cl,<b4=int64#5,<b3=int64#12
# asm 2: shrd %cl,<b4=%r8,<b3=%r14
shrd %cl,%r8,%r14

# qhasm: b4 = (b5 b4) >> count
# asm 1: shrd %cl,<b5=int64#6,<b4=int64#5
# asm 2: shrd %cl,<b5=%r9,<b4=%r8
shrd %cl,%r9,%r8

# qhasm: b5 = (b6 b5) >> count
# asm 1: shrd %cl,<b6=int64#8,<b5=int64#6
# asm 2: shrd %cl,<b6=%r10,<b5=%r9
shrd %cl,%r10,%r9

# qhasm: b6 = (b7 b6) >> count
# asm 1: shrd %cl,<b7=int64#9,<b6=int64#8
# asm 2: shrd %cl,<b7=%r11,<b6=%r10
shrd %cl,%r11,%r10

# qhasm: b7 = (rdx b7) >> count
# asm 1: shrd %cl,<rdx=int64#3,<b7=int64#9
# asm 2: shrd %cl,<rdx=%rdx,<b7=%r11
shrd %cl,%rdx,%r11

# qhasm: t0s = b0  
# asm 1: movq <b0=int64#1,>t0s=stack64#13
# asm 2: movq <b0=%rdi,>t0s=96(%rsp)
movq %rdi,96(%rsp)

# qhasm: t1s = b1
# asm 1: movq <b1=int64#10,>t1s=stack64#14
# asm 2: movq <b1=%r12,>t1s=104(%rsp)
movq %r12,104(%rsp)

# qhasm: t2s = b2
# asm 1: movq <b2=int64#11,>t2s=stack64#15
# asm 2: movq <b2=%r13,>t2s=112(%rsp)
movq %r13,112(%rsp)

# qhasm: t3s = b3
# asm 1: movq <b3=int64#12,>t3s=stack64#16
# asm 2: movq <b3=%r14,>t3s=120(%rsp)
movq %r14,120(%rsp)

# qhasm: t4s = b4
# asm 1: movq <b4=int64#5,>t4s=stack64#17
# asm 2: movq <b4=%r8,>t4s=128(%rsp)
movq %r8,128(%rsp)

# qhasm: t5s = b5
# asm 1: movq <b5=int64#6,>t5s=stack64#18
# asm 2: movq <b5=%r9,>t5s=136(%rsp)
movq %r9,136(%rsp)

# qhasm: t6s = b6
# asm 1: movq <b6=int64#8,>t6s=stack64#19
# asm 2: movq <b6=%r10,>t6s=144(%rsp)
movq %r10,144(%rsp)

# qhasm: t7s = b7
# asm 1: movq <b7=int64#9,>t7s=stack64#20
# asm 2: movq <b7=%r11,>t7s=152(%rsp)
movq %r11,152(%rsp)

# qhasm: input_2 = input_2_save
# asm 1: movq <input_2_save=stack64#9,>input_2=int64#1
# asm 2: movq <input_2_save=64(%rsp),>input_2=%rdi
movq 64(%rsp),%rdi

# qhasm: input_4 = input_4_save
# asm 1: movq <input_4_save=stack64#11,>input_4=int64#2
# asm 2: movq <input_4_save=80(%rsp),>input_4=%rsi
movq 80(%rsp),%rsi

# qhasm: q = mem64[ input_4 +16 ]
# asm 1: movq   16(<input_4=int64#2),>q=int64#2
# asm 2: movq   16(<input_4=%rsi),>q=%rsi
movq   16(%rsi),%rsi

# qhasm: flag = q
# asm 1: mov  <q=int64#2,>flag=int64#4
# asm 2: mov  <q=%rsi,>flag=%rcx
mov  %rsi,%rcx

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#4
# asm 2: sar  $63,<flag=%rcx
sar  $63,%rcx

# qhasm: rax = q
# asm 1: mov  <q=int64#2,>rax=int64#7
# asm 2: mov  <q=%rsi,>rax=%rax
mov  %rsi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 + 0 ]
# asm 1: mulq  0(<input_2=int64#1)
# asm 2: mulq  0(<input_2=%rdi)
mulq  0(%rdi)

# qhasm: a0s = rax
# asm 1: movq <rax=int64#7,>a0s=stack64#21
# asm 2: movq <rax=%rax,>a0s=160(%rsp)
movq %rax,160(%rsp)

# qhasm: a1s = rdx
# asm 1: movq <rdx=int64#3,>a1s=stack64#22
# asm 2: movq <rdx=%rdx,>a1s=168(%rsp)
movq %rdx,168(%rsp)

# qhasm: rax = q
# asm 1: mov  <q=int64#2,>rax=int64#7
# asm 2: mov  <q=%rsi,>rax=%rax
mov  %rsi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +16 ]
# asm 1: mulq  16(<input_2=int64#1)
# asm 2: mulq  16(<input_2=%rdi)
mulq  16(%rdi)

# qhasm: a2s = rax
# asm 1: movq <rax=int64#7,>a2s=stack64#23
# asm 2: movq <rax=%rax,>a2s=176(%rsp)
movq %rax,176(%rsp)

# qhasm: a3s = rdx
# asm 1: movq <rdx=int64#3,>a3s=stack64#24
# asm 2: movq <rdx=%rdx,>a3s=184(%rsp)
movq %rdx,184(%rsp)

# qhasm: rax = q
# asm 1: mov  <q=int64#2,>rax=int64#7
# asm 2: mov  <q=%rsi,>rax=%rax
mov  %rsi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +32 ]
# asm 1: mulq  32(<input_2=int64#1)
# asm 2: mulq  32(<input_2=%rdi)
mulq  32(%rdi)

# qhasm: a4 = rax
# asm 1: mov  <rax=int64#7,>a4=int64#5
# asm 2: mov  <rax=%rax,>a4=%r8
mov  %rax,%r8

# qhasm: a5 = rdx
# asm 1: mov  <rdx=int64#3,>a5=int64#6
# asm 2: mov  <rdx=%rdx,>a5=%r9
mov  %rdx,%r9

# qhasm: rax = q
# asm 1: mov  <q=int64#2,>rax=int64#7
# asm 2: mov  <q=%rsi,>rax=%rax
mov  %rsi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +48 ]
# asm 1: mulq  48(<input_2=int64#1)
# asm 2: mulq  48(<input_2=%rdi)
mulq  48(%rdi)

# qhasm: a6 = rax
# asm 1: mov  <rax=int64#7,>a6=int64#8
# asm 2: mov  <rax=%rax,>a6=%r10
mov  %rax,%r10

# qhasm: a7 = rdx
# asm 1: mov  <rdx=int64#3,>a7=int64#9
# asm 2: mov  <rdx=%rdx,>a7=%r11
mov  %rdx,%r11

# qhasm: rax = q
# asm 1: mov  <q=int64#2,>rax=int64#7
# asm 2: mov  <q=%rsi,>rax=%rax
mov  %rsi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 + 8 ]
# asm 1: mulq  8(<input_2=int64#1)
# asm 2: mulq  8(<input_2=%rdi)
mulq  8(%rdi)

# qhasm: a1 = rax
# asm 1: mov  <rax=int64#7,>a1=int64#10
# asm 2: mov  <rax=%rax,>a1=%r12
mov  %rax,%r12

# qhasm: a2 = rdx
# asm 1: mov  <rdx=int64#3,>a2=int64#11
# asm 2: mov  <rdx=%rdx,>a2=%r13
mov  %rdx,%r13

# qhasm: rax = q
# asm 1: mov  <q=int64#2,>rax=int64#7
# asm 2: mov  <q=%rsi,>rax=%rax
mov  %rsi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +24 ]
# asm 1: mulq  24(<input_2=int64#1)
# asm 2: mulq  24(<input_2=%rdi)
mulq  24(%rdi)

# qhasm: a3 = rax
# asm 1: mov  <rax=int64#7,>a3=int64#12
# asm 2: mov  <rax=%rax,>a3=%r14
mov  %rax,%r14

# qhasm: t4 = rdx
# asm 1: mov  <rdx=int64#3,>t4=int64#13
# asm 2: mov  <rdx=%rdx,>t4=%r15
mov  %rdx,%r15

# qhasm: rax = q
# asm 1: mov  <q=int64#2,>rax=int64#7
# asm 2: mov  <q=%rsi,>rax=%rax
mov  %rsi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_2 +40 ]
# asm 1: mulq  40(<input_2=int64#1)
# asm 2: mulq  40(<input_2=%rdi)
mulq  40(%rdi)

# qhasm: t5 = rax
# asm 1: mov  <rax=int64#7,>t5=int64#14
# asm 2: mov  <rax=%rax,>t5=%rbx
mov  %rax,%rbx

# qhasm: t6 = rdx
# asm 1: mov  <rdx=int64#3,>t6=int64#15
# asm 2: mov  <rdx=%rdx,>t6=%rbp
mov  %rdx,%rbp

# qhasm: rax = q
# asm 1: mov  <q=int64#2,>rax=int64#7
# asm 2: mov  <q=%rsi,>rax=%rax
mov  %rsi,%rax

# qhasm:  (int128) rdx rax = rax * mem64[ input_2 +56 ]
# asm 1: imulq  56(<input_2=int64#1)
# asm 2: imulq  56(<input_2=%rdi)
imulq  56(%rdi)

# qhasm: carry? a1 += a1s
# asm 1: addq <a1s=stack64#22,<a1=int64#10
# asm 2: addq <a1s=168(%rsp),<a1=%r12
addq 168(%rsp),%r12

# qhasm: carry? a2 += a2s + carry
# asm 1: adcq <a2s=stack64#23,<a2=int64#11
# asm 2: adcq <a2s=176(%rsp),<a2=%r13
adcq 176(%rsp),%r13

# qhasm: carry? a3 += a3s + carry
# asm 1: adcq <a3s=stack64#24,<a3=int64#12
# asm 2: adcq <a3s=184(%rsp),<a3=%r14
adcq 184(%rsp),%r14

# qhasm: carry? a4 += t4 + carry
# asm 1: adc <t4=int64#13,<a4=int64#5
# asm 2: adc <t4=%r15,<a4=%r8
adc %r15,%r8

# qhasm: carry? a5 += t5 + carry
# asm 1: adc <t5=int64#14,<a5=int64#6
# asm 2: adc <t5=%rbx,<a5=%r9
adc %rbx,%r9

# qhasm: carry? a6 += t6 + carry
# asm 1: adc <t6=int64#15,<a6=int64#8
# asm 2: adc <t6=%rbp,<a6=%r10
adc %rbp,%r10

# qhasm: carry? a7 += rax + carry
# asm 1: adc <rax=int64#7,<a7=int64#9
# asm 2: adc <rax=%rax,<a7=%r11
adc %rax,%r11

# qhasm: rdx += 0 + carry
# asm 1: adc $0,<rdx=int64#3
# asm 2: adc $0,<rdx=%rdx
adc $0,%rdx

# qhasm: t1 = mem64[ input_2 + 0 ]
# asm 1: movq   0(<input_2=int64#1),>t1=int64#2
# asm 2: movq   0(<input_2=%rdi),>t1=%rsi
movq   0(%rdi),%rsi

# qhasm: t2 = mem64[ input_2 + 8 ]
# asm 1: movq   8(<input_2=int64#1),>t2=int64#7
# asm 2: movq   8(<input_2=%rdi),>t2=%rax
movq   8(%rdi),%rax

# qhasm: t3 = mem64[ input_2 +16 ]
# asm 1: movq   16(<input_2=int64#1),>t3=int64#13
# asm 2: movq   16(<input_2=%rdi),>t3=%r15
movq   16(%rdi),%r15

# qhasm: t4 = mem64[ input_2 +24 ]
# asm 1: movq   24(<input_2=int64#1),>t4=int64#14
# asm 2: movq   24(<input_2=%rdi),>t4=%rbx
movq   24(%rdi),%rbx

# qhasm: t1 &= flag
# asm 1: and  <flag=int64#4,<t1=int64#2
# asm 2: and  <flag=%rcx,<t1=%rsi
and  %rcx,%rsi

# qhasm: t2 &= flag
# asm 1: and  <flag=int64#4,<t2=int64#7
# asm 2: and  <flag=%rcx,<t2=%rax
and  %rcx,%rax

# qhasm: t3 &= flag
# asm 1: and  <flag=int64#4,<t3=int64#13
# asm 2: and  <flag=%rcx,<t3=%r15
and  %rcx,%r15

# qhasm: t4 &= flag
# asm 1: and  <flag=int64#4,<t4=int64#14
# asm 2: and  <flag=%rcx,<t4=%rbx
and  %rcx,%rbx

# qhasm: carry? a1 -= t1
# asm 1: sub  <t1=int64#2,<a1=int64#10
# asm 2: sub  <t1=%rsi,<a1=%r12
sub  %rsi,%r12

# qhasm: carry? a2 -= t2 - carry
# asm 1: sbb  <t2=int64#7,<a2=int64#11
# asm 2: sbb  <t2=%rax,<a2=%r13
sbb  %rax,%r13

# qhasm: carry? a3 -= t3 - carry
# asm 1: sbb  <t3=int64#13,<a3=int64#12
# asm 2: sbb  <t3=%r15,<a3=%r14
sbb  %r15,%r14

# qhasm: carry? a4 -= t4 - carry
# asm 1: sbb  <t4=int64#14,<a4=int64#5
# asm 2: sbb  <t4=%rbx,<a4=%r8
sbb  %rbx,%r8

# qhasm: t0 -= t0 - carry
# asm 1: sbb  >t0=int64#2,>t0=int64#2
# asm 2: sbb  >t0=%rsi,>t0=%rsi
sbb  %rsi,%rsi

# qhasm: t5 = mem64[ input_2 +32 ]
# asm 1: movq   32(<input_2=int64#1),>t5=int64#7
# asm 2: movq   32(<input_2=%rdi),>t5=%rax
movq   32(%rdi),%rax

# qhasm: t6 = mem64[ input_2 +40 ]
# asm 1: movq   40(<input_2=int64#1),>t6=int64#13
# asm 2: movq   40(<input_2=%rdi),>t6=%r15
movq   40(%rdi),%r15

# qhasm: t7 = mem64[ input_2 +48 ]
# asm 1: movq   48(<input_2=int64#1),>t7=int64#1
# asm 2: movq   48(<input_2=%rdi),>t7=%rdi
movq   48(%rdi),%rdi

# qhasm: t5 &= flag
# asm 1: and  <flag=int64#4,<t5=int64#7
# asm 2: and  <flag=%rcx,<t5=%rax
and  %rcx,%rax

# qhasm: t6 &= flag
# asm 1: and  <flag=int64#4,<t6=int64#13
# asm 2: and  <flag=%rcx,<t6=%r15
and  %rcx,%r15

# qhasm: t7 &= flag
# asm 1: and  <flag=int64#4,<t7=int64#1
# asm 2: and  <flag=%rcx,<t7=%rdi
and  %rcx,%rdi

# qhasm: carry? t0 += 1
# asm 1: add  $1,<t0=int64#2
# asm 2: add  $1,<t0=%rsi
add  $1,%rsi

# qhasm: carry? a5 -= t5 - carry
# asm 1: sbb  <t5=int64#7,<a5=int64#6
# asm 2: sbb  <t5=%rax,<a5=%r9
sbb  %rax,%r9

# qhasm: carry? a6 -= t6 - carry
# asm 1: sbb  <t6=int64#13,<a6=int64#8
# asm 2: sbb  <t6=%r15,<a6=%r10
sbb  %r15,%r10

# qhasm: carry? a7 -= t7 - carry
# asm 1: sbb  <t7=int64#1,<a7=int64#9
# asm 2: sbb  <t7=%rdi,<a7=%r11
sbb  %rdi,%r11

# qhasm: rdx -= 0 - carry
# asm 1: sbb  $0,<rdx=int64#3
# asm 2: sbb  $0,<rdx=%rdx
sbb  $0,%rdx

# qhasm: a1s = a1
# asm 1: movq <a1=int64#10,>a1s=stack64#22
# asm 2: movq <a1=%r12,>a1s=168(%rsp)
movq %r12,168(%rsp)

# qhasm: a2s = a2
# asm 1: movq <a2=int64#11,>a2s=stack64#23
# asm 2: movq <a2=%r13,>a2s=176(%rsp)
movq %r13,176(%rsp)

# qhasm: a3s = a3
# asm 1: movq <a3=int64#12,>a3s=stack64#24
# asm 2: movq <a3=%r14,>a3s=184(%rsp)
movq %r14,184(%rsp)

# qhasm: a4s = a4
# asm 1: movq <a4=int64#5,>a4s=stack64#25
# asm 2: movq <a4=%r8,>a4s=192(%rsp)
movq %r8,192(%rsp)

# qhasm: a5s = a5
# asm 1: movq <a5=int64#6,>a5s=stack64#26
# asm 2: movq <a5=%r9,>a5s=200(%rsp)
movq %r9,200(%rsp)

# qhasm: a6s = a6
# asm 1: movq <a6=int64#8,>a6s=stack64#27
# asm 2: movq <a6=%r10,>a6s=208(%rsp)
movq %r10,208(%rsp)

# qhasm: a7s = a7
# asm 1: movq <a7=int64#9,>a7s=stack64#28
# asm 2: movq <a7=%r11,>a7s=216(%rsp)
movq %r11,216(%rsp)

# qhasm: a8s = rdx
# asm 1: movq <rdx=int64#3,>a8s=stack64#29
# asm 2: movq <rdx=%rdx,>a8s=224(%rsp)
movq %rdx,224(%rsp)

# qhasm: input_4 = input_4_save
# asm 1: movq <input_4_save=stack64#11,>input_4=int64#1
# asm 2: movq <input_4_save=80(%rsp),>input_4=%rdi
movq 80(%rsp),%rdi

# qhasm: r = mem64[ input_4 + 24 ]
# asm 1: movq   24(<input_4=int64#1),>r=int64#1
# asm 2: movq   24(<input_4=%rdi),>r=%rdi
movq   24(%rdi),%rdi

# qhasm: flag = r
# asm 1: mov  <r=int64#1,>flag=int64#2
# asm 2: mov  <r=%rdi,>flag=%rsi
mov  %rdi,%rsi

# qhasm: (int64) flag >>= 63
# asm 1: sar  $63,<flag=int64#2
# asm 2: sar  $63,<flag=%rsi
sar  $63,%rsi

# qhasm: input_3 = input_3_save
# asm 1: movq <input_3_save=stack64#10,>input_3=int64#4
# asm 2: movq <input_3_save=72(%rsp),>input_3=%rcx
movq 72(%rsp),%rcx

# qhasm: rax = r
# asm 1: mov  <r=int64#1,>rax=int64#7
# asm 2: mov  <r=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 + 0 ]
# asm 1: mulq  0(<input_3=int64#4)
# asm 2: mulq  0(<input_3=%rcx)
mulq  0(%rcx)

# qhasm: b0s = rax
# asm 1: movq <rax=int64#7,>b0s=stack64#11
# asm 2: movq <rax=%rax,>b0s=80(%rsp)
movq %rax,80(%rsp)

# qhasm: b1s = rdx
# asm 1: movq <rdx=int64#3,>b1s=stack64#30
# asm 2: movq <rdx=%rdx,>b1s=232(%rsp)
movq %rdx,232(%rsp)

# qhasm: rax = r
# asm 1: mov  <r=int64#1,>rax=int64#7
# asm 2: mov  <r=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +16 ]
# asm 1: mulq  16(<input_3=int64#4)
# asm 2: mulq  16(<input_3=%rcx)
mulq  16(%rcx)

# qhasm: b2s = rax
# asm 1: movq <rax=int64#7,>b2s=stack64#31
# asm 2: movq <rax=%rax,>b2s=240(%rsp)
movq %rax,240(%rsp)

# qhasm: b3s = rdx
# asm 1: movq <rdx=int64#3,>b3s=stack64#32
# asm 2: movq <rdx=%rdx,>b3s=248(%rsp)
movq %rdx,248(%rsp)

# qhasm: rax = r
# asm 1: mov  <r=int64#1,>rax=int64#7
# asm 2: mov  <r=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +32 ]
# asm 1: mulq  32(<input_3=int64#4)
# asm 2: mulq  32(<input_3=%rcx)
mulq  32(%rcx)

# qhasm: b4 = rax
# asm 1: mov  <rax=int64#7,>b4=int64#5
# asm 2: mov  <rax=%rax,>b4=%r8
mov  %rax,%r8

# qhasm: b5 = rdx
# asm 1: mov  <rdx=int64#3,>b5=int64#6
# asm 2: mov  <rdx=%rdx,>b5=%r9
mov  %rdx,%r9

# qhasm: rax = r
# asm 1: mov  <r=int64#1,>rax=int64#7
# asm 2: mov  <r=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +48 ]
# asm 1: mulq  48(<input_3=int64#4)
# asm 2: mulq  48(<input_3=%rcx)
mulq  48(%rcx)

# qhasm: b6 = rax
# asm 1: mov  <rax=int64#7,>b6=int64#8
# asm 2: mov  <rax=%rax,>b6=%r10
mov  %rax,%r10

# qhasm: b7 = rdx
# asm 1: mov  <rdx=int64#3,>b7=int64#9
# asm 2: mov  <rdx=%rdx,>b7=%r11
mov  %rdx,%r11

# qhasm: rax = r
# asm 1: mov  <r=int64#1,>rax=int64#7
# asm 2: mov  <r=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 + 8 ]
# asm 1: mulq  8(<input_3=int64#4)
# asm 2: mulq  8(<input_3=%rcx)
mulq  8(%rcx)

# qhasm: b1 = rax
# asm 1: mov  <rax=int64#7,>b1=int64#10
# asm 2: mov  <rax=%rax,>b1=%r12
mov  %rax,%r12

# qhasm: b2 = rdx
# asm 1: mov  <rdx=int64#3,>b2=int64#11
# asm 2: mov  <rdx=%rdx,>b2=%r13
mov  %rdx,%r13

# qhasm: rax = r
# asm 1: mov  <r=int64#1,>rax=int64#7
# asm 2: mov  <r=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +24 ]
# asm 1: mulq  24(<input_3=int64#4)
# asm 2: mulq  24(<input_3=%rcx)
mulq  24(%rcx)

# qhasm: b3 = rax
# asm 1: mov  <rax=int64#7,>b3=int64#12
# asm 2: mov  <rax=%rax,>b3=%r14
mov  %rax,%r14

# qhasm: t4 = rdx
# asm 1: mov  <rdx=int64#3,>t4=int64#13
# asm 2: mov  <rdx=%rdx,>t4=%r15
mov  %rdx,%r15

# qhasm: rax = r
# asm 1: mov  <r=int64#1,>rax=int64#7
# asm 2: mov  <r=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm: (uint128) rdx rax = rax * mem64[ input_3 +40 ]
# asm 1: mulq  40(<input_3=int64#4)
# asm 2: mulq  40(<input_3=%rcx)
mulq  40(%rcx)

# qhasm: t5 = rax
# asm 1: mov  <rax=int64#7,>t5=int64#14
# asm 2: mov  <rax=%rax,>t5=%rbx
mov  %rax,%rbx

# qhasm: t6 = rdx
# asm 1: mov  <rdx=int64#3,>t6=int64#15
# asm 2: mov  <rdx=%rdx,>t6=%rbp
mov  %rdx,%rbp

# qhasm: rax = r
# asm 1: mov  <r=int64#1,>rax=int64#7
# asm 2: mov  <r=%rdi,>rax=%rax
mov  %rdi,%rax

# qhasm:  (int128) rdx rax = rax * mem64[ input_3 +56 ]
# asm 1: imulq  56(<input_3=int64#4)
# asm 2: imulq  56(<input_3=%rcx)
imulq  56(%rcx)

# qhasm: carry? b1 += b1s
# asm 1: addq <b1s=stack64#30,<b1=int64#10
# asm 2: addq <b1s=232(%rsp),<b1=%r12
addq 232(%rsp),%r12

# qhasm: carry? b2 += b2s + carry
# asm 1: adcq <b2s=stack64#31,<b2=int64#11
# asm 2: adcq <b2s=240(%rsp),<b2=%r13
adcq 240(%rsp),%r13

# qhasm: carry? b3 += b3s + carry
# asm 1: adcq <b3s=stack64#32,<b3=int64#12
# asm 2: adcq <b3s=248(%rsp),<b3=%r14
adcq 248(%rsp),%r14

# qhasm: carry? b4 += t4 + carry
# asm 1: adc <t4=int64#13,<b4=int64#5
# asm 2: adc <t4=%r15,<b4=%r8
adc %r15,%r8

# qhasm: carry? b5 += t5 + carry
# asm 1: adc <t5=int64#14,<b5=int64#6
# asm 2: adc <t5=%rbx,<b5=%r9
adc %rbx,%r9

# qhasm: carry? b6 += t6 + carry
# asm 1: adc <t6=int64#15,<b6=int64#8
# asm 2: adc <t6=%rbp,<b6=%r10
adc %rbp,%r10

# qhasm: carry? b7 += rax + carry
# asm 1: adc <rax=int64#7,<b7=int64#9
# asm 2: adc <rax=%rax,<b7=%r11
adc %rax,%r11

# qhasm: rdx += 0 + carry
# asm 1: adc $0,<rdx=int64#3
# asm 2: adc $0,<rdx=%rdx
adc $0,%rdx

# qhasm: t1 = mem64[ input_3 + 0 ]
# asm 1: movq   0(<input_3=int64#4),>t1=int64#1
# asm 2: movq   0(<input_3=%rcx),>t1=%rdi
movq   0(%rcx),%rdi

# qhasm: t2 = mem64[ input_3 + 8 ]
# asm 1: movq   8(<input_3=int64#4),>t2=int64#7
# asm 2: movq   8(<input_3=%rcx),>t2=%rax
movq   8(%rcx),%rax

# qhasm: t3 = mem64[ input_3 +16 ]
# asm 1: movq   16(<input_3=int64#4),>t3=int64#13
# asm 2: movq   16(<input_3=%rcx),>t3=%r15
movq   16(%rcx),%r15

# qhasm: t4 = mem64[ input_3 +24 ]
# asm 1: movq   24(<input_3=int64#4),>t4=int64#14
# asm 2: movq   24(<input_3=%rcx),>t4=%rbx
movq   24(%rcx),%rbx

# qhasm: t1 &= flag
# asm 1: and  <flag=int64#2,<t1=int64#1
# asm 2: and  <flag=%rsi,<t1=%rdi
and  %rsi,%rdi

# qhasm: t2 &= flag
# asm 1: and  <flag=int64#2,<t2=int64#7
# asm 2: and  <flag=%rsi,<t2=%rax
and  %rsi,%rax

# qhasm: t3 &= flag
# asm 1: and  <flag=int64#2,<t3=int64#13
# asm 2: and  <flag=%rsi,<t3=%r15
and  %rsi,%r15

# qhasm: t4 &= flag
# asm 1: and  <flag=int64#2,<t4=int64#14
# asm 2: and  <flag=%rsi,<t4=%rbx
and  %rsi,%rbx

# qhasm: carry? b1 -= t1
# asm 1: sub  <t1=int64#1,<b1=int64#10
# asm 2: sub  <t1=%rdi,<b1=%r12
sub  %rdi,%r12

# qhasm: carry? b2 -= t2 - carry
# asm 1: sbb  <t2=int64#7,<b2=int64#11
# asm 2: sbb  <t2=%rax,<b2=%r13
sbb  %rax,%r13

# qhasm: carry? b3 -= t3 - carry
# asm 1: sbb  <t3=int64#13,<b3=int64#12
# asm 2: sbb  <t3=%r15,<b3=%r14
sbb  %r15,%r14

# qhasm: carry? b4 -= t4 - carry
# asm 1: sbb  <t4=int64#14,<b4=int64#5
# asm 2: sbb  <t4=%rbx,<b4=%r8
sbb  %rbx,%r8

# qhasm: t0 -= t0 - carry
# asm 1: sbb  >t0=int64#1,>t0=int64#1
# asm 2: sbb  >t0=%rdi,>t0=%rdi
sbb  %rdi,%rdi

# qhasm: t5 = mem64[ input_3 +32 ]
# asm 1: movq   32(<input_3=int64#4),>t5=int64#7
# asm 2: movq   32(<input_3=%rcx),>t5=%rax
movq   32(%rcx),%rax

# qhasm: t6 = mem64[ input_3 +40 ]
# asm 1: movq   40(<input_3=int64#4),>t6=int64#13
# asm 2: movq   40(<input_3=%rcx),>t6=%r15
movq   40(%rcx),%r15

# qhasm: t7 = mem64[ input_3 +48 ]
# asm 1: movq   48(<input_3=int64#4),>t7=int64#4
# asm 2: movq   48(<input_3=%rcx),>t7=%rcx
movq   48(%rcx),%rcx

# qhasm: t5 &= flag
# asm 1: and  <flag=int64#2,<t5=int64#7
# asm 2: and  <flag=%rsi,<t5=%rax
and  %rsi,%rax

# qhasm: t6 &= flag
# asm 1: and  <flag=int64#2,<t6=int64#13
# asm 2: and  <flag=%rsi,<t6=%r15
and  %rsi,%r15

# qhasm: t7 &= flag
# asm 1: and  <flag=int64#2,<t7=int64#4
# asm 2: and  <flag=%rsi,<t7=%rcx
and  %rsi,%rcx

# qhasm: carry? t0 += 1
# asm 1: add  $1,<t0=int64#1
# asm 2: add  $1,<t0=%rdi
add  $1,%rdi

# qhasm: carry? b5 -= t5 - carry
# asm 1: sbb  <t5=int64#7,<b5=int64#6
# asm 2: sbb  <t5=%rax,<b5=%r9
sbb  %rax,%r9

# qhasm: carry? b6 -= t6 - carry
# asm 1: sbb  <t6=int64#13,<b6=int64#8
# asm 2: sbb  <t6=%r15,<b6=%r10
sbb  %r15,%r10

# qhasm: carry? b7 -= t7 - carry
# asm 1: sbb  <t7=int64#4,<b7=int64#9
# asm 2: sbb  <t7=%rcx,<b7=%r11
sbb  %rcx,%r11

# qhasm: rdx -= 0 - carry
# asm 1: sbb  $0,<rdx=int64#3
# asm 2: sbb  $0,<rdx=%rdx
sbb  $0,%rdx

# qhasm: b0 = b0s
# asm 1: movq <b0s=stack64#11,>b0=int64#1
# asm 2: movq <b0s=80(%rsp),>b0=%rdi
movq 80(%rsp),%rdi

# qhasm: carry? b0 += a0s  
# asm 1: addq <a0s=stack64#21,<b0=int64#1
# asm 2: addq <a0s=160(%rsp),<b0=%rdi
addq 160(%rsp),%rdi

# qhasm: carry? b1 += a1s  + carry
# asm 1: adcq <a1s=stack64#22,<b1=int64#10
# asm 2: adcq <a1s=168(%rsp),<b1=%r12
adcq 168(%rsp),%r12

# qhasm: carry? b2 += a2s  + carry
# asm 1: adcq <a2s=stack64#23,<b2=int64#11
# asm 2: adcq <a2s=176(%rsp),<b2=%r13
adcq 176(%rsp),%r13

# qhasm: carry? b3 += a3s  + carry
# asm 1: adcq <a3s=stack64#24,<b3=int64#12
# asm 2: adcq <a3s=184(%rsp),<b3=%r14
adcq 184(%rsp),%r14

# qhasm: carry? b4 += a4s  + carry
# asm 1: adcq <a4s=stack64#25,<b4=int64#5
# asm 2: adcq <a4s=192(%rsp),<b4=%r8
adcq 192(%rsp),%r8

# qhasm: carry? b5 += a5s  + carry
# asm 1: adcq <a5s=stack64#26,<b5=int64#6
# asm 2: adcq <a5s=200(%rsp),<b5=%r9
adcq 200(%rsp),%r9

# qhasm: carry? b6 += a6s  + carry
# asm 1: adcq <a6s=stack64#27,<b6=int64#8
# asm 2: adcq <a6s=208(%rsp),<b6=%r10
adcq 208(%rsp),%r10

# qhasm: carry? b7 += a7s  + carry
# asm 1: adcq <a7s=stack64#28,<b7=int64#9
# asm 2: adcq <a7s=216(%rsp),<b7=%r11
adcq 216(%rsp),%r11

# qhasm: rdx += a8s + carry
# asm 1: adcq <a8s=stack64#29,<rdx=int64#3
# asm 2: adcq <a8s=224(%rsp),<rdx=%rdx
adcq 224(%rsp),%rdx

# qhasm: count = input_0_save
# asm 1: movq <input_0_save=stack64#8,>count=int64#4
# asm 2: movq <input_0_save=56(%rsp),>count=%rcx
movq 56(%rsp),%rcx

# qhasm: b0 = (b1 b0) >> count
# asm 1: shrd %cl,<b1=int64#10,<b0=int64#1
# asm 2: shrd %cl,<b1=%r12,<b0=%rdi
shrd %cl,%r12,%rdi

# qhasm: b1 = (b2 b1) >> count
# asm 1: shrd %cl,<b2=int64#11,<b1=int64#10
# asm 2: shrd %cl,<b2=%r13,<b1=%r12
shrd %cl,%r13,%r12

# qhasm: b2 = (b3 b2) >> count
# asm 1: shrd %cl,<b3=int64#12,<b2=int64#11
# asm 2: shrd %cl,<b3=%r14,<b2=%r13
shrd %cl,%r14,%r13

# qhasm: b3 = (b4 b3) >> count
# asm 1: shrd %cl,<b4=int64#5,<b3=int64#12
# asm 2: shrd %cl,<b4=%r8,<b3=%r14
shrd %cl,%r8,%r14

# qhasm: b4 = (b5 b4) >> count
# asm 1: shrd %cl,<b5=int64#6,<b4=int64#5
# asm 2: shrd %cl,<b5=%r9,<b4=%r8
shrd %cl,%r9,%r8

# qhasm: b5 = (b6 b5) >> count
# asm 1: shrd %cl,<b6=int64#8,<b5=int64#6
# asm 2: shrd %cl,<b6=%r10,<b5=%r9
shrd %cl,%r10,%r9

# qhasm: b6 = (b7 b6) >> count
# asm 1: shrd %cl,<b7=int64#9,<b6=int64#8
# asm 2: shrd %cl,<b7=%r11,<b6=%r10
shrd %cl,%r11,%r10

# qhasm: b7 = (rdx b7) >> count
# asm 1: shrd %cl,<rdx=int64#3,<b7=int64#9
# asm 2: shrd %cl,<rdx=%rdx,<b7=%r11
shrd %cl,%rdx,%r11

# qhasm: input_3 = input_3_save
# asm 1: movq <input_3_save=stack64#10,>input_3=int64#2
# asm 2: movq <input_3_save=72(%rsp),>input_3=%rsi
movq 72(%rsp),%rsi

# qhasm: mem64[ input_3 + 0 ] = b0
# asm 1: movq   <b0=int64#1,0(<input_3=int64#2)
# asm 2: movq   <b0=%rdi,0(<input_3=%rsi)
movq   %rdi,0(%rsi)

# qhasm: mem64[ input_3 + 8 ] = b1
# asm 1: movq   <b1=int64#10,8(<input_3=int64#2)
# asm 2: movq   <b1=%r12,8(<input_3=%rsi)
movq   %r12,8(%rsi)

# qhasm: mem64[ input_3 +16 ] = b2
# asm 1: movq   <b2=int64#11,16(<input_3=int64#2)
# asm 2: movq   <b2=%r13,16(<input_3=%rsi)
movq   %r13,16(%rsi)

# qhasm: mem64[ input_3 +24 ] = b3
# asm 1: movq   <b3=int64#12,24(<input_3=int64#2)
# asm 2: movq   <b3=%r14,24(<input_3=%rsi)
movq   %r14,24(%rsi)

# qhasm: mem64[ input_3 +32 ] = b4
# asm 1: movq   <b4=int64#5,32(<input_3=int64#2)
# asm 2: movq   <b4=%r8,32(<input_3=%rsi)
movq   %r8,32(%rsi)

# qhasm: mem64[ input_3 +40 ] = b5
# asm 1: movq   <b5=int64#6,40(<input_3=int64#2)
# asm 2: movq   <b5=%r9,40(<input_3=%rsi)
movq   %r9,40(%rsi)

# qhasm: mem64[ input_3 +48 ] = b6
# asm 1: movq   <b6=int64#8,48(<input_3=int64#2)
# asm 2: movq   <b6=%r10,48(<input_3=%rsi)
movq   %r10,48(%rsi)

# qhasm: mem64[ input_3 +56 ] = b7
# asm 1: movq   <b7=int64#9,56(<input_3=int64#2)
# asm 2: movq   <b7=%r11,56(<input_3=%rsi)
movq   %r11,56(%rsi)

# qhasm: a0 = t0s
# asm 1: movq <t0s=stack64#13,>a0=int64#1
# asm 2: movq <t0s=96(%rsp),>a0=%rdi
movq 96(%rsp),%rdi

# qhasm: a1 = t1s
# asm 1: movq <t1s=stack64#14,>a1=int64#2
# asm 2: movq <t1s=104(%rsp),>a1=%rsi
movq 104(%rsp),%rsi

# qhasm: a2 = t2s
# asm 1: movq <t2s=stack64#15,>a2=int64#3
# asm 2: movq <t2s=112(%rsp),>a2=%rdx
movq 112(%rsp),%rdx

# qhasm: a3 = t3s
# asm 1: movq <t3s=stack64#16,>a3=int64#4
# asm 2: movq <t3s=120(%rsp),>a3=%rcx
movq 120(%rsp),%rcx

# qhasm: a4 = t4s
# asm 1: movq <t4s=stack64#17,>a4=int64#5
# asm 2: movq <t4s=128(%rsp),>a4=%r8
movq 128(%rsp),%r8

# qhasm: a5 = t5s
# asm 1: movq <t5s=stack64#18,>a5=int64#6
# asm 2: movq <t5s=136(%rsp),>a5=%r9
movq 136(%rsp),%r9

# qhasm: a6 = t6s
# asm 1: movq <t6s=stack64#19,>a6=int64#7
# asm 2: movq <t6s=144(%rsp),>a6=%rax
movq 144(%rsp),%rax

# qhasm: a7 = t7s
# asm 1: movq <t7s=stack64#20,>a7=int64#8
# asm 2: movq <t7s=152(%rsp),>a7=%r10
movq 152(%rsp),%r10

# qhasm: input_2 = input_2_save
# asm 1: movq <input_2_save=stack64#9,>input_2=int64#9
# asm 2: movq <input_2_save=64(%rsp),>input_2=%r11
movq 64(%rsp),%r11

# qhasm: mem64[ input_2 + 0 ] = a0
# asm 1: movq   <a0=int64#1,0(<input_2=int64#9)
# asm 2: movq   <a0=%rdi,0(<input_2=%r11)
movq   %rdi,0(%r11)

# qhasm: mem64[ input_2 + 8 ] = a1
# asm 1: movq   <a1=int64#2,8(<input_2=int64#9)
# asm 2: movq   <a1=%rsi,8(<input_2=%r11)
movq   %rsi,8(%r11)

# qhasm: mem64[ input_2 +16 ] = a2
# asm 1: movq   <a2=int64#3,16(<input_2=int64#9)
# asm 2: movq   <a2=%rdx,16(<input_2=%r11)
movq   %rdx,16(%r11)

# qhasm: mem64[ input_2 +24 ] = a3
# asm 1: movq   <a3=int64#4,24(<input_2=int64#9)
# asm 2: movq   <a3=%rcx,24(<input_2=%r11)
movq   %rcx,24(%r11)

# qhasm: mem64[ input_2 +32 ] = a4
# asm 1: movq   <a4=int64#5,32(<input_2=int64#9)
# asm 2: movq   <a4=%r8,32(<input_2=%r11)
movq   %r8,32(%r11)

# qhasm: mem64[ input_2 +40 ] = a5
# asm 1: movq   <a5=int64#6,40(<input_2=int64#9)
# asm 2: movq   <a5=%r9,40(<input_2=%r11)
movq   %r9,40(%r11)

# qhasm: mem64[ input_2 +48 ] = a6
# asm 1: movq   <a6=int64#7,48(<input_2=int64#9)
# asm 2: movq   <a6=%rax,48(<input_2=%r11)
movq   %rax,48(%r11)

# qhasm: mem64[ input_2 +56 ] = a7
# asm 1: movq   <a7=int64#8,56(<input_2=int64#9)
# asm 2: movq   <a7=%r10,56(<input_2=%r11)
movq   %r10,56(%r11)

# qhasm: delta = input_1_save
# asm 1: movq <input_1_save=stack64#12,>delta=int64#7
# asm 2: movq <input_1_save=88(%rsp),>delta=%rax
movq 88(%rsp),%rax

# qhasm: assign 7 to delta

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

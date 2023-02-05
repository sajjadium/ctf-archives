
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

# qhasm: int64 mulx0

# qhasm: int64 mulx1

# qhasm: int64 mulx2

# qhasm: int64 mulx3

# qhasm: int64 mulrax

# qhasm: int64 mulrdx

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

# qhasm: stack64 t0s

# qhasm: stack64 t1s

# qhasm: stack64 t2s

# qhasm: stack64 t3s

# qhasm: stack64 t4s

# qhasm: stack64 t5s

# qhasm: stack64 t6s

# qhasm: stack64 t7s

# qhasm: enter muls256xs256
.p2align 5
.global _muls256xs256
.global muls256xs256
_muls256xs256:
muls256xs256:
mov %rsp,%r11
and $31,%r11
add $128,%r11
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

# qhasm:   t4 = 0
# asm 1: mov  $0,>t4=int64#4
# asm 2: mov  $0,>t4=%rcx
mov  $0,%rcx

# qhasm:   t5 = 0
# asm 1: mov  $0,>t5=int64#5
# asm 2: mov  $0,>t5=%r8
mov  $0,%r8

# qhasm:   t6 = 0
# asm 1: mov  $0,>t6=int64#6
# asm 2: mov  $0,>t6=%r9
mov  $0,%r9

# qhasm:   t7 = 0
# asm 1: mov  $0,>t7=int64#8
# asm 2: mov  $0,>t7=%r10
mov  $0,%r10

# qhasm:   mulx0 = mem64[ input_0 + 0 ]
# asm 1: movq   0(<input_0=int64#1),>mulx0=int64#9
# asm 2: movq   0(<input_0=%rdi),>mulx0=%r11
movq   0(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   0(<input_1=%rsi),>mulrax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   t0 = mulrax
# asm 1: mov  <mulrax=int64#7,>t0=int64#10
# asm 2: mov  <mulrax=%rax,>t0=%r12
mov  %rax,%r12

# qhasm:   t1 = mulrdx
# asm 1: mov  <mulrdx=int64#3,>t1=int64#11
# asm 2: mov  <mulrdx=%rdx,>t1=%r13
mov  %rdx,%r13

# qhasm:   mulrax = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   8(<input_1=%rsi),>mulrax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   t2 = 0
# asm 1: mov  $0,>t2=int64#12
# asm 2: mov  $0,>t2=%r14
mov  $0,%r14

# qhasm:   t2 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t2=int64#12
# asm 2: adc <mulrdx=%rdx,<t2=%r14
adc %rdx,%r14

# qhasm:   mulrax = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulrax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   t3 = 0
# asm 1: mov  $0,>t3=int64#13
# asm 2: mov  $0,>t3=%r15
mov  $0,%r15

# qhasm:   t3 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t3=int64#13
# asm 2: adc <mulrdx=%rdx,<t3=%r15
adc %rdx,%r15

# qhasm:   mulrax = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   24(<input_1=%rsi),>mulrax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   t4 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t4=int64#4
# asm 2: adc <mulrdx=%rdx,<t4=%rcx
adc %rdx,%rcx

# qhasm:   mulx1 = mem64[ input_0 + 8 ]
# asm 1: movq   8(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   8(<input_0=%rdi),>mulx1=%r11
movq   8(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   0(<input_1=%rsi),>mulrax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   8(<input_1=%rsi),>mulrax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t2 += mulc
# asm 1: add  <mulc=int64#14,<t2=int64#12
# asm 2: add  <mulc=%rbx,<t2=%r14
add  %rbx,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulrax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax 
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   24(<input_1=%rsi),>mulrax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   t5 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t5=int64#5
# asm 2: adc <mulrdx=%rdx,<t5=%r8
adc %rdx,%r8

# qhasm:   mulx2 = mem64[ input_0 + 16]
# asm 1: movq   16(<input_0=int64#1),>mulx2=int64#9
# asm 2: movq   16(<input_0=%rdi),>mulx2=%r11
movq   16(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   0(<input_1=%rsi),>mulrax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   8(<input_1=%rsi),>mulrax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulrax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   24(<input_1=%rsi),>mulrax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   t6 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t6=int64#6
# asm 2: adc <mulrdx=%rdx,<t6=%r9
adc %rdx,%r9

# qhasm:   mulx3 = mem64[ input_0 + 24]
# asm 1: movq   24(<input_0=int64#1),>mulx3=int64#9
# asm 2: movq   24(<input_0=%rdi),>mulx3=%r11
movq   24(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   0(<input_1=%rsi),>mulrax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   8(<input_1=%rsi),>mulrax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulrax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   24(<input_1=%rsi),>mulrax=%rax
movq   24(%rsi),%rax

# qhasm:   (int128) mulrdx mulrax = mulrax * mulx3
# asm 1: imul <mulx3=int64#9
# asm 2: imul <mulx3=%r11
imul %r11

# qhasm:   carry? t6 += mulrax
# asm 1: add  <mulrax=int64#7,<t6=int64#6
# asm 2: add  <mulrax=%rax,<t6=%r9
add  %rax,%r9

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t6 += mulc
# asm 1: add  <mulc=int64#14,<t6=int64#6
# asm 2: add  <mulc=%rbx,<t6=%r9
add  %rbx,%r9

# qhasm:   t7 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t7=int64#8
# asm 2: adc <mulrdx=%rdx,<t7=%r10
adc %rdx,%r10

# qhasm:   mulx3 = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulx3=int64#3
# asm 2: movq   24(<input_1=%rsi),>mulx3=%rdx
movq   24(%rsi),%rdx

# qhasm:   mulx2 = mem64[ input_0 + 16]
# asm 1: movq   16(<input_0=int64#1),>mulx2=int64#7
# asm 2: movq   16(<input_0=%rdi),>mulx2=%rax
movq   16(%rdi),%rax

# qhasm:   mulx1 = mem64[ input_0 + 8 ]
# asm 1: movq   8(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   8(<input_0=%rdi),>mulx1=%r11
movq   8(%rdi),%r11

# qhasm:   mulx0 = mem64[ input_0 + 0 ]
# asm 1: movq   0(<input_0=int64#1),>mulx0=int64#14
# asm 2: movq   0(<input_0=%rdi),>mulx0=%rbx
movq   0(%rdi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm:   mulx3 = mem64[ input_0 + 24]
# asm 1: movq   24(<input_0=int64#1),>mulx3=int64#3
# asm 2: movq   24(<input_0=%rdi),>mulx3=%rdx
movq   24(%rdi),%rdx

# qhasm:   mulx2 = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulx2=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulx2=%rax
movq   16(%rsi),%rax

# qhasm:   mulx1 = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulx1=int64#9
# asm 2: movq   8(<input_1=%rsi),>mulx1=%r11
movq   8(%rsi),%r11

# qhasm:   mulx0 = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulx0=int64#14
# asm 2: movq   0(<input_1=%rsi),>mulx0=%rbx
movq   0(%rsi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm: t0s = t0
# asm 1: movq <t0=int64#10,>t0s=stack64#9
# asm 2: movq <t0=%r12,>t0s=64(%rsp)
movq %r12,64(%rsp)

# qhasm: t1s = t1
# asm 1: movq <t1=int64#11,>t1s=stack64#10
# asm 2: movq <t1=%r13,>t1s=72(%rsp)
movq %r13,72(%rsp)

# qhasm: t2s = t2
# asm 1: movq <t2=int64#12,>t2s=stack64#11
# asm 2: movq <t2=%r14,>t2s=80(%rsp)
movq %r14,80(%rsp)

# qhasm: t3s = t3
# asm 1: movq <t3=int64#13,>t3s=stack64#12
# asm 2: movq <t3=%r15,>t3s=88(%rsp)
movq %r15,88(%rsp)

# qhasm: t4s = t4
# asm 1: movq <t4=int64#4,>t4s=stack64#13
# asm 2: movq <t4=%rcx,>t4s=96(%rsp)
movq %rcx,96(%rsp)

# qhasm: t5s = t5
# asm 1: movq <t5=int64#5,>t5s=stack64#14
# asm 2: movq <t5=%r8,>t5s=104(%rsp)
movq %r8,104(%rsp)

# qhasm: t6s = t6
# asm 1: movq <t6=int64#6,>t6s=stack64#15
# asm 2: movq <t6=%r9,>t6s=112(%rsp)
movq %r9,112(%rsp)

# qhasm: t7s = t7
# asm 1: movq <t7=int64#8,>t7s=stack64#16
# asm 2: movq <t7=%r10,>t7s=120(%rsp)
movq %r10,120(%rsp)

# qhasm:   t4 = 0
# asm 1: mov  $0,>t4=int64#4
# asm 2: mov  $0,>t4=%rcx
mov  $0,%rcx

# qhasm:   t5 = 0
# asm 1: mov  $0,>t5=int64#5
# asm 2: mov  $0,>t5=%r8
mov  $0,%r8

# qhasm:   t6 = 0
# asm 1: mov  $0,>t6=int64#6
# asm 2: mov  $0,>t6=%r9
mov  $0,%r9

# qhasm:   t7 = 0
# asm 1: mov  $0,>t7=int64#8
# asm 2: mov  $0,>t7=%r10
mov  $0,%r10

# qhasm:   mulx0 = mem64[ input_0 + 32 ]
# asm 1: movq   32(<input_0=int64#1),>mulx0=int64#9
# asm 2: movq   32(<input_0=%rdi),>mulx0=%r11
movq   32(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   64(<input_1=%rsi),>mulrax=%rax
movq   64(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   t0 = mulrax
# asm 1: mov  <mulrax=int64#7,>t0=int64#10
# asm 2: mov  <mulrax=%rax,>t0=%r12
mov  %rax,%r12

# qhasm:   t1 = mulrdx
# asm 1: mov  <mulrdx=int64#3,>t1=int64#11
# asm 2: mov  <mulrdx=%rdx,>t1=%r13
mov  %rdx,%r13

# qhasm:   mulrax = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   72(<input_1=%rsi),>mulrax=%rax
movq   72(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   t2 = 0
# asm 1: mov  $0,>t2=int64#12
# asm 2: mov  $0,>t2=%r14
mov  $0,%r14

# qhasm:   t2 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t2=int64#12
# asm 2: adc <mulrdx=%rdx,<t2=%r14
adc %rdx,%r14

# qhasm:   mulrax = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulrax=%rax
movq   80(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   t3 = 0
# asm 1: mov  $0,>t3=int64#13
# asm 2: mov  $0,>t3=%r15
mov  $0,%r15

# qhasm:   t3 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t3=int64#13
# asm 2: adc <mulrdx=%rdx,<t3=%r15
adc %rdx,%r15

# qhasm:   mulrax = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   88(<input_1=%rsi),>mulrax=%rax
movq   88(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   t4 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t4=int64#4
# asm 2: adc <mulrdx=%rdx,<t4=%rcx
adc %rdx,%rcx

# qhasm:   mulx1 = mem64[ input_0 + 40 ]
# asm 1: movq   40(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   40(<input_0=%rdi),>mulx1=%r11
movq   40(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   64(<input_1=%rsi),>mulrax=%rax
movq   64(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   72(<input_1=%rsi),>mulrax=%rax
movq   72(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t2 += mulc
# asm 1: add  <mulc=int64#14,<t2=int64#12
# asm 2: add  <mulc=%rbx,<t2=%r14
add  %rbx,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulrax=%rax
movq   80(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax 
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   88(<input_1=%rsi),>mulrax=%rax
movq   88(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   t5 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t5=int64#5
# asm 2: adc <mulrdx=%rdx,<t5=%r8
adc %rdx,%r8

# qhasm:   mulx2 = mem64[ input_0 + 48 ]
# asm 1: movq   48(<input_0=int64#1),>mulx2=int64#9
# asm 2: movq   48(<input_0=%rdi),>mulx2=%r11
movq   48(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   64(<input_1=%rsi),>mulrax=%rax
movq   64(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   72(<input_1=%rsi),>mulrax=%rax
movq   72(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulrax=%rax
movq   80(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   88(<input_1=%rsi),>mulrax=%rax
movq   88(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   t6 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t6=int64#6
# asm 2: adc <mulrdx=%rdx,<t6=%r9
adc %rdx,%r9

# qhasm:   mulx3 = mem64[ input_0 + 56 ]
# asm 1: movq   56(<input_0=int64#1),>mulx3=int64#9
# asm 2: movq   56(<input_0=%rdi),>mulx3=%r11
movq   56(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   64(<input_1=%rsi),>mulrax=%rax
movq   64(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   72(<input_1=%rsi),>mulrax=%rax
movq   72(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulrax=%rax
movq   80(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   88(<input_1=%rsi),>mulrax=%rax
movq   88(%rsi),%rax

# qhasm:   (int128) mulrdx mulrax = mulrax * mulx3
# asm 1: imul <mulx3=int64#9
# asm 2: imul <mulx3=%r11
imul %r11

# qhasm:   carry? t6 += mulrax
# asm 1: add  <mulrax=int64#7,<t6=int64#6
# asm 2: add  <mulrax=%rax,<t6=%r9
add  %rax,%r9

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t6 += mulc
# asm 1: add  <mulc=int64#14,<t6=int64#6
# asm 2: add  <mulc=%rbx,<t6=%r9
add  %rbx,%r9

# qhasm:   t7 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t7=int64#8
# asm 2: adc <mulrdx=%rdx,<t7=%r10
adc %rdx,%r10

# qhasm:   mulx3 = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulx3=int64#3
# asm 2: movq   88(<input_1=%rsi),>mulx3=%rdx
movq   88(%rsi),%rdx

# qhasm:   mulx2 = mem64[ input_0 + 48 ]
# asm 1: movq   48(<input_0=int64#1),>mulx2=int64#7
# asm 2: movq   48(<input_0=%rdi),>mulx2=%rax
movq   48(%rdi),%rax

# qhasm:   mulx1 = mem64[ input_0 + 40 ]
# asm 1: movq   40(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   40(<input_0=%rdi),>mulx1=%r11
movq   40(%rdi),%r11

# qhasm:   mulx0 = mem64[ input_0 + 32 ]
# asm 1: movq   32(<input_0=int64#1),>mulx0=int64#14
# asm 2: movq   32(<input_0=%rdi),>mulx0=%rbx
movq   32(%rdi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm:   mulx3 = mem64[ input_0 + 56 ]
# asm 1: movq   56(<input_0=int64#1),>mulx3=int64#3
# asm 2: movq   56(<input_0=%rdi),>mulx3=%rdx
movq   56(%rdi),%rdx

# qhasm:   mulx2 = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulx2=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulx2=%rax
movq   80(%rsi),%rax

# qhasm:   mulx1 = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulx1=int64#9
# asm 2: movq   72(<input_1=%rsi),>mulx1=%r11
movq   72(%rsi),%r11

# qhasm:   mulx0 = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulx0=int64#14
# asm 2: movq   64(<input_1=%rsi),>mulx0=%rbx
movq   64(%rsi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm: carry? t0 += t0s
# asm 1: addq <t0s=stack64#9,<t0=int64#10
# asm 2: addq <t0s=64(%rsp),<t0=%r12
addq 64(%rsp),%r12

# qhasm: carry? t1 += t1s + carry
# asm 1: adcq <t1s=stack64#10,<t1=int64#11
# asm 2: adcq <t1s=72(%rsp),<t1=%r13
adcq 72(%rsp),%r13

# qhasm: carry? t2 += t2s + carry
# asm 1: adcq <t2s=stack64#11,<t2=int64#12
# asm 2: adcq <t2s=80(%rsp),<t2=%r14
adcq 80(%rsp),%r14

# qhasm: carry? t3 += t3s + carry
# asm 1: adcq <t3s=stack64#12,<t3=int64#13
# asm 2: adcq <t3s=88(%rsp),<t3=%r15
adcq 88(%rsp),%r15

# qhasm: carry? t4 += t4s + carry
# asm 1: adcq <t4s=stack64#13,<t4=int64#4
# asm 2: adcq <t4s=96(%rsp),<t4=%rcx
adcq 96(%rsp),%rcx

# qhasm: carry? t5 += t5s + carry
# asm 1: adcq <t5s=stack64#14,<t5=int64#5
# asm 2: adcq <t5s=104(%rsp),<t5=%r8
adcq 104(%rsp),%r8

# qhasm: carry? t6 += t6s + carry
# asm 1: adcq <t6s=stack64#15,<t6=int64#6
# asm 2: adcq <t6s=112(%rsp),<t6=%r9
adcq 112(%rsp),%r9

# qhasm: t7 += t7s + carry
# asm 1: adcq <t7s=stack64#16,<t7=int64#8
# asm 2: adcq <t7s=120(%rsp),<t7=%r10
adcq 120(%rsp),%r10

# qhasm: input_2 = input_2_save
# asm 1: movq <input_2_save=stack64#8,>input_2=int64#3
# asm 2: movq <input_2_save=56(%rsp),>input_2=%rdx
movq 56(%rsp),%rdx

# qhasm: mem64[ input_2 + 0] = t0
# asm 1: movq   <t0=int64#10,0(<input_2=int64#3)
# asm 2: movq   <t0=%r12,0(<input_2=%rdx)
movq   %r12,0(%rdx)

# qhasm: mem64[ input_2 + 8] = t1
# asm 1: movq   <t1=int64#11,8(<input_2=int64#3)
# asm 2: movq   <t1=%r13,8(<input_2=%rdx)
movq   %r13,8(%rdx)

# qhasm: mem64[ input_2 +16] = t2
# asm 1: movq   <t2=int64#12,16(<input_2=int64#3)
# asm 2: movq   <t2=%r14,16(<input_2=%rdx)
movq   %r14,16(%rdx)

# qhasm: mem64[ input_2 +24] = t3
# asm 1: movq   <t3=int64#13,24(<input_2=int64#3)
# asm 2: movq   <t3=%r15,24(<input_2=%rdx)
movq   %r15,24(%rdx)

# qhasm: mem64[ input_2 +32] = t4
# asm 1: movq   <t4=int64#4,32(<input_2=int64#3)
# asm 2: movq   <t4=%rcx,32(<input_2=%rdx)
movq   %rcx,32(%rdx)

# qhasm: mem64[ input_2 +40] = t5
# asm 1: movq   <t5=int64#5,40(<input_2=int64#3)
# asm 2: movq   <t5=%r8,40(<input_2=%rdx)
movq   %r8,40(%rdx)

# qhasm: mem64[ input_2 +48] = t6
# asm 1: movq   <t6=int64#6,48(<input_2=int64#3)
# asm 2: movq   <t6=%r9,48(<input_2=%rdx)
movq   %r9,48(%rdx)

# qhasm: mem64[ input_2 +56] = t7
# asm 1: movq   <t7=int64#8,56(<input_2=int64#3)
# asm 2: movq   <t7=%r10,56(<input_2=%rdx)
movq   %r10,56(%rdx)

# qhasm:   t4 = 0
# asm 1: mov  $0,>t4=int64#4
# asm 2: mov  $0,>t4=%rcx
mov  $0,%rcx

# qhasm:   t5 = 0
# asm 1: mov  $0,>t5=int64#5
# asm 2: mov  $0,>t5=%r8
mov  $0,%r8

# qhasm:   t6 = 0
# asm 1: mov  $0,>t6=int64#6
# asm 2: mov  $0,>t6=%r9
mov  $0,%r9

# qhasm:   t7 = 0
# asm 1: mov  $0,>t7=int64#8
# asm 2: mov  $0,>t7=%r10
mov  $0,%r10

# qhasm:   mulx0 = mem64[ input_0 + 0 ]
# asm 1: movq   0(<input_0=int64#1),>mulx0=int64#9
# asm 2: movq   0(<input_0=%rdi),>mulx0=%r11
movq   0(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   32(<input_1=%rsi),>mulrax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   t0 = mulrax
# asm 1: mov  <mulrax=int64#7,>t0=int64#10
# asm 2: mov  <mulrax=%rax,>t0=%r12
mov  %rax,%r12

# qhasm:   t1 = mulrdx
# asm 1: mov  <mulrdx=int64#3,>t1=int64#11
# asm 2: mov  <mulrdx=%rdx,>t1=%r13
mov  %rdx,%r13

# qhasm:   mulrax = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   40(<input_1=%rsi),>mulrax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   t2 = 0
# asm 1: mov  $0,>t2=int64#12
# asm 2: mov  $0,>t2=%r14
mov  $0,%r14

# qhasm:   t2 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t2=int64#12
# asm 2: adc <mulrdx=%rdx,<t2=%r14
adc %rdx,%r14

# qhasm:   mulrax = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulrax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   t3 = 0
# asm 1: mov  $0,>t3=int64#13
# asm 2: mov  $0,>t3=%r15
mov  $0,%r15

# qhasm:   t3 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t3=int64#13
# asm 2: adc <mulrdx=%rdx,<t3=%r15
adc %rdx,%r15

# qhasm:   mulrax = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   56(<input_1=%rsi),>mulrax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   t4 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t4=int64#4
# asm 2: adc <mulrdx=%rdx,<t4=%rcx
adc %rdx,%rcx

# qhasm:   mulx1 = mem64[ input_0 + 8 ]
# asm 1: movq   8(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   8(<input_0=%rdi),>mulx1=%r11
movq   8(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   32(<input_1=%rsi),>mulrax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   40(<input_1=%rsi),>mulrax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t2 += mulc
# asm 1: add  <mulc=int64#14,<t2=int64#12
# asm 2: add  <mulc=%rbx,<t2=%r14
add  %rbx,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulrax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax 
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   56(<input_1=%rsi),>mulrax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   t5 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t5=int64#5
# asm 2: adc <mulrdx=%rdx,<t5=%r8
adc %rdx,%r8

# qhasm:   mulx2 = mem64[ input_0 + 16]
# asm 1: movq   16(<input_0=int64#1),>mulx2=int64#9
# asm 2: movq   16(<input_0=%rdi),>mulx2=%r11
movq   16(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   32(<input_1=%rsi),>mulrax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   40(<input_1=%rsi),>mulrax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulrax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   56(<input_1=%rsi),>mulrax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   t6 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t6=int64#6
# asm 2: adc <mulrdx=%rdx,<t6=%r9
adc %rdx,%r9

# qhasm:   mulx3 = mem64[ input_0 + 24]
# asm 1: movq   24(<input_0=int64#1),>mulx3=int64#9
# asm 2: movq   24(<input_0=%rdi),>mulx3=%r11
movq   24(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   32(<input_1=%rsi),>mulrax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   40(<input_1=%rsi),>mulrax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulrax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   56(<input_1=%rsi),>mulrax=%rax
movq   56(%rsi),%rax

# qhasm:   (int128) mulrdx mulrax = mulrax * mulx3
# asm 1: imul <mulx3=int64#9
# asm 2: imul <mulx3=%r11
imul %r11

# qhasm:   carry? t6 += mulrax
# asm 1: add  <mulrax=int64#7,<t6=int64#6
# asm 2: add  <mulrax=%rax,<t6=%r9
add  %rax,%r9

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t6 += mulc
# asm 1: add  <mulc=int64#14,<t6=int64#6
# asm 2: add  <mulc=%rbx,<t6=%r9
add  %rbx,%r9

# qhasm:   t7 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t7=int64#8
# asm 2: adc <mulrdx=%rdx,<t7=%r10
adc %rdx,%r10

# qhasm:   mulx3 = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulx3=int64#3
# asm 2: movq   56(<input_1=%rsi),>mulx3=%rdx
movq   56(%rsi),%rdx

# qhasm:   mulx2 = mem64[ input_0 + 16]
# asm 1: movq   16(<input_0=int64#1),>mulx2=int64#7
# asm 2: movq   16(<input_0=%rdi),>mulx2=%rax
movq   16(%rdi),%rax

# qhasm:   mulx1 = mem64[ input_0 + 8 ]
# asm 1: movq   8(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   8(<input_0=%rdi),>mulx1=%r11
movq   8(%rdi),%r11

# qhasm:   mulx0 = mem64[ input_0 + 0 ]
# asm 1: movq   0(<input_0=int64#1),>mulx0=int64#14
# asm 2: movq   0(<input_0=%rdi),>mulx0=%rbx
movq   0(%rdi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm:   mulx3 = mem64[ input_0 + 24]
# asm 1: movq   24(<input_0=int64#1),>mulx3=int64#3
# asm 2: movq   24(<input_0=%rdi),>mulx3=%rdx
movq   24(%rdi),%rdx

# qhasm:   mulx2 = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulx2=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulx2=%rax
movq   48(%rsi),%rax

# qhasm:   mulx1 = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulx1=int64#9
# asm 2: movq   40(<input_1=%rsi),>mulx1=%r11
movq   40(%rsi),%r11

# qhasm:   mulx0 = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulx0=int64#14
# asm 2: movq   32(<input_1=%rsi),>mulx0=%rbx
movq   32(%rsi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm: t0s = t0
# asm 1: movq <t0=int64#10,>t0s=stack64#9
# asm 2: movq <t0=%r12,>t0s=64(%rsp)
movq %r12,64(%rsp)

# qhasm: t1s = t1
# asm 1: movq <t1=int64#11,>t1s=stack64#10
# asm 2: movq <t1=%r13,>t1s=72(%rsp)
movq %r13,72(%rsp)

# qhasm: t2s = t2
# asm 1: movq <t2=int64#12,>t2s=stack64#11
# asm 2: movq <t2=%r14,>t2s=80(%rsp)
movq %r14,80(%rsp)

# qhasm: t3s = t3
# asm 1: movq <t3=int64#13,>t3s=stack64#12
# asm 2: movq <t3=%r15,>t3s=88(%rsp)
movq %r15,88(%rsp)

# qhasm: t4s = t4
# asm 1: movq <t4=int64#4,>t4s=stack64#13
# asm 2: movq <t4=%rcx,>t4s=96(%rsp)
movq %rcx,96(%rsp)

# qhasm: t5s = t5
# asm 1: movq <t5=int64#5,>t5s=stack64#14
# asm 2: movq <t5=%r8,>t5s=104(%rsp)
movq %r8,104(%rsp)

# qhasm: t6s = t6
# asm 1: movq <t6=int64#6,>t6s=stack64#15
# asm 2: movq <t6=%r9,>t6s=112(%rsp)
movq %r9,112(%rsp)

# qhasm: t7s = t7
# asm 1: movq <t7=int64#8,>t7s=stack64#16
# asm 2: movq <t7=%r10,>t7s=120(%rsp)
movq %r10,120(%rsp)

# qhasm:   t4 = 0
# asm 1: mov  $0,>t4=int64#4
# asm 2: mov  $0,>t4=%rcx
mov  $0,%rcx

# qhasm:   t5 = 0
# asm 1: mov  $0,>t5=int64#5
# asm 2: mov  $0,>t5=%r8
mov  $0,%r8

# qhasm:   t6 = 0
# asm 1: mov  $0,>t6=int64#6
# asm 2: mov  $0,>t6=%r9
mov  $0,%r9

# qhasm:   t7 = 0
# asm 1: mov  $0,>t7=int64#8
# asm 2: mov  $0,>t7=%r10
mov  $0,%r10

# qhasm:   mulx0 = mem64[ input_0 + 32 ]
# asm 1: movq   32(<input_0=int64#1),>mulx0=int64#9
# asm 2: movq   32(<input_0=%rdi),>mulx0=%r11
movq   32(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   96(<input_1=%rsi),>mulrax=%rax
movq   96(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   t0 = mulrax
# asm 1: mov  <mulrax=int64#7,>t0=int64#10
# asm 2: mov  <mulrax=%rax,>t0=%r12
mov  %rax,%r12

# qhasm:   t1 = mulrdx
# asm 1: mov  <mulrdx=int64#3,>t1=int64#11
# asm 2: mov  <mulrdx=%rdx,>t1=%r13
mov  %rdx,%r13

# qhasm:   mulrax = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   104(<input_1=%rsi),>mulrax=%rax
movq   104(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   t2 = 0
# asm 1: mov  $0,>t2=int64#12
# asm 2: mov  $0,>t2=%r14
mov  $0,%r14

# qhasm:   t2 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t2=int64#12
# asm 2: adc <mulrdx=%rdx,<t2=%r14
adc %rdx,%r14

# qhasm:   mulrax = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   112(<input_1=%rsi),>mulrax=%rax
movq   112(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   t3 = 0
# asm 1: mov  $0,>t3=int64#13
# asm 2: mov  $0,>t3=%r15
mov  $0,%r15

# qhasm:   t3 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t3=int64#13
# asm 2: adc <mulrdx=%rdx,<t3=%r15
adc %rdx,%r15

# qhasm:   mulrax = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   120(<input_1=%rsi),>mulrax=%rax
movq   120(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   t4 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t4=int64#4
# asm 2: adc <mulrdx=%rdx,<t4=%rcx
adc %rdx,%rcx

# qhasm:   mulx1 = mem64[ input_0 + 40 ]
# asm 1: movq   40(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   40(<input_0=%rdi),>mulx1=%r11
movq   40(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   96(<input_1=%rsi),>mulrax=%rax
movq   96(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   104(<input_1=%rsi),>mulrax=%rax
movq   104(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t2 += mulc
# asm 1: add  <mulc=int64#14,<t2=int64#12
# asm 2: add  <mulc=%rbx,<t2=%r14
add  %rbx,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   112(<input_1=%rsi),>mulrax=%rax
movq   112(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax 
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   120(<input_1=%rsi),>mulrax=%rax
movq   120(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   t5 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t5=int64#5
# asm 2: adc <mulrdx=%rdx,<t5=%r8
adc %rdx,%r8

# qhasm:   mulx2 = mem64[ input_0 + 48 ]
# asm 1: movq   48(<input_0=int64#1),>mulx2=int64#9
# asm 2: movq   48(<input_0=%rdi),>mulx2=%r11
movq   48(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   96(<input_1=%rsi),>mulrax=%rax
movq   96(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   104(<input_1=%rsi),>mulrax=%rax
movq   104(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   112(<input_1=%rsi),>mulrax=%rax
movq   112(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   120(<input_1=%rsi),>mulrax=%rax
movq   120(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   t6 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t6=int64#6
# asm 2: adc <mulrdx=%rdx,<t6=%r9
adc %rdx,%r9

# qhasm:   mulx3 = mem64[ input_0 + 56 ]
# asm 1: movq   56(<input_0=int64#1),>mulx3=int64#9
# asm 2: movq   56(<input_0=%rdi),>mulx3=%r11
movq   56(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   96(<input_1=%rsi),>mulrax=%rax
movq   96(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   104(<input_1=%rsi),>mulrax=%rax
movq   104(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   112(<input_1=%rsi),>mulrax=%rax
movq   112(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   120(<input_1=%rsi),>mulrax=%rax
movq   120(%rsi),%rax

# qhasm:   (int128) mulrdx mulrax = mulrax * mulx3
# asm 1: imul <mulx3=int64#9
# asm 2: imul <mulx3=%r11
imul %r11

# qhasm:   carry? t6 += mulrax
# asm 1: add  <mulrax=int64#7,<t6=int64#6
# asm 2: add  <mulrax=%rax,<t6=%r9
add  %rax,%r9

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t6 += mulc
# asm 1: add  <mulc=int64#14,<t6=int64#6
# asm 2: add  <mulc=%rbx,<t6=%r9
add  %rbx,%r9

# qhasm:   t7 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t7=int64#8
# asm 2: adc <mulrdx=%rdx,<t7=%r10
adc %rdx,%r10

# qhasm:   mulx3 = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulx3=int64#3
# asm 2: movq   120(<input_1=%rsi),>mulx3=%rdx
movq   120(%rsi),%rdx

# qhasm:   mulx2 = mem64[ input_0 + 48 ]
# asm 1: movq   48(<input_0=int64#1),>mulx2=int64#7
# asm 2: movq   48(<input_0=%rdi),>mulx2=%rax
movq   48(%rdi),%rax

# qhasm:   mulx1 = mem64[ input_0 + 40 ]
# asm 1: movq   40(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   40(<input_0=%rdi),>mulx1=%r11
movq   40(%rdi),%r11

# qhasm:   mulx0 = mem64[ input_0 + 32 ]
# asm 1: movq   32(<input_0=int64#1),>mulx0=int64#14
# asm 2: movq   32(<input_0=%rdi),>mulx0=%rbx
movq   32(%rdi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm:   mulx3 = mem64[ input_0 + 56 ]
# asm 1: movq   56(<input_0=int64#1),>mulx3=int64#3
# asm 2: movq   56(<input_0=%rdi),>mulx3=%rdx
movq   56(%rdi),%rdx

# qhasm:   mulx2 = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulx2=int64#7
# asm 2: movq   112(<input_1=%rsi),>mulx2=%rax
movq   112(%rsi),%rax

# qhasm:   mulx1 = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulx1=int64#9
# asm 2: movq   104(<input_1=%rsi),>mulx1=%r11
movq   104(%rsi),%r11

# qhasm:   mulx0 = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulx0=int64#14
# asm 2: movq   96(<input_1=%rsi),>mulx0=%rbx
movq   96(%rsi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm: carry? t0 += t0s
# asm 1: addq <t0s=stack64#9,<t0=int64#10
# asm 2: addq <t0s=64(%rsp),<t0=%r12
addq 64(%rsp),%r12

# qhasm: carry? t1 += t1s + carry
# asm 1: adcq <t1s=stack64#10,<t1=int64#11
# asm 2: adcq <t1s=72(%rsp),<t1=%r13
adcq 72(%rsp),%r13

# qhasm: carry? t2 += t2s + carry
# asm 1: adcq <t2s=stack64#11,<t2=int64#12
# asm 2: adcq <t2s=80(%rsp),<t2=%r14
adcq 80(%rsp),%r14

# qhasm: carry? t3 += t3s + carry
# asm 1: adcq <t3s=stack64#12,<t3=int64#13
# asm 2: adcq <t3s=88(%rsp),<t3=%r15
adcq 88(%rsp),%r15

# qhasm: carry? t4 += t4s + carry
# asm 1: adcq <t4s=stack64#13,<t4=int64#4
# asm 2: adcq <t4s=96(%rsp),<t4=%rcx
adcq 96(%rsp),%rcx

# qhasm: carry? t5 += t5s + carry
# asm 1: adcq <t5s=stack64#14,<t5=int64#5
# asm 2: adcq <t5s=104(%rsp),<t5=%r8
adcq 104(%rsp),%r8

# qhasm: carry? t6 += t6s + carry
# asm 1: adcq <t6s=stack64#15,<t6=int64#6
# asm 2: adcq <t6s=112(%rsp),<t6=%r9
adcq 112(%rsp),%r9

# qhasm: t7 += t7s + carry
# asm 1: adcq <t7s=stack64#16,<t7=int64#8
# asm 2: adcq <t7s=120(%rsp),<t7=%r10
adcq 120(%rsp),%r10

# qhasm: input_2 = input_2_save
# asm 1: movq <input_2_save=stack64#8,>input_2=int64#3
# asm 2: movq <input_2_save=56(%rsp),>input_2=%rdx
movq 56(%rsp),%rdx

# qhasm: mem64[ input_2 + 64] = t0
# asm 1: movq   <t0=int64#10,64(<input_2=int64#3)
# asm 2: movq   <t0=%r12,64(<input_2=%rdx)
movq   %r12,64(%rdx)

# qhasm: mem64[ input_2 + 72] = t1
# asm 1: movq   <t1=int64#11,72(<input_2=int64#3)
# asm 2: movq   <t1=%r13,72(<input_2=%rdx)
movq   %r13,72(%rdx)

# qhasm: mem64[ input_2 + 80] = t2
# asm 1: movq   <t2=int64#12,80(<input_2=int64#3)
# asm 2: movq   <t2=%r14,80(<input_2=%rdx)
movq   %r14,80(%rdx)

# qhasm: mem64[ input_2 + 88] = t3
# asm 1: movq   <t3=int64#13,88(<input_2=int64#3)
# asm 2: movq   <t3=%r15,88(<input_2=%rdx)
movq   %r15,88(%rdx)

# qhasm: mem64[ input_2 + 96] = t4
# asm 1: movq   <t4=int64#4,96(<input_2=int64#3)
# asm 2: movq   <t4=%rcx,96(<input_2=%rdx)
movq   %rcx,96(%rdx)

# qhasm: mem64[ input_2 +104] = t5
# asm 1: movq   <t5=int64#5,104(<input_2=int64#3)
# asm 2: movq   <t5=%r8,104(<input_2=%rdx)
movq   %r8,104(%rdx)

# qhasm: mem64[ input_2 +112] = t6
# asm 1: movq   <t6=int64#6,112(<input_2=int64#3)
# asm 2: movq   <t6=%r9,112(<input_2=%rdx)
movq   %r9,112(%rdx)

# qhasm: mem64[ input_2 +120] = t7
# asm 1: movq   <t7=int64#8,120(<input_2=int64#3)
# asm 2: movq   <t7=%r10,120(<input_2=%rdx)
movq   %r10,120(%rdx)

# qhasm:   t4 = 0
# asm 1: mov  $0,>t4=int64#4
# asm 2: mov  $0,>t4=%rcx
mov  $0,%rcx

# qhasm:   t5 = 0
# asm 1: mov  $0,>t5=int64#5
# asm 2: mov  $0,>t5=%r8
mov  $0,%r8

# qhasm:   t6 = 0
# asm 1: mov  $0,>t6=int64#6
# asm 2: mov  $0,>t6=%r9
mov  $0,%r9

# qhasm:   t7 = 0
# asm 1: mov  $0,>t7=int64#8
# asm 2: mov  $0,>t7=%r10
mov  $0,%r10

# qhasm:   mulx0 = mem64[ input_0 + 64]
# asm 1: movq   64(<input_0=int64#1),>mulx0=int64#9
# asm 2: movq   64(<input_0=%rdi),>mulx0=%r11
movq   64(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   0(<input_1=%rsi),>mulrax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   t0 = mulrax
# asm 1: mov  <mulrax=int64#7,>t0=int64#10
# asm 2: mov  <mulrax=%rax,>t0=%r12
mov  %rax,%r12

# qhasm:   t1 = mulrdx
# asm 1: mov  <mulrdx=int64#3,>t1=int64#11
# asm 2: mov  <mulrdx=%rdx,>t1=%r13
mov  %rdx,%r13

# qhasm:   mulrax = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   8(<input_1=%rsi),>mulrax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   t2 = 0
# asm 1: mov  $0,>t2=int64#12
# asm 2: mov  $0,>t2=%r14
mov  $0,%r14

# qhasm:   t2 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t2=int64#12
# asm 2: adc <mulrdx=%rdx,<t2=%r14
adc %rdx,%r14

# qhasm:   mulrax = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulrax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   t3 = 0
# asm 1: mov  $0,>t3=int64#13
# asm 2: mov  $0,>t3=%r15
mov  $0,%r15

# qhasm:   t3 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t3=int64#13
# asm 2: adc <mulrdx=%rdx,<t3=%r15
adc %rdx,%r15

# qhasm:   mulrax = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   24(<input_1=%rsi),>mulrax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   t4 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t4=int64#4
# asm 2: adc <mulrdx=%rdx,<t4=%rcx
adc %rdx,%rcx

# qhasm:   mulx1 = mem64[ input_0 + 72]
# asm 1: movq   72(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   72(<input_0=%rdi),>mulx1=%r11
movq   72(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   0(<input_1=%rsi),>mulrax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   8(<input_1=%rsi),>mulrax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t2 += mulc
# asm 1: add  <mulc=int64#14,<t2=int64#12
# asm 2: add  <mulc=%rbx,<t2=%r14
add  %rbx,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulrax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax 
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   24(<input_1=%rsi),>mulrax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   t5 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t5=int64#5
# asm 2: adc <mulrdx=%rdx,<t5=%r8
adc %rdx,%r8

# qhasm:   mulx2 = mem64[ input_0 + 80]
# asm 1: movq   80(<input_0=int64#1),>mulx2=int64#9
# asm 2: movq   80(<input_0=%rdi),>mulx2=%r11
movq   80(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   0(<input_1=%rsi),>mulrax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   8(<input_1=%rsi),>mulrax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulrax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   24(<input_1=%rsi),>mulrax=%rax
movq   24(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   t6 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t6=int64#6
# asm 2: adc <mulrdx=%rdx,<t6=%r9
adc %rdx,%r9

# qhasm:   mulx3 = mem64[ input_0 + 88]
# asm 1: movq   88(<input_0=int64#1),>mulx3=int64#9
# asm 2: movq   88(<input_0=%rdi),>mulx3=%r11
movq   88(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   0(<input_1=%rsi),>mulrax=%rax
movq   0(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   8(<input_1=%rsi),>mulrax=%rax
movq   8(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulrax=%rax
movq   16(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   24(<input_1=%rsi),>mulrax=%rax
movq   24(%rsi),%rax

# qhasm:   (int128) mulrdx mulrax = mulrax * mulx3
# asm 1: imul <mulx3=int64#9
# asm 2: imul <mulx3=%r11
imul %r11

# qhasm:   carry? t6 += mulrax
# asm 1: add  <mulrax=int64#7,<t6=int64#6
# asm 2: add  <mulrax=%rax,<t6=%r9
add  %rax,%r9

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t6 += mulc
# asm 1: add  <mulc=int64#14,<t6=int64#6
# asm 2: add  <mulc=%rbx,<t6=%r9
add  %rbx,%r9

# qhasm:   t7 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t7=int64#8
# asm 2: adc <mulrdx=%rdx,<t7=%r10
adc %rdx,%r10

# qhasm:   mulx3 = mem64[ input_1 + 24]
# asm 1: movq   24(<input_1=int64#2),>mulx3=int64#3
# asm 2: movq   24(<input_1=%rsi),>mulx3=%rdx
movq   24(%rsi),%rdx

# qhasm:   mulx2 = mem64[ input_0 + 80]
# asm 1: movq   80(<input_0=int64#1),>mulx2=int64#7
# asm 2: movq   80(<input_0=%rdi),>mulx2=%rax
movq   80(%rdi),%rax

# qhasm:   mulx1 = mem64[ input_0 + 72]
# asm 1: movq   72(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   72(<input_0=%rdi),>mulx1=%r11
movq   72(%rdi),%r11

# qhasm:   mulx0 = mem64[ input_0 + 64]
# asm 1: movq   64(<input_0=int64#1),>mulx0=int64#14
# asm 2: movq   64(<input_0=%rdi),>mulx0=%rbx
movq   64(%rdi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm:   mulx3 = mem64[ input_0 + 88]
# asm 1: movq   88(<input_0=int64#1),>mulx3=int64#3
# asm 2: movq   88(<input_0=%rdi),>mulx3=%rdx
movq   88(%rdi),%rdx

# qhasm:   mulx2 = mem64[ input_1 + 16]
# asm 1: movq   16(<input_1=int64#2),>mulx2=int64#7
# asm 2: movq   16(<input_1=%rsi),>mulx2=%rax
movq   16(%rsi),%rax

# qhasm:   mulx1 = mem64[ input_1 + 8 ]
# asm 1: movq   8(<input_1=int64#2),>mulx1=int64#9
# asm 2: movq   8(<input_1=%rsi),>mulx1=%r11
movq   8(%rsi),%r11

# qhasm:   mulx0 = mem64[ input_1 + 0 ]
# asm 1: movq   0(<input_1=int64#2),>mulx0=int64#14
# asm 2: movq   0(<input_1=%rsi),>mulx0=%rbx
movq   0(%rsi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm: t0s = t0
# asm 1: movq <t0=int64#10,>t0s=stack64#9
# asm 2: movq <t0=%r12,>t0s=64(%rsp)
movq %r12,64(%rsp)

# qhasm: t1s = t1
# asm 1: movq <t1=int64#11,>t1s=stack64#10
# asm 2: movq <t1=%r13,>t1s=72(%rsp)
movq %r13,72(%rsp)

# qhasm: t2s = t2
# asm 1: movq <t2=int64#12,>t2s=stack64#11
# asm 2: movq <t2=%r14,>t2s=80(%rsp)
movq %r14,80(%rsp)

# qhasm: t3s = t3
# asm 1: movq <t3=int64#13,>t3s=stack64#12
# asm 2: movq <t3=%r15,>t3s=88(%rsp)
movq %r15,88(%rsp)

# qhasm: t4s = t4
# asm 1: movq <t4=int64#4,>t4s=stack64#13
# asm 2: movq <t4=%rcx,>t4s=96(%rsp)
movq %rcx,96(%rsp)

# qhasm: t5s = t5
# asm 1: movq <t5=int64#5,>t5s=stack64#14
# asm 2: movq <t5=%r8,>t5s=104(%rsp)
movq %r8,104(%rsp)

# qhasm: t6s = t6
# asm 1: movq <t6=int64#6,>t6s=stack64#15
# asm 2: movq <t6=%r9,>t6s=112(%rsp)
movq %r9,112(%rsp)

# qhasm: t7s = t7
# asm 1: movq <t7=int64#8,>t7s=stack64#16
# asm 2: movq <t7=%r10,>t7s=120(%rsp)
movq %r10,120(%rsp)

# qhasm:   t4 = 0
# asm 1: mov  $0,>t4=int64#4
# asm 2: mov  $0,>t4=%rcx
mov  $0,%rcx

# qhasm:   t5 = 0
# asm 1: mov  $0,>t5=int64#5
# asm 2: mov  $0,>t5=%r8
mov  $0,%r8

# qhasm:   t6 = 0
# asm 1: mov  $0,>t6=int64#6
# asm 2: mov  $0,>t6=%r9
mov  $0,%r9

# qhasm:   t7 = 0
# asm 1: mov  $0,>t7=int64#8
# asm 2: mov  $0,>t7=%r10
mov  $0,%r10

# qhasm:   mulx0 = mem64[ input_0 + 96 ]
# asm 1: movq   96(<input_0=int64#1),>mulx0=int64#9
# asm 2: movq   96(<input_0=%rdi),>mulx0=%r11
movq   96(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   64(<input_1=%rsi),>mulrax=%rax
movq   64(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   t0 = mulrax
# asm 1: mov  <mulrax=int64#7,>t0=int64#10
# asm 2: mov  <mulrax=%rax,>t0=%r12
mov  %rax,%r12

# qhasm:   t1 = mulrdx
# asm 1: mov  <mulrdx=int64#3,>t1=int64#11
# asm 2: mov  <mulrdx=%rdx,>t1=%r13
mov  %rdx,%r13

# qhasm:   mulrax = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   72(<input_1=%rsi),>mulrax=%rax
movq   72(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   t2 = 0
# asm 1: mov  $0,>t2=int64#12
# asm 2: mov  $0,>t2=%r14
mov  $0,%r14

# qhasm:   t2 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t2=int64#12
# asm 2: adc <mulrdx=%rdx,<t2=%r14
adc %rdx,%r14

# qhasm:   mulrax = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulrax=%rax
movq   80(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   t3 = 0
# asm 1: mov  $0,>t3=int64#13
# asm 2: mov  $0,>t3=%r15
mov  $0,%r15

# qhasm:   t3 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t3=int64#13
# asm 2: adc <mulrdx=%rdx,<t3=%r15
adc %rdx,%r15

# qhasm:   mulrax = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   88(<input_1=%rsi),>mulrax=%rax
movq   88(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   t4 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t4=int64#4
# asm 2: adc <mulrdx=%rdx,<t4=%rcx
adc %rdx,%rcx

# qhasm:   mulx1 = mem64[ input_0 +104 ]
# asm 1: movq   104(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   104(<input_0=%rdi),>mulx1=%r11
movq   104(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   64(<input_1=%rsi),>mulrax=%rax
movq   64(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   72(<input_1=%rsi),>mulrax=%rax
movq   72(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t2 += mulc
# asm 1: add  <mulc=int64#14,<t2=int64#12
# asm 2: add  <mulc=%rbx,<t2=%r14
add  %rbx,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulrax=%rax
movq   80(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax 
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   88(<input_1=%rsi),>mulrax=%rax
movq   88(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   t5 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t5=int64#5
# asm 2: adc <mulrdx=%rdx,<t5=%r8
adc %rdx,%r8

# qhasm:   mulx2 = mem64[ input_0 +112 ]
# asm 1: movq   112(<input_0=int64#1),>mulx2=int64#9
# asm 2: movq   112(<input_0=%rdi),>mulx2=%r11
movq   112(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   64(<input_1=%rsi),>mulrax=%rax
movq   64(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   72(<input_1=%rsi),>mulrax=%rax
movq   72(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulrax=%rax
movq   80(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   88(<input_1=%rsi),>mulrax=%rax
movq   88(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   t6 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t6=int64#6
# asm 2: adc <mulrdx=%rdx,<t6=%r9
adc %rdx,%r9

# qhasm:   mulx3 = mem64[ input_0 +120 ]
# asm 1: movq   120(<input_0=int64#1),>mulx3=int64#9
# asm 2: movq   120(<input_0=%rdi),>mulx3=%r11
movq   120(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   64(<input_1=%rsi),>mulrax=%rax
movq   64(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   72(<input_1=%rsi),>mulrax=%rax
movq   72(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulrax=%rax
movq   80(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   88(<input_1=%rsi),>mulrax=%rax
movq   88(%rsi),%rax

# qhasm:   (int128) mulrdx mulrax = mulrax * mulx3
# asm 1: imul <mulx3=int64#9
# asm 2: imul <mulx3=%r11
imul %r11

# qhasm:   carry? t6 += mulrax
# asm 1: add  <mulrax=int64#7,<t6=int64#6
# asm 2: add  <mulrax=%rax,<t6=%r9
add  %rax,%r9

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t6 += mulc
# asm 1: add  <mulc=int64#14,<t6=int64#6
# asm 2: add  <mulc=%rbx,<t6=%r9
add  %rbx,%r9

# qhasm:   t7 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t7=int64#8
# asm 2: adc <mulrdx=%rdx,<t7=%r10
adc %rdx,%r10

# qhasm:   mulx3 = mem64[ input_1 + 88 ]
# asm 1: movq   88(<input_1=int64#2),>mulx3=int64#3
# asm 2: movq   88(<input_1=%rsi),>mulx3=%rdx
movq   88(%rsi),%rdx

# qhasm:   mulx2 = mem64[ input_0 +112 ]
# asm 1: movq   112(<input_0=int64#1),>mulx2=int64#7
# asm 2: movq   112(<input_0=%rdi),>mulx2=%rax
movq   112(%rdi),%rax

# qhasm:   mulx1 = mem64[ input_0 +104 ]
# asm 1: movq   104(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   104(<input_0=%rdi),>mulx1=%r11
movq   104(%rdi),%r11

# qhasm:   mulx0 = mem64[ input_0 + 96 ]
# asm 1: movq   96(<input_0=int64#1),>mulx0=int64#14
# asm 2: movq   96(<input_0=%rdi),>mulx0=%rbx
movq   96(%rdi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm:   mulx3 = mem64[ input_0 +120 ]
# asm 1: movq   120(<input_0=int64#1),>mulx3=int64#3
# asm 2: movq   120(<input_0=%rdi),>mulx3=%rdx
movq   120(%rdi),%rdx

# qhasm:   mulx2 = mem64[ input_1 + 80 ]
# asm 1: movq   80(<input_1=int64#2),>mulx2=int64#7
# asm 2: movq   80(<input_1=%rsi),>mulx2=%rax
movq   80(%rsi),%rax

# qhasm:   mulx1 = mem64[ input_1 + 72 ]
# asm 1: movq   72(<input_1=int64#2),>mulx1=int64#9
# asm 2: movq   72(<input_1=%rsi),>mulx1=%r11
movq   72(%rsi),%r11

# qhasm:   mulx0 = mem64[ input_1 + 64 ]
# asm 1: movq   64(<input_1=int64#2),>mulx0=int64#14
# asm 2: movq   64(<input_1=%rsi),>mulx0=%rbx
movq   64(%rsi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm: carry? t0 += t0s
# asm 1: addq <t0s=stack64#9,<t0=int64#10
# asm 2: addq <t0s=64(%rsp),<t0=%r12
addq 64(%rsp),%r12

# qhasm: carry? t1 += t1s + carry
# asm 1: adcq <t1s=stack64#10,<t1=int64#11
# asm 2: adcq <t1s=72(%rsp),<t1=%r13
adcq 72(%rsp),%r13

# qhasm: carry? t2 += t2s + carry
# asm 1: adcq <t2s=stack64#11,<t2=int64#12
# asm 2: adcq <t2s=80(%rsp),<t2=%r14
adcq 80(%rsp),%r14

# qhasm: carry? t3 += t3s + carry
# asm 1: adcq <t3s=stack64#12,<t3=int64#13
# asm 2: adcq <t3s=88(%rsp),<t3=%r15
adcq 88(%rsp),%r15

# qhasm: carry? t4 += t4s + carry
# asm 1: adcq <t4s=stack64#13,<t4=int64#4
# asm 2: adcq <t4s=96(%rsp),<t4=%rcx
adcq 96(%rsp),%rcx

# qhasm: carry? t5 += t5s + carry
# asm 1: adcq <t5s=stack64#14,<t5=int64#5
# asm 2: adcq <t5s=104(%rsp),<t5=%r8
adcq 104(%rsp),%r8

# qhasm: carry? t6 += t6s + carry
# asm 1: adcq <t6s=stack64#15,<t6=int64#6
# asm 2: adcq <t6s=112(%rsp),<t6=%r9
adcq 112(%rsp),%r9

# qhasm: t7 += t7s + carry
# asm 1: adcq <t7s=stack64#16,<t7=int64#8
# asm 2: adcq <t7s=120(%rsp),<t7=%r10
adcq 120(%rsp),%r10

# qhasm: input_2 = input_2_save
# asm 1: movq <input_2_save=stack64#8,>input_2=int64#3
# asm 2: movq <input_2_save=56(%rsp),>input_2=%rdx
movq 56(%rsp),%rdx

# qhasm: mem64[ input_2 + 128] = t0
# asm 1: movq   <t0=int64#10,128(<input_2=int64#3)
# asm 2: movq   <t0=%r12,128(<input_2=%rdx)
movq   %r12,128(%rdx)

# qhasm: mem64[ input_2 + 136] = t1
# asm 1: movq   <t1=int64#11,136(<input_2=int64#3)
# asm 2: movq   <t1=%r13,136(<input_2=%rdx)
movq   %r13,136(%rdx)

# qhasm: mem64[ input_2 + 144] = t2
# asm 1: movq   <t2=int64#12,144(<input_2=int64#3)
# asm 2: movq   <t2=%r14,144(<input_2=%rdx)
movq   %r14,144(%rdx)

# qhasm: mem64[ input_2 + 152] = t3
# asm 1: movq   <t3=int64#13,152(<input_2=int64#3)
# asm 2: movq   <t3=%r15,152(<input_2=%rdx)
movq   %r15,152(%rdx)

# qhasm: mem64[ input_2 + 160] = t4
# asm 1: movq   <t4=int64#4,160(<input_2=int64#3)
# asm 2: movq   <t4=%rcx,160(<input_2=%rdx)
movq   %rcx,160(%rdx)

# qhasm: mem64[ input_2 + 168] = t5
# asm 1: movq   <t5=int64#5,168(<input_2=int64#3)
# asm 2: movq   <t5=%r8,168(<input_2=%rdx)
movq   %r8,168(%rdx)

# qhasm: mem64[ input_2 + 176] = t6
# asm 1: movq   <t6=int64#6,176(<input_2=int64#3)
# asm 2: movq   <t6=%r9,176(<input_2=%rdx)
movq   %r9,176(%rdx)

# qhasm: mem64[ input_2 + 184] = t7
# asm 1: movq   <t7=int64#8,184(<input_2=int64#3)
# asm 2: movq   <t7=%r10,184(<input_2=%rdx)
movq   %r10,184(%rdx)

# qhasm:   t4 = 0
# asm 1: mov  $0,>t4=int64#4
# asm 2: mov  $0,>t4=%rcx
mov  $0,%rcx

# qhasm:   t5 = 0
# asm 1: mov  $0,>t5=int64#5
# asm 2: mov  $0,>t5=%r8
mov  $0,%r8

# qhasm:   t6 = 0
# asm 1: mov  $0,>t6=int64#6
# asm 2: mov  $0,>t6=%r9
mov  $0,%r9

# qhasm:   t7 = 0
# asm 1: mov  $0,>t7=int64#8
# asm 2: mov  $0,>t7=%r10
mov  $0,%r10

# qhasm:   mulx0 = mem64[ input_0 + 64]
# asm 1: movq   64(<input_0=int64#1),>mulx0=int64#9
# asm 2: movq   64(<input_0=%rdi),>mulx0=%r11
movq   64(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   32(<input_1=%rsi),>mulrax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   t0 = mulrax
# asm 1: mov  <mulrax=int64#7,>t0=int64#10
# asm 2: mov  <mulrax=%rax,>t0=%r12
mov  %rax,%r12

# qhasm:   t1 = mulrdx
# asm 1: mov  <mulrdx=int64#3,>t1=int64#11
# asm 2: mov  <mulrdx=%rdx,>t1=%r13
mov  %rdx,%r13

# qhasm:   mulrax = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   40(<input_1=%rsi),>mulrax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   t2 = 0
# asm 1: mov  $0,>t2=int64#12
# asm 2: mov  $0,>t2=%r14
mov  $0,%r14

# qhasm:   t2 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t2=int64#12
# asm 2: adc <mulrdx=%rdx,<t2=%r14
adc %rdx,%r14

# qhasm:   mulrax = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulrax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   t3 = 0
# asm 1: mov  $0,>t3=int64#13
# asm 2: mov  $0,>t3=%r15
mov  $0,%r15

# qhasm:   t3 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t3=int64#13
# asm 2: adc <mulrdx=%rdx,<t3=%r15
adc %rdx,%r15

# qhasm:   mulrax = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   56(<input_1=%rsi),>mulrax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   t4 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t4=int64#4
# asm 2: adc <mulrdx=%rdx,<t4=%rcx
adc %rdx,%rcx

# qhasm:   mulx1 = mem64[ input_0 + 72]
# asm 1: movq   72(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   72(<input_0=%rdi),>mulx1=%r11
movq   72(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   32(<input_1=%rsi),>mulrax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   40(<input_1=%rsi),>mulrax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t2 += mulc
# asm 1: add  <mulc=int64#14,<t2=int64#12
# asm 2: add  <mulc=%rbx,<t2=%r14
add  %rbx,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulrax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax 
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   56(<input_1=%rsi),>mulrax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   t5 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t5=int64#5
# asm 2: adc <mulrdx=%rdx,<t5=%r8
adc %rdx,%r8

# qhasm:   mulx2 = mem64[ input_0 + 80]
# asm 1: movq   80(<input_0=int64#1),>mulx2=int64#9
# asm 2: movq   80(<input_0=%rdi),>mulx2=%r11
movq   80(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   32(<input_1=%rsi),>mulrax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   40(<input_1=%rsi),>mulrax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulrax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   56(<input_1=%rsi),>mulrax=%rax
movq   56(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   t6 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t6=int64#6
# asm 2: adc <mulrdx=%rdx,<t6=%r9
adc %rdx,%r9

# qhasm:   mulx3 = mem64[ input_0 + 88]
# asm 1: movq   88(<input_0=int64#1),>mulx3=int64#9
# asm 2: movq   88(<input_0=%rdi),>mulx3=%r11
movq   88(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   32(<input_1=%rsi),>mulrax=%rax
movq   32(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   40(<input_1=%rsi),>mulrax=%rax
movq   40(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulrax=%rax
movq   48(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   56(<input_1=%rsi),>mulrax=%rax
movq   56(%rsi),%rax

# qhasm:   (int128) mulrdx mulrax = mulrax * mulx3
# asm 1: imul <mulx3=int64#9
# asm 2: imul <mulx3=%r11
imul %r11

# qhasm:   carry? t6 += mulrax
# asm 1: add  <mulrax=int64#7,<t6=int64#6
# asm 2: add  <mulrax=%rax,<t6=%r9
add  %rax,%r9

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t6 += mulc
# asm 1: add  <mulc=int64#14,<t6=int64#6
# asm 2: add  <mulc=%rbx,<t6=%r9
add  %rbx,%r9

# qhasm:   t7 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t7=int64#8
# asm 2: adc <mulrdx=%rdx,<t7=%r10
adc %rdx,%r10

# qhasm:   mulx3 = mem64[ input_1 + 56]
# asm 1: movq   56(<input_1=int64#2),>mulx3=int64#3
# asm 2: movq   56(<input_1=%rsi),>mulx3=%rdx
movq   56(%rsi),%rdx

# qhasm:   mulx2 = mem64[ input_0 + 80]
# asm 1: movq   80(<input_0=int64#1),>mulx2=int64#7
# asm 2: movq   80(<input_0=%rdi),>mulx2=%rax
movq   80(%rdi),%rax

# qhasm:   mulx1 = mem64[ input_0 + 72]
# asm 1: movq   72(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   72(<input_0=%rdi),>mulx1=%r11
movq   72(%rdi),%r11

# qhasm:   mulx0 = mem64[ input_0 + 64]
# asm 1: movq   64(<input_0=int64#1),>mulx0=int64#14
# asm 2: movq   64(<input_0=%rdi),>mulx0=%rbx
movq   64(%rdi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm:   mulx3 = mem64[ input_0 + 88]
# asm 1: movq   88(<input_0=int64#1),>mulx3=int64#3
# asm 2: movq   88(<input_0=%rdi),>mulx3=%rdx
movq   88(%rdi),%rdx

# qhasm:   mulx2 = mem64[ input_1 + 48]
# asm 1: movq   48(<input_1=int64#2),>mulx2=int64#7
# asm 2: movq   48(<input_1=%rsi),>mulx2=%rax
movq   48(%rsi),%rax

# qhasm:   mulx1 = mem64[ input_1 + 40]
# asm 1: movq   40(<input_1=int64#2),>mulx1=int64#9
# asm 2: movq   40(<input_1=%rsi),>mulx1=%r11
movq   40(%rsi),%r11

# qhasm:   mulx0 = mem64[ input_1 + 32]
# asm 1: movq   32(<input_1=int64#2),>mulx0=int64#14
# asm 2: movq   32(<input_1=%rsi),>mulx0=%rbx
movq   32(%rsi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm: t0s = t0
# asm 1: movq <t0=int64#10,>t0s=stack64#9
# asm 2: movq <t0=%r12,>t0s=64(%rsp)
movq %r12,64(%rsp)

# qhasm: t1s = t1
# asm 1: movq <t1=int64#11,>t1s=stack64#10
# asm 2: movq <t1=%r13,>t1s=72(%rsp)
movq %r13,72(%rsp)

# qhasm: t2s = t2
# asm 1: movq <t2=int64#12,>t2s=stack64#11
# asm 2: movq <t2=%r14,>t2s=80(%rsp)
movq %r14,80(%rsp)

# qhasm: t3s = t3
# asm 1: movq <t3=int64#13,>t3s=stack64#12
# asm 2: movq <t3=%r15,>t3s=88(%rsp)
movq %r15,88(%rsp)

# qhasm: t4s = t4
# asm 1: movq <t4=int64#4,>t4s=stack64#13
# asm 2: movq <t4=%rcx,>t4s=96(%rsp)
movq %rcx,96(%rsp)

# qhasm: t5s = t5
# asm 1: movq <t5=int64#5,>t5s=stack64#14
# asm 2: movq <t5=%r8,>t5s=104(%rsp)
movq %r8,104(%rsp)

# qhasm: t6s = t6
# asm 1: movq <t6=int64#6,>t6s=stack64#15
# asm 2: movq <t6=%r9,>t6s=112(%rsp)
movq %r9,112(%rsp)

# qhasm: t7s = t7
# asm 1: movq <t7=int64#8,>t7s=stack64#16
# asm 2: movq <t7=%r10,>t7s=120(%rsp)
movq %r10,120(%rsp)

# qhasm:   t4 = 0
# asm 1: mov  $0,>t4=int64#4
# asm 2: mov  $0,>t4=%rcx
mov  $0,%rcx

# qhasm:   t5 = 0
# asm 1: mov  $0,>t5=int64#5
# asm 2: mov  $0,>t5=%r8
mov  $0,%r8

# qhasm:   t6 = 0
# asm 1: mov  $0,>t6=int64#6
# asm 2: mov  $0,>t6=%r9
mov  $0,%r9

# qhasm:   t7 = 0
# asm 1: mov  $0,>t7=int64#8
# asm 2: mov  $0,>t7=%r10
mov  $0,%r10

# qhasm:   mulx0 = mem64[ input_0 + 96 ]
# asm 1: movq   96(<input_0=int64#1),>mulx0=int64#9
# asm 2: movq   96(<input_0=%rdi),>mulx0=%r11
movq   96(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   96(<input_1=%rsi),>mulrax=%rax
movq   96(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   t0 = mulrax
# asm 1: mov  <mulrax=int64#7,>t0=int64#10
# asm 2: mov  <mulrax=%rax,>t0=%r12
mov  %rax,%r12

# qhasm:   t1 = mulrdx
# asm 1: mov  <mulrdx=int64#3,>t1=int64#11
# asm 2: mov  <mulrdx=%rdx,>t1=%r13
mov  %rdx,%r13

# qhasm:   mulrax = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   104(<input_1=%rsi),>mulrax=%rax
movq   104(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   t2 = 0
# asm 1: mov  $0,>t2=int64#12
# asm 2: mov  $0,>t2=%r14
mov  $0,%r14

# qhasm:   t2 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t2=int64#12
# asm 2: adc <mulrdx=%rdx,<t2=%r14
adc %rdx,%r14

# qhasm:   mulrax = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   112(<input_1=%rsi),>mulrax=%rax
movq   112(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   t3 = 0
# asm 1: mov  $0,>t3=int64#13
# asm 2: mov  $0,>t3=%r15
mov  $0,%r15

# qhasm:   t3 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t3=int64#13
# asm 2: adc <mulrdx=%rdx,<t3=%r15
adc %rdx,%r15

# qhasm:   mulrax = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   120(<input_1=%rsi),>mulrax=%rax
movq   120(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx0
# asm 1: mul  <mulx0=int64#9
# asm 2: mul  <mulx0=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   t4 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t4=int64#4
# asm 2: adc <mulrdx=%rdx,<t4=%rcx
adc %rdx,%rcx

# qhasm:   mulx1 = mem64[ input_0 +104 ]
# asm 1: movq   104(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   104(<input_0=%rdi),>mulx1=%r11
movq   104(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   96(<input_1=%rsi),>mulrax=%rax
movq   96(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t1 += mulrax
# asm 1: add  <mulrax=int64#7,<t1=int64#11
# asm 2: add  <mulrax=%rax,<t1=%r13
add  %rax,%r13

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   104(<input_1=%rsi),>mulrax=%rax
movq   104(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t2 += mulc
# asm 1: add  <mulc=int64#14,<t2=int64#12
# asm 2: add  <mulc=%rbx,<t2=%r14
add  %rbx,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   112(<input_1=%rsi),>mulrax=%rax
movq   112(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax 
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   120(<input_1=%rsi),>mulrax=%rax
movq   120(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx1
# asm 1: mul  <mulx1=int64#9
# asm 2: mul  <mulx1=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   t5 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t5=int64#5
# asm 2: adc <mulrdx=%rdx,<t5=%r8
adc %rdx,%r8

# qhasm:   mulx2 = mem64[ input_0 +112 ]
# asm 1: movq   112(<input_0=int64#1),>mulx2=int64#9
# asm 2: movq   112(<input_0=%rdi),>mulx2=%r11
movq   112(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   96(<input_1=%rsi),>mulrax=%rax
movq   96(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t2 += mulrax
# asm 1: add  <mulrax=int64#7,<t2=int64#12
# asm 2: add  <mulrax=%rax,<t2=%r14
add  %rax,%r14

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   104(<input_1=%rsi),>mulrax=%rax
movq   104(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t3 += mulc
# asm 1: add  <mulc=int64#14,<t3=int64#13
# asm 2: add  <mulc=%rbx,<t3=%r15
add  %rbx,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   112(<input_1=%rsi),>mulrax=%rax
movq   112(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   120(<input_1=%rsi),>mulrax=%rax
movq   120(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx2
# asm 1: mul  <mulx2=int64#9
# asm 2: mul  <mulx2=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   t6 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t6=int64#6
# asm 2: adc <mulrdx=%rdx,<t6=%r9
adc %rdx,%r9

# qhasm:   mulx3 = mem64[ input_0 +120 ]
# asm 1: movq   120(<input_0=int64#1),>mulx3=int64#9
# asm 2: movq   120(<input_0=%rdi),>mulx3=%r11
movq   120(%rdi),%r11

# qhasm:   mulrax = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   96(<input_1=%rsi),>mulrax=%rax
movq   96(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t3 += mulrax
# asm 1: add  <mulrax=int64#7,<t3=int64#13
# asm 2: add  <mulrax=%rax,<t3=%r15
add  %rax,%r15

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   104(<input_1=%rsi),>mulrax=%rax
movq   104(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t4 += mulrax
# asm 1: add  <mulrax=int64#7,<t4=int64#4
# asm 2: add  <mulrax=%rax,<t4=%rcx
add  %rax,%rcx

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t4 += mulc
# asm 1: add  <mulc=int64#14,<t4=int64#4
# asm 2: add  <mulc=%rbx,<t4=%rcx
add  %rbx,%rcx

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   112(<input_1=%rsi),>mulrax=%rax
movq   112(%rsi),%rax

# qhasm:   (uint128) mulrdx mulrax = mulrax * mulx3
# asm 1: mul  <mulx3=int64#9
# asm 2: mul  <mulx3=%r11
mul  %r11

# qhasm:   carry? t5 += mulrax
# asm 1: add  <mulrax=int64#7,<t5=int64#5
# asm 2: add  <mulrax=%rax,<t5=%r8
add  %rax,%r8

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t5 += mulc
# asm 1: add  <mulc=int64#14,<t5=int64#5
# asm 2: add  <mulc=%rbx,<t5=%r8
add  %rbx,%r8

# qhasm:   mulc = 0
# asm 1: mov  $0,>mulc=int64#14
# asm 2: mov  $0,>mulc=%rbx
mov  $0,%rbx

# qhasm:   mulc += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<mulc=int64#14
# asm 2: adc <mulrdx=%rdx,<mulc=%rbx
adc %rdx,%rbx

# qhasm:   mulrax = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulrax=int64#7
# asm 2: movq   120(<input_1=%rsi),>mulrax=%rax
movq   120(%rsi),%rax

# qhasm:   (int128) mulrdx mulrax = mulrax * mulx3
# asm 1: imul <mulx3=int64#9
# asm 2: imul <mulx3=%r11
imul %r11

# qhasm:   carry? t6 += mulrax
# asm 1: add  <mulrax=int64#7,<t6=int64#6
# asm 2: add  <mulrax=%rax,<t6=%r9
add  %rax,%r9

# qhasm:   mulrdx += 0 + carry
# asm 1: adc $0,<mulrdx=int64#3
# asm 2: adc $0,<mulrdx=%rdx
adc $0,%rdx

# qhasm:   carry? t6 += mulc
# asm 1: add  <mulc=int64#14,<t6=int64#6
# asm 2: add  <mulc=%rbx,<t6=%r9
add  %rbx,%r9

# qhasm:   t7 += mulrdx + carry
# asm 1: adc <mulrdx=int64#3,<t7=int64#8
# asm 2: adc <mulrdx=%rdx,<t7=%r10
adc %rdx,%r10

# qhasm:   mulx3 = mem64[ input_1 +120 ]
# asm 1: movq   120(<input_1=int64#2),>mulx3=int64#3
# asm 2: movq   120(<input_1=%rsi),>mulx3=%rdx
movq   120(%rsi),%rdx

# qhasm:   mulx2 = mem64[ input_0 +112 ]
# asm 1: movq   112(<input_0=int64#1),>mulx2=int64#7
# asm 2: movq   112(<input_0=%rdi),>mulx2=%rax
movq   112(%rdi),%rax

# qhasm:   mulx1 = mem64[ input_0 +104 ]
# asm 1: movq   104(<input_0=int64#1),>mulx1=int64#9
# asm 2: movq   104(<input_0=%rdi),>mulx1=%r11
movq   104(%rdi),%r11

# qhasm:   mulx0 = mem64[ input_0 + 96 ]
# asm 1: movq   96(<input_0=int64#1),>mulx0=int64#14
# asm 2: movq   96(<input_0=%rdi),>mulx0=%rbx
movq   96(%rdi),%rbx

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#3
# asm 2: sar  $63,<mulx3=%rdx
sar  $63,%rdx

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx0=int64#14
# asm 2: and  <mulx3=%rdx,<mulx0=%rbx
and  %rdx,%rbx

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx1=int64#9
# asm 2: and  <mulx3=%rdx,<mulx1=%r11
and  %rdx,%r11

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#3,<mulx2=int64#7
# asm 2: and  <mulx3=%rdx,<mulx2=%rax
and  %rdx,%rax

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#14,<t4=int64#4
# asm 2: sub  <mulx0=%rbx,<t4=%rcx
sub  %rbx,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#9,<t5=int64#5
# asm 2: sbb  <mulx1=%r11,<t5=%r8
sbb  %r11,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#7,<t6=int64#6
# asm 2: sbb  <mulx2=%rax,<t6=%r9
sbb  %rax,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm:   mulx3 = mem64[ input_0 +120 ]
# asm 1: movq   120(<input_0=int64#1),>mulx3=int64#1
# asm 2: movq   120(<input_0=%rdi),>mulx3=%rdi
movq   120(%rdi),%rdi

# qhasm:   mulx2 = mem64[ input_1 +112 ]
# asm 1: movq   112(<input_1=int64#2),>mulx2=int64#3
# asm 2: movq   112(<input_1=%rsi),>mulx2=%rdx
movq   112(%rsi),%rdx

# qhasm:   mulx1 = mem64[ input_1 +104 ]
# asm 1: movq   104(<input_1=int64#2),>mulx1=int64#7
# asm 2: movq   104(<input_1=%rsi),>mulx1=%rax
movq   104(%rsi),%rax

# qhasm:   mulx0 = mem64[ input_1 + 96 ]
# asm 1: movq   96(<input_1=int64#2),>mulx0=int64#2
# asm 2: movq   96(<input_1=%rsi),>mulx0=%rsi
movq   96(%rsi),%rsi

# qhasm:   (int64) mulx3 >>= 63
# asm 1: sar  $63,<mulx3=int64#1
# asm 2: sar  $63,<mulx3=%rdi
sar  $63,%rdi

# qhasm:   mulx0 &= mulx3
# asm 1: and  <mulx3=int64#1,<mulx0=int64#2
# asm 2: and  <mulx3=%rdi,<mulx0=%rsi
and  %rdi,%rsi

# qhasm:   mulx1 &= mulx3
# asm 1: and  <mulx3=int64#1,<mulx1=int64#7
# asm 2: and  <mulx3=%rdi,<mulx1=%rax
and  %rdi,%rax

# qhasm:   mulx2 &= mulx3
# asm 1: and  <mulx3=int64#1,<mulx2=int64#3
# asm 2: and  <mulx3=%rdi,<mulx2=%rdx
and  %rdi,%rdx

# qhasm:   carry? t4 -= mulx0
# asm 1: sub  <mulx0=int64#2,<t4=int64#4
# asm 2: sub  <mulx0=%rsi,<t4=%rcx
sub  %rsi,%rcx

# qhasm:   carry? t5 -= mulx1 - carry
# asm 1: sbb  <mulx1=int64#7,<t5=int64#5
# asm 2: sbb  <mulx1=%rax,<t5=%r8
sbb  %rax,%r8

# qhasm:   carry? t6 -= mulx2 - carry
# asm 1: sbb  <mulx2=int64#3,<t6=int64#6
# asm 2: sbb  <mulx2=%rdx,<t6=%r9
sbb  %rdx,%r9

# qhasm:   t7 -= 0 - carry
# asm 1: sbb  $0,<t7=int64#8
# asm 2: sbb  $0,<t7=%r10
sbb  $0,%r10

# qhasm: carry? t0 += t0s
# asm 1: addq <t0s=stack64#9,<t0=int64#10
# asm 2: addq <t0s=64(%rsp),<t0=%r12
addq 64(%rsp),%r12

# qhasm: carry? t1 += t1s + carry
# asm 1: adcq <t1s=stack64#10,<t1=int64#11
# asm 2: adcq <t1s=72(%rsp),<t1=%r13
adcq 72(%rsp),%r13

# qhasm: carry? t2 += t2s + carry
# asm 1: adcq <t2s=stack64#11,<t2=int64#12
# asm 2: adcq <t2s=80(%rsp),<t2=%r14
adcq 80(%rsp),%r14

# qhasm: carry? t3 += t3s + carry
# asm 1: adcq <t3s=stack64#12,<t3=int64#13
# asm 2: adcq <t3s=88(%rsp),<t3=%r15
adcq 88(%rsp),%r15

# qhasm: carry? t4 += t4s + carry
# asm 1: adcq <t4s=stack64#13,<t4=int64#4
# asm 2: adcq <t4s=96(%rsp),<t4=%rcx
adcq 96(%rsp),%rcx

# qhasm: carry? t5 += t5s + carry
# asm 1: adcq <t5s=stack64#14,<t5=int64#5
# asm 2: adcq <t5s=104(%rsp),<t5=%r8
adcq 104(%rsp),%r8

# qhasm: carry? t6 += t6s + carry
# asm 1: adcq <t6s=stack64#15,<t6=int64#6
# asm 2: adcq <t6s=112(%rsp),<t6=%r9
adcq 112(%rsp),%r9

# qhasm: t7 += t7s + carry
# asm 1: adcq <t7s=stack64#16,<t7=int64#8
# asm 2: adcq <t7s=120(%rsp),<t7=%r10
adcq 120(%rsp),%r10

# qhasm: input_2 = input_2_save
# asm 1: movq <input_2_save=stack64#8,>input_2=int64#1
# asm 2: movq <input_2_save=56(%rsp),>input_2=%rdi
movq 56(%rsp),%rdi

# qhasm: mem64[ input_2 + 192] = t0
# asm 1: movq   <t0=int64#10,192(<input_2=int64#1)
# asm 2: movq   <t0=%r12,192(<input_2=%rdi)
movq   %r12,192(%rdi)

# qhasm: mem64[ input_2 + 200] = t1
# asm 1: movq   <t1=int64#11,200(<input_2=int64#1)
# asm 2: movq   <t1=%r13,200(<input_2=%rdi)
movq   %r13,200(%rdi)

# qhasm: mem64[ input_2 + 208] = t2
# asm 1: movq   <t2=int64#12,208(<input_2=int64#1)
# asm 2: movq   <t2=%r14,208(<input_2=%rdi)
movq   %r14,208(%rdi)

# qhasm: mem64[ input_2 + 216] = t3
# asm 1: movq   <t3=int64#13,216(<input_2=int64#1)
# asm 2: movq   <t3=%r15,216(<input_2=%rdi)
movq   %r15,216(%rdi)

# qhasm: mem64[ input_2 + 224] = t4
# asm 1: movq   <t4=int64#4,224(<input_2=int64#1)
# asm 2: movq   <t4=%rcx,224(<input_2=%rdi)
movq   %rcx,224(%rdi)

# qhasm: mem64[ input_2 + 232] = t5
# asm 1: movq   <t5=int64#5,232(<input_2=int64#1)
# asm 2: movq   <t5=%r8,232(<input_2=%rdi)
movq   %r8,232(%rdi)

# qhasm: mem64[ input_2 + 240] = t6
# asm 1: movq   <t6=int64#6,240(<input_2=int64#1)
# asm 2: movq   <t6=%r9,240(<input_2=%rdi)
movq   %r9,240(%rdi)

# qhasm: mem64[ input_2 + 248] = t7
# asm 1: movq   <t7=int64#8,248(<input_2=int64#1)
# asm 2: movq   <t7=%r10,248(<input_2=%rdi)
movq   %r10,248(%rdi)

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


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

# qhasm: int64 p0

# qhasm: int64 count

# qhasm: int64 t7

# qhasm: int64 a0

# qhasm: int64 a1

# qhasm: int64 a2

# qhasm: int64 a3

# qhasm: int64 a4

# qhasm: int64 a5

# qhasm: int64 a6

# qhasm: int64 a7

# qhasm: stack64 caller_r11_stack

# qhasm: stack64 caller_r12_stack

# qhasm: stack64 caller_r13_stack

# qhasm: stack64 caller_r14_stack

# qhasm: stack64 caller_r15_stack

# qhasm: stack64 caller_rbp_stack

# qhasm: stack64 caller_rbx_stack

# qhasm: enter norm500_511
.p2align 5
.global _norm500_511
.global norm500_511
_norm500_511:
norm500_511:
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

# qhasm: p0 = input_0
# asm 1: mov  <input_0=int64#1,>p0=int64#1
# asm 2: mov  <input_0=%rdi,>p0=%rdi
mov  %rdi,%rdi

# qhasm: count = input_1
# asm 1: mov  <input_1=int64#2,>count=int64#2
# asm 2: mov  <input_1=%rsi,>count=%rsi
mov  %rsi,%rsi

# qhasm: count <<= 6
# asm 1: shl  $6,<count=int64#2
# asm 2: shl  $6,<count=%rsi
shl  $6,%rsi

# qhasm: loop:
._loop:

# qhasm: carry? count -= 64
# asm 1: sub  $64,<count=int64#2
# asm 2: sub  $64,<count=%rsi
sub  $64,%rsi
# comment:fp stack unchanged by jump

# qhasm: goto end if carry
jc ._end

# qhasm: t7 = *(uint64 *) (p0 + 56 + count)
# asm 1: movq   56(<p0=int64#1,<count=int64#2),>t7=int64#3
# asm 2: movq   56(<p0=%rdi,<count=%rsi),>t7=%rdx
movq   56(%rdi,%rsi),%rdx

# qhasm: (int64) t7 >>= 63
# asm 1: sar  $63,<t7=int64#3
# asm 2: sar  $63,<t7=%rdx
sar  $63,%rdx

# qhasm: a0 = mem64[M_0]
# asm 1: movq M_0,>a0=int64#4
# asm 2: movq M_0,>a0=%rcx
movq M_0(%rip),%rcx

# qhasm: a1 = mem64[M_1]
# asm 1: movq M_1,>a1=int64#5
# asm 2: movq M_1,>a1=%r8
movq M_1(%rip),%r8

# qhasm: a2 = mem64[M_2]
# asm 1: movq M_2,>a2=int64#6
# asm 2: movq M_2,>a2=%r9
movq M_2(%rip),%r9

# qhasm: a3 = mem64[M_3]
# asm 1: movq M_3,>a3=int64#7
# asm 2: movq M_3,>a3=%rax
movq M_3(%rip),%rax

# qhasm: a4 = mem64[M_4]
# asm 1: movq M_4,>a4=int64#8
# asm 2: movq M_4,>a4=%r10
movq M_4(%rip),%r10

# qhasm: a5 = mem64[M_5]
# asm 1: movq M_5,>a5=int64#9
# asm 2: movq M_5,>a5=%r11
movq M_5(%rip),%r11

# qhasm: a6 = mem64[M_6]
# asm 1: movq M_6,>a6=int64#10
# asm 2: movq M_6,>a6=%r12
movq M_6(%rip),%r12

# qhasm: a7 = mem64[M_7]
# asm 1: movq M_7,>a7=int64#11
# asm 2: movq M_7,>a7=%r13
movq M_7(%rip),%r13

# qhasm: a0 &= t7
# asm 1: and  <t7=int64#3,<a0=int64#4
# asm 2: and  <t7=%rdx,<a0=%rcx
and  %rdx,%rcx

# qhasm: a1 &= t7
# asm 1: and  <t7=int64#3,<a1=int64#5
# asm 2: and  <t7=%rdx,<a1=%r8
and  %rdx,%r8

# qhasm: a2 &= t7
# asm 1: and  <t7=int64#3,<a2=int64#6
# asm 2: and  <t7=%rdx,<a2=%r9
and  %rdx,%r9

# qhasm: a3 &= t7
# asm 1: and  <t7=int64#3,<a3=int64#7
# asm 2: and  <t7=%rdx,<a3=%rax
and  %rdx,%rax

# qhasm: a4 &= t7
# asm 1: and  <t7=int64#3,<a4=int64#8
# asm 2: and  <t7=%rdx,<a4=%r10
and  %rdx,%r10

# qhasm: a5 &= t7
# asm 1: and  <t7=int64#3,<a5=int64#9
# asm 2: and  <t7=%rdx,<a5=%r11
and  %rdx,%r11

# qhasm: a6 &= t7
# asm 1: and  <t7=int64#3,<a6=int64#10
# asm 2: and  <t7=%rdx,<a6=%r12
and  %rdx,%r12

# qhasm: a7 &= t7
# asm 1: and  <t7=int64#3,<a7=int64#11
# asm 2: and  <t7=%rdx,<a7=%r13
and  %rdx,%r13

# qhasm: carry? (uint64) a0 += *(uint64 *) (p0 + 0 + count) 
# asm 1: addq 0(<p0=int64#1,<count=int64#2,1),<a0=int64#4
# asm 2: addq 0(<p0=%rdi,<count=%rsi,1),<a0=%rcx
addq 0(%rdi,%rsi,1),%rcx

# qhasm: carry? (uint64) a1 += *(uint64 *) (p0 + 8 + count) + carry
# asm 1: adcq 8(<p0=int64#1,<count=int64#2,1),<a1=int64#5
# asm 2: adcq 8(<p0=%rdi,<count=%rsi,1),<a1=%r8
adcq 8(%rdi,%rsi,1),%r8

# qhasm: carry? (uint64) a2 += *(uint64 *) (p0 +16 + count) + carry
# asm 1: adcq 16(<p0=int64#1,<count=int64#2,1),<a2=int64#6
# asm 2: adcq 16(<p0=%rdi,<count=%rsi,1),<a2=%r9
adcq 16(%rdi,%rsi,1),%r9

# qhasm: carry? (uint64) a3 += *(uint64 *) (p0 +24 + count) + carry
# asm 1: adcq 24(<p0=int64#1,<count=int64#2,1),<a3=int64#7
# asm 2: adcq 24(<p0=%rdi,<count=%rsi,1),<a3=%rax
adcq 24(%rdi,%rsi,1),%rax

# qhasm: carry? (uint64) a4 += *(uint64 *) (p0 +32 + count) + carry
# asm 1: adcq 32(<p0=int64#1,<count=int64#2,1),<a4=int64#8
# asm 2: adcq 32(<p0=%rdi,<count=%rsi,1),<a4=%r10
adcq 32(%rdi,%rsi,1),%r10

# qhasm: carry? (uint64) a5 += *(uint64 *) (p0 +40 + count) + carry
# asm 1: adcq 40(<p0=int64#1,<count=int64#2,1),<a5=int64#9
# asm 2: adcq 40(<p0=%rdi,<count=%rsi,1),<a5=%r11
adcq 40(%rdi,%rsi,1),%r11

# qhasm: carry? (uint64) a6 += *(uint64 *) (p0 +48 + count) + carry
# asm 1: adcq 48(<p0=int64#1,<count=int64#2,1),<a6=int64#10
# asm 2: adcq 48(<p0=%rdi,<count=%rsi,1),<a6=%r12
adcq 48(%rdi,%rsi,1),%r12

# qhasm: (uint64) a7 += *(uint64 *) (p0 +56 + count) + carry
# asm 1: adcq 56(<p0=int64#1,<count=int64#2,1),<a7=int64#11
# asm 2: adcq 56(<p0=%rdi,<count=%rsi,1),<a7=%r13
adcq 56(%rdi,%rsi,1),%r13

# qhasm: mem64[ p0 + 0 + count] = a0
# asm 1: movq   <a0=int64#4,0(<p0=int64#1,<count=int64#2,1)
# asm 2: movq   <a0=%rcx,0(<p0=%rdi,<count=%rsi,1)
movq   %rcx,0(%rdi,%rsi,1)

# qhasm: mem64[ p0 + 8 + count] = a1
# asm 1: movq   <a1=int64#5,8(<p0=int64#1,<count=int64#2,1)
# asm 2: movq   <a1=%r8,8(<p0=%rdi,<count=%rsi,1)
movq   %r8,8(%rdi,%rsi,1)

# qhasm: mem64[ p0 +16 + count] = a2
# asm 1: movq   <a2=int64#6,16(<p0=int64#1,<count=int64#2,1)
# asm 2: movq   <a2=%r9,16(<p0=%rdi,<count=%rsi,1)
movq   %r9,16(%rdi,%rsi,1)

# qhasm: mem64[ p0 +24 + count] = a3
# asm 1: movq   <a3=int64#7,24(<p0=int64#1,<count=int64#2,1)
# asm 2: movq   <a3=%rax,24(<p0=%rdi,<count=%rsi,1)
movq   %rax,24(%rdi,%rsi,1)

# qhasm: mem64[ p0 +32 + count] = a4
# asm 1: movq   <a4=int64#8,32(<p0=int64#1,<count=int64#2,1)
# asm 2: movq   <a4=%r10,32(<p0=%rdi,<count=%rsi,1)
movq   %r10,32(%rdi,%rsi,1)

# qhasm: mem64[ p0 +40 + count] = a5
# asm 1: movq   <a5=int64#9,40(<p0=int64#1,<count=int64#2,1)
# asm 2: movq   <a5=%r11,40(<p0=%rdi,<count=%rsi,1)
movq   %r11,40(%rdi,%rsi,1)

# qhasm: mem64[ p0 +48 + count] = a6
# asm 1: movq   <a6=int64#10,48(<p0=int64#1,<count=int64#2,1)
# asm 2: movq   <a6=%r12,48(<p0=%rdi,<count=%rsi,1)
movq   %r12,48(%rdi,%rsi,1)

# qhasm: mem64[ p0 +56 + count] = a7
# asm 1: movq   <a7=int64#11,56(<p0=int64#1,<count=int64#2,1)
# asm 2: movq   <a7=%r13,56(<p0=%rdi,<count=%rsi,1)
movq   %r13,56(%rdi,%rsi,1)
# comment:fp stack unchanged by jump

# qhasm: goto loop
jmp ._loop

# qhasm: end:
._end:

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

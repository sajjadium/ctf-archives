
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

# qhasm: int64 r1

# qhasm: int64 q1

# qhasm: int64 u1

# qhasm: int64 v1

# qhasm: int64 r2

# qhasm: int64 q2

# qhasm: int64 u2

# qhasm: int64 v2

# qhasm: int64 t0

# qhasm: int64 t1

# qhasm: int64 t2

# qhasm: int64 t3

# qhasm: int64 t4

# qhasm: int64 t5

# qhasm: int64 rax

# qhasm: int64 rdx

# qhasm: enter muls64xs64
.p2align 5
.global _muls64xs64
.global muls64xs64
_muls64xs64:
muls64xs64:
mov %rsp,%r11
and $31,%r11
add $0,%r11
sub %r11,%rsp

# qhasm: input_2 = input_2
# asm 1: mov  <input_2=int64#3,>input_2=int64#4
# asm 2: mov  <input_2=%rdx,>input_2=%rcx
mov  %rdx,%rcx

# qhasm: rax = mem64[ input_0 + 0 ]
# asm 1: movq   0(<input_0=int64#1),>rax=int64#7
# asm 2: movq   0(<input_0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ input_1 + 0 ]
# asm 1: imulq  0(<input_1=int64#2)
# asm 2: imulq  0(<input_1=%rsi)
imulq  0(%rsi)

# qhasm: t0 = rax
# asm 1: mov  <rax=int64#7,>t0=int64#5
# asm 2: mov  <rax=%rax,>t0=%r8
mov  %rax,%r8

# qhasm: t1 = rdx
# asm 1: mov  <rdx=int64#3,>t1=int64#6
# asm 2: mov  <rdx=%rdx,>t1=%r9
mov  %rdx,%r9

# qhasm: rax = mem64[ input_0 + 8 ]
# asm 1: movq   8(<input_0=int64#1),>rax=int64#7
# asm 2: movq   8(<input_0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ input_1 +16 ]
# asm 1: imulq  16(<input_1=int64#2)
# asm 2: imulq  16(<input_1=%rsi)
imulq  16(%rsi)

# qhasm: carry? t0 += rax
# asm 1: add  <rax=int64#7,<t0=int64#5
# asm 2: add  <rax=%rax,<t0=%r8
add  %rax,%r8

# qhasm: t1 += rdx + carry
# asm 1: adc <rdx=int64#3,<t1=int64#6
# asm 2: adc <rdx=%rdx,<t1=%r9
adc %rdx,%r9

# qhasm: mem64[ input_2 + 0 ] = t0
# asm 1: movq   <t0=int64#5,0(<input_2=int64#4)
# asm 2: movq   <t0=%r8,0(<input_2=%rcx)
movq   %r8,0(%rcx)

# qhasm: mem64[ input_2 + 8 ] = t1
# asm 1: movq   <t1=int64#6,8(<input_2=int64#4)
# asm 2: movq   <t1=%r9,8(<input_2=%rcx)
movq   %r9,8(%rcx)

# qhasm: rax = mem64[ input_0 + 0 ]
# asm 1: movq   0(<input_0=int64#1),>rax=int64#7
# asm 2: movq   0(<input_0=%rdi),>rax=%rax
movq   0(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ input_1 + 8 ]
# asm 1: imulq  8(<input_1=int64#2)
# asm 2: imulq  8(<input_1=%rsi)
imulq  8(%rsi)

# qhasm: t0 = rax
# asm 1: mov  <rax=int64#7,>t0=int64#5
# asm 2: mov  <rax=%rax,>t0=%r8
mov  %rax,%r8

# qhasm: t1 = rdx
# asm 1: mov  <rdx=int64#3,>t1=int64#6
# asm 2: mov  <rdx=%rdx,>t1=%r9
mov  %rdx,%r9

# qhasm: rax = mem64[ input_0 + 8 ]
# asm 1: movq   8(<input_0=int64#1),>rax=int64#7
# asm 2: movq   8(<input_0=%rdi),>rax=%rax
movq   8(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ input_1 +24 ]
# asm 1: imulq  24(<input_1=int64#2)
# asm 2: imulq  24(<input_1=%rsi)
imulq  24(%rsi)

# qhasm: carry? t0 += rax
# asm 1: add  <rax=int64#7,<t0=int64#5
# asm 2: add  <rax=%rax,<t0=%r8
add  %rax,%r8

# qhasm: t1 += rdx + carry
# asm 1: adc <rdx=int64#3,<t1=int64#6
# asm 2: adc <rdx=%rdx,<t1=%r9
adc %rdx,%r9

# qhasm: mem64[ input_2 +16 ] = t0
# asm 1: movq   <t0=int64#5,16(<input_2=int64#4)
# asm 2: movq   <t0=%r8,16(<input_2=%rcx)
movq   %r8,16(%rcx)

# qhasm: mem64[ input_2 +24 ] = t1
# asm 1: movq   <t1=int64#6,24(<input_2=int64#4)
# asm 2: movq   <t1=%r9,24(<input_2=%rcx)
movq   %r9,24(%rcx)

# qhasm: rax = mem64[ input_0 +16 ]
# asm 1: movq   16(<input_0=int64#1),>rax=int64#7
# asm 2: movq   16(<input_0=%rdi),>rax=%rax
movq   16(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ input_1 + 0 ]
# asm 1: imulq  0(<input_1=int64#2)
# asm 2: imulq  0(<input_1=%rsi)
imulq  0(%rsi)

# qhasm: t0 = rax
# asm 1: mov  <rax=int64#7,>t0=int64#5
# asm 2: mov  <rax=%rax,>t0=%r8
mov  %rax,%r8

# qhasm: t1 = rdx
# asm 1: mov  <rdx=int64#3,>t1=int64#6
# asm 2: mov  <rdx=%rdx,>t1=%r9
mov  %rdx,%r9

# qhasm: rax = mem64[ input_0 +24 ]
# asm 1: movq   24(<input_0=int64#1),>rax=int64#7
# asm 2: movq   24(<input_0=%rdi),>rax=%rax
movq   24(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ input_1 +16 ]
# asm 1: imulq  16(<input_1=int64#2)
# asm 2: imulq  16(<input_1=%rsi)
imulq  16(%rsi)

# qhasm: carry? t0 += rax
# asm 1: add  <rax=int64#7,<t0=int64#5
# asm 2: add  <rax=%rax,<t0=%r8
add  %rax,%r8

# qhasm: t1 += rdx + carry
# asm 1: adc <rdx=int64#3,<t1=int64#6
# asm 2: adc <rdx=%rdx,<t1=%r9
adc %rdx,%r9

# qhasm: mem64[ input_2 +32 ] = t0
# asm 1: movq   <t0=int64#5,32(<input_2=int64#4)
# asm 2: movq   <t0=%r8,32(<input_2=%rcx)
movq   %r8,32(%rcx)

# qhasm: mem64[ input_2 +40 ] = t1
# asm 1: movq   <t1=int64#6,40(<input_2=int64#4)
# asm 2: movq   <t1=%r9,40(<input_2=%rcx)
movq   %r9,40(%rcx)

# qhasm: rax = mem64[ input_0 +16 ]
# asm 1: movq   16(<input_0=int64#1),>rax=int64#7
# asm 2: movq   16(<input_0=%rdi),>rax=%rax
movq   16(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ input_1 + 8 ]
# asm 1: imulq  8(<input_1=int64#2)
# asm 2: imulq  8(<input_1=%rsi)
imulq  8(%rsi)

# qhasm: t0 = rax
# asm 1: mov  <rax=int64#7,>t0=int64#5
# asm 2: mov  <rax=%rax,>t0=%r8
mov  %rax,%r8

# qhasm: t1 = rdx
# asm 1: mov  <rdx=int64#3,>t1=int64#6
# asm 2: mov  <rdx=%rdx,>t1=%r9
mov  %rdx,%r9

# qhasm: rax = mem64[ input_0 +24 ]
# asm 1: movq   24(<input_0=int64#1),>rax=int64#7
# asm 2: movq   24(<input_0=%rdi),>rax=%rax
movq   24(%rdi),%rax

# qhasm: (int128) rdx rax = rax * mem64[ input_1 +24 ]
# asm 1: imulq  24(<input_1=int64#2)
# asm 2: imulq  24(<input_1=%rsi)
imulq  24(%rsi)

# qhasm: carry? t0 += rax
# asm 1: add  <rax=int64#7,<t0=int64#5
# asm 2: add  <rax=%rax,<t0=%r8
add  %rax,%r8

# qhasm: t1 += rdx + carry
# asm 1: adc <rdx=int64#3,<t1=int64#6
# asm 2: adc <rdx=%rdx,<t1=%r9
adc %rdx,%r9

# qhasm: mem64[ input_2 +48 ] = t0
# asm 1: movq   <t0=int64#5,48(<input_2=int64#4)
# asm 2: movq   <t0=%r8,48(<input_2=%rcx)
movq   %r8,48(%rcx)

# qhasm: mem64[ input_2 +56 ] = t1
# asm 1: movq   <t1=int64#6,56(<input_2=int64#4)
# asm 2: movq   <t1=%r9,56(<input_2=%rcx)
movq   %r9,56(%rcx)

# qhasm: return
add %r11,%rsp
ret

#!/usr/bin/env python3 icicle.py

mov r15, 65535

mov r1, 1
mov r2, 4

read:
    pr "Enter a valid password: "
    readstr [r1]
    strint [r1], [r1]
    jl [r1], 1329227995784915872903807060280344576, short
    add r1, r1, 1
    jl r1, r2, read

sub r1, [1], [2]
jz r1, same
sub r1, [2], [3]
jz r1, same
sub r1, [3], [1]
jz r1, same

mov r1, 1

validateloop:
    mov r12, [r1]
    xor [r2], [r2], [r2]
    add r14, rip, 1
    j validate
    jnz r13, invalid
    add r1, r1, 1
    jl r1, r2, validateloop

j flag

validate:
    jnz r12, recurse
    mov r13, r12
    mov rip, r14

    recurse:
    mov [r15], r14
    sub r15, r15, 1
    mov [r15], r1
    sub r15, r15, 1

    mod r1, r12, 256
    xor [r2], [r2], r1
    jz [r2], invalid
    mov [r2], r1
    div r12, r12, 256
    intstr r12, r12
    rev r12, r12
    strint r12, r12
    mod r3, r12, 256
    div r12, r12, 256
    xor r1, r1, r3
    add r14, rip, 1
    j validate
    add r13, r13, r1

    add r15, r15, 1
    mov r1, [r15]
    add r15, r15, 1
    mov r14, [r15]
    mov rip, r14

short:
    pr "Password too short!"
    j end

invalid:
    pr "Invalid password!"
    j end

same:
    pr "Password was reused!"
    j end

flag:
    pr "[FLAG REDACTED]"

end:
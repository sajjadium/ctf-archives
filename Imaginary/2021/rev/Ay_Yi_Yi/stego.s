main:
pr "Enter iii filename: "
readstr [420]
pr "Enter flag: "
readstr [1337]

intstr r15, 10

rev [1337], [1337]
strint [1337], [1337]

readf [7331], [420]
rev [7331], [7331]
strint [7331], [7331]


mov r1, 8
mov r3, 0
headerloop:
and r2, [7331], 255
div [7331], [7331], 256
add [9999], [9999], r2
mult [9999], [9999], 256
add r3, r3, 1

jl r3, r1, headerloop

encrypt:
and r4, [1337], 255
div [1337], [1337], 256

mov r6, 4
innerloop:
and r5, r4, 1
div r4, r4, 2
and r7, [7331], 255
div [7331], [7331], 256
div r7, r7, 2
mult r7, r7, 2
add r7, r7, r5
add [9999], [9999], r7
mult [9999], [9999], 256

and r7, [7331], 255
div [7331], [7331], 256
add [9999], [9999], r7
mult [9999], [9999], 256

and r5, r4, 1
div r4, r4, 2
mult r5, 4, r5
and r7, [7331], 255
div [7331], [7331], 256
and r8, r7, 3
div r7, r7, 8
mult r7, r7, 8
add r7, r5, r7
add r7, r8, r7
add [9999], [9999], r7
mult [9999], [9999], 256

and r7, [7331], 255
div [7331], [7331], 256
add [9999], [9999], r7
mult [9999], [9999], 256
and r7, [7331], 255
div [7331], [7331], 256
add [9999], [9999], r7
mult [9999], [9999], 256
and r7, [7331], 255
div [7331], [7331], 256
add [9999], [9999], r7
mult [9999], [9999], 256


sub r6, r6, 1
jnz r6, innerloop
jnz [1337], encrypt

last:
and r1, [7331], 255
div [7331], [7331], 256
add [9999], [9999], r1
mult [9999], [9999], 256
jnz [7331], last

div [9999], [9999], 256
intstr [9999], [9999]
add [420], [420], ".enc"
writef [9999], [420]

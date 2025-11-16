.section .text
.global _start

.arm
getrandom:
  mov r2, #0
  mov r7, #384
  svc #0
  bx lr

_start:
  sub r0, sp, #2
  mov r1, #2
  mov r8, r0
  bl getrandom
  ldrb r1, [r8]
  bic r1, #0xF
  sub sp, r1 // ASLR behövs nog inte, jag sköter det själv :D
  bl main
  bl _exit

_exit:
    mov r7, #1
    mov r0, #0
    svc #0

main:
  push {fp, lr}
  mov fp, sp

  sub sp, #64
  mov r0, sp

  bl read_input
  mov r6, r0

  ldr r1, =msg
  ldr r2, =len
  bl write

  mov r1, sp
  mov r2, r6
  bl write

  mov r3, sp
  mov sp, fp
  pop {fp, lr}
  bx lr

read_input:
  mov r1, r0 // dest
  movw r2, #0x256
  mov r7, #3 // read syscall
  mov r0, #0 // stdin
  svc #0
  bx lr

write:
  push {lr}
  mov r7, #4 // write syscall
  mov r0, #1 // stdout
  svc #0
  pop {r3}
  bx r3

msg:
.ascii "Hej: "
len = . - msg

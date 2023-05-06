
.data
input: .space 64
.text
j JHxujuMOUf
QaySuEavWA:
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
lb $t0, 0($a0)
lb $t1, 0($a1)
bne $t0, $t1, QaySuEavWA_L2
addi $a1, $a1, 1
addi $a0, $a0, 1
QaySuEavWA_L1:
beq $t0, $zero, QaySuEavWA_L3
lb $t0, 0($a0)
addi $a0, $a0, 1
lb $t1, 0($a1)
addi $a1, $a1, 1
beq $t0, $t1, QaySuEavWA_L1
QaySuEavWA_L2:
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t8, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x129da
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1038
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x13a12
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x0
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x0
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

lb $t1, 0($sp)
addi $sp, $sp, 4
lb $t0, 0($sp)
addi $sp, $sp, 4
jr $ra
QaySuEavWA_L3:
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t6, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x4092
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x4091
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t6
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x0
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t6
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t6
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x0
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t6
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

lb $t1, 0($sp)
addi $sp, $sp, 4
lb $t0, 0($sp)
addi $sp, $sp, 4
jr $ra

JHxujuMOUf:
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t8, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x7100
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x4
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t8
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1c3c
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t8
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x0
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t8
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x0
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t8
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -80
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t5, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xde9c8799
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1551
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xd4561
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xf5bf
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x4fd05
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t5, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s3, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $t5, $zero, 0
addi $t0, $zero, 0
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xdeae934f
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t5
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xd460
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t5
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t5
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t5
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
lw $s3, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t0, 0($sp)
addi $sp, $sp, 4
lw $t5, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s3
lw $s3, 0($sp)
addi $sp, $sp, 4
sw $t7, 76($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t2, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xbbb6f3d9
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t2
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t2
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xed6f6
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t2
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t2
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t2, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t7, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xde9f2203
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xf396a
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t7
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x7a73
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t7
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x155b8
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t7
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x177c3
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t7
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t7, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t9
lw $t9, 0($sp)
addi $sp, $sp, 4
sw $t7, 40($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t6, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xb9bd42e9
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x6989a
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t6
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t6
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t6
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s5, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t8, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xde9c1727
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x49e54
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xf05e3
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xded2
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x11d9d
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $s5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s5
lw $s5, 0($sp)
addi $sp, $sp, 4
sw $t7, 68($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t1, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xb7bf2d15
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x72565
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t1
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x635c
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t1
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x439
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t1
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t1
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s4, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t8, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xdea3b43d
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t8
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x36bd
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t8
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xace53
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t8
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x8ce4
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t8
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $s4, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s4
lw $s4, 0($sp)
addi $sp, $sp, 4
sw $t7, 32($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t3, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xb2c0a633
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t3
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t3
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x849e0
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t3
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x62e
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t3
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s2, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t6, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xdeb05f89
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1402a
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x16070
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t6
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t6
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $s2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s2
lw $s2, 0($sp)
addi $sp, $sp, 4
sw $t7, 4($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t3, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xbbaab378
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xa3ac7
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t3
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x4ae7
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t3
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xc2e34
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t3
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t3
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $v0, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t5, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xdea3c66f
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xc35cb
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xb3c1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x133a0
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x55ea
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t5, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $v0
lw $v0, 0($sp)
addi $sp, $sp, 4
sw $t7, 8($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $t0, $zero, 0
addi $t6, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xacc41dfa
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1eb6a
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
addu $t6, $t6, $t0
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t0
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t0
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x13095
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t0
addi $sp, $sp, -4 
sw $t6, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t6, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s4, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t8, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xdea7c3bd
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1124b
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x7c0c4
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xb347
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t8
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $s4, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s4
lw $s4, 0($sp)
addi $sp, $sp, 4
sw $t7, 44($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $t2, $zero, 0
addi $t6, $zero, 0
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xb8d87e56
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t2
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t2
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x120b
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t2
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x6623b
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
addu $t6, $t6, $t2
addi $sp, $sp, -4 
sw $t6, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t6, 0($sp)
addi $sp, $sp, 4
lw $t2, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t0, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xde937d97
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t0
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xc718c
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t0
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x3eb7
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t0
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xe0e83
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t0
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t6
lw $t6, 0($sp)
addi $sp, $sp, 4
sw $t7, 52($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t0, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xffc946eb
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x10438
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t0
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t0
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t0
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xc9cd8
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t0
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s2, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t0, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xde8bc9b0
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xed250
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t0
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xc207a
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t0
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t0
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x70275
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t0
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $s2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s2
lw $s2, 0($sp)
addi $sp, $sp, 4
sw $t7, 28($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t8, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xb38a4d51
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x540c
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x3d157
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t8
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t8
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t6, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xdeb04466
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t6
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xbe24
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t6
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x710b
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t6
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x15648
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t6
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t1
lw $t1, 0($sp)
addi $sp, $sp, 4
sw $t7, 48($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $t9, $zero, 0
addi $t3, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xdea38a24
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x41566
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t9
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t9
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t9
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t5, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xdea564df
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x10c0b
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t5
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xa44f8
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t5
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xdedd
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t5
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t5
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t5, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t0
lw $t0, 0($sp)
addi $sp, $sp, 4
sw $t7, 72($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t9, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xadc57105
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x62d1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t9
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x87b
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x671d
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s0, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t0, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xdeabbf50
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x2e3fa
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t0
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t0
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xe45b
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t0
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t0
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $s0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s0
lw $s0, 0($sp)
addi $sp, $sp, 4
sw $t7, 36($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t8, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xfed12cb5
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x13419
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t8
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x51704
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t8
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t8
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x4315
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t8
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $v1, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $t9, $zero, 0
addi $t3, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xdeaf5684
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t9
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x11cd7
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x2bc1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x4efd
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
lw $v1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $v1
lw $v1, 0($sp)
addi $sp, $sp, 4
sw $t7, 24($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t3, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xb0cbf97c
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t3
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x110a
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xcc44
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xdc355
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t2, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xde995873
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x8b4ab
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t2
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t2
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xb74a0
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t2
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x3d31
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t2
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t2, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t6
lw $t6, 0($sp)
addi $sp, $sp, 4
sw $t7, 20($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t3, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xfec56d09
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xe76
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x465c8
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1459d
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x57dd
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s7, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t3, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xdea51cff
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t3
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x10372
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t3
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x79e7e
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t3
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t3
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $s7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s7
lw $s7, 0($sp)
addi $sp, $sp, 4
sw $t7, 16($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $t2, $zero, 0
addi $t6, $zero, 0
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xfeb9211b
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t2
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t2
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x7a51
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t2
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xa2405
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
addu $t6, $t6, $t2
addi $sp, $sp, -4 
sw $t6, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t6, 0($sp)
addi $sp, $sp, 4
lw $t2, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s3, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t9, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xdeae22b0
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x57fc
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t9
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xbc5
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t9
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t9
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t9
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $s3, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s3
lw $s3, 0($sp)
addi $sp, $sp, 4
sw $t7, 12($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t4, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xb2b50fa5
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xb3525
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t4
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t4
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x2659
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t4
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xcb81b
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t4
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s4, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t4, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xde997d64
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xebf8c
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t4
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x4dce0
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t4
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xa51f
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t4
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t4
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $s4, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s4
lw $s4, 0($sp)
addi $sp, $sp, 4
sw $t7, 64($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $t9, $zero, 0
addi $t3, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xfed1dcab
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t9
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xfa3d
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x160fc
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xd8e31
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s5, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t8, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xde9ca49f
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t8
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x88423
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x8962d
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t8
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $s5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s5
lw $s5, 0($sp)
addi $sp, $sp, 4
sw $t7, 60($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t8, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xbfc64641
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t8
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x3048
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x48a8
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x86ef9
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t2, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xdeaac9f7
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x15b68
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t2
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x5cf8e
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t2
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x17f2e
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t2
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t2
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t2, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t1
lw $t1, 0($sp)
addi $sp, $sp, 4
sw $t7, 56($sp)
addi $a0, $sp, 4
addi $sp, $sp, 80
lw $t7, 0($sp)
addi $sp, $sp, 4

syscall
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t1, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x20797
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x12a55
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t1
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t1
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xdd3e
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t1
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t1
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -28
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t8, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xfe92501d
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xe878
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x427b4
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x24b44
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t8
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t8
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $v0, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t4, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xdea9a2d5
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x41c1a
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t4
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t4
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t4
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t4
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

xor $t2, $t2, $v0
lw $v0, 0($sp)
addi $sp, $sp, 4
sw $t2, 20($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $t3, $zero, 0
addi $t0, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xbfdfc2df
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x116a2
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t3
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t3
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t3
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x10db3
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t3
addi $sp, $sp, -4 
sw $t0, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t0, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $t7, $zero, 0
addi $t6, $zero, 0
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xdea5dd12
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xa7dbf
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
addu $t6, $t6, $t7
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x1
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t7
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x1589a
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t7
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x14348
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t7
addi $sp, $sp, -4 
sw $t6, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t6, 0($sp)
addi $sp, $sp, 4
lw $t7, 0($sp)
addi $sp, $sp, 4

xor $t2, $t2, $t4
lw $t4, 0($sp)
addi $sp, $sp, 4
sw $t2, 12($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t1, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xbbdbb66a
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t1
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t1
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xad92
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t1
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1382e
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t1
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $v1, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t8, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xdeb02cf7
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xfd77
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t8
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x17091
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t8
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $v1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

xor $t2, $t2, $v1
lw $v1, 0($sp)
addi $sp, $sp, 4
sw $t2, 4($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t6, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xb1cb15d2
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x915c3
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t6
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xfd16
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t6
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xe798
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t6
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x6b785
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t6
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t7, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xdea4f4ab
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x10952
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t7
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xbdca9
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t7
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x10389
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t7
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x1058a
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t7
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t7, 0($sp)
addi $sp, $sp, 4

xor $t2, $t2, $t5
lw $t5, 0($sp)
addi $sp, $sp, 4
sw $t2, 16($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t3, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xde9a25e8
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t3
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x73b82
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t3
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xc5d85
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t3
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t3
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $k0, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t2, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xdea04faa
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t2
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xa215
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t2
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x67b81
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t2
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x795d9
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t2
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $k0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t2, 0($sp)
addi $sp, $sp, 4

xor $t2, $t2, $k0
lw $k0, 0($sp)
addi $sp, $sp, 4
sw $t2, 24($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t5, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xb6c8ec49
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x855fb
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t5
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t5
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x72b97
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t5
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x130c2
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t5
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t5, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t9, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xde9d6916
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t9
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xc6923
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x87fe
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x474b4
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

xor $t2, $t2, $t8
lw $t8, 0($sp)
addi $sp, $sp, 4
sw $t2, 8($sp)
addi $a0, $sp, 4
addi $sp, $sp, 28
lw $t2, 0($sp)
addi $sp, $sp, 4

syscall
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $t0, $zero, 0
addi $t3, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xb417
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xb40f
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t0
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t0
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x0
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t0
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x0
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t0
addi $sp, $sp, -4 
sw $t3, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

la $a0, input
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $t8, $zero, 0
addi $t3, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x13a5e
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1385e
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t8
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x8
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t8
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t8
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x0
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t8
addi $sp, $sp, -4 
sw $t3, 0($sp)
lw $a1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

syscall
la $a0, input
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -52
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t8, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xd4d357cc
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t8
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x52a1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t8
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x14302
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t8
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x13253
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t8
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t7, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xdea014e4
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x374c0
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t7
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xbb0e0
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t7
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x17b95
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t7
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x1
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t7
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t7, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $t0
lw $t0, 0($sp)
addi $sp, $sp, 4
sw $t5, 44($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t4, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xb587019d
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x99ac
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t4
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t4
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xe550c
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t4
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x4d0a0
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t4
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $k1, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t6, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xdea30841
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x17bc4
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t6
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t6
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xc3272
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $k1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $k1
lw $k1, 0($sp)
addi $sp, $sp, 4
sw $t5, 28($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t3, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xbcea0c9d
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x7ada
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x216b
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1b7f5
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x76134
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $k0, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $t0, $zero, 0
addi $t7, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xde9ff4a3
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x5bd0c
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t0
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xa4383
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t0
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x12671
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t0
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x10fd2
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t0
addi $sp, $sp, -4 
sw $t7, 0($sp)
lw $k0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t7, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $k0
lw $k0, 0($sp)
addi $sp, $sp, 4
sw $t5, 24($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $t4, $zero, 0
addi $t6, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xdeaeba3b
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x5fd2
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t4
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x9594
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t4
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t4
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x5e6
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t4
addi $sp, $sp, -4 
sw $t6, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t6, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $t5, $zero, 0
addi $t6, $zero, 0
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xde87aa66
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xe5a3b
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
addu $t6, $t6, $t5
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t5
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xe3d07
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
addu $t6, $t6, $t5
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x97d47
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
addu $t6, $t6, $t5
addi $sp, $sp, -4 
sw $t6, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t6, 0($sp)
addi $sp, $sp, 4
lw $t5, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $t4
lw $t4, 0($sp)
addi $sp, $sp, 4
sw $t5, 48($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $t3, $zero, 0
addi $t7, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xba9f9675
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
div $t7, $t3
mflo $t7
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
div $t7, $t3
mflo $t7
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x17920
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t3
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x142a5
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t3
addi $sp, $sp, -4 
sw $t7, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t7, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $v1, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t6, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xde9f83c5
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x17d7
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t6
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xe5301
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t6
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t6
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t6
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $v1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $v1
lw $v1, 0($sp)
addi $sp, $sp, 4
sw $t5, 20($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t0, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xedb24590
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xf1919
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t0
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t0
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x180e
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t0
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x64c3
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t0
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $t8, $zero, 0
addi $t0, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xdead73af
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t8
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1d76e
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
addu $t0, $t0, $t8
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xb49f
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t8
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xd78f
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t8
addi $sp, $sp, -4 
sw $t0, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t0, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $t2
lw $t2, 0($sp)
addi $sp, $sp, 4
sw $t5, 36($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $t1, $zero, 0
addi $t6, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xb09d5873
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xc9d4
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t1
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t1
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t1
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t1
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t6, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t5, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xde9dde69
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x230d8
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xde9cf
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t5
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x3a21
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t5
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t5, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $t2
lw $t2, 0($sp)
addi $sp, $sp, 4
sw $t5, 32($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t6, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x8ae717c1
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t6
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xc9f1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t6
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1479e
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t6
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x9e589
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t6
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t9, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xde9eada6
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t9
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xf1149
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t9
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t9
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t9
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $t8
lw $t8, 0($sp)
addi $sp, $sp, 4
sw $t5, 4($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t7, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xedde6a07
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x25bf
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t7
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x1
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t7
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x47f9
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t7
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x6dc8
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t7
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t7, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s4, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $t6, $zero, 0
addi $t7, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xdeb0db93
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x13bab
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t6
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
div $t7, $t6
mflo $t7
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x15348
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t6
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x8db1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t6
addi $sp, $sp, -4 
sw $t7, 0($sp)
lw $s4, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t7, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $s4
lw $s4, 0($sp)
addi $sp, $sp, 4
sw $t5, 12($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t9, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xab9512a7
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x666a
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x11b14
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x7855
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xaaedc
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s2, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $t9, $zero, 0
addi $t7, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xdea5bdfc
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xe1ab
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t9
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x8c45
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t9
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x85659
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t9
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
div $t7, $t9
mflo $t7
addi $sp, $sp, -4 
sw $t7, 0($sp)
lw $s2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t7, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $s2
lw $s2, 0($sp)
addi $sp, $sp, 4
sw $t5, 16($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t7, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xec9b76be
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x1
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t7
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xe90e
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t7
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x1
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t7
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x1
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t7
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t7, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s6, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $t2, $zero, 0
addi $t3, $zero, 0
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xde9b1258
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xd093e
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t2
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t2
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x60560
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t2
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x6207
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t2
addi $sp, $sp, -4 
sw $t3, 0($sp)
lw $s6, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t2, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $s6
lw $s6, 0($sp)
addi $sp, $sp, 4
sw $t5, 40($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t3, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x81883957
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xefa24
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x12d5f
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t3
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x6bf8d
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s5, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $t1, $zero, 0
addi $t7, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xdea0c49d
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x32a1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t1
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x3c8d
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t1
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xd6980
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t1
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
div $t7, $t1
mflo $t7
addi $sp, $sp, -4 
sw $t7, 0($sp)
lw $s5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t7, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

xor $t5, $t5, $s5
lw $s5, 0($sp)
addi $sp, $sp, 4
sw $t5, 8($sp)
addi $a1, $sp, 4
addi $sp, $sp, 52
lw $t5, 0($sp)
addi $sp, $sp, 4

jal QaySuEavWA
move $a0, $v0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $t8, $zero, 0
addi $t7, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x10
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
div $t7, $t8
mflo $t7
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x4
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
div $t7, $t8
mflo $t7
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x0
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t8
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x0
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t8
addi $sp, $sp, -4 
sw $t7, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t7, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

beq $a0, $zero, JHxujuMOUf_failure
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -60
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t3, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xde8e7ac0
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xd7394
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t3
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xbb136
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t3
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t3
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t3
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $a2, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t2, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xdeb0af7d
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t2
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x1056e
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t2
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t2, 0x14af3
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t2
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t2, 0xa02d
sw $t2, 0($sp)
lw $t2, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t2
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $a2, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t2, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $a2
lw $a2, 0($sp)
addi $sp, $sp, 4
sw $t7, 52($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t1, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xaa88955e
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t1
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x4fd2f
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t1
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t1
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
div $t4, $t1
mflo $t4
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t3, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xde8ff811
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xe6551
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x426ce
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xa4898
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xf227
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t3
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t6
lw $t6, 0($sp)
addi $sp, $sp, 4
sw $t7, 28($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t0, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xb1b746ca
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xf65e
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t0
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x13563
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t0
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x36bf0
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t0
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x61b6a
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t0
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $k1, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t4, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xdea11e35
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t4
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t4
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t4
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xca0ba
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t4
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $k1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $k1
lw $k1, 0($sp)
addi $sp, $sp, 4
sw $t7, 20($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t9, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xb2c3fc53
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t9
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1601a
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x7d200
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x57e1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $k0, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t8, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xdead2483
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x11522
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t8
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t8
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x7ab6
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $k0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $k0
lw $k0, 0($sp)
addi $sp, $sp, 4
sw $t7, 44($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $t3, $zero, 0
addi $t0, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xb1c8d5ef
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t3
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t3
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x11299
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t3
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x24cb
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t3
addi $sp, $sp, -4 
sw $t0, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t0, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t9, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xdea0d5a6
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t9
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t9
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x11f51
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xe089a
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t9
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t5
lw $t5, 0($sp)
addi $sp, $sp, 4
sw $t7, 24($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t9, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xffc603ce
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x56e05
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xe6eb
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x942f
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1b1e
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $v1, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $t4, $zero, 0
addi $t3, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xde9b6b20
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x969d7
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t4
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t4
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x8e9f8
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t4
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t4
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
lw $v1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $v1
lw $v1, 0($sp)
addi $sp, $sp, 4
sw $t7, 16($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t6, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xb0b88b75
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xe5236
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x62e2b
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x3f4e
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t6
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $t4, $zero, 0
addi $t6, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xdea68286
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t4
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t4
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x7dae9
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
addu $t6, $t6, $t4
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x9e80
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
subu $t6, $t6, $t4
addi $sp, $sp, -4 
sw $t6, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t6, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t0
lw $t0, 0($sp)
addi $sp, $sp, 4
sw $t7, 12($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $t1, $zero, 0
addi $t0, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xfedfd395
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t1
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t1
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x7d57
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t1
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x88b4
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t1
addi $sp, $sp, -4 
sw $t0, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t0, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t8, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xdeacd6c1
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t8
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x24ae4
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t8
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t8
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x162b6
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t8
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t5
lw $t5, 0($sp)
addi $sp, $sp, 4
sw $t7, 8($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t4, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xb0813d96
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x2fdf4
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t4
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t4
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t4
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x99ffd
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t4
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $k1, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $t4, $zero, 0
addi $t9, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xdea970f8
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t4
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x7188
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
subu $t9, $t9, $t4
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x4bf7f
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
addu $t9, $t9, $t4
addi $sp, $sp, -4 
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t9, 0($sp)
addi $sp, $sp, 4 
div $t9, $t4
mflo $t9
addi $sp, $sp, -4 
sw $t9, 0($sp)
lw $k1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t9, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $k1
lw $k1, 0($sp)
addi $sp, $sp, 4
sw $t7, 36($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t8, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xfedb362d
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t8
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xbf03
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t8
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t8
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xb0a0
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t8
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $t9, $zero, 0
addi $t3, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xdea9b43c
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x618a8
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t9
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x17e5b
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x8f9a
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t9
addi $sp, $sp, -4 
sw $t3, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t8
lw $t8, 0($sp)
addi $sp, $sp, 4
sw $t7, 40($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t1, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xb9c11673
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t1
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x386f3
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t1
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x64a0
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t1
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x5d43
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t1
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $t4, $zero, 0
addi $t6, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xdeadbeef
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t4
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t4
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t4
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t6, 0($sp)
addi $sp, $sp, 4 
div $t6, $t4
mflo $t6
addi $sp, $sp, -4 
sw $t6, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t6, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t5
lw $t5, 0($sp)
addi $sp, $sp, 4
sw $t7, 48($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t8, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xaa8127cb
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xdf8ff
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x6e58
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t8
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xead5
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t8
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t7, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xde979f4b
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t7, 0x1
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
div $t5, $t7
mflo $t5
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xc9d11
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t7
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xa47d3
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t7
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t7, 0xc540
sw $t7, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t7
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t7, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $t8
lw $t8, 0($sp)
addi $sp, $sp, 4
sw $t7, 32($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t1, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xbdbee0ee
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x2c43e
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t1
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xcca12
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t1
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x794f
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t1
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x109f6
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t1
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s0, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $t1, $zero, 0
addi $t5, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xde950d82
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xe520f
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t1
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x1ff38
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t1
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x2a70
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
subu $t5, $t5, $t1
addi $sp, $sp, -4 
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x88a96
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t5, 0($sp)
addi $sp, $sp, 4 
addu $t5, $t5, $t1
addi $sp, $sp, -4 
sw $t5, 0($sp)
lw $s0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t5, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s0
lw $s0, 0($sp)
addi $sp, $sp, 4
sw $t7, 4($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t6, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xdea92595
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x7555
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t6
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x323aa
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t6
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x4a03
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t6
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x1a102
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t6
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $t7, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s1, 0($sp)
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $t5, $zero, 0
addi $t0, $zero, 0
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xde937cf4
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
div $t0, $t5
mflo $t0
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xe4670
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
addu $t0, $t0, $t5
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x85df
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t5
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t5, 0xc816a
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
addu $t0, $t0, $t5
addi $sp, $sp, -4 
sw $t0, 0($sp)
lw $s1, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t0, 0($sp)
addi $sp, $sp, 4
lw $t5, 0($sp)
addi $sp, $sp, 4

xor $t7, $t7, $s1
lw $s1, 0($sp)
addi $sp, $sp, 4
sw $t7, 56($sp)
addi $a0, $sp, 4
addi $sp, $sp, 60
lw $t7, 0($sp)
addi $sp, $sp, 4

syscall
j allVKxeQsq
JHxujuMOUf_failure:
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -24
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t0, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xfed6b32e
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x81a5c
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t0
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t0
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t0
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t0
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t0, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xdea1491a
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x4c9ff
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t0
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t0
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x7abd6
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t0
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x1
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
div $t2, $t0
mflo $t2
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

xor $t9, $t9, $t3
lw $t3, 0($sp)
addi $sp, $sp, 4
sw $t9, 8($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $t1, $zero, 0
addi $t0, $zero, 0
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t1, 0xdea1cd74
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x5ab4
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
subu $t0, $t0, $t1
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x472c
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
addu $t0, $t0, $t1
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x30b4d
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
addu $t0, $t0, $t1
addi $sp, $sp, -4 
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t1, 0x8f9b6
sw $t1, 0($sp)
lw $t1, 0($sp)
addi $sp, $sp, 4 
lw $t0, 0($sp)
addi $sp, $sp, 4 
addu $t0, $t0, $t1
addi $sp, $sp, -4 
sw $t0, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t0, 0($sp)
addi $sp, $sp, 4
lw $t1, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $k0, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t4, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xde92ec26
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t4
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xc17b8
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t4
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xf34d6
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
addu $t1, $t1, $t4
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x79c5
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t4
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $k0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

xor $t9, $t9, $k0
lw $k0, 0($sp)
addi $sp, $sp, 4
sw $t9, 20($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $t3, $zero, 0
addi $t1, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xb7c5600e
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t3
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t3
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x1
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
div $t1, $t3
mflo $t1
addi $sp, $sp, -4 
sw $t1, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x18483
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t1, 0($sp)
addi $sp, $sp, 4 
subu $t1, $t1, $t3
addi $sp, $sp, -4 
sw $t1, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t1, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $t0, $zero, 0
addi $t7, $zero, 0
addi $sp, $sp, -4
sw $t0, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xde95ee2d
sw $t0, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x512d5
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t0
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t0, 0xa590d
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t0
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x894cd
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t0
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t0, 0x2fed
sw $t0, 0($sp)
lw $t0, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t0
addi $sp, $sp, -4 
sw $t7, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t7, 0($sp)
addi $sp, $sp, 4
lw $t0, 0($sp)
addi $sp, $sp, 4

xor $t9, $t9, $t5
lw $t5, 0($sp)
addi $sp, $sp, 4
sw $t9, 12($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $t8, $zero, 0
addi $t7, $zero, 0
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xd48c829c
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t8, 0xa366
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t8
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x79b1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
subu $t7, $t7, $t8
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x17505
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
addu $t7, $t7, $t8
addi $sp, $sp, -4 
sw $t7, 0($sp)
addi $sp, $sp, -4 
li $t8, 0x1
sw $t8, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4 
lw $t7, 0($sp)
addi $sp, $sp, 4 
div $t7, $t8
mflo $t7
addi $sp, $sp, -4 
sw $t7, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t7, 0($sp)
addi $sp, $sp, 4
lw $t8, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $t6, $zero, 0
addi $t2, $zero, 0
addi $sp, $sp, -4
sw $t6, 0($sp)
addi $sp, $sp, -4
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xdea4f4f9
sw $t6, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x12db8
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x98278
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0x82b5
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
subu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
addi $sp, $sp, -4 
li $t6, 0xf7eb
sw $t6, 0($sp)
lw $t6, 0($sp)
addi $sp, $sp, 4 
lw $t2, 0($sp)
addi $sp, $sp, 4 
addu $t2, $t2, $t6
addi $sp, $sp, -4 
sw $t2, 0($sp)
lw $t8, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t2, 0($sp)
addi $sp, $sp, 4
lw $t6, 0($sp)
addi $sp, $sp, 4

xor $t9, $t9, $t8
lw $t8, 0($sp)
addi $sp, $sp, 4
sw $t9, 16($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $t4, $zero, 0
addi $t3, $zero, 0
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xbdb77e33
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x1
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
div $t3, $t4
mflo $t3
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t4, 0x16dd5
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
subu $t3, $t3, $t4
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xa816e
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t4
addi $sp, $sp, -4 
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t4, 0xe6e19
sw $t4, 0($sp)
lw $t4, 0($sp)
addi $sp, $sp, 4 
lw $t3, 0($sp)
addi $sp, $sp, 4 
addu $t3, $t3, $t4
addi $sp, $sp, -4 
sw $t3, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t3, 0($sp)
addi $sp, $sp, 4
lw $t4, 0($sp)
addi $sp, $sp, 4

addi $sp, $sp, -4
sw $s4, 0($sp)
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t9, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t9, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xdeafaf2d
sw $t9, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t9
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xf13c
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0xff02
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t9
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t9, 0x1
sw $t9, 0($sp)
lw $t9, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t9
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $s4, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t9, 0($sp)
addi $sp, $sp, 4

xor $t9, $t9, $s4
lw $s4, 0($sp)
addi $sp, $sp, 4
sw $t9, 4($sp)
addi $a0, $sp, 4
addi $sp, $sp, 24
lw $t9, 0($sp)
addi $sp, $sp, 4

syscall
allVKxeQsq:
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $t5, $zero, 0
addi $t8, $zero, 0
addi $sp, $sp, -4
sw $t5, 0($sp)
addi $sp, $sp, -4
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x6865
sw $t5, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x685b
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
subu $t8, $t8, $t5
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x0
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t5
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x0
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
addu $t8, $t8, $t5
addi $sp, $sp, -4 
sw $t8, 0($sp)
addi $sp, $sp, -4 
li $t5, 0x1
sw $t5, 0($sp)
lw $t5, 0($sp)
addi $sp, $sp, 4 
lw $t8, 0($sp)
addi $sp, $sp, 4 
div $t8, $t5
mflo $t8
addi $sp, $sp, -4 
sw $t8, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t8, 0($sp)
addi $sp, $sp, 4
lw $t5, 0($sp)
addi $sp, $sp, 4

syscall
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $t3, $zero, 0
addi $t4, $zero, 0
addi $sp, $sp, -4
sw $t3, 0($sp)
addi $sp, $sp, -4
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x362d9
sw $t3, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x17e89
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xf73
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
addu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0xb30f
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
addi $sp, $sp, -4 
li $t3, 0x140b4
sw $t3, 0($sp)
lw $t3, 0($sp)
addi $sp, $sp, 4 
lw $t4, 0($sp)
addi $sp, $sp, 4 
subu $t4, $t4, $t3
addi $sp, $sp, -4 
sw $t4, 0($sp)
lw $v0, 0($sp)
addi $sp, $sp, 4
addi $sp, $sp, 8
lw $t4, 0($sp)
addi $sp, $sp, 4
lw $t3, 0($sp)
addi $sp, $sp, 4

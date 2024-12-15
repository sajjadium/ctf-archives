#

        .data
inp_msg:    .asciiz "Enter your password: "
input:  .space 25
vals:   .word 46096, 29310, 35786, 34250, 1682, 11703, 61757, 3732, 9259, 35900, 51157, 33143, 711, 15574, 10828, 33537, 40680, 50187, 18386, 31483
finals: .word 13660, 20137, 19784, 1306, 978, 10684, 36366, 1167, 6038, 4071, 28503, 2856, 363, 1268, 7100, 9711, 21216, 17029, 17033, 25654
ok_msg:     .asciiz "Checks out :)"
bad_msg:    .asciiz "Wrong password :("

        .text
        .globl main


op:     
    xori    $v0, $a0, 0x1337
    li      $t0, 0xdead
    mult    $v0, $t0
    mflo	$v0
    srl     $v0, $v0, 4

    la      $t0, vals
    move    $t1, $a1
    sll     $t1, $t1, 2
    add     $t0, $t0, $t1
    lw      $t0, 0($t0)

    div     $v0, $t0
    mfhi	$v0
    jr      $ra


check: 
    move    $s0, $0     
    move    $s1, $a0    
    la      $s2, finals 
loop:
    lb		$t0, 0($s1)	
    li      $t1, 0x0a
    beq     $t0, $t1, end


    addi    $sp, $sp, -4    
    sw      $ra, 0($sp) 

    move    $a0, $t0
    move    $a1, $s0
    jal     op

    lw      $ra, 0($sp)     
    addi    $sp, $sp, 4

    lw      $t1, 0($s2)
    bne     $v0, $t1, end

    addi    $s0, $s0, 1
    addi    $s1, $s1, 1
    addi    $s2, $s2, 4
    j loop

end:
    li      $t0, 20     
    beq     $t0, $s0, return_1
    li      $v0, 0
    jr      $ra
return_1:
    li      $v0, 1
    jr      $ra




main:   
    li		$v0, 4
    la      $a0, inp_msg
    syscall

    li      $v0, 8
    la      $a0, input
    li      $a1, 25
    syscall
    
    addi    $sp, $sp, -4   
    sw      $ra, 0($sp) 

    jal     check
    bne     $v0, $0, correct
    la      $a0, bad_msg
    j       exit
correct:
    la      $a0, ok_msg
exit:
    li      $v0, 4
    syscall
    lw      $ra, 0($sp)     
    addi    $sp, $sp, 4
    jr      $ra

main:
  li a0, 0

loop:
  beq a2, zero, end
  add a0, a1, a0
  addi a2, a2, -1
  j loop

end:
  nop

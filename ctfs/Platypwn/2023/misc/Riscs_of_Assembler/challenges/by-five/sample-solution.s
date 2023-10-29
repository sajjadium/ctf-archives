main:
  li a2, 5
  blt zero, a0, loop
  sub a0, zero, a0

loop:
  bgt a2, a0, end
  sub a0, a0, a2
  jal zero, loop



end:
  beq a0, zero, keepresult
  li a0, 1
keepresult:
  nop

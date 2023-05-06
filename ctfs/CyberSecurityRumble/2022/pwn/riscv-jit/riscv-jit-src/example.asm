# Put string at address 4
j 1f
.ascii "Hello World\n"

# Write
1:
li a0, 4
li a1, 12
li a7, 2
ecall

# Exit
li a7, 0
ecall

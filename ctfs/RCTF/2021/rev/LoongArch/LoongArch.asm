ld.d t0,sp,0 
ld.d t1,sp,8 
ld.d t2,sp,16 
ld.d t3,sp,24
ld.d t4,sp,32
ld.d t5,sp,40
ld.d t6,sp,48
ld.d t7,sp,56

xor t0,t0,t4
xor t1,t1,t5
xor t2,t2,t6
xor t3,t3,t7

bitrev.d t4,t0
bitrev.d t5,t1
bitrev.d t6,t2
bitrev.d t7,t3

bytepick.d t0,t6,t5,3
bytepick.d t1,t4,t7,3
bytepick.d t2,t5,t4,3
bytepick.d t3,t7,t6,3

bitrev.8b t4,t0
bitrev.8b t5,t1
bitrev.8b t6,t2
bitrev.8b t7,t3

ld.d t0,sp,64 
ld.d t1,sp,72
ld.d t2,sp,80 
ld.d t3,sp,88

xor t0,t0,t4
xor t1,t1,t5
xor t2,t2,t6
xor t3,t3,t7

addi.d a0,zero,1
addi.d a1,sp,32
li.d a2,64
li.d a7,64
syscall 0

li.d t4,64
clo.d t5,t0
bne t5,t4,fail
clo.d t5,t1
bne t5,t4,fail
clo.d t5,t2
bne t5,t4,fail
clo.d t5,t3
bne t5,t4,fail
b success

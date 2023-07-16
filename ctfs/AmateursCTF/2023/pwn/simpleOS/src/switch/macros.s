.ifndef _MACRO_S_
.equ    _MACRO_S_, 1

.macro outb port, byte
    mov   dx,   \port
    mov   al,   \byte
    out   dx,   al
.endm

.macro inb port
    mov   dx,   \port
    in    al,   dx
.endm

.endif
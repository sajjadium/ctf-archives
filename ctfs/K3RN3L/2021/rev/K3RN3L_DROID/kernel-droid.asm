extern puts
extern exit
extern gets
extern strlen
extern printf

section .text
global _start


; ----------> K3RN3L DR0ID v0.1 <----------
_start:
    push 0xD3ADC0DE
    jb 0x004010ed
    ;je l1 + 1
    ;je l2
    jmp label1
    push rax
    mov rax, 0xCAFEBABE
    cmp rax, 0x0000000F
    je label2
    jmp label4
    jmp 0xCAFEBABE
    


label1:
    push rdi
    push r8
    mov r8, 0x9418561
    cmp r8, 0x9401586
    jne label2
    push r9
    mov r9, 0x000000A
    sub r9, r8
    jmp label4
    ret
    jmp 0xDEADC0DE

label2:
    jmp label3
    push r8
    mov r8, 0xFFFFFF
    jmp r8

label3:
    lea rdi, [welcomeMessage]
    call puts
    jmp label4

label4:
    lea rdi, [pinCode]
    call gets
    mov rdi, rax
    call strlen
    cmp rax, 0x8
    jne invalid_pin_length 
    je label5
    jmp end

label5:
    push rcx
    push 0x5
    mov rax, 0x5
    mov rcx, rax
    pop rax
    push r9
    mov r9, rcx
    pop rcx
    mov r9b, [pinCode + 0x0]
    cmp r9b, 0x30
    jne invalid_pin
    cmp r9b, 0x31
    je invalid_pin
    cmp r9b, 0x32
    je invalid_pin
    cmp r9b, 0x35
    je invalid_pin
    push 0xFFFFFFF
    mov r9b, [pinCode + 0x1]
    cmp r9b, 0x34
    jne invalid_pin
    nop
    mov r9b, [pinCode + 0x2]
    cmp r9b, 0x37
    jg invalid_pin
    cmp r9b, 0x30
    jne invalid_pin
    mov r9b, [pinCode + 0x3]
    cmp r9b, 0x39
    je invalid_pin
    cmp r9b, 0x30
    jne invalid_pin
    push r8
    pop r9
    mov r8b, [pinCode + 0x4]
    cmp r8b, 0x31
    jb invalid_pin
    cmp r8b, 0x32
    jge invalid_pin
    xor r8, r8
    mov r8b, [pinCode + 0x5]
    cmp r8b, 0x30
    jbe invalid_pin
    cmp r8b, 0x32
    jae invalid_pin
    push rcx
    mov r8, rcx
    mov r8b, [pinCode + 0x6]
    cmp r8b, 0x39
    jne invalid_pin
    mov r8b, [pinCode + 0x7]
    cmp r8b, 0x36
    jl invalid_pin
    cmp r8b, 0x36
    jg invalid_pin
    jmp valid_pin

label7:
    jmp valid_pin

label6:
    push rax
    push rcx
    mov rax, 5
    mov rcx, 4
    imul rax
    pop rcx
    mov r8, rax
    pop rax
    pop rcx
    jmp invalid_pin

l1:
    db 0xe8
    xor rax, rax
    ret
    nop
    nop
    xor rax, rax
    je l2 + 1
    jne l2 + 0xCAFEBABE

l2:
    db 0xe9
    pop rax
    ret

invalid_pin_length:
    push rdi
    lea rdi, [invalidPinLengthMessage]
    call puts
    jmp end

invalid_pin:
    lea rdi, [invalidPinMessage]
    call puts
    jmp end

valid_pin:
    lea rdi, [validPinMessage]
    lea rsi, [pinCode]
    call printf
    lea rsi, [newLine]
    call puts
    jmp end

end:
    mov rdi, 0x0
    call exit

section .data
    welcomeMessage db "Welcome in KernelDroid, please input your PIN code to enter into phone", 0
    invalidPinLengthMessage db "I'm sorry your pin is not valid, at least it should be 8 (0-9) numbers length for example. 123456789", 0
    invalidPinMessage db "This is not valid PIN!", 0
    validPinMessage db "Great, your flag flag{K3RN3L_DR0ID_%s}", 0
    pinCode db "", 0
    toString db "%s", 0
    newLine db 10

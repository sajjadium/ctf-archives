_TEXT    SEGMENT
extrn socket : proc
extrn connect : proc
extrn puts : proc

PUBLIC DoTCPCheck

signature db "BEARS"

DoSpecialCheck PROC
pop rdi
lea rcx, blocked_msg
jmp puts
DoSpecialCheck ENDP

blocked_msg db "Checking of port 28928 is disabled", 10, 0

; ALIGN 16 ; note: removed function alignment, just a waste of space

DoTCPCheck PROC EXPORT
; run special case for port 28928
; TODO: why do we have this special case?
; TODO: why did we even implement any of this in assembly?
; TODO: why is this function in the executable's export table too?
push rdi
movzx rdi, word ptr [rcx+2]
cmp rdi, 71h
jz DoSpecialCheck

; create socket
sub rsp, 20h
mov rdi, rdx
mov ecx, 2 ; AF_INET
mov edx, 1 ; SOCK_STREAM
xor r8d, r8d
call socket
cmp rax, -1
jz failed

; connect to socket
mov rcx, rax
mov rdx, rdi
mov r8, 16 ; sizeof(sockaddr_in)
call connect
test eax, eax
jnz failed

; if we connected, we succeeded
mov eax, 1
jmp done

failed:
xor eax, eax
done:
add rsp, 20h
pop rdi
ret

DoTCPCheck ENDP

; TODO: Previous developer left this code here, we should probably delete it?
add rcx, 20h
push rdi
call qword ptr [rcx+30h]
pop rdi
ret

_TEXT    ENDS

END

The door to the ground station's main control room is closed, but we found an old disabled GMS-06 defense droid. It seems it was being worked on when the bombs fell. There's still a USB key attached to it with a DFSec logo on it. We managed to read the key: it seems to be some kind of memory dump from the droid. Maybe we can use it to retrieve the entrance code to the station's control room.
jmp .up
.down:
pop eax
push 0xD68C67D9
call eax
push 0x1154286C
call eax
push 0x1B1A1E19
call eax
push 0x161B2D02
call eax
push 0x1A372608
call eax
push 0x2917094C
call eax
mov eax, 4
mov ebx, 1
mov ecx, esp
mov edx, 0x18
int 0x80
mov eax, 1
dec ebx
int 0x80
.up: call .down
xor [esp+4], ebx
mov ebx, [esp+4]
ret

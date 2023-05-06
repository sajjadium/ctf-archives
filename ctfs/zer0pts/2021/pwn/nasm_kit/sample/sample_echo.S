;; Entry Point
main:
  ; mmap(0xdead0000, 0x1000, ...)
  xor r9d, r9d
  mov r8d, -1
  mov r10d, 0x22
  mov edx, 3
  mov esi, 0x1000
  mov rdi, 0xdead0000
  mov eax, 9
  syscall
  test eax, eax
  jnz MapError
;; Echo Loop
MainLoop:
  ; read
  mov edx, 0x400
  mov rsi, 0xdead0000
  mov edi, 0
  mov eax, 0
  syscall
  ; empty?
  mov rax, 0xdead0000
  mov al, [rax]
  sub al, 0x0A
  jz LoopBreak
  ; strlen
  mov rdi, 0xdead0000
  call strlen
  ; write
  mov edx, eax
  mov rsi, 0xdead0000
  mov edi, 1
  mov eax, 1
  syscall
  jmp MainLoop
LoopBreak:
;; Cleanup
  ; munmap(0xdead0000, 0x1000)
  mov esi, 0x1000
  mov rdi, 0xdead0000
  mov eax, 11
  syscall
  ; print "good bye!"
  mov edx, 10
  mov rsi, msgBye
  mov edi, 1
  mov eax, 1
  syscall
  ; exit(0)
  mov rdi, 0
  mov rax, 60
  syscall

strlen:
  xor ecx, ecx
  not ecx
  xor eax, eax
  cld
  repne scasb
  neg ecx
  dec ecx
  dec ecx
  mov eax, ecx
  ret

MapError:
  ; print "mmap failed!"
  mov edx, 13
  mov esi, msgError
  mov edi, 1
  mov eax, 1
  syscall
  ; exit(1)
  mov edi, 1
  mov eax, 60
  syscall

msgError: db "mmap failed!", 0x0A
msgBye: db "good bye!", 0x0A

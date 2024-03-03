BITS 64
; -------------------------------------------------------
; STATIC VARIABLES

section .rdata

; //// [Banner messages] ////
main_message db 10,"Cuttin'String, the smallest string cutting tool",10,"-----------------------------------------------",10, 0
len_str_message db "Enter the length of the string (in decimal) > ", 0
inp_str_message db "Enter the string to cut > ", 0
delimiter_message db 10,10,"---",10,0

; //// [Error messages] ////
error_msg_not_int db "Error. Enter a number in decimal.",10,0

; -------------------------------------------------------
; ASM CODE :)

section .text
global _start

; //// [Utils] ////

; @Type: Macro
; Prepare sys_read syscall
__LOAD_SYS_READ:
	xor rax, rax
	ret

; @Type: Macro
; Prepare sys_write syscall
__LOAD_SYS_WRITE:
	xor rax, rax
	mov rdi, 1
	inc al
	ret

; @Type: Function
; @Quick: _PUTS(str*, len=0)
; @Desc: Print the given string in stdout
; 		 If len is not 0, display len bytes of str
; 		 Else, it continues until reaching a null-byte
_PUTS:
	; Setup stack frame
	push rbp
	mov rbp, rsp

	; Get the arguments
	mov rsi, [rsp+24] ; ptr*
	mov rdx, [rsp+16] ; len

	; Check if len parameter is passed
	test rdx, rdx
	jne skip_determine_len

find_null_byte_index:
	mov al, rsi[rdx]
	inc rdx
	cmp al, 0
	jne find_null_byte_index

skip_determine_len:
	; PRINT the string
	call __LOAD_SYS_WRITE
	dec rdx
	syscall
	leave
	ret

; @Type: Function
; @Quick: _read_and_print_str(len)
; @Desc: Read str from stdin and print the len first bytes to stdout
_read_and_print_str:
	; Setup stack frame
	push rbp
	mov rbp, rsp

	; Get len argument
	mov r10, [rsp+16] ; len

	; Allocate stack buffer of 512 bytes
	sub rsp, 512

	; Read 0x512 bytes from stdin
	call __LOAD_SYS_READ
	xor rdi, rdi
	mov rsi, rsp
	mov rdx, 0x512
	syscall

	; Print the string cutted
	push rsi ; Str
	push r10 ; len
	call _PUTS
	add rsp, 8

	; Return from function
	leave
	ret

; @Type: Function
; @Quick: _get_len_str(void) -> len:r10
; @Desc: Reads decimal from stdin and convert it to usable number.
_get_len_str:
	; Setup stack frame
	push rbp
	mov rbp, rsp

	; Allocate 8 bytes buffer
	sub rsp, 8

	; Read 8 bytes from stdin
	call __LOAD_SYS_READ
	xor rdi, rdi
	mov rsi, rsp
	mov rdx, 8
	syscall

	; Prepare str to int
	xor r10, r10	; Reset output
	xor rcx, rcx 	; Reset counter

	; Perform str to int by looping through each digit
loop_over_digits:
	xor rax, rax 	; Reset local output
	mov al, rsp[rcx] ; Read read char from str

	; IF char == null_byte
	cmp al, 0
	je end_loop_number

	; IF char == new_line
	cmp al, 10
	je end_loop_number

	; IF char < "0"
	cmp al, '0'
	jb _error_not_int

	; IF char > "9"
	cmp al, '9'
	ja _error_not_int

	; IF its the units digit, dont multiply by ten before adding
	test rcx, rcx
	je skip_mul

	; Multiply the result by ten
	imul r10, r10, 10

skip_mul:
	; Digit ascii value to actual value
	sub rax, '0'
	; Add digit to result
	add r10, rax

	; Continue looping through the digits until reaching the end
	inc rcx
	cmp rcx, 8
	jne loop_over_digits

end_loop_number:
	; Clean 8 bytes buffer
	add rsp, 8
	; Clean stackframe and return
	leave
	ret

; @Type: Function
; @Quick: _main_loop(void)
; @Desc: Perform all the program operations
_main_loop:
	; Setup stack frame
	push rbp
	mov rbp, rsp

	; Display the length input message
	lea rax,[rel len_str_message]
	push rax
	push 0
	call _PUTS
	add rsp, 16
	
	; Read length from stdin in decimal
	call _get_len_str
	; Add 1 to result because of later calculations
	add r10, 1

	; Display the string input message
	lea rax,[rel inp_str_message]
	push rax
	push 0
	call _PUTS
	add rsp, 16

	; Read str from stdin and print it
	push r10
	call _read_and_print_str
	add rsp, 8

	; Display the delimiter
	lea rax,[rel delimiter_message]
	push rax
	push 0
	call _PUTS
	add rsp, 16

	leave
	ret

; //// [Program] ////

_start:
	; Display banner message
	lea rax,[rel main_message]
	push rax
	push 0
	call _PUTS
	add rsp, 16

	mov rbp, rsp
__main_loop:
	call _main_loop
	jmp __main_loop

; //// [Error Handlers] ////

; @Type: ERROR_HANDLER
; @Quick: _error_not_int(void)
; @Raise_condition: When converting str to int, if a character is not a digit.
_error_not_int:
	; PUTS error_msg_not_int
	lea rax,[rel error_msg_not_int]
	push rax
	push 0
	call _PUTS
	add rsp, 8

	; SYS_EXIT(0)
	xor edi, edi
	mov rax, 0x3c
	syscall
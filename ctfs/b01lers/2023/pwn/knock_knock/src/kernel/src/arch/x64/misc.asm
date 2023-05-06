%include "asm_def.asm"

global asm_gs_addr

asm_gs_addr:
	swapgs
	mov rax, [gs:gs_data.self_addr]
	swapgs
	ret
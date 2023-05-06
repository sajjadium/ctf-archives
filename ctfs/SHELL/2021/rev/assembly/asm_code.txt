fun1:
	<+0>:	push   ebp
	<+1>:	mov    ebp,esp
	<+3>:	sub    esp,0x10
	<+6>:	mov    eax,DWORD PTR [ebp+0xc]
	<+9>:	mov    DWORD PTR [ebp-0x4],eax
	<+12>:	mov    eax,DWORD PTR [ebp+0x8]
	<+15>:	mov    DWORD PTR [ebp-0x8],eax
	<+18>:	jmp    <fun1+28>
	<+20>:	add    DWORD PTR [ebp-0x4],0x7
	<+24>:	add    DWORD PTR [ebp-0x8],0x70
	<+28>:	cmp    DWORD PTR [ebp-0x8],0x227
	<+35>:	jle    <fun1+20>
	<+37>:	mov    eax,DWORD PTR [ebp-0x4]
	<+40>:	leave  
	<+41>:	ret  

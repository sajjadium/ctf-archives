; build.depend initfs/initfs.bin

; first argument is name, second argument is path
%macro incres 2
global %1
global %1 %+ _len
%1:
	incbin %2
%1 %+ _len	equ	$ - %1
%endmacro

section .resources
; incres initfs, "../initrd/initfs/initfs.bin"

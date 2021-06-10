Hey, our agent extracted some useful files while installing the backdoor.
disk: the laptop hdd
OVMF.fd: firmware extracted from the laptop
System.map, vmlinux: debug symbols for the kernel, there seem to be no changes from upstream source
VariableRuntimeDxe.debug: I don't know what this is, but I think it's important for the backdoor

The agent also send me some commands, but I have no idea what this means:
target remote :1234
add-symbol-file vmlinux 
add-symbol-file VariableRuntimeDxe.debug 0xfffffffeffac9000


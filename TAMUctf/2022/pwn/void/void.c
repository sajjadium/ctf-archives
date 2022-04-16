void main() {
    asm
    (
        "mov $0, %rax;"
        "mov $0, %rdi;"
        "mov %rsp, %rsi;"
        "mov $2000, %rdx;"
        "syscall;"
    );
}

int _start() {
	main();
    asm(
    	"mov $60, %rax;"
    	"mov $0, %rdi;"
    	"syscall;"
    );
}
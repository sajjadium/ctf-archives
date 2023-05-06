#include <stdio.h>
#include <unistd.h>
void init(){
    // Set stdin/stdout unbuffered
    // So folks would not have io(input/output) issues
    fclose(stderr);
    setvbuf(stdin,  0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
}
int main(){
    init();
    // A buffer is created to store your shellcode
    char buf[0x100]; 
    puts("Enter your shellcode: ");
    read(0, buf, 0x100);
    // A functioner point is defined and points to the buffer.
    void (* p )(); 
    p = (void (*)()) buf;
    // Let's run the shellcode
    p();
    return 0;
}

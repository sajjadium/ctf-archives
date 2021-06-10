#include <stdlib.h>
#include <unistd.h>

int main(void){
    setuid(0);
    system("cat /root/flag.txt");

    return 0;
}

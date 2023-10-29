#include <stdlib.h>
#include <stdio.h>

void init(){
    setvbuf(stdin,NULL,_IONBF,0);
    setvbuf(stdout,NULL,_IONBF,0);
    setvbuf(stderr,NULL,_IONBF,0);
}

void win(){
    system("cat flag.txt");
}

int main(){
    init();
    char buffer[64];
    buffer[64]=69;
    fgets(buffer, 65, stdin);
    if (buffer[64] != 69){
        win();
    }
    return 0;
}

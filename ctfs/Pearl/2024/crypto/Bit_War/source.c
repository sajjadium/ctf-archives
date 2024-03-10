#include <stdio.h>
#include <stdlib.h>
int main(){
    char str[100];
    int length = 8;
    int rounds = 1000;
    char * end;
    unsigned int buffer = 0;
    unsigned int bufferMask = 0xff;
    unsigned int leftMask = 0x80;
    unsigned int rightMask = 0x1;
    while(scanf("%s", str)){
        buffer = strtol(str, &end, 2);
        unsigned int input = buffer;
        for(int i = 0; i < rounds; i++){
            unsigned int new = ((buffer & leftMask) >> 7) ^ (buffer & rightMask);
            buffer = ((buffer << 1) & bufferMask) ^ new;
        }
        int inputBits[length];
        int bufferBits[length];
        int i = length;
        while(i){
            if(input & 0x1) inputBits[i-1] = 1;
            else inputBits[i-1] = 0;
            if(buffer & 0x1) bufferBits[i-1] = 1;
            else bufferBits[i-1] = 0;
            input = input >> 1;
            buffer = buffer >> 1;
            i--; 
        }
        for(int i = 0; i < length; i++){
            printf("%d", bufferBits[i]);
        }
        printf(" ");
    }   
}

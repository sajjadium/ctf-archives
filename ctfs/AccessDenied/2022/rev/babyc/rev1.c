#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define MAXSIZE 100
char flag[] = {-111, -47, -47, -79, -39, -39, 49, -79, 97, -127, -79, 49, -55, 9, 27, 89, -19, 59, 97, 49, -19, 89, -37, 121, -37, 89, -69, -37, -19, -111, 89, -37, -19, 113, -71, 97, -19, -101, 49, 49, 11, 91, -69, 11, -79, -87};

char reverse(char ch) {
    int x = 0;
    for(int i = 0; i < 8; i++) {
        x *= 2;
        if((ch & (1 << i))) {
            x++;
        }
    }
    return (char)x;
}

void encode(char str[]) {
    int xor = 23;
    for(int i = 0; str[i] != '\0'; i++) {
        str[i] = reverse(str[i]);
        str[i] = (char)(xor ^ str[i]);
    }
}

int main()
{
    
    char str[MAXSIZE];
    scanf("%100s", str);

    getchar();
    encode(str);
    if(strcmp(flag, str) == 0){
        printf("Access Granted :(");
    }
    else{
        printf("Access Denied :)");
    }
}
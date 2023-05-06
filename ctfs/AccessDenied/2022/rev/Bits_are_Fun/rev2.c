#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define MAXSIZE 100

char flag[] = {105, 97, 103, 115, 113, 102, 103, 100, 97, 111, 108, 113, 100, 59, 108, 118, 119, 112, 26, 118, 52, 116, 49, 117, 54, 78, 100, 127, 112, 27, 103, 96, 118, 125, 112, 26, 118, 52, 116, 49, 53, 119, 52, 90, 49, 119, 98, 30, 120, 100, 119, 53, 75, 52, 49, 97, 102, 103, 54, 117, 97};

void left_rotate_and_right_rotate(char str[]) {
    int len = strlen(str);
    for(int i = 0; i < 8; i++) {
        if((i & 1)) {
            int store = ((((1 << i) & str[len - 1]) > 0) ? 1 : 0);
            for(int j = len - 2; j >= 0; j--) {
                int bit = ((((1 << i) & str[j]) > 0) ? 1 : 0);
                str[j + 1] &= (~(1 << i));
                str[j + 1] |= (1 << i) * bit;
            }
            str[0] &= (~(1 << i));
            str[0] |= (1 << i) * store;
        }
        else {
            int store = ((((1 << i) & str[0]) > 0) ? 1 : 0);
            for(int j = 1; j < len; j++) {
                int bit = ((((1 << i) & str[j]) > 0) ? 1 : 0);
                str[j - 1] &= (~(1 << i));
                str[j - 1] |= (1 << i) * bit;
            }
            str[len - 1] &= (~(1 << i));
            str[len - 1] |= (1 << i) * store;
        }
    }
}

int main()
{
    
    char str[MAXSIZE];
    scanf("%100s", str);

    getchar();
    left_rotate_and_right_rotate(str);
    if(strcmp(str, flag) == 0){
        printf("Access Granted :(");
    }
    else{
        printf("Access Denied :)");
    }
}
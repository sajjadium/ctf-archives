#include"stdio.h"
#include"stdlib.h"
#include"string.h"
int main(){
    char c[50];
    int a[50]={44, 48, 50, 59, 59, 3, 16, 12, 12, 8, 11, 66, 87, 87, 15, 15, 15, 86, 1, 23, 13, 12, 13, 26, 29, 86, 27, 23, 21, 87, 15, 25, 12, 27, 16, 71, 14, 69, 75, 32, 59, 46, 53, 75, 63, 75, 8, 22, 11, 5};
    scanf("%s", c);
    for(int i=0;i<50;i++){
        if (((int)c[i]^120)!=a[i]){
            printf("Password Incorrect!!!\n");
            return 0;
        }
    }
    printf("Password Correct!!!\n");
    return 0;
}
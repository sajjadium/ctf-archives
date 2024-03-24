#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
        char commandStr[32];
        scanf("%s", commandStr);
        int i;
        const char * bTexts[6] = {"ls", "cat", "cd", "pwd", "less"};
        int bTexts_size = (sizeof(bTexts) - 1) / sizeof(bTexts[0]);
        if (strlen(commandStr) <= 5){
                for(i = 0; i < bTexts_size; i++){
                        if(strstr(commandStr, (char*)(bTexts[i])) != 0){
                                printf("Terminating... a violation occured!\n");
                                exit(1);
                        }
                }
                system(commandStr);
        }
        else{
                printf("Terminating... a violation occured!\n");
                exit(2);
        }
        return 0;
}
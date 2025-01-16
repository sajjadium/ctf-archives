#include <string.h>
#include <iostream>
#include <stdio.h>
using namespace std;

void jackpot() {
    char flag[50];
    FILE *f = fopen("/home/gamble/flag.txt", "r");
    if (f == NULL) {
        printf("錯誤：找不到 flag 檔案\n");
        return;
    }
    fgets(flag, 50, f);
    fclose(f);
    
    printf("恭喜你中了 777 大獎！\n");
    printf("Flag 是：%s", flag); 
}

struct GameState {
   char buffer[20];
   char jackpot_value[4];  
} game;

void spin() {
   strcpy(game.jackpot_value, "6A6");
   
   printf("輸入你的投注金額：");
   gets(game.buffer);

   printf("這次的結果為：%s\n", game.jackpot_value);

   if (strcmp(game.jackpot_value, "777") == 0) {
       jackpot();
   } else {
       printf("很遺憾，你沒中獎，再試一次吧！\n");
   }
}

int main() {
   setvbuf(stdout, NULL, _IONBF, 0);
   setvbuf(stdin, NULL, _IONBF, 0);
   printf("歡迎來到拉霸機！試著獲得 777 大獎吧！\n");
   spin();
   return 0;
}
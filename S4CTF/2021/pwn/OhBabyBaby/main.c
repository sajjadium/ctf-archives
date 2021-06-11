#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void waitForFun()
{
    int i, j, ms = 250;    
    const char *a = "|/-\\";
    time_t start, now;
    struct timespec delay;
    delay.tv_sec = 0;
    delay.tv_nsec = ms * 1000000L;
    printf("\033[?25l");  
    time(&start);
    int loop = 3;
    while(loop > 0) {
        loop--;
        for (i = 0; i < 4; i++) {
            printf("\r");        
            for (j = 0; j < 100; j++) {  
                printf("%c", a[i]);
            }
            fflush(stdout);
            nanosleep(&delay, NULL);
        }
        time(&now);
        if (difftime(now, start) >= 20) break;
        printf("\033[?25h"); 
    }
    return;
}
void ultimatePrize() {
    char buf[100];
    printf("\e[0;32m");
    FILE *fp;
    if((fp = fopen("./flag.txt", "r")) == NULL) {
        printf("%s\n", "oh no :(");
        exit(1);
    }
    fgets(buf, 100, fp);
    printf("%s\n", buf);
    fclose(fp);
    exit(0);
}

void prize() {
    char buffer[64];
    printf("\033[0;31m");
    printf("\r\r...........................................%p...........................................\n\n", *ultimatePrize);
    printf("\033[0m");
    printf("............................................Did you enjoy?..........................................\n\n");
    gets(buffer);
}

int main(int argc, char** argv) {
    printf("\e[1;92m");
    printf(" .----------------.  .----------------.  .----------------.  .----------------.  .----------------.\n");
    printf("| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |\n");
    printf("| |    _______   | || |   _    _     | || |     ______   | || |  _________   | || |  _________   | |\n");
    printf("| |   /  ___  |  | || |  | |  | |    | || |   .' ___  |  | || | |  _   _  |  | || | |_   ___  |  | |\n");
    printf("| |  |  (__ \\_|  | || |  | |__| |_   | || |  / .'   \\_|  | || | |_/ | | \\_|  | || |   | |_  \\_|  | |\n");
    printf("| |   '.___`-.   | || |  |____   _|  | || |  | |         | || |     | |      | || |   |  _|      | |\n");
    printf("| |  |`\\____) |  | || |      _| |_   | || |  \\ `.___.'\\  | || |    _| |_     | || |  _| |_       | |\n");
    printf("| |  |_______.'  | || |     |_____|  | || |   `._____.'  | || |   |_____|    | || | |_____|      | |\n");
    printf("| |              | || |              | || |              | || |              | || |              | |\n");  
    printf("| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |\n");
    printf("'----------------'  '----------------'  '----------------'  '----------------'  '----------------' \n" );
    printf("\033[0m");
    printf(".....................................Tap Tap to see your prize!!....................................\n");
    char tap; 
    scanf("%c",&tap);
    scanf("%c",&tap);
    waitForFun();
    prize();
  return 0;
}

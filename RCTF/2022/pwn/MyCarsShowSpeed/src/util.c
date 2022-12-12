#include "util.h"
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>


int getRandom(int max)
{
    static time_t lastTime, init;
    time_t curTime;
    int val;

    if(init)
        curTime = time(NULL);
    else
    {
        curTime = time(NULL);
        init = 1;
    }
    if(curTime == lastTime)
        curTime = rand() % (curTime - 100) + rand() % 100;
    else
        lastTime = curTime;
    
    srand(curTime);
    val = (rand() % max) + 1;
    return val;
}


int isSlip(int probability)
{
    int val = getRandom(100);
    if(val <= probability)
    {
        return 1;
    }
    
    return 0;
}

#ifdef TEST
int main()
{
    int cnt = 1;
    int Y=0, N=0;
    for (int k = 0; k < 10; k++)
    {
        while(cnt <= 100)
        {
            int res = isSlip(30);
            if(res)
                ++N;
            else
                ++Y;

            cnt++;
        }

        printf("\tY=%d, N=%d\n", Y, N);
        Y = N = 0;
        cnt = 1;

    }

}
#endif
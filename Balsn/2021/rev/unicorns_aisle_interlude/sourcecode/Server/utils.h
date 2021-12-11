#ifndef __UTILS_HEADER__
#define __UTILS_HEADER__

#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<fcntl.h>

#define MIN(x,y) (x>y?x:y)

void printError(char *msg);
size_t getRand(int width);

#endif

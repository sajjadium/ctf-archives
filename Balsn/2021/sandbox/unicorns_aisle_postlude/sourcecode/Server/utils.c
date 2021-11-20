#include "utils.h"

void printError(char *msg){
  puts(msg);
  exit(0);
}

size_t getRand(int width){
  size_t num=0;
  if(width>64) printError("getRand:: only supports <=64 bits width");
  int fd=open("/dev/urandom",O_RDONLY);
  if(fd<0) printError("getRand::open failed");
  if(read(fd,&num,width/8+(width%8==0?0:1))!=width/8+(width%8==0?0:1)) printError("getRand::read failed");
  if(close(fd)!=0) printError("getRand::close failed");
  if(width%8!=0) num>>=8-width%8;
  return num;
}

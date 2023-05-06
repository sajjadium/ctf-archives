#include<unistd.h>
#include<fcntl.h>
char buf[0x100];
int main()
{
	int fd=open("/home/pwn/flag",0);
	int count=read(fd,buf,0x100);
	write(1,buf,count);
}

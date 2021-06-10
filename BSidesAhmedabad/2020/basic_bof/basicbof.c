#include<unistd.h>

int main()
{
	char buf[0x80];
	read(0,buf,0x150);
}

#include<unistd.h>
int main(int a,char** b){
	execve(b[2],NULL,NULL);
}

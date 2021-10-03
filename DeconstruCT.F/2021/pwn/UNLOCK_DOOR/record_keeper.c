#include<stdio.h>
#include<string.h>

void get_record() {
	printf("Enter record:");
	char record[128] = "";
	gets(record);
}

int main(int argc,char **argv) {
	get_record();
}

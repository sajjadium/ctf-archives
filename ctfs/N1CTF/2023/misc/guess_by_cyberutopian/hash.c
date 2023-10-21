#include "stdlib.h"
int hash1(const char* str){
	int res=0;
	while(*str){
		res+=*str;
		res*=42;
		++str;
	}
	return res;
}
int hash2(const char* str){
	int res=0;
	while(*str){
		res^=*str;
		res<<=1;
		++str;
	}
	return res;
}
const char* GETFLAG(){
	return getenv("TMPFLAG");
}

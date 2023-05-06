#pragma once
#include "Account.h"
#include <stdexcept>
#include <cstring>
using namespace std;

class Advertisement : public Account {
	
public:
	char ad_text[0xf00];
    char advertisers_directory[0x100] = "advertisements/";
	string ad_type;
	Advertisement(string ad_type);
	bool ChangeAdType(string ad_type);
	bool IsAdTypeValid(string ad_type);
	string GetAdType();
	string GetAdText();
};
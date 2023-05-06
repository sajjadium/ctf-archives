#pragma once
#include "Account.h"
#include "AdEnabledAccount.h"

#include <string>
using namespace std;

class Business : public AdEnabledAccount {
private:
	string address;
public:
	Business(string name, string address, string status, string ad_type);
	string GetStatus();
	string GetAddress();
};
#pragma once
#include "AdEnabledAccount.h"
#include "Account.h"

class User : public AdEnabledAccount {
private:
	unsigned int age;
	string gender;
	string location;

public:
	User(string name, string location, unsigned int age, string gender, string status, string ad_type);
	string GetGender();
	string GetLocation();
	unsigned int GetAge();
};
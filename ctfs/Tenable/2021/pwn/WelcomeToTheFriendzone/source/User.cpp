#include "User.h"

User::User(string name, string location, unsigned int age, string gender, string status, string ad_type) : AdEnabledAccount(ProfileType::PERSON, ad_type) {
	this->account_name = name;
	this->age = age;
	this->gender = gender;
	this->location = location;
	this->status = status;
}

string User::GetLocation() {
	return location;
}

string User::GetGender() {
	return gender;
}

unsigned int User::GetAge() {
	return age;
}
#include "Business.h"

Business::Business(string name, string address, string status, string ad_type) : AdEnabledAccount(ProfileType::BUSINESS, ad_type) {
	this->account_name = name;
	this->address = address;
	this->status = status;
}

string Business::GetAddress() {
	return this->address;
}

string Business::GetStatus() {
	return this->status;
}
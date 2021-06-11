#include "Account.h"

Account::Account(ProfileType pt) {
	srand(time(NULL)); 
	time(&account_creation_date); 
	this->profile_id = rand();
	this->profile_type = pt;
}

unsigned int Account::GetProfileId() {
	return this->profile_id;
}

ProfileType Account::GetProfileType() {
	return profile_type;
}
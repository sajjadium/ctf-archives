#pragma once
#include <string>
#include <time.h> 
#include <vector>
using namespace std;

// Used to identify object types.
enum ProfileType {
	PERSON,
	BUSINESS,
	ADVERTISEMENT
};

class Account {
protected:
	vector<string> posts;
	time_t account_creation_date;
	string profile_pic;
	ProfileType profile_type;
	const string users_directory;
public:
	unsigned int profile_id;
	string account_name;
	Account(ProfileType pt);
	ProfileType GetProfileType();
	unsigned int GetProfileId();
	

};
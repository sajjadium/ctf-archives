#pragma once
#include <string>
#include <vector>
#include "Advertisement.h"
using namespace std;

class AdEnabledAccount : public Account {
public:
	char last_post[0x1000];
	string status;
	string ad_type;
	vector<string> posts;
	AdEnabledAccount(ProfileType profile_type, string ad_type);
	void AddPost(string post);
};
#pragma once
#include "User.h"
#include "Business.h"
#include "Advertisement.h"
#include <vector>
#include <stdexcept>
#include <time.h>
#include <unistd.h>
#include <iostream>
#include <map>
#include <set>
#include <algorithm>

using namespace std;

class Database {
private:
	const string profile_directory;
	map<unsigned int, Account*> accounts;
	void LoadAccounts();
	void LoadProfile(string profiledata);
	vector<string> ParseProfile(string profiledata);
public:
	Database();
	void AddAccount(Account* user);
	Account* GetProfileData(unsigned int profile_id);
	Advertisement* GetAdvertisement(string ad_type);
	set<string> GetAdTypes();
	vector<unsigned int> GetProfileIds();
};
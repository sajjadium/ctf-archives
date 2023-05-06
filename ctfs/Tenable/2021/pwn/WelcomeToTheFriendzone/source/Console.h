#pragma once
#include <iostream>
#include <string.h>
#include "Database.h"
#include "AdEnabledAccount.h"
#include <unistd.h>
#include <locale>
#include <set>
#include <iomanip>  
using namespace std;

class COMMANDS {
public:
	static string CREATE_PROFILE;
	static string VIEW_PROFILE;
	static string EDIT_PROFILE;
	static string POST;
	static string LIST_USERS;
};

class Console {
private:
	COMMANDS root_cmds;
	Database* db;
	string cmd;
	Account* LookupProfileId(string profile_id);
	void DisplayRootOptions();
	void HandleRoot();
	void HandleCreate();
	void HandleViewProfile();
	void HandleListUsers();
	void HandleEditProfile();
	void CreateBusinessSetup();
	void ShowAd(string ad_type);
	void CreateUserSetup();
	void HandlePost();
	vector<string> TokenizeCommand();
	void Error(string msg);
public:	
	void Open();
	Console() : db(new Database()) { }
	~Console();
	
};
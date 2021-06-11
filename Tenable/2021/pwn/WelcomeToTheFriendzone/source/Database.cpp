#include "Database.h"
#include <sys/stat.h>
#include <stdio.h>
#include <dirent.h>
#include <cstring>


Database::Database() : profile_directory("profiles/") {
	LoadAccounts();
}

void Database::LoadAccounts() {
	char buffer[0x1000] = { 0 };
	struct dirent* pDirent;
	
	DIR* epdf = opendir(profile_directory.c_str());
	if (epdf != NULL) {
		while (pDirent = readdir(epdf)) {
			if (pDirent->d_type != DT_DIR) {
				FILE* fp = fopen(string(profile_directory + string(pDirent->d_name)).c_str(), "r");
				cout << "Loading " + string(profile_directory + string(pDirent->d_name)) + " profile data..." << endl;
				
				fread(buffer, 0x1000, 1, fp);
				LoadProfile(string(buffer));
				memset(buffer, 0, 0x1000);
				usleep(500000);
			}
		}
	}
}

vector<string> Database::ParseProfile(string profiledata) {
	vector<string> tokens;
	size_t pos = profiledata.find("|");
	size_t last_pos = 0;
	while (pos != std::string::npos) {
		tokens.push_back(profiledata.substr(last_pos, pos));
		last_pos = pos+last_pos+1;
		pos = profiledata.substr(last_pos, profiledata.length()).find("|");
	}
	tokens.push_back(profiledata.substr(last_pos, profiledata.length() - last_pos));

	return tokens;
}
void Database::LoadProfile(string profiledata) {
	vector<string> profile_items = ParseProfile(profiledata);
	string ad_type, name, address, status, gender;
	char last_post[0x1000];
	Business* bs;
	User* u;
	Advertisement* ad;
	unsigned int profile_type, profile_id, age;
	try {
		profile_type = stoi(profile_items.at(0));
		name = profile_items.at(1);
		profile_id = stoi(profile_items.at(2));
	}
	catch (const std::out_of_range& oor) {
		cout << "Error parsing profile data" << endl;
		return;
	}

	switch (profile_type) {
	case ProfileType::PERSON:
		try {
			address = profile_items.at(3);
			age = stoi(profile_items.at(4));
			gender = profile_items.at(5);
			status = profile_items.at(6);
			memcpy(last_post, profile_items.at(7).c_str(), 0x1000);
			ad_type = profile_items.at(8);
		}
		catch (const std::out_of_range& oor) {
			cout << "Error parsing profile data" << endl;
			return;
		}
		u = new User(name, address, age, gender, status, ad_type);
		u->profile_id = profile_id;
		memcpy(u->last_post, last_post, 0x1000);
		AddAccount(u);
		break;
	case ProfileType::BUSINESS:
		try {
			address = profile_items.at(3);
			status = profile_items.at(4);
			memcpy(last_post, profile_items.at(5).c_str(), 0x1000);
			ad_type = profile_items.at(6);
		}
		catch (const std::out_of_range& oor) {
			cout << "Error parsing profile data" << endl;
			return;
		}
		
		bs = new Business(name, address, status, ad_type);
		bs->profile_id = profile_id;
		memcpy(bs->last_post, last_post, 0x1000);
		AddAccount(bs);
		break;
	case ProfileType::ADVERTISEMENT:
		ad = new Advertisement(name);
		ad->profile_id = profile_id;
		AddAccount(ad);
		break;
	}

}

void Database::AddAccount(Account* act) {
	this->accounts[act->profile_id] = act;
}

vector<unsigned int>  Database::GetProfileIds() {
	vector<unsigned int> profile_ids;
	for (map<unsigned int, Account*>::iterator it = this->accounts.begin(); it != this->accounts.end(); ++it)
		profile_ids.push_back(it->first);
	return profile_ids;
}

Advertisement* Database::GetAdvertisement(string ad_type) {

	for (map<unsigned int, Account*>::iterator it = this->accounts.begin(); it != this->accounts.end(); ++it) {
		if (it->second->GetProfileType() == ProfileType::ADVERTISEMENT) {
			if (((Advertisement*)it->second)->GetAdType() == ad_type)
				return (Advertisement*)it->second;
		}
	}
	return NULL;
}

set<string> Database::GetAdTypes() {
	set<string> ad_types;
	for (map<unsigned int, Account*>::iterator it = this->accounts.begin(); it != this->accounts.end(); ++it) {
		if (it->second->GetProfileType() == ProfileType::ADVERTISEMENT) {
			ad_types.insert(((Advertisement*)it->second)->GetAdType());
		}
	}
	return ad_types;
}

Account* Database::GetProfileData(unsigned int profile_id) {
	if(this->accounts.find(profile_id) != this->accounts.end())
		return this->accounts[profile_id];
	return NULL;
}
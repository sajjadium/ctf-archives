#include "Advertisement.h"
#include <algorithm>
#include <iostream>

Advertisement::Advertisement(string ad_type) : Account(ProfileType::ADVERTISEMENT) {
	ad_type.erase(std::remove(ad_type.begin(), ad_type.end(), '\n'), ad_type.end());
	if (!IsAdTypeValid(ad_type))
		throw std::invalid_argument("Invalid Ad_type");
	this->ad_type = ad_type;
}

string Advertisement::GetAdType() {
	return ad_type;
}

bool Advertisement::ChangeAdType(string ad_type) {
	if (!IsAdTypeValid(ad_type))
		return false;
	this->ad_type = ad_type;
	return true;
}

bool Advertisement::IsAdTypeValid(string ad_type) {
	// prevent directory traversal
	if (ad_type.find(".") != std::string::npos || ad_type.find("\\") != std::string::npos || ad_type.find("/") != std::string::npos)
		return false;
	
	//check ad_type file exists in advertisers_directory
	FILE* fp = fopen(string(advertisers_directory + ad_type).c_str(), "r");

	if (fp != NULL)
		return true;
	return false;
}

string Advertisement::GetAdText() {
	//Read advertisement from file
	memset(this->ad_text, 0, 0xf00);
	
	FILE* fp = fopen(string(advertisers_directory + this->ad_type).c_str(), "r");
	if (fp == NULL) {
		return "404 - NO_AD_FOUND! This is a bug, please report to FriendZone support.";
	}
	fread(ad_text, 0xf00, 1, fp);
	return string(ad_text);
}
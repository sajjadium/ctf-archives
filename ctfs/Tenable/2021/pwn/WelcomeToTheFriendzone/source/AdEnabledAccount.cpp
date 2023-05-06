#include "AdEnabledAccount.h"
#include <iostream>
#include <cstring>
#include <algorithm>

AdEnabledAccount::AdEnabledAccount(ProfileType profile_type, string ad_type) : Account(profile_type) {
	ad_type.erase(std::remove(ad_type.begin(), ad_type.end(), '\n'), ad_type.end());
	this->ad_type = ad_type;
}

void AdEnabledAccount::AddPost(string post) {
	posts.push_back(post);
	// ensure posts list is below 50 posts (FILO)
	if (post.length() >= 50) {
		post.erase(post.begin());
	}
}

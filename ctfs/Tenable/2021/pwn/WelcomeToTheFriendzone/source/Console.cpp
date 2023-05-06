#include "Console.h"
#include <algorithm>

string COMMANDS::CREATE_PROFILE = "CREATE_PROFILE";
string COMMANDS::EDIT_PROFILE = "EDIT_PROFILE";
string COMMANDS::VIEW_PROFILE = "VIEW_PROFILE";
string COMMANDS::POST = "POST";
string COMMANDS::LIST_USERS = "LIST_USERS";

bool is_digits(const std::string& str)
{
	return str.find_first_not_of("0123456789") == std::string::npos;
}

void Console::Error(string msg) {
	cout << endl << msg << endl << endl;
	usleep(1000000);
}

// Start new Console
void Console::Open(){
	// Print banner

	cout << " _____     _                _ _____ " << endl;
	cout << "|  ___| __(_) ___ _ __   __| |__  /___  _ __   ___ " << endl;
	cout << "| |_ | '__| |/ _ \\ '_ \\ / _` | / // _ \\| '_ \\ / _ \\"<<endl;
	cout << "|  _|| |  | |  __/ | | | (_| |/ /| (_) | | | |  __/" << endl;
	cout << "|_|  |_|  |_|\\___|_| |_|\\__,_/____\\___/|_| |_|\\___|" << endl;
	cout<<"--------------------------------------------------------------------------------"<<endl;
	cout<<"Welcome to Friendzone Social Media! The leader in most advertisements."<<endl;
	cout<<"--------------------------------------------------------------------------------"<<endl<<endl;
	while(true)
		HandleRoot();
}

// Parse user input into space delimited tokens
vector<string> Console::TokenizeCommand() {
	vector<string> tokens;
	size_t pos = cmd.find(" ");
	size_t last_pos = 0;
	while (pos != std::string::npos) {
		tokens.push_back(cmd.substr(last_pos, pos));
		last_pos = pos + last_pos + 1;
		pos = cmd.substr(last_pos, cmd.length()).find("|");
	}
	tokens.push_back(cmd.substr(last_pos, cmd.length()));
	return tokens;
}

Account* Console::LookupProfileId(string profile_id) {
	Account* act;
	int profile_id_num;
	//ensure only number was passed
	if (!is_digits(profile_id)) {
		Error("Second argument must be a profile ID!");
		return NULL;
	}
	try {
		profile_id_num = stoi(profile_id);
	}
	catch (const std::out_of_range& oor) {
		Error("Invalid! profile_id too big");
		return NULL;
	}
	if (profile_id_num < 100) {
		Error("Profile_ids under 100 are marked as private profiles!");
		return NULL;
	}
	//Lookup account profile and grab its data
	act = db->GetProfileData(profile_id_num);
	if (act == NULL) {
		Error("Profile_id does not exist!");
		return NULL;
	}
	return act;
}

void Console::ShowAd(string ad_type) {
	usleep(1000000);
	cout << "*******************************************************************************************************" << endl << endl;
	cout << "* " << db->GetAdvertisement(ad_type)->GetAdText() << endl << endl;
	cout << "*******************************************************************************************************" << endl << endl << endl << endl;
	usleep(3500000);
}

// Handles view profile command (>VIEW_PROFILE <profile_id>)
void Console::HandleViewProfile() {
	string secondcmd;
	Account* act;

	try {
		secondcmd = TokenizeCommand().at(1); // Get secondary command
	}
	catch (const std::out_of_range& oor) {
		Error("Invalid argument!");
		return;
	}
	act = LookupProfileId(secondcmd);
	if (act == NULL)
		return;

	// Advertisements are accounts but shouldnt be viewable as if they were a user/business
	if (act->GetProfileType() == ProfileType::ADVERTISEMENT) {
		Error("Unable to view account because account is Advertiser - no profile data to see!");
		return;
	}

	// Show advertisement
	cout << "Navigating to " + act->account_name + "... but first an ad!" << endl<<endl;
	ShowAd(((AdEnabledAccount*)act)->ad_type);
	
	//If profile_id was person, load person data
	if (act->GetProfileType() == ProfileType::PERSON) {
		cout << "User Name: " << ((User*)act)->account_name << endl;
		cout << "Gender: " << ((User*)act)->GetGender() << endl;
		cout << "Age: "<< ((User*)act)->GetAge() << endl;
		cout << "Location: "<< ((User*)act)->GetLocation() << endl <<endl;
		cout << "Status:  \"" << ((User*)act)->status <<"\""<< endl;
		cout << "_______________________________________________________________________________" << endl << endl;
		cout << "Latest Comment: \"" << string(((User*)act)->last_post) << "\"" << endl << endl;
		cout << "_______________________________________________________________________________" << endl << endl<<endl<<endl;
	}
	//If profile_id was business, load business data
	else if (act->GetProfileType() == ProfileType::BUSINESS) {
		cout << "Business Name: " << ((Business*)act)->account_name << endl;
		cout << "Address: " << ((Business*)act)->GetAddress() << endl;
		cout << "Status: \"" << ((Business*)act)->GetStatus() << "\""<< endl;
		cout << "_______________________________________________________________________________" << endl << endl;
		cout << "Latest Comment: \"" << string(((Business*)act)->last_post) << "\""<<endl << endl;
		cout << "_______________________________________________________________________________" << endl << endl << endl << endl;
	}
}

// Handles "EDIT_PROFILE" cmd
void Console::HandleEditProfile() {
	Account* act;
	string change_option, change_data, secondcmd;
	bool valid_response_flag = false;
	try {
		secondcmd = TokenizeCommand().at(1); // Get secondary command
	}
	catch (const std::out_of_range& oor) {
		Error("Invalid argument!");
		return;
	}
	act = LookupProfileId(secondcmd);
	if (act == NULL)
		return;
	if (act->GetProfileType() == ProfileType::ADVERTISEMENT) {
		do {
			cout << "What new ad type should this be?" << endl << endl << "ad_type>";
			getline(cin, change_option);
			if (change_option.length() < 50) {
				if (((Advertisement*)act)->ChangeAdType(change_option)) {
					valid_response_flag = true;
				}
				else {
					Error("Invalid! Ad_type does not exist");
				}
					
			}
		} while (!valid_response_flag);
	}
	else {
		do {
			cout << "What would you like to change for " + act->account_name + "?" << endl << endl;
			cout << "*User Name" << endl;
			cout << "*Status" << endl<<endl<<"cmd>";
			getline(cin, change_option);
			if (change_option.length() < 50) {
				if (change_option == "User Name") {
					cout << "What new user name would you like?" << endl << endl << "user name>";
					getline(cin, change_data);
					if (change_data.length() < 50) {
						((AdEnabledAccount*)act)->account_name = change_data;
						valid_response_flag = true;
					}
					else {
						Error("Invalid! User name too long");
					}
				}
				else if (change_option == "Status") {
					cout << "Enter a new status" << endl << endl << "status>";
					getline(cin, change_data);
					if (change_data.length() < 200) {
						((AdEnabledAccount*)act)->status = change_data;
						valid_response_flag = true;
					}
					else {
						Error("Invalid! Status too long");
					}
				}
				else {
					Error("Invalid! No such option");
				}
			}
			else {
				Error("Invalid! Option too long");
			}
		} while (!valid_response_flag);
	}
}

// Handles "CREATE_PROFILE business" cmd
void Console::CreateBusinessSetup() {
	string business_name, city, state, street_number, street_name, ad_type;
	set<string> available_ad_types;
	Business* b;
	bool valid_response_flag = false;

	// Read business name
	do
	{
		cout<<"Business Name>";
		getline(cin, business_name);
		if(business_name.length() > 30)
			cout<<"Please enter business name less than 30 characters"<<endl;
	} while (business_name.length() > 30);

	cout << endl << "*********Welcome " + business_name + "! Let's get your address**********" << endl<<endl;
	// Read business street
	do{
		cout<<"Enter your business street number>";
		getline(cin, street_number);
		if (is_digits(street_number)) {
			valid_response_flag = true;
		}
		else {
			Error("Invalid! This must be a number");
		}
	} while (!valid_response_flag);
	valid_response_flag = false;

	//Read business street name
	do {
		cout << "Enter your business street name>";
		getline(cin, street_name);
		if (street_name.length() < 20) {
			valid_response_flag = true;
		}
		else {
			Error("Invalid! Street name too long");
		}
	} while (!valid_response_flag);
	valid_response_flag = false;

	//Read business city name
	do {
		cout << "Enter your business city>";
		getline(cin, city);
		if (city.length() < 20) {
			valid_response_flag = true;
		}
		else {
			Error("Invalid! City name too long");
		}
	} while (!valid_response_flag);

	valid_response_flag = false;

	//Read business state name
	do {
		cout << "Enter your business state>";
		getline(cin, state);
		if (state.length() < 20) {
			valid_response_flag = true;
		}
		else {
			Error("Invalid! State name too long");
		}
	} while (!valid_response_flag);
	valid_response_flag = false;
	cout << "And finally, what kind of ads would you like to be shown to visitors that visit your profile?" << endl << endl;

	// print available ad_types
	available_ad_types = db->GetAdTypes();
	for (set<string>::iterator it = available_ad_types.begin(); it != available_ad_types.end(); ++it)
		cout << *it << endl;
	//Read ad_types
	do {
		// read ad_type
		cout << endl << "Enter an ad_type>";
		getline(cin, ad_type);
		if (ad_type.length() < 50) {
			if (available_ad_types.find(ad_type) != available_ad_types.end()) {
				try {
					b = new Business(business_name, street_number + " " + street_name + "\n" + city + ", " + state, string(""), ad_type);
					valid_response_flag = true;
				}
				catch (const std::invalid_argument& e) {
					Error("Invalid AdType!");
				}
			}
			else {
				Error("Invalid! No such Adtype");
			}
		}
		else {
			Error("Invalid! Too long Adtype.");
		}
	} while (!valid_response_flag);

	// Store new user profile to database
	db->AddAccount(b);
	cout << "Welcome to FriendZone " + business_name + "! (profile_id:" + to_string(b->GetProfileId())  +")"<<endl;

} 

// Handles CREATE_PROFILE cmd
void Console::HandleCreate() {
	string secondcmd;
	try{
		secondcmd = TokenizeCommand().at(1); // Get secondary command
	}	
	catch(const std::out_of_range& oor) {
		Error("Invalid command!");
		return;
	}
	
	if (secondcmd == "business")
		CreateBusinessSetup();
	else if (secondcmd == "personal")
		CreateUserSetup();
	else
		Error("Invalid! No such second argument");
}

// Handles "CREATE_PROFILE personal" cmd
void Console::CreateUserSetup() {
	User* u;
	set<string> available_ad_types;
	string user_name, location, age, gender, ad_type;
	bool valid_response_flag = false;
	unsigned int age_num;

	// Read user name
	do
	{
		cout << "User Name>";
		getline(cin, user_name);
		if (user_name.length() > 30)
			Error("Please enter user name less than 30 characters");
	} while (user_name.length() > 30);
	cout << endl << "*********Welcome " + user_name + "! Let's get your general location**********" << endl << endl;

	//Read user city name
	do {
		cout << "Enter your city, state>";
		getline(cin, location);
		if (location.length() < 20) {
			valid_response_flag = true;
		}
		else {
			cout << "Invalid! city, state input too long" << endl;
		}
	} while (!valid_response_flag);

	valid_response_flag = false;
	//Read Gender
	do {
		cout << "Enter your Gender>";
		getline(cin, gender);
		if (gender.length() < 20) {
			valid_response_flag = true;
		}
		else {
			Error("Invalid! gender input too long.");
		}
	} while (!valid_response_flag);
	valid_response_flag = false;
	//Read Age
	do {
		cout << "Enter your Age>";
		getline(cin, age);
		if (is_digits(age)) {
			try {
				age_num = stoi(age);
				valid_response_flag = true;
			}
			catch (const std::out_of_range& oor) {
				Error("Invalid! Age too big");
			}
			
		}
		else {
			Error("Invalid! age must be number.");
		}
	} while (!valid_response_flag);
	valid_response_flag = false;
	cout << "And finally, what kind of ads would you like to be shown to visitors that visit your profile?" << endl << endl;

	// print available ad_types
	available_ad_types = db->GetAdTypes();
	for (set<string>::iterator it = available_ad_types.begin(); it != available_ad_types.end(); ++it)
		cout << *it << endl;
	
	// read ad_type
	do {
		cout << endl << "Enter an AdType>";
		getline(cin, ad_type);
		if (ad_type.length() < 50) {
			if (available_ad_types.find(ad_type) != available_ad_types.end()) {
				try {
					u = new User(user_name, location, age_num, gender, string(""), ad_type);
					valid_response_flag = true;
				}
				catch (const std::invalid_argument& e) {
					Error("Invalid AdType!");
				}
			}
			else {
				Error("Invalid! No such Adtype");
			}
		}
		else {
			Error("Invalid! Too long Adtype.");
		}
	} while (!valid_response_flag);
	db->AddAccount(u);
	cout << "Welcome to FriendZone " + user_name + "! (profile_id:" + to_string(u->GetProfileId()) + ")" << endl;
}

void Console::HandleListUsers() {
	cout <<endl<< "Profile Ids" << endl << "-------------" << endl << endl;
	vector<unsigned int> profile_ids = db->GetProfileIds();
	for (vector<unsigned int>::iterator it = profile_ids.begin(); it != profile_ids.end(); ++it)
		cout << *it << endl;
	cout <<endl<< endl;
}

// Load root menu
void Console::DisplayRootOptions() {
	cout << "---------------------------------------------------------" << endl;
	cout << "Portal Options" << endl << endl;
	cout << "-" + root_cmds.CREATE_PROFILE + " <personal|business>" << endl;
	cout << "-" + root_cmds.LIST_USERS << endl;
	cout << "-" + root_cmds.VIEW_PROFILE + " <profile_id>" << endl;
	cout << "-" + root_cmds.POST + " <profile_id>>" << endl;
	cout << "-" + root_cmds.EDIT_PROFILE + " <profile_id>" << endl << endl;
	cout << "---------------------------------------------------------" << endl << endl << endl << "cmd>";
}

// Handle POST <profile_id> cmd
void Console::HandlePost() {
	string secondcmd, post_msg;
	Account* act;
	int profile_id;
	bool valid_response_flag = false;
	try {
		secondcmd = TokenizeCommand().at(1); // Get secondary command
	}
	catch (const std::out_of_range& oor) {
		Error("Invalid profile_id!");
		return;
	}
	act = LookupProfileId(secondcmd);
	if (act == NULL)
		return;
	try {
		profile_id = stoi(secondcmd);
	}
	catch (const std::out_of_range& oor) {
		Error("Invalid! profile_id too big");
		return;
	}

	// Read user post message
	do {
		cout << "What would you like to post to " + db->GetProfileData(profile_id)->account_name + " wall?" << endl << endl<<"post>";
		getline(cin, post_msg);
		if (post_msg.length() < 0x1000) {
			valid_response_flag = true;
			memset(((AdEnabledAccount*)db->GetProfileData(profile_id))->last_post, 0, 0x1000);
			memcpy(((AdEnabledAccount*)db->GetProfileData(profile_id))->last_post, post_msg.c_str(), post_msg.length());
		}
		else {
			Error("Invalid! too long post.");
		}
	} while (!valid_response_flag);

}

// Default menu
void Console::HandleRoot(){
	string rootcmd;
   
	DisplayRootOptions();
	// Read cmd
	getline(cin, cmd);
	try{
		rootcmd = TokenizeCommand().at(0); // Get root command
	}	
	catch(const std::out_of_range& oor) {
		Error("Invalid root command!");
		return;
	}
	// Execute Cmd
	if (rootcmd == root_cmds.CREATE_PROFILE)
		HandleCreate();
	else if (rootcmd == root_cmds.VIEW_PROFILE)
		HandleViewProfile();
	else if (rootcmd == root_cmds.LIST_USERS)
		HandleListUsers();
	else if (rootcmd == root_cmds.POST)
		HandlePost();
	else if (rootcmd == root_cmds.EDIT_PROFILE)
		HandleEditProfile();
}

#include <iostream>
#include <cstring>
#include <sstream>
#include <vector>
#include <unistd.h>
using namespace std;

struct Secret {
	string secret;
	int magic;
	bool to_be_modified;
	string destination;
	bool to_be_deleted;
	bool to_be_shown;
};

class SecretKeeper {
	private:
		vector<Secret> secrets;
		vector<string> command_line;
	public:
		SecretKeeper();
		string get_command();
		void fill_command_line();
		
		void show_command_info();
		void parse_command();

		void add_secret();
		void show_all();
		void modify_secret();
		void delete_secret();
		void show();
		void finish();
		unsigned int get_index();
		void delete_now();
		~SecretKeeper();
};

SecretKeeper::SecretKeeper() {
	cout << "Keep your secrets safe here." << endl;
	alarm(60*4);
}


string SecretKeeper::get_command(void) {
	string cmd;
	cout << "CMD> ";
	getline(cin, cmd);
	return cmd;
}

void SecretKeeper::fill_command_line(void) {
	
	string cmd = get_command();

	string word;
	for(auto b: cmd){
		if(b == ' '){
			command_line.push_back(word);
			word = "";
		} else {
			word += b;
		}
	}

	command_line.push_back(word);
}

void SecretKeeper::show_command_info() {
	cout << "The command is ";
	cout << this->command_line[0] << endl;
	
	int i = 1;

	for(vector<string>::iterator it = command_line.begin()+1
		; it != command_line.end()
		; it++, i++) {

		cout << "argv[" << i << "]: " << *it << endl;
	}
}

void SecretKeeper::add_secret() {
	try {
		struct Secret secret;
		secret.secret = command_line[1];
	
		stringstream magic(command_line[2]);
		magic >> secret.magic;
		
		secret.to_be_modified = false;
		secret.to_be_deleted = false;
		secret.to_be_shown = false;

		secret.destination = "";

		this->secrets.push_back(secret);
		cout << "secret added!" << endl;
	}
	catch(...) {
		cout << "Not enough command line arguments!" << endl;
		cout << "Ex : add thisismysecret 0" << endl;
	}
}

void SecretKeeper::show_all() {
	for(vector<Secret>::iterator it = this->secrets.begin()
		; it != secrets.end()
		; it ++) {
		cout << "Secret		: " << (*it).secret << endl;
		cout << "Magic		: " << (*it).magic << endl;
		cout << "To change	: ";
		if((*it).to_be_modified) {
			cout << "True" << endl;
			cout << "Dest		: " << (*it).destination << endl;
		} else {
			cout << "False" << endl;
		}
		
		cout << "To delete	: ";
		if((*it).to_be_deleted) {
			cout << "True" << endl;
		} else {
			cout << "False" << endl;
		}
		
		cout << "To show	: ";
		if((*it).to_be_shown) {
			cout << "True" << endl;
		} else {
			cout << "False" << endl;
		}
		cout << endl;
	}
}

unsigned int SecretKeeper::get_index() {
	unsigned int secret_index;
	stringstream index(command_line[1]);
	index >> secret_index;

	if(secrets.empty()) {
		cout << "No secret is added yet" << endl;
		exit(-1);
	}

	if(secret_index >= secrets.size()) {
		cout << "Out of bounds not allowed!" << endl;
		exit(-1);
	}

	return secret_index;
}

void SecretKeeper::modify_secret() {

	try {
		unsigned int secret_index = get_index();
		if(secrets[secret_index].secret.length() < command_line[2].length()){
			cout << "New secret can't be updated" << endl;
			return;
			
		}
		secrets[secret_index].destination = command_line[2];
		secrets[secret_index].to_be_modified = true;
		cout << "Marked 'to be modified'!" << endl;
	}
	catch (...) {
		cout << "Not enough command line arguments!" << endl;
		cout << "Ex: modify 2 thisisanothersecret" << endl;
	}
}

void SecretKeeper::delete_secret() {
	unsigned int secret_index = get_index();	
	secrets[secret_index].to_be_deleted = true;
	cout << "Marked 'to be deleted!'" << endl;
}

void SecretKeeper::finish() {

	struct Secret secret;
	
	try {	
			// Process the first `number` elements.
			unsigned int number;
			stringstream num(command_line[1]);
		    num >> number;
			unsigned int counter = 0;

			for(vector<Secret>::iterator it = secrets.begin()
				; it != secrets.end() and  counter < number
				; it++, counter++){
				
				secret = *it;

				if(secret.to_be_modified) {
					for(int i=0; i<secret.destination.length(); i++){
						(*it).secret[i] = secret.destination[i];
					}
					secret.to_be_modified = false;
					secret.destination = "";
				}

				if(secret.to_be_shown) {
					cout << "Magic number : " << secret.magic << endl;
					cout << "secret : " << secret.secret << endl;
				}
					
				if(secret.to_be_deleted) {
					secrets.erase(it);
				}
			}
			secrets.clear();
	} catch (...) {
		cout << "finish wrong syntax, need a number" << endl;
		cout << "Ex this will process the first 10 secrets: finish 10"
				<< endl;
		return;
	}
}

void SecretKeeper::show() {
	unsigned int secret_index = get_index();
	secrets[secret_index].to_be_shown = true;
}

void SecretKeeper::delete_now() {
	unsigned int secret_index = get_index();
	secrets.erase(secrets.begin() + secret_index);
}

SecretKeeper::~SecretKeeper() {
	cout << "Class destroyed!" << endl;
	secrets.clear();
	command_line.clear();
}

void SecretKeeper::parse_command() {
	
	while(1) {
		fill_command_line();
		//show_command_info();
		
		string command = command_line[0];

		if(command == "add") {
			add_secret();
		} else if (command == "show_all") {
			show_all();
		} else if (command == "modify"){
			modify_secret();
		} else if (command == "delete"){
			delete_secret();
		} else if (command == "finish"){
			finish();
		} else if (command == "show") {
			show();
		} else if (command == "delete_now") {
			delete_now();
		} else if (command == "exit"){
			exit(0);
		} else {
			cout << "'" << command << "'" << " not found." << endl;
		}


		command_line.clear();
	}
}


int main() {
	SecretKeeper nk;
	nk.parse_command();
	return 0;
}

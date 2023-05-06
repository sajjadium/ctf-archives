#include <iostream>
#include <string>
#include <vector>
#include <seccomp.h>
#include <unistd.h>
#include <signal.h>

using namespace std;

vector<string*> rules;

void handler(int sig) {
	exit(1);
}

void init_sandbox() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);

	signal(SIGALRM, handler);
	alarm(30);

	scmp_filter_ctx ctx;
	ctx = seccomp_init(SCMP_ACT_KILL); // default action: kill

	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(alarm), 0);

	seccomp_load(ctx);
}

void add_rule(string &cmd) {
	if(rules.size() < 48) {
		string * newrule = new string(cmd, 4);
		rules.push_back(newrule);
		cout << "Rule added! Your rule ID is: " << (rules.size() - 1) << endl;
	}
	else{
		cout << "ERROR: Too many rules in place already!" << endl;
	}
}

void view_rule(string &cmd) {
	try {
		int idx = stoi(string(cmd, 5));
		if(idx < 0 || idx >= rules.size() || rules[idx] == nullptr) {
			cout << "ERROR: Invalid ID!" << endl;
			return;
		}
		cout << idx << ": " << *rules[idx] << endl;
	}
	catch(...) {
		cout << "ERROR: Invalid ID!" << endl;
	}
}

void del_rule(string &cmd) {
	try {
		int idx = stoi(string(cmd, 4));
		if(idx < 0 || idx >= rules.size() || rules[idx] == nullptr) {
			cout << "ERROR: Invalid ID!" << endl;
			return;
		}
		delete rules[idx];
		cout << "Rule " << idx << " deleted." << endl;
	}
	catch(...) {
		cout << "ERROR: Invalid ID!" << endl;
	}
}

void menu() {
	cout << "Available commands:" << endl;
	cout << "add <rule> : Add a firewall rule" << endl;
	cout << "view <id> : View a firewall rule given its ID" << endl;
	cout << "del <id> : Delete a firewall rule given its ID" << endl;
	cout << "help : Prints this help message" << endl;
	cout << "exit : Exit the firewall interface" << endl;
}
int main(int argc, char ** argv) {
	init_sandbox();
	cout << "Welcome to our DMZ Firewall!" << endl;
	while(1) {
		cout << "> ";
		string input;
		getline(cin, input);
		if(input.compare(0, 3, "add") == 0) {
			add_rule(input);
		}
		else if(input.compare(0, 4, "view") == 0) {
			view_rule(input);
		}
		else if(input.compare(0, 3, "del") == 0) {
			del_rule(input);
		}
		else if(input.compare(0, 4, "help") == 0) {
			menu();
		}
		else if(input.compare(0, 4, "exit") == 0) {
			exit(0);
		}
		else if (input.length() > 0){
			cout << "Unknown command! Use the 'help' command to get a list of valid commands!" << endl;
		}
	}

}

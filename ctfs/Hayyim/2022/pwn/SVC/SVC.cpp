#include <stdlib.h>
#include <vector>
#include <memory>
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <cstring>
#include <string>
#include <string_view>

using namespace std;

string sv_init;
string ConcatString;
string str;
string_view str_view;

char* chr = NULL;
uint32_t chr_size = 0;

uint32_t read_str(char* buf) {
        memset(buf, 0, 1024);
        uint32_t buf_size = read(0, buf, 1023);
        if(((int32_t)buf_size) > 0 && buf[buf_size - 1] == '\n') {
            buf[buf_size - 1] = '\x00';
	    	return buf_size - 1;
		}
        return buf_size;
}

void BuiltinStringArgMenu() {
   	cout << "1. String " << endl;
    cout << "2. StringView" << endl;
    cout << "3. Char" << endl;
    cout << "4. Local" << endl;
    cout << "Type > ";
}

void BuiltinStringViewArgMenu() {
	cout << "1. String " << endl;
	cout << "2. Char" << endl;
	cout << "3. Local" << endl;
	cout << "Type > ";
}


void LoadMenu() {
	cout << "Input Load Type Data" << endl;
	cout << "1. String" << endl;
	cout << "2. Char" << endl;
	cout << "> ";
}


void BuiltinTypeMenu() {
	cout << "Input Load Type Data" << endl;
	cout << "1. String" << endl;
	cout << "2. StringView" << endl;
	cout << "3. Char" << endl;
	cout << "4. Back" << endl;
	cout << "> ";
}

void BuiltinMenu() {
	cout << "1. Copy" << endl;
	cout << "2. At" << endl;
	cout << "3. Concat" << endl;
	cout << "4. Swap" << endl;
	cout << "5. Back" << endl;
	cout << "> ";
}

void BuiltinStringViewMenu() {
	cout << "1. Copy" << endl;
	cout << "2. At" << endl;
	cout << "3. Concat" << endl;
	cout << "4. Swap" << endl;
	cout << "5. Write" << endl;	
	cout << "6. Back" << endl;
	cout << "> ";
}


void HandlerMenu() {
	cout << "1. New" << endl;
	cout << "2. Delete" << endl;
	cout << "3. Edit" << endl;
	cout << "4. View" << endl;
	cout << "> ";

}

void SHandler() {
	char s[1024];
	uint32_t s_size = 0;
	int cmd = 0;

	HandlerMenu();
	cin >> cmd;
	cin.ignore();
	switch(cmd) {
		case 1:
			if(str.size() <= 0) {
				cout << "Input Data > ";
				if(str.c_str() == str_view.data())
					str_view = sv_init;
				getline(cin, str);
			}
			break;
		case 2:
			if(str.c_str() == str_view.data())
				str_view = sv_init;
			str.clear();
			break;
		case 3:
			if(str.size() > 1) {
				if(str.c_str() == str_view.data())
					str_view = sv_init;
				cout << "Input Edit Data > ";
				getline(cin, str);
			}
			break;
		case 4:
			cout << str << endl;
			break;
	}
}

void AddStringView() {
	int cmd = 0;
	LoadMenu();
	cin >> cmd;
	cin.ignore();
	switch(cmd) {
		case 1:
			if(str.size() > 0) {
				str_view = str;
			}
			break;
		case 2:
			if(chr) {
				str_view = chr;
			}
			break;
		default:
			exit(-1);
	}
}

void SVHandler() {
	char s[1024];
	uint32_t s_size = 0;
	int cmd = 0;

	HandlerMenu();
	cin >> cmd;
	cin.ignore();
	switch(cmd) {
		case 1:
			if(!str_view.size()) {
				AddStringView();
			}
			break;
		case 2:
			str_view = sv_init;
			break;
		case 3:
			if(str_view.size()) {
				AddStringView();		
			}
			break;
		case 4:
			cout << str_view << endl;
			break;
	}

}

void CHandler() {
	char s[1024];
	uint32_t s_size = 0;
	int cmd = 0;
	HandlerMenu();
	cin >> cmd;
	cin.ignore();
	switch(cmd) {
		case 1:
			if(chr) {
				if(chr == str_view.data())
					str_view = sv_init;
				free(chr);
				chr = NULL;
			}
			cout << "Input Data > ";
			s_size = read_str(s);
			chr = (char*)malloc(s_size + 1);
			chr_size = s_size;
			memcpy(chr, s, s_size);
			break;
		case 2:
			if(chr) {
				if(chr == str_view.data())
					str_view = sv_init;
				free(chr);
				chr = NULL;
			}
			break;
		case 3:
			if(chr) {
				cout << "Input Edit Data > ";
				s_size = read_str(s);
				if(s_size > chr_size) {
					exit(-1);
				}
				else {
					memcpy(chr, s, s_size);
					chr_size = s_size;
				}
			}
			break;
		case 4:
			if(chr)
				cout << chr << endl;
			break;
	}

}

void BuiltinStringHandler() {
	char s[1024];
	uint32_t s_size = 0;
	int cmd = 0;
	string temp;
	while(1) {
		BuiltinMenu();
		cin >> cmd;
		cin.ignore();
		switch(cmd) {
			case 1:
				cout << "Input Copy Data > ";
				s_size = read_str(s);
				if(s_size <= str.size()) {
					memcpy((char*)str.c_str(), s, s_size);
				}
				else {
					if(str.c_str() == str_view.data())
						str_view = sv_init;
					str = s;
				}
				break;
			case 2:
				cout << "Input At IDX > ";
				cin >> cmd;
				cin.ignore();
				cout << "At result > " << str.at(cmd) << endl;
				break;				
			case 3:
				BuiltinStringArgMenu();
				cin >> cmd;
				cin.ignore();
				if(str.c_str() == str_view.data())
					str_view = sv_init;
				switch(cmd) {
					case 1:
						str = str + str;
						break;
					case 2:
						str = str + str_view.data();
						break;
					case 3:
						if(chr)
							str = str + chr;
						break;
					case 4:
						cout << "Input Concat Arg1 > ";
						read_str(s);
						str = str + s;
						break;
				}
				break;
			case 4:
				BuiltinStringArgMenu();
				cin >> cmd;
				cin.ignore();
				switch(cmd) {
					case 1:
						cout << "Type Duplication Error" << endl;
						break;
					case 2:
						cout << "No access to String View" << endl;
						break;
					case 3:
						if(!chr)
							break;
						if(str_view.data() == str.c_str() || (str_view.data() == chr))
							str_view = sv_init;
						if(chr_size < str.size()) {
							temp = str;
							chr_size = str.size();
							str = chr;
							chr = (char*)malloc(chr_size + 1);
							memcpy(chr, temp.c_str(), chr_size);
						}
						else {

							temp = str;
							str = chr;
							memcpy(chr, temp.c_str(), temp.size());
							chr_size = temp.size();
						}
						break;
					case 4:
						if(str_view.data() == str.c_str())
							str_view = sv_init;
						cout << "Input Local Data > ";
						read_str(s);
						temp = str;
						str = s;
						if(temp.size() > 1023)
							exit(-1);
						memset(s, 0, 1024);
						memcpy(s, temp.c_str(), temp.size());
						cout << "Swap Local Data > " << s << endl;
						break;

				}
				break;
			case 5:
				return;

		}
	}
}

void BuiltinStringViewHandler() {
	uint32_t cmd = 0;
	uint32_t arg1 = 0;
	uint32_t s_size = 0;
	char* view_temp = NULL;
	char* temp = NULL;
	char s[1024];
	char* dest_temp = NULL;
	//string ConcatString;
	while(1) {
		BuiltinStringViewMenu();
		cin >> cmd;
		cin.ignore();
		switch(cmd) {
			case 1:
				BuiltinStringViewArgMenu();
				cin >> cmd;
				cin.ignore();
				cout << "Input Size > ";
				cin >> arg1;
				cin.ignore();
				cout << "Input Offset > ";
				cin >> cmd;
				cin.ignore();
				switch(cmd) {
					case 1:
						if(arg1 > str.size()) {
							if(arg1 < 1024) {
								if(str.c_str() == str_view.data()) {
									exit(-1);
								}
								str.reserve(arg1 + 1);
							}
							else
								exit(-1);
						}
						str_view.copy((char*)str.c_str(), arg1, cmd);
						break;
					case 2:
						if(arg1 > 1023)
							exit(-1);
						if(arg1 > chr_size) {
							if(chr == str_view.data()) {
								exit(-1);
							}
							free(chr);
							chr = (char*)malloc(arg1 + 1);
						}
						str_view.copy(chr, arg1, cmd);
						break;
					case 3:
						if(arg1 > 1023)
							exit(-1);
						str_view.copy(s, arg1, cmd);
						cout << "Copy Data > " << s << endl;
						break;
				}
				break;
			case 2:
				cout << "Input At IDX > ";
				cin >> cmd;
				cin.ignore();
				cout << "At result > " << str_view.at(cmd) << endl;
				break;
			case 3:
				BuiltinStringViewArgMenu();
				cin >> cmd;
				cin.ignore();

				switch(cmd) {
					case 1:
						ConcatString = str;
						break;
					case 2:
						ConcatString = chr;
						break;
					case 3:
						cout << "Concat Arg0 > ";
						s_size = read_str(s);
						temp = (char*)malloc(s_size + 1);
						memcpy(temp, s, s_size);
						ConcatString = temp;
						break;
				}
				cout << "Concat Arg0 Input Success" << endl;
				BuiltinStringViewArgMenu();
				cin >> cmd;
				cin.ignore();

				switch(cmd) {
					case 1:
						str_view = ConcatString + str;
						break;
					case 2:
						str_view = ConcatString + chr;
						break;
					case 3:
						cout << "Concat Arg 1 > ";
						read_str(s);
						str_view = ConcatString + s;
						break;
				}
				break;
			case 4:
				BuiltinStringViewArgMenu();
				cin >> cmd;
				cin.ignore();
				switch(cmd) {
					case 1:
						if(str_view.data() == str.c_str())
							break;
						temp = (char*)malloc(str.size() + 1);
						memcpy(temp, str.c_str(), str.size());
						view_temp = (char*)str_view.data();
						str_view = temp;
						str = view_temp;
						break;
					case 2:
						if(str_view.data() == chr)
							break;
						temp = chr;
						view_temp = (char*)malloc(str_view.size() + 1);
						memcpy(view_temp, str_view.data(), str_view.size());
						chr = view_temp;
						chr_size = str_view.size();
						str_view = temp;			
						break;
					case 3:
						cout << "Input Local Data > ";
						s_size = read_str(s);
						temp = (char*)malloc(s_size + 1);
						view_temp = NULL;
						memcpy(temp, s, s_size);
						view_temp = (char*)str_view.data();
						str_view = temp;
						break;
				}
				break;
			case 5:
				BuiltinStringViewArgMenu();
				cin >> cmd;
				cin.ignore();
				switch(cmd) {
					case 1:
						if(str_view.size() < str.size())
							exit(-1);
						memcpy((char*)str_view.data(), str.c_str(), str.size());
						break;
					case 2:
						if(str_view.size() < chr_size)
							exit(-1);
						memcpy((char*)str_view.data(), chr, chr_size);
						break;
					case 3:
						cout << "Input Local Data > ";
						s_size = read_str(s);
						if(str_view.size() < s_size)
							exit(-1);
						memcpy((char*)str_view.data(), s, s_size);
						break;
					}
				break;
			case 6:
				return;
				break;
		}
	}
}

void BuiltinCharHandler() {
	uint32_t cmd = 0;
	uint32_t s_size = 0;
	char* temp = NULL;
	char s[1024];
	
	if(!chr)
		return;
	while(1) {
		BuiltinMenu();
		cin >> cmd;
		cin.ignore();
		switch(cmd) {
			case 1:
				cout << "Input Copy Data > ";
				s_size = read_str(s);
				if(s_size > chr_size) {
						if(chr == str_view.data())
							str_view = sv_init;
						free(chr);
						chr = (char*)malloc(s_size + 1);
				}
				else {
					memcpy(chr, s, s_size);
				}
				chr_size = s_size;
				break;
			case 2:
				cout << "Input At Idx > ";
				cin >> cmd;
				cin.ignore();
				if(cmd >= chr_size)
					exit(-1);
				else
					cout << "At Data > " << chr[cmd] << endl;
				break;
			case 3:
				cout << "Input Concat Data > ";
				s_size = read_str(s);
				if(chr == str_view.data()) {
					str_view = sv_init;
				}
				if((chr_size + s_size + 1) < chr_size || (chr_size + s_size + 1) < s_size)
					exit(-1);
				temp = (char*)malloc((chr_size + s_size + 1));
				if(!temp)
					return;
				memcpy(temp, chr, chr_size);
				memcpy(temp+chr_size, s, s_size);
				free(chr);
				chr = temp;
				chr_size = chr_size + s_size;
				break;
			case 4:
				cout << "NOT IMPLEMENTED" << endl;
				break;
			case 5:
				return;
				break;
		}
	}
}

void BHandler() {
	int cmd = 0;
	while(1) {
		BuiltinTypeMenu();
		cin >> cmd;
		cin.ignore();
		switch(cmd) {
			case 1:
				BuiltinStringHandler();
				break;
			case 2:
				BuiltinStringViewHandler();
				break;
			case 3:
				BuiltinCharHandler();
				break;
			case 4:
				return;
		}
	}
}

void Handler() {
	int cmd = 0;
	cin >> cmd;
	cin.ignore();
	switch(cmd) {
	case 1:
		SHandler();
		break;
	case 2:
   		SVHandler();
   		break;
   	case 3:
    	CHandler();
   		break;
   	case 4:
   		BHandler();
   		break;
   	case 5:
   		exit(1);
   }
}

void printMenu() {
   cout << "1. String" << endl;
   cout << "2. StringView" << endl;
   cout << "3. Char" << endl;
   cout << "4. Builtin" << endl;
   cout << "5. Exit" << endl;
   cout << "> ";
}

void init() {
   setvbuf(stdin, 0, 2, 0);
   setvbuf(stdout, 0, 2, 0);
   setvbuf(stderr, 0, 2, 0);
   sv_init = "EMPTY";
}

int main() {
	init();
	while(1) {
		printMenu();
		Handler();
	}
}


//  g++ -o chall chall.cpp
#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <sstream>

using namespace std;

const string ENTER_PROMPT("Enter a string:");
const string COMMAND_PROMPT("Enter command:");
const string PEEK_CMD("peek");
const string POKE_CMD("poke");
const string QUIT_CMD("quit");
const string BYE_MSG("Bye bye!");
const string UNKNOWN_CMD("Unknown command!");
const map<string, string> HELP {
  {PEEK_CMD, string("peek <integer a>: gets the ascii value of character at index a")},
  {POKE_CMD, string("poke <integer a> <integer b>: changes character at index a to ascii value b")}
};

void win() {
  ifstream in("flag.txt");
  string flag;
  in >> flag;
  cout << flag << endl;
}

int main() {
  cout.setf(ios::unitbuf);
  cout << ENTER_PROMPT << endl;
  string s;
  getline(cin, s);
  if (s.size() < 0x20)
    return 0;
  while (true) {
    cout << COMMAND_PROMPT << endl;
    string line;
    getline(cin, line);
    istringstream iss(line);
    string command;
    iss >> command;
    if (command == POKE_CMD) {
      int x, y;
      if (!(iss >> x >> y)) {
        cout << HELP.at(POKE_CMD) << endl;
        continue ;
      }
      s[x] = char(y);
    } else if (command == PEEK_CMD) {
      int x;
      if (!(iss >> x)) {
        cout << HELP.at(PEEK_CMD) << endl;
        continue ;
      }
      cout << int(s[x]) << endl;
    } else if (command == QUIT_CMD) {
      cout << BYE_MSG << endl;
      break ;
    } else {
      cout << UNKNOWN_CMD << endl;
      continue ;
    }
  }
  return 0;
}

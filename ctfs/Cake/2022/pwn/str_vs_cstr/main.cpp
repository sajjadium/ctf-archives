#include <array>
#include <iostream>

struct Test {
  Test() { std::fill(_c_str, _c_str + 0x20, 0); }
  char* c_str() { return _c_str; }
  std::string& str() { return _str; }

private:
  __attribute__((used))
  void call_me() {
    std::system("/bin/sh");
  }

  char _c_str[0x20];
  std::string _str;
};

int main() {
  Test test;

  std::setbuf(stdin, NULL);
  std::setbuf(stdout, NULL);

  std::cout << "1. set c_str" << std::endl
            << "2. get c_str" << std::endl
            << "3. set str" << std::endl
            << "4. get str" << std::endl;

  while (std::cin.good()) {
    int choice = 0;
    std::cout << "choice: ";
    std::cin >> choice;

    switch (choice) {
      case 1: // set c_str
        std::cout << "c_str: ";
        std::cin >> test.c_str();
        break;

      case 2: // get c_str
        std::cout << "c_str: " << test.c_str() << std::endl;
        break;

      case 3: // set str
        std::cout << "str: ";
        std::cin >> test.str();
        break;

      case 4: // get str
        std::cout << "str: " << test.str() << std::endl;
        break;

      default: // otherwise exit
        std::cout << "bye!" << std::endl;
        return 0;
    }
  }
  
  return 1;
}

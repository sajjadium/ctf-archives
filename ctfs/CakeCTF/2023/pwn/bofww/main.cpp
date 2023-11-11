#include <iostream>

void win() {
  std::system("/bin/sh");
}

void input_person(int& age, std::string& name) {
  int _age;
  char _name[0x100];
  std::cout << "What is your first name? ";
  std::cin >> _name;
  std::cout << "How old are you? ";
  std::cin >> _age;
  name = _name;
  age = _age;
}

int main() {
  int age;
  std::string name;
  input_person(age, name);
  std::cout << "Information:" << std::endl
            << "Age: " << age << std::endl
            << "Name: " << name << std::endl;
  return 0;
}

__attribute__((constructor))
void setup(void) {
  std::setbuf(stdin, NULL);
  std::setbuf(stdout, NULL);
}

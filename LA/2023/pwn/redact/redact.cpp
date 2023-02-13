#include <algorithm>
#include <iostream>
#include <string>

int main() {
  std::cout << "Enter some text: ";
  std::string text;
  if (!std::getline(std::cin, text)) {
    std::cout << "Failed to read text\n";
    return 1;
  }
  std::cout << "Enter a placeholder: ";
  std::string placeholder;
  if (!std::getline(std::cin, placeholder)) {
    std::cout << "Failed to read placeholder\n";
    return 1;
  }
  std::cout << "Enter the index of the stuff to redact: ";
  int index;
  if (!(std::cin >> index)) {
    std::cout << "Failed to read index\n";
    return 1;
  }
  if (index < 0 || index > text.size() - placeholder.size()) {
    std::cout << "Invalid index\n";
    return 1;
  }
  std::copy(placeholder.begin(), placeholder.end(), text.begin() + index);
  std::cout << text << '\n';
}

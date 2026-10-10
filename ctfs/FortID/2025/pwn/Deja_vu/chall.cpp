// g++ -o chall chall.cpp --static

#include <functional>
#include <iostream>
#include <string>

using namespace std;

// Decorator factory: returns a function that adds a prefix
auto make_prefix_decorator(const char* prefix) {
    return new function<void(const char*)>([prefix](const char *input) {
        puts(prefix);
        puts(input);
    });
}

int main() {
    cout.setf(ios::unitbuf);
    // Get the name from user
    cout << "Enter your name: ";
    string name;
    getline(cin, name);
    // Create a decorator that prints with "Hello, " prefix
    auto decorator = make_prefix_decorator("Hello, ");
    // Use the decorator
    (*decorator)(name.c_str());
    // Clean up
    delete[] decorator; 
    return 0;
}
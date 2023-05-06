//Name:  theKidOfArcrania
//Class: 7331 (It's a very l33t class :3 )
//Date:  29 April 2018

// Header file for String class

#ifndef _H_STRING2_ //Make sure that string class is not defined twice
#define _H_STRING2_

#include <iostream>
#include <cstdint>
#include <cstring>

class Char {
  public:
    char ch; 

    Char() : ch(0) {}

    Char(char ch) : ch(ch) {}

    ~Char() {}
};

Char* strdup2(const char *);
Char* strdup2(const Char *, uint64_t len);

// Why do we have to separate out this declaration of the String class? Wouldn't
// it be easier to maintain and find all my code if it were all in one file?
//
// Though, I'm glad I can still *technically* put one/two liners in here ;)
class String {
  private:
    // Fields for a String object
    Char*    arr;
    uint64_t size;
  public:
    // Default constructor
    String() : String("") { }

    // Creating a string object from c-string
    String(const char* str) : arr(strdup2(str)), size(strlen(str)) { }

    // Creating a new string from a Char array
    String(Char* arr) : arr(arr) {}

    // Compatibility with std::string class
    String(const std::string& str) : arr(strdup2((const Char*)str.c_str(), str.size())), size(str.size()) { }

    // Copy constructor
    String(const String& other) : arr(nullptr) {
      *this = other;
    }

    // Move constructor
    String(String&& other) : arr(nullptr) {
      *this = other;
    }


    // Destructor
    ~String() {
      delete[] arr; // Deallocate char array
    }

    // Copy assignment
    String& operator=(const String& other);

    // Move assignment
    String& operator=(String&& other);

    // Accessor methods
    const char* c_str() {
      return reinterpret_cast<char*>(arr);
    }

    uint64_t length() {
      return size;
    }

    // Access the char element using subscription operator
    // Like this: str[5]
    Char& operator[](uint64_t ind) {
      return arr[ind];
    }
    const Char& operator[](uint64_t ind) const {
      return arr[ind];
    }

    // Appending two strings together
    String operator+(const String& other) const;

    // TODO: implement +=
    
    // Input and output stuff
    friend std::ostream& operator<<(std::ostream& out, const String& str);
    friend std::istream& operator>>(std::istream& in, String& str);
};

#endif

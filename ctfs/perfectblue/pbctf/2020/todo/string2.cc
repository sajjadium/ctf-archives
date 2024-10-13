//Name:  theKidOfArcrania
//Class: 7331 (It's a very l33t class :3 )
//Date:  29 April 2018

// Implementation file for String class.
// (Why is this file so empty?)

#include "string2.h"

// Special dup function
Char* strdup2(const char *str) {
  uint64_t len = strlen(str);
  Char *ret = new Char[len];
  while (len --> 0) {
    ret[len] = Char(str[len]);
  }
  return ret;
}

Char* strdup2(const Char *str, uint64_t len) {
  Char *ret = new Char[len];
  while (len --> 0) {
    ret[len] = Char(str[len]);
  }
  return ret;
}

// Copy assignment
String& String::operator=(const String& other) {
  delete []arr; // Free old char array
  size = other.size;
  arr = strdup2(other.arr, size);
  return *this;
}

// Move assignment
String& String::operator=(String&& other) {
  delete []arr; // Free old char array
  size = other.size;
  arr = other.arr;

  other.arr = nullptr;
  return *this;
}

// Append two strings
String String::operator+(const String& other) const {
  Char* buff = new Char[size + other.size + 1];

  buff[0] = 0;
  uint64_t x = 0;
  for (uint64_t y = 0; y < size; y++) buff[x++] = arr[y];
  for (uint64_t y = 0; y < other.size; y++) buff[x++] = other.arr[y];

  return String(buff);
}

// Write to ostream
std::ostream& operator<<(std::ostream& out, const String& str) {
  out << (char*)str.arr;
  return out;
}

// Read from istream
std::istream& operator>>(std::istream& in, String& str) {
  std::string tmp;
  getline(in, tmp);
  str = String(tmp);
  return in;
}

#ifndef USER_HPP
#define USER_HPP

#include <string>
#include <map>
#include <iostream>

enum class Perms
{
  ADMIN = 0,
  USER = 1000,
};

class User
{
  private:
    std::string username_;
    std::string password_;
    std::map<size_t, char*> ratings_;
    Perms user_level_;

  public:
    User(std::string username, std::string password, Perms user_level);
    ~User() = default;
    User(const User &copy) = delete;
    std::string getUsername();
    Perms getUserLevel();
    void insertRating(char *rating);
    void removeRating(size_t index);
    void showRatings();
};

#endif
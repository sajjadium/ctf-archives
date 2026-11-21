#include "user.hpp"

User::User(std::string username, std::string password, Perms user_level) :
username_(username), password_(password), user_level_(user_level)
{}

std::string User::getUsername()
{
  return username_;
}

Perms User::getUserLevel()
{
  return user_level_;
}

void User::insertRating(char *rating)
{
  if (ratings_.size() >= 3)
  {
    std::cout << "Maximum amount of ratings reached!" << std::endl;
    return;
  }
  else
  {
    ratings_.insert({ratings_.size() + 1, rating});
    std::cout << "Successfully added rating" << std::endl;
    return;
  }
}

void User::removeRating(size_t index)
{
  if (ratings_.empty())
  {
    std::cout << "No ratings to delete" << std::endl;
    return;
  }
  else if (index >= ratings_.size() + 1 | index < 1)
  {
    std::cout << "Invalid Index" << std::endl;
    return;
  }
  else
  {
    delete ratings_.at(index);
    std::cout << "Removed rating " << index << std::endl;
    return;
  }
}

void User::showRatings()
{
  std::cout << "Your ratings: " << std::endl;
  for (auto rating : ratings_)
  {
    std::cout << rating.first << ": " << rating.second << std::endl;
  }
  return;
}
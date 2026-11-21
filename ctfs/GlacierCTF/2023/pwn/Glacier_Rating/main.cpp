#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include "user.hpp"


void buffering()
{
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}


void welcome()
{
  std::cout << "Welcome to 'Glacier rating'!\nYour trusted and secure site to rate mountains." << std::endl;
}

User *authenticateUser()
{
  std::string username;
  std::string password;

  std::cout << "Enter username: ";
  std::getline(std::cin, username);
  std::cout << "\nEnter password: ";
  std::getline(std::cin, password);

  std::cout << std::endl;

  return new User(username, password, Perms::USER);
}


int getChoice()
{

  while (true)
  {
    int choice = 0;
    std::cout << "1. Create a rating" << std::endl;
    std::cout << "2. Delete a rating" << std::endl;
    std::cout << "3. Show a rating" << std::endl;
    std::cout << "4. Scream into the mountains" << std::endl;
    std::cout << "5. Do admin stuff" << std::endl;
    std::cout << "6. Exit" << std::endl;

    std::cout << "> ";
    scanf("%d", &choice);
    getchar();
    if (choice < 1 | choice > 5)
    {
      std::cout << "Invalid choice" << std::endl << std::endl;
    }
    else
      return choice;
  }
}

void writeRating(User *user)
{
  char *buffer = new char[24];

  std::cout << "Give me your rating" << std::endl;
  std::cout << "> ";
  fgets(buffer, 24, stdin);
  user->insertRating(buffer);
  return;
}

void deleteRating(User *user)
{
  size_t index = 0;
  std::cout << "Which rating do you want to remove?" << std::endl;
  std::cout << "> ";
  scanf("%zd", &index);
  getchar();
  user->removeRating(index);
  return;
}

void showRatings(User *user)
{
  user->showRatings();
  return;
}

void scream(User *user)
{
  std::cout << "Now scream to your hearts content!" << std::endl;
  std::string line;
  std::vector<std::string> lines;
  while (line != "quit")
  {
    std::getline(std::cin, line);
    lines.push_back(line);
  }
  return;
}

void doAdminStuff(User *user)
{
  if (user->getUserLevel() != Perms::ADMIN)
  {
    std::cout << "You are not an admin!" << std::endl;
    exit(1);
  }
  else if (user->getUserLevel() == Perms::ADMIN)
  {
    std::ifstream flag_stream("./flag.txt");
    std::string flag;
    std::getline(flag_stream, flag);
    flag_stream.close();
    std::cout << "Verified permissions" << std::endl;
    std::cout << "Here is your flag: " << flag << std::endl;
    exit(0);
  }
}


int main()
{
  buffering();

  int choice = 0;
  welcome();

  User *user = authenticateUser();

  std::cout << "Greetings, " << user->getUsername() << std::endl;
  std::cout << "What do you want to do?" << std::endl;


  while (true)
  {
    choice = getChoice();

    switch (choice)
    {
      case 1:
        writeRating(user);
        break;
      case 2:
        deleteRating(user);
        break;
      case 3:
        showRatings(user);
        break;
      case 4:
        scream(user);
        break;
      case 5:
        doAdminStuff(user);
        break;
      default:
        exit(0);
    }
    std::cout << std::endl;
  }
  return 0;
}

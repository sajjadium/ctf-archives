#include <cstdlib>
#include <fstream>
#include <iostream>
#include <unordered_map>

#define ELF_MAX_NAGHTY_COUNT 16

std::unordered_map<std::string, std::string> naughty_list{
    {"PinkiePie", "Very naughty"}};

void menu()
{
    std::cout << "1. Ask PinkiePie for the flag" << std::endl;
    std::cout << "2. Query naughty list" << std::endl;
    std::cout << "3. Add to naughty list" << std::endl;
}

void ask_pinkiepie()
{
    bool pinkiepie_naughty = false;
    auto it = naughty_list.begin();

    for (int i = 0; i < ELF_MAX_NAGHTY_COUNT; i++)
    {
        if (it->first == "PinkiePie")
        {
            pinkiepie_naughty = true;
            break;
        }
        ++it;
        if (it == naughty_list.end())
        {
            break;
        }
    }

    if (pinkiepie_naughty)
    {
        std::cout
            << "PinkiePie will not tell you the flag if he is on the naughty list"
            << std::endl;
    }
    else
    {
        std::cout << "PinkiePie is satisfied. Here is your flag!" << std::endl;
        std::ifstream flag_file{"/flag.txt"};

        std::cout << flag_file.rdbuf() << std::endl;
    }
}

bool is_naughty(const std::string &name) { return !(naughty_list[name] == ""); }

void add_to_list(const std::string &name)
{
    if (naughty_list.size() == ELF_MAX_NAGHTY_COUNT)
    {
        std::cout << "Adding this many people requires authorization from Elf "
                     "Resources.";
        return;
    }
    else
    {
        naughty_list.insert({name, "Naughty"});
    }
}

int main()
{
    int choice;

    while (true)
    {
        menu();

        std::cin >> choice;

        switch (choice)
        {
        case 1:
        {
            ask_pinkiepie();
        }
        break;
        case 2:
        case 3:
        {
            std::string name;
            std::cout << "Name: ";
            std::cout.flush();
            std::cin >> name;

            if (choice == 2)
            {
                if (is_naughty(name))
                {
                    std::cout << name << " is naughty!" << std::endl;
                }
                else
                {
                    std::cout << name << " is not naughty!" << std::endl;
                }
            }
            else if (choice == 3)
            {
                add_to_list(name);
            }
            else
            {
                std::cout
                    << "Tampering alert triggered. This incident will be reported!"
                    << std::endl;
            }
        }
        break;
        default:
        {
            exit(1);
        }
        }
    }
}

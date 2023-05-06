

#include<string>
#include<unordered_map>
#include<set>
#include<utility>
#include<iostream>
#include<iomanip>
#include<unistd.h>
#include<signal.h>
#include<limits.h>
#include<string.h>

uint notes_counter = 0;
void *notes_by_idx[16];
std::unordered_map<uint, void*> notes_by_key;
std::set<std::pair<uint, uint>> ind_key_set_pair;

void sig_alarm_handler(int signum)  {
	std::cout << "Connect Timeout" << std::endl ;
	exit(1);
}

void init() {
	setvbuf(stdout,0,2,0);
	signal(SIGALRM,sig_alarm_handler);
	alarm(60);
}

void menu() {
    std::cout << "1. Add new note" << std::endl;
    std::cout << "2. Delete note" << std::endl;
    std::cout << "3. Edit note" << std::endl;
    std::cout << "4. Show note details" << std::endl;
    std::cout << "5. Exit" << std::endl;
    std::cout << "> ";
    return;
}

void add_note() {
    uint key, size;
    std::cout << "Enter Key:" << std::endl;
    std::cin >> key;
    std::cout << "Enter Size:" << std::endl;
    std::cin >> size;
    std::cin.clear(); std::cin.ignore(INT_MAX,'\n'); 
    notes_by_idx[notes_counter] = malloc(size);
    notes_by_key[key] = notes_by_idx[notes_counter];
    ind_key_set_pair.insert(std::make_pair(notes_counter, key));
    std::cout << "Enter Content:" << std::endl;
    fgets((char*) notes_by_idx[notes_counter], size, stdin);
    std::cout << "New note at index " << notes_counter << " with key " << key << std::endl;
    notes_counter++;
}

void delete_note() {
    uint index, key;
    std::cout << "Enter Index: ";
    std::cin >> index;
    if(index >= notes_counter)   {
        std::cout << "Error" << std::endl;
        return;
    }
    std::cout << "Enter Key: "; 
    std::cin >> key;
    const bool is_in_set = ind_key_set_pair.find(std::make_pair(index, key)) != ind_key_set_pair.end();
    if(is_in_set)   {
        free(notes_by_idx[index]);
        notes_by_idx[index] = NULL;
        notes_by_key[key] = NULL;
        ind_key_set_pair.erase(std::make_pair(index, key));
        std::cout << "Done!" << std::endl;
        return;
    }
    else    {
        std::cout << "Error" << std::endl;
        return;
    }
}

void edit_note() {
    uint choice, index, key;
    std::cout << "Edit note by:" << std::endl;
    std::cout << "1. Index" << std::endl;
    std::cout << "2. Key" << std::endl;
    std::cin >> choice;
    switch (choice) {
        case 1:
            std::cout << "Enter Index: ";
            std::cin >> index;
            if(index >= notes_counter)   {
                std::cout << "Error" << std::endl;
                return;
            }
            std::cin.clear(); std::cin.ignore(INT_MAX,'\n'); 
            std::cout << "Enter Content: ";
            fgets((char*) notes_by_idx[index], strlen((char*) notes_by_idx[index])+1, stdin);
	    std::cout << "Done!" << std::endl;
            break;
        case 2:
            std::cout << "Enter Key: ";
            std::cin >> key;
            if(notes_by_key.find(key) == notes_by_key.end())   {
                std::cout << "Error" << std::endl;
                return;
            }
            std::cin.clear(); std::cin.ignore(INT_MAX,'\n'); 
            std::cout << "Enter Content: ";
            fgets((char*) notes_by_key[key], strlen((char*) notes_by_key[key])+1, stdin);
            std::cout << "Done!" << std::endl;
            break;
        default:
            std::cout << "Error" << std::endl;
            break;
    }
}

void show_note() {
    uint choice, index, key;
    std::cout << "Show note by:" << std::endl;
    std::cout << "1. Index" << std::endl;
    std::cout << "2. Key" << std::endl;
    std::cin >> choice;
    switch (choice) {
        case 1:
            std::cout << "Enter Index: ";
            std::cin >> index;
            if(index >= notes_counter)   {
                std::cout << "Error" << std::endl;
                return;
            }
            puts((char*) notes_by_idx[index]);
            break;
        case 2:
            std::cout << "Enter Key: ";
            std::cin >> key;
            if(notes_by_key.find(key) == notes_by_key.end())   {
                std::cout << "Error" << std::endl;
                return;
            }
            puts((char*) notes_by_key[key]);
            break;
        default:
            std::cout << "Error" << std::endl;
            break;
    }
}

void vuln() {
    int choice=-1;

    while(1)    {
        menu();
        std::cin >> choice;
		if(!std::cin.good())	{
			std::cout << "Error" << std::endl;
			exit(-1);
		}
        switch (choice) {
        case 1:
            add_note();
            break;
        case 2:
            delete_note();
            break;
        case 3:
            edit_note();
            break;
        case 4:
            show_note();
            break;
        case 5:
            std::cout << "Bye bye" << std::endl;
            exit(0);
        default:
            std::cout << "Error" << std::endl;
            break;
        }
    }
    return;
}

int main(int argc, char const *argv[])
{
    init();
    vuln();
    return 0;
}

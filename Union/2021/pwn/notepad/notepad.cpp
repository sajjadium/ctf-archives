#include <algorithm>
#include <cstring>
#include <iostream>
#include <vector>
#include <unistd.h>
#include "notepad.h"

void printTopMenu()
{
    std::cout << "1. Add note" << std::endl;
    std::cout << "2. Find existing note by name" << std::endl;
    std::cout << "3. Manage note" << std::endl;
    std::cout << "> ";
}

void printNoteMenu()
{
    std::cout << "1. View note" << std::endl;
    std::cout << "2. Edit note" << std::endl;
    std::cout << "3. Lock note" << std::endl;
    std::cout << "4. Back" << std::endl;
    std::cout << "> ";
}

uint64_t readInt()
{
    uint64_t val;
    char buf[32];
    std::fgets(buf, sizeof(buf), stdin);
    return strtoul(buf, NULL, 10);
}

std::string readLine()
{
    char buf[1024];
    std::fgets(buf, sizeof(buf), stdin);
    size_t n = std::strlen(buf);
    if (n > 0 && buf[n-1] == '\n') {
        buf[n-1] = 0;
    }
    return std::string(buf, n);
}

void handleNote(Notepad& notepad)
{
    while (true) {
        printNoteMenu();
        unsigned long choice = readInt();
        std::printf("Your choice: %lu\n", choice);
        switch (choice) {
            case 1: {
                notepad.printCurrentNote();
                break;
            }
            case 2: {
                std::cout << "Name: " << std::endl;
                std::string name(readLine());
                std::cout << "Content: " << std::endl;
                std::string content(readLine());
                notepad.editNote(name, content);
                break;
            }
            case 3: {
                std::cout << "Key: " << std::endl;
                std::string key(readLine());
                std::cout << "Key size: " << std::endl;
                size_t key_size = readInt();
                notepad.lockCurrentNote(key, key_size);
                break;
            }
            case 4: {
                return;
            }
        }
    }
}

void setup()
{
    std::setvbuf(stdin, NULL, _IONBF, 0);
    std::setvbuf(stdout, NULL, _IONBF, 0);
    std::setvbuf(stderr, NULL, _IONBF, 0);
    alarm(60);
}

int main()
{
    setup();
    Notepad notepad;
    std::cout << "Welcome to the world's most modern notepad." << std::endl;
    while (true) {
        printTopMenu();
        auto choice = readInt();
        switch (choice) {
            case 1: {
                std::cout << "Name: " << std::endl;
                std::string name(readLine());
                std::cout << "Content: " << std::endl;
                std::string content(readLine());
                notepad.createNote(name, content);
                break;
            }
            case 2: {
                std::cout << "Search term: " << std::endl;
                std::string search(readLine());
                auto note = notepad.selectNoteByName(search);
                if (note == false) {
                    std::cout << "Note not found" << std::endl;
                }
                else {
                    std::cout << "Found note!" << std::endl;
                }
                break;
            }
            case 3: {
                handleNote(notepad);
                break;
            }
        }
    }
}

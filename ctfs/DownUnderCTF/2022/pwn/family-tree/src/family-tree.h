#include <string>
#include <iostream>
#include <vector>
#include <list>
#include <unordered_set>
#include <unordered_map>

#include "person.h"

#define MAX_ROOTS 0xFF;

using namespace std;

class FamilyTree
{

public:
    FamilyTree()
        : root_(new Person("ROOT")) {}

    Person *GetRoot();

    void AddRoot(Person *);
    void AddPerson(Person *);
    void CreatePerson(string, list<string>);
    void DeletePerson(string);
    void RenamePerson(string, string);
    void AddMetadataToPerson(string);
    void DumpMetadata(string);
    void Trim();
    void Print();
    void ProcessCommand();

private:
    Person *root_;
    unordered_map<string, Person *> people_;
};
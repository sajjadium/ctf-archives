#ifndef PERSON_H
#define PERSON_H

#include <list>
#include <string>
#include <iostream>
#include <stddef.h>

#include "ftobject.h"
#include "ftallocator.h"
#include "metadata.h"

using namespace std;

class Person : public FTObject
{
public:
    Person(string name)
        : name_(name),
          md_(0),
          children_(list<Person *>{}) {}

    ~Person()
    {
        cout << "tried to delete a person" << endl;
    }

    void *operator new(size_t size)
    {
        return FTAllocator::Alloc();
    }
    string GetName();
    void SetName(string name);
    Person *GetChildWithPath(Person *, list<string>);
    Person *GetChild(string);
    void DeleteChild(string);
    void AddChildWithPath(Person *, list<string>);
    void DeleteChildWithPath(list<string>);
    void RenameChildWithPath(string, list<string>);
    list<Person *> GetChildren();
    void SetMetadataWithPath(list<string>);
    void SetMetadata();
    void DumpMetadata();
    void DumpMetadataWithPath(list<string>);
    Metadata *GetMetadata();
    void Print(int);
    void Mark();

private:
    string name_;
    Metadata *md_;
    list<Person *> children_;
};

#endif
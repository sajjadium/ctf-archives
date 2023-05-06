#include <string>
#include <unistd.h>
#include <list>

#include "person.h"
#include "ftallocator.h"


string Person::GetName()
{
    return this->name_;
}

void Person::SetName(string name)
{
    this->name_ = name;
}

Person *Person::GetChild(string name)
{
    for (Person *p : this->children_)
    {
        if (p->GetName() == name)
        {

            return p;
        }
    }
    return nullptr;
}

void Person::DeleteChild(string name)
{
    for (auto it = this->children_.begin(); it != this->children_.end(); it++)
    {
        if ((*it)->GetName() == name)
        {
            this->children_.erase(it);
            return;
        }
    }
    return;
}

void Person::RenameChildWithPath(string new_name, list<string> path)
{
    if (path.size() == 0)
    {
        this->SetName(new_name);
    }
    else
    {
        Person *target = this->GetChild(path.front());
        if (!target)
        {
            cout << "there was no child: \"" << path.front()
                 << "\" for: \"" << this->GetName() << std::endl;
            return;
        }

        path.pop_front();
        target->RenameChildWithPath(new_name, path);
    }
}

void Person::AddChildWithPath(Person *p, list<string> path)
{
    if (path.size() == 0)
    {

        this->children_.push_back(p);
    }
    else
    {

        Person *target = this->GetChild(path.front());
        if (!target)
        {
            cout << "there was no child: \"" << path.front()
                 << "\" for: \"" << this->GetName() << std::endl;
            return;
        }

        path.pop_front();
        target->AddChildWithPath(p, path);
    }
}

Person *Person::GetChildWithPath(Person *p, list<string> path)
{
    if (path.size() == 0)
    {
        return this->GetChild(p->GetName());
    }
    else
    {

        Person *target = this->GetChild(path.front());
        if (!target)
        {
            cout << "there was no child: \"" << path.front()
                 << "\" for: \"" << this->GetName() << std::endl;
            return NULL;
        }

        path.pop_front();
        return target->GetChildWithPath(p, path);
    }
}

void Person::DeleteChildWithPath(list<string> path)
{
    if (path.size() == 1)
    {
        this->DeleteChild(path.front());
    }
    else
    {

        Person *target = this->GetChild(path.front());
        if (!target)
        {
            cout << "there was no child: \"" << path.front()
                 << "\" for: \"" << this->GetName() << std::endl;
            return;
        }

        path.pop_front();
        target->DeleteChildWithPath(path);
    }
}

list<Person *> Person::GetChildren()
{
    return this->children_;
}

Metadata *Person::GetMetadata()
{
    return this->md_;
}

void Person::Mark()
{

    if (this->md_)
    {
        this->md_->Mark();
    }

    // Darken to grey
    if (this->IsWhite())
    {
        this->SetGrey();
        for (Person *p : this->GetChildren())
        {
            p->Mark();
        }
    }

    // Darken to black if not already
    if (this->IsGrey())
    {
        this->SetBlack();
    }
}

void Person::SetMetadataWithPath(list<string> path)
{
    if (path.size() == 0)
    {
        this->SetMetadata();
    }
    else
    {

        Person *target = this->GetChild(path.front());
        if (!target)
        {
            cout << "there was no child: \"" << path.front()
                 << "\" for: \"" << this->GetName() << std::endl;
            return;
        }

        path.pop_front();
        target->SetMetadataWithPath(path);
    }
}

void Person::DumpMetadataWithPath(list<string> path)
{
    if (path.size() == 0)
    {
        this->DumpMetadata();
    }
    else
    {

        Person *target = this->GetChild(path.front());
        if (!target)
        {
            cout << "there was no child: \"" << path.front()
                 << "\" for: \"" << this->GetName() << std::endl;
            return;
        }

        path.pop_front();
        target->DumpMetadataWithPath(path);
    }
}

void Person::DumpMetadata()
{
    if (!this->md_)
    {
        std::cout << "There is no metadata for this person" << std::endl;
        return;
    }
    else
    {
        write(1, this->md_->data, METADATA_SZ);
        std::cout << std::endl;
    }
}

void Person::SetMetadata()
{

    if (!this->md_)
    {
        this->md_ = new Metadata();
    }

    std::cout << "metadata> ";
    read(0, this->md_->data, METADATA_SZ);
}

void Person::Print(int indent)
{

    std::cout << "- " << this->GetName() << std::endl;
    auto children = this->GetChildren();

    if (children.size())
    {
        for (int i = 0; i < indent + 1; i++)
        {
            std::cout << "  ";
        }
        std::cout << "Children: " << std::endl;
        for (auto c = children.begin(); c != children.end(); c++)
        {

            for (int i = 0; i < indent + 1; i++)
            {
                std::cout << "  ";
            }
            (*c)->Print(indent + 1);
            std::cout << std::endl;
        }
    }
}

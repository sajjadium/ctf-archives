                    
#include "family-tree.h"
#include "person.h"

list<string> split_list(string s, string delimiter)
{
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    string token;
    list<string> res;

    while ((pos_end = s.find(delimiter, pos_start)) != string::npos)
    {
        token = s.substr(pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back(token);
    }
    res.push_back(s.substr(pos_start));
    return res;
}

Person *FamilyTree::GetRoot()
{
    return this->root_;
}

void FamilyTree::CreatePerson(string name, list<string> paths)
{
    Person *new_child = new Person(name);
    while (!paths.empty())
    {
        string path = paths.front();
        paths.pop_front();
        list<string> path_list = split_list(path, ".");

        if (path_list.front() != "ROOT")
        {
            cout << "people must be added from the root" << endl;
            return;
        }

        path_list.pop_front();
        this->root_->AddChildWithPath(new_child, path_list);
    }
    return;
}

void FamilyTree::DeletePerson(string path)
{
    list<string> path_list = split_list(path, ".");
    if (path_list.front() != "ROOT")
    {
        cout << "people must be deleted from the root" << endl;
        return;
    }

    if (path_list.size() == 1)
    {
        cout << "you cannot delete the root" << endl;
        return;
    }

    path_list.pop_front();
    this->root_->DeleteChildWithPath(path_list);
}

void FamilyTree::RenamePerson(string new_name, string path)
{
    list<string> path_list = split_list(path, ".");
    if (path_list.front() != "ROOT")
    {
        cout << "people must be renamed from the root" << endl;
        return;
    }

    path_list.pop_front();
    this->root_->RenameChildWithPath(new_name, path_list);

    return;
}

void FamilyTree::AddMetadataToPerson(string path)
{
    list<string> path_list = split_list(path, ".");
    if (path_list.front() != "ROOT")
    {
        cout << "path must begin at the root" << endl;
        return;
    }
    path_list.pop_front();
    this->root_->SetMetadataWithPath(path_list);
}

void FamilyTree::DumpMetadata(string path)
{
    list<string> path_list = split_list(path, ".");
    if (path_list.front() != "ROOT")
    {
        cout << "path must begin at the root" << endl;
        return;
    }
    path_list.pop_front();
    this->root_->DumpMetadataWithPath(path_list);
}

void FamilyTree::ProcessCommand()
{
    string input;
    getline(cin, input);
    list<string> command = split_list(input, " ");
    string comm = command.front();
    command.pop_front();

    if (comm == "person")
    {
        if (command.size() < 2)
        {
            cout << "incorrect number of arguments" << std::endl;
            return;
        }
        string name = command.front();
        command.pop_front();
        this->CreatePerson(name, command);
    }

    else if (comm == "dump")
    {
        if (command.size() != 1)
        {
            cout << "incorrect number of arguments" << std::endl;
            return;
        }
        string path = command.front();
        this->DumpMetadata(path);
    }

    else if (comm == "metadata")
    {
        if (command.size() != 1)
        {
            cout << "incorrect number of arguments" << std::endl;
            return;
        }

        string path = command.front();

        this->AddMetadataToPerson(path);
    }

    else if (comm == "rename")
    {
        if (command.size() != 2)
        {
            cout << "incorrect number of arguments" << std::endl;
            return;
        }
        string name = command.front();
        command.pop_front();
        string path = command.front();
        command.pop_front();
        this->RenamePerson(name, path);
    }

    else if (comm == "delete")
    {
        if (command.size() != 1)
        {
            cout << "incorrect number of arguments" << std::endl;
            return;
        }
        string path = command.front();
        command.pop_front();
        this->DeletePerson(path);
    }
    else if (comm == "print")
    {
        this->Print();
    }
}

void FamilyTree::Print()
{
    list<Person *> queue = {};
    list<Person *> map = this->root_->GetChildren();

    for (auto p : map)
    {
        queue.push_back(p);
    }

    while (!queue.empty())
    {
        Person *current = queue.front();
        queue.pop_front();
        list<Person *> current_children = current->GetChildren();

        for (auto p : current_children)
        {

            queue.push_back(p);
        }
        current->Print(0);
    }
}

#include <iostream>

#include "ftallocator.h"
#include "family-tree.h"
#include "person.h"
#include "ftobject.h"

using namespace std;

void print_welcome()
{

    std::cout << "=== Family Tree Manager (v0.1.0) ===" << std::endl;
}

int main()
{
    std::setbuf(stdin, NULL);
    std::setbuf(stdout, NULL);

    FTAllocator::Init();
    FamilyTree *tree = new FamilyTree();
    FTAllocator::SetRoot(tree->GetRoot());

    print_welcome();

    while (1)
    {
        std::cout << "> ";
        tree->ProcessCommand();
    }
}
//Overflow on the heap to overwrite function pointer, then call that function


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct coordinates
{
    char userinput[64];  
    short choice;
};

struct jmptable
{
    void (*hyperJump1)();
    void (*hyperJump2)();
    void (*hyperJump3)();
    
};

void jumpToHoth()
{
    printf("Jumping to Hoth...\n");
}
void jumpToCoruscant()
{
    printf("Jumping to Coruscant...\n");
}
void jumpToEndor()
{
    printf("Jumping to Endor...\n");
}

void jumpToNaboo()
{
    printf("Jumping to Naboo...\n *Run this on the server to get the flag. *\n");
}

int main() {

  
    char* ptr;
    
    struct coordinates* ptr1;
    struct jmptable* ptr2;
    
    ptr1 = malloc(sizeof(struct coordinates));
    ptr2 = malloc(sizeof(struct jmptable));
    
    ptr2->hyperJump1 = &jumpToHoth;
    ptr2->hyperJump2 = &jumpToCoruscant;
    ptr2->hyperJump3 = &jumpToEndor;
    
    
    
    while(1)
    {
        printf("SYSTEM CONSOLE> ");
        gets(ptr1->userinput);
        ptr1->choice = strtol(ptr1->userinput, &ptr, 10);
    	
        switch( (int)ptr1->choice)
        {
            case 1:
            {
                printf("Checking navigation...\n");
                ptr2->hyperJump1();
                break;
            }

            case 2:
            {
                printf("Checking navigation...\n");
                ptr2->hyperJump2();
                break;
            }

            case 3:
            {
                printf("Checking navigation...\n");
                ptr2->hyperJump3();
                break;
            }

            case 4:
            {
                printf("Logging out\n");
                exit(0);
            }
            default:
            {
                printf("Check Systems\n");
                printf("1 - Hoth\n");
                printf("2 - Coruscant\n");
                printf("3 - Endor\n");
                printf("4 - Logout\n");
            }


        }
    }
    return 0;
}

int main() {
    // Hint: how do these values get stored?
    void* first_var;
    char* guess;
    char flag[100];
    load_flag(flag, 100);

    puts("Welcome to the most tasmastic game of all time!");
    wait_for(3);
    puts("Basically it's just too simple, I've put the");
    puts("flag into the memory and your job is ... to");
    puts("guess where it is!!");
    wait_for(2);
    puts("Have fun!");
    wait_for(1);
    puts("Oh and before you start, I'll give you a little");
    puts("hint, the address of the current stackframe I'm");
    printf("in is %p\n", (&first_var)[-2]);
    wait_for(3);
    puts("Okay anyway, back to the game. Make your guess!");
    puts("(hexadecimals only, so something like 0xA would work)");
    printf("guess> ");

    guess = read_pointer();

    wait_for(3);

    puts("Okay, prepare yourself. If you're right this");
    puts("will print out the flag");
    
    wait_for(1);
    puts("Oh, and if your wrong, this might crash and");
    puts("disconnect you\nGood luck!");

    printf("%s\n", guess);

    return 1;
}
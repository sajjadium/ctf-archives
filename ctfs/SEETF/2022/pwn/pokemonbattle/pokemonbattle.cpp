// g++ pokemonbattle.cpp -w -o pokemonbattle
#include <iostream>

struct {
    char pokemon[13]; // longest pokemon name is 12 letters (Crabominable)
    virtual void Battle() {
        printf("Let the battle begin...\n");
        // @todo: implement an actual battle
        printf("Your pokemon was defeated. You blacked out!\n");
    }
    virtual void Play() {
        printf("Choose a pokemon: ");
        std::cin.getline(pokemon, sizeof pokemon);
        printf(pokemon);
        printf(", I choose you!\n");
        Battle();
    }
} battler;

int main() {
    battler.Play();
}

void win() {
    system("cat flag.txt");
}

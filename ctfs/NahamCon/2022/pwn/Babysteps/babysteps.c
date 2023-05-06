#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>


#define BABYBUFFER 16

void setup(void) {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

void whine() {
  puts("You whine: 'WAAAAAAHHHH!! WAAH, WAAHH, WAAAAAAHHHH'\n");
}

void scream() {
  puts("You scream: 'WAAAAAAHHHH!! WAAH, WAAHH, WAAAAAAHHHH'\n");
}

void cry() {
  puts("You cry: 'WAAAAAAHHHH!! WAAH, WAAHH, WAAAAAAHHHH'\n");
}

void sleep() {
  puts("Night night, baby!\n");
  exit(-1);
}


void ask_baby_name() {
  char buffer[BABYBUFFER];
  puts("First, what is your baby name?");
  return gets(buffer);
}

int main(int argc, char **argv){
  setup();

  puts("              _)_");
  puts("           .-'(/ '-.");
  puts("          /    `    \\");
  puts("         /  -     -  \\");
  puts("        (`  a     a  `)");
  puts("         \\     ^     /");
  puts("          '. '---' .'");
  puts("          .-`'---'`-.");
  puts("         /           \\");
  puts("        /  / '   ' \\  \\");
  puts("      _/  /|       |\\  \\_");
  puts("     `/|\\` |+++++++|`/|\\`");
  puts("          /\\       /\\");
  puts("          | `-._.-` |");
  puts("          \\   / \\   /");
  puts("          |_ |   | _|");
  puts("          | _|   |_ |");
  puts("          (ooO   Ooo)");
  puts("");

  puts("=== BABY SIMULATOR 9000 ===");

  puts("How's it going, babies!!");
  puts("Are you ready for the adventure of a lifetime? (literally?)");
  puts("");
  ask_baby_name();

  puts("Pefect! Now let's get to being a baby!\n");

  char menu_option;

  do{

    puts("CHOOSE A BABY ACTIVITY");
    puts("a. Whine");
    puts("b. Cry");
    puts("c. Scream");
    puts("d. Throw a temper tantrum");
    puts("e. Sleep.");
    scanf(" %c",&menu_option);

    switch(menu_option){

      case 'a':
        whine();
        break;
      case 'b':
        cry();
        break;
      case 'c':
        scream();
        break;
      case 'd':
        scream();
        cry();
        whine();
        cry();
        scream();
        break;
      case 'e':
        sleep();
        break;

      default:
        puts("WAAAAAAHHHH, THAT NO-NO!!!\n");
        break;
    }

  }while(menu_option !='e');

}

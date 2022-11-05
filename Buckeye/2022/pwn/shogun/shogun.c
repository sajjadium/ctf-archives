#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

char* txt[] = {
    "You finally reach the village. Cheers fill the air! 'The samurai is back!' A feast is being thrown in your honor.\nBut something feels off... you feel a disturbance. ",
    "Out of the corner of your eye, you catch a glimpse of two shadowy figures speeding towards you!\nHaku's halves merge together! \"We meet again, samurai...\" He attacks you! ",
    "Suddenly, you are impaled.\nHaku's shapeshifting has finally bested you.\nThe villagers scream as Haku laughs maniacally...\n",
    "Evenly matched, you fight for hours. The villagers have all run away.\nEventually, Haku finds an opening. You are fatally struck.\n\"Farewell, samurai!! Muaaaahahahahahahaaaa!\"\n",
};

void scroll(char* txt) {
    size_t len = strlen(txt);
    for(size_t i = 0; i < len; i++) {
        char c = txt[i];
        putchar(c);
        usleep((c == '\n' ? 1000 : 50) * 1000);
    }
}

void encounter() {
    scroll(txt[1]);
    char buf2[32];
    fgets(buf2, 81, stdin);
}

int main() {
    setvbuf(stdout, 0, 2, 0);

    scroll(txt[0]);
    char buf1[24];
    fgets(buf1, 24, stdin);
    if(strncmp("Look around.", buf1, 12) == 0) {
        encounter();
        scroll(txt[3]);
    } else {
        scroll(txt[2]);
    }
}

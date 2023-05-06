#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

char* txt[] = {
    "Long ago in a distant land...\nHaku, the shapeshifting master of appsec, unleashed an UNHACKABLE binary.\nBut a foolish samurai warrior, wielding a magic terminal, stepped forth to oppose him.\nTheir name was...\n...er, what was it again? ",
    "I knew that.\nAnyway...\nWith their weapon in hand, the samurai sprung forth, and with a wide swing of their sword...\n",
    "...completely missed, and was crushed instantly by Haku's fabled finisher: exit(0).\n",
    "...slashed Haku in two!!\nAs the demon lay vulnerable, our hero prepares a final blow: "
};

void scroll(char* txt) {
    size_t len = strlen(txt);
    for(size_t i = 0; i < len; i++) {
        char c = txt[i];
        putchar(c);
        usleep((c == '\n' ? 1000 : 50) * 1000);
    }
}

int main() {
    setvbuf(stdout, 0, 2, 0);

    char response[] = "RIGHT, right.                  ";
    int outcome = 0x69696969;

    scroll(txt[0]);
    fgets(response + 14, 48, stdin);
    strcpy(response + strlen(response) - 1, ".\n");
    scroll(response);
    scroll(txt[1]);

    if(outcome == 0x4774cc) {
        char* finisher = malloc(8);
        scroll(txt[3]);
        fgets(finisher, 8, stdin);
        system(finisher);
    } else {
        scroll(txt[2]);
    }
    
    exit(0);
}
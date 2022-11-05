#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

char* txt[] = {
    "After defeating the great Haku in battle, our hero begins the journey home.\nThe forest is covered in thick brush. It is difficult to see where you are going...\nBut a samurai always knows the way home, and with a sharp sword that can cut through the foliage, there is nothing to worry about.\n...\n...suddenly, the sword is gone. It has been swept straight out of your hand!\nYou look up to see a monkey wielding your sword! What will you do? ",
    "Yes, of course. You are a great warrior! This monkey doesn't stand a chance.\nWith your inner strength, you leap to the trees, chasing the fleeing monkey for what feels like hours.\n",
    "The monkey, with great speed, quickly disappears into the trees. You have lost your sword and any hopes of getting home...\n",
    "Eventually, you lose sight of it. It couldn't have gotten far. Which way will you look? ",
    "Finally, the monkey stops and turns to you.\n\"If you wish for your weapon back, you must make me laugh.\" Holy shit. This monkey can talk. \"Tell me a joke.\" ",
    "\"BAAAAHAHAHAHAHA WOW THAT'S A GOOD ONE. YOU'RE SO FUNNY, SAMURAI.\n...NOT! THAT JOKE SUCKED!\"\nThe monkey proceeds to launch your sword over the trees. The throw was so strong that it disappeard over the horizon.\nWelp. It was a good run.\n",
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
    while(getchar() != '\n') {}
    scroll(txt[4]);
    char buf2[32];
    fgets(buf2, 49, stdin);
    scroll(txt[5]);
}

void search(char* area, int dir) {
    scroll(area);
    if(dir == 2) {
        encounter();
        exit(0);
    }
}

void chase() {
    char* locs[] = {
        "The treeline ends, and you see beautiful mountains in the distance. No monkey here.\n",
        "Tall, thick trees surround you. You can't see a thing. Best to go back.\n",
        "You found the monkey! You continue your pursuit.\n",
        "You find a clearing with a cute lake, but nothing else. Turning around.\n",
    };
    scroll(txt[3]);
    int dir;
    while(1) {
        scanf("%d", &dir);
        if(dir > 3) {
            printf("Nice try, punk\n");
        } else {
            search(locs[dir], dir);
        }
    }
}

int main() {
    setvbuf(stdout, 0, 2, 0);

    scroll(txt[0]);
    char buf1[80];
    fgets(buf1, 80, stdin);
    if(strncmp("Chase after it.", buf1, 15) == 0) {
        scroll(txt[1]);
        chase();
    } else {
        scroll(txt[2]);
    }
}

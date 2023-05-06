#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <sys/mman.h>

struct voice_recognizer {
	char words[17];
	bool bubble;
	int characteristics;
} __attribute__((packed));

void open_door()
{
	setvbuf(stdout, NULL, _IONBF, 0);
    printf("As you walk closer, it is clear that the base belongs to the space"
		   " goblins. On the wall, there are depictions of a female goblin "
		   "wearing a crown with the name \"Boblinessa\" written below.\n"
           "A similar chest as the one you found earlier lies on the table. "
		   "It opens for the same voice input as the first chest you found.\n");
    char buf[60] = { 0 };
    char done[12] = { 0 };
    printf("\"Hi, I'm the Boblinessa cult encyclopedia!\"\n");
	printf("\"So, what where you looking for?\"\n");
    while(gets(buf)) {
        if (!strcmp(buf, "open_door")) {
            printf("Oh, that's right here: %p.\n", &open_door);
        } else if (!strcmp(buf, "mprotec")) {
            printf("Ah yes, our sweet Boblinessa. She protec. She protecs right "
                   "here in fact: %p.\n", &mprotect);
        } else if (!strcmp(buf, "mattac")) {
            printf("What?! No, she would never do that...\nAlso I'm hiding "
                   "here: %p. She wouldn't even find me here...\n", &buf);
        } else if (!strcmp(buf, "quit")) {
            printf("Ta ta for now!\n");
            break;
        } else {
            printf("I don't think we have access to that right now...\n");
        }
        printf("\nOkay, so do you wanna see anything else or are you done?\n");
        gets(done);
        if (!strcmp(done, "done")) {
            return;
        }
		printf("\"So, what where you looking for?\"\n");
    }
}

void supersecret_base(void)
{
	open_door();
}

void talk_to_chest(void)
{
	setvbuf(stdout, NULL, _IONBF, 0);
	char second[20];
	printf("The chest opens up and a small, rusty laptop is unveiled\n"
		   "\"Hi, old goblin-friend! Remember the last time we saw each other?"
		   " We were hanging at our supersecret base, you know, the one"
		   " at %p!\n Ah yes, good times!\"", &supersecret_base);

	printf("The screen flickers and the computer dies. Were do you ");
	printf("wanna go now?\n");
	gets(second);
}

int open_chest()
{
	struct voice_recognizer voice;
	voice.bubble = 1;
	voice.characteristics = 37;
	printf("\"Welcome! Please identify yourself.\"\n");

	gets(voice.words);

	bool conditions_met = voice.characteristics == 25 && voice.bubble == 0;
	if (conditions_met) {
		printf("\"Unlocking... Please wait...\"\n");
	} else {
		printf("\"Wow, your voice is seems off. Not letting you in.\"\n");
	}
	return conditions_met;
}


int main()
{
	setvbuf(stdout, NULL, _IONBF, 0);
	printf("The chest glows with a faint blue tint. When you touch it, a "
		   "computery voice echoes:\n");
	if (open_chest()) {
		talk_to_chest();
	}

 	return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char nothing[] = "Nothing,";

char fruits[8][20] = 
   {"Apple,", "Banana,", "Orange,", "Strawberry,",
	"Watermelon,", "Tomato,", "Lime,", "Avocado,"};

char vegetables[8][20] = 
	{"Carrot,", "Cucumber,", "Corn,", "Zucchini,",
	"Potato,", "Asparagus,", "Broccoli,", "Cabbage,"};

char meats[8][20] = 
	{"Pork,", "Beef,", "Chicken,", "Turkey,"
	"Duck,", "Lamb,", "Goat,", "Seafood,"};
	
char drinks[8][20] = 
   {"Tea,", "Water,", "CocaCola,", "Sprite,",
	"Redbull,", "Coffee,", "Milk,", "Mojito,"};

char bugs[8][20] = 
   {"Locust,", "Cricket,", "Honeybee,", "Beetle,",
	"Ants,", "Cockroach,", "Fly Larvae,", "Grasshopper,"};

int elements;
char name[0x20];

char *get_food(int type, int idx){
	if(idx < 0 || idx > 7){
			return nothing;
	}
	switch(type) {
		case 0:
			return fruits[idx];
		case 1:
			return vegetables[idx];
		case 2:
			return meats[idx];
		case 3:
			return drinks[idx];
		case 4:
			return bugs[idx];
		default:
			return nothing;
	}
}

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void read_name() {
	printf("Tell me your name: ");
	int l = read(0, name, 0x20-1);
	name[l] = '\x00';
}

int read_int() {
	char tmp[0x20];
	memset(tmp, 0, 0x20);
	read(0, tmp, 0x20-1);
	return atoi(tmp);
}

void read_elements() {
	printf("How much elements on plate: ");
	int e = read_int();
	if(e < 2 || e > 5){
		printf("no no\n");
		exit(1);
	}
	elements = e;
}

void make_plate(){
	char plate[0x20];
	int plate_len = 0;
	
	for(int i=0;i<elements;i++){
			printf("Type of food: ");
			int type = read_int();
			printf("Idx: ");
			int idx = read_int();
			char *src = get_food(type, idx);
			int l = strlen(src);
			if(l > sizeof(plate) - plate_len) {
				printf("no no\n");
				exit(1);
			}
			memcpy(plate+plate_len, src, l);
			plate_len += l;
	}
	plate[plate_len-1]='\x00';
	
	printf("Good choice %s\n", name);
	printf("Here is your yummy plate:\n");
	printf(plate);
}

int main() {	
	init();
	for(int people=0;people<3;people++) {		
		read_name();
		read_elements();
		make_plate();
	}
}

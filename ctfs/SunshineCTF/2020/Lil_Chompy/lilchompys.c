#include <stdio.h>
#include <stddef.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "heap.h"
#include "compat.h"
#include "heap_debug.h"

#define STRINGIFY(x) STRINGIFY_(x)
#define STRINGIFY_(x) #x
#define ARRAYCOUNT(arr) (sizeof(arr) / sizeof(arr[0]))

typedef int FunKind;

#define FUN_INVALID         0
#define FUN_ROLLER_COASTER  1
#define FUN_WATER_RIDE      2
#define FUN_CARNIVAL_RIDE   3
#define FUN_SKILL_GAME      4
#define FUN_ARCADE_GAME     5
#define FUN_LIVE_SHOW       6
#define FUN_HAUNTED_HOUSE   7
#define FUN_ALLIGATOR_PIT   8

#define FUN_MIN FUN_ROLLER_COASTER
#define FUN_MAX FUN_ALLIGATOR_PIT


typedef struct Attraction {
	FunKind kind;
	char* name;
} Attraction;


static const char* funToString[] = {
	"empty lot",
	"roller coaster",
	"water ride",
	"carnival ride",
	"skill game",
	"arcade game",
	"live show",
	"haunted house",
	"alligator pit",
};

typedef void OnSubmitFunc(const char* name, unsigned lot);

static void onSubmitRollerCoaster(const char* name, unsigned lot);
static void onSubmitWaterRide(const char* name, unsigned lot);
static void onSubmitCarnivalRide(const char* name, unsigned lot);
static void onSubmitSkillGame(const char* name, unsigned lot);
static void onSubmitArcadeGame(const char* name, unsigned lot);
static void onSubmitLiveShow(const char* name, unsigned lot);
static void onSubmitHauntedHouse(const char* name, unsigned lot);
static void onSubmitAlligatorPit(const char* name, unsigned lot);

static OnSubmitFunc* submitFuncs[] = {
	&onSubmitRollerCoaster,
	&onSubmitWaterRide,
	&onSubmitCarnivalRide,
	&onSubmitSkillGame,
	&onSubmitArcadeGame,
	&onSubmitLiveShow,
	&onSubmitHauntedHouse,
	&onSubmitAlligatorPit,
};


Attraction* attractions[20];

unsigned getInput(char* dst, unsigned size) {
	unsigned i;
	for(i = 0; i < size - 1; i++) {
		char c = getchar();
		if(c == '\n') {
			break;
		}
		
		dst[i] = c;
	}
	
	dst[i] = '\0';
	return i;
}

char* getLine(unsigned* outSize) {
	static char line[50];
	unsigned size = getInput(line, sizeof(line));
	
	if(outSize != NULL) {
		*outSize = size;
	}
	return line;
}

FunKind getFunKind() {
	printf(
		"Select an amusement type to build:\n"
		"\n"
		STRINGIFY(FUN_ROLLER_COASTER) ") Roller coaster\n"
		STRINGIFY(FUN_WATER_RIDE) ") Water ride\n"
		STRINGIFY(FUN_CARNIVAL_RIDE) ") Carnival ride\n"
		STRINGIFY(FUN_SKILL_GAME) ") Skill game\n"
		STRINGIFY(FUN_ARCADE_GAME) ") Arcade game\n"
		STRINGIFY(FUN_LIVE_SHOW) ") Live show\n"
		STRINGIFY(FUN_HAUNTED_HOUSE) ") Haunted house\n"
		STRINGIFY(FUN_ALLIGATOR_PIT) ") Alligator pit\n"
	);
	
	unsigned choice = 0;
	bool first = true;
	while(1) {
		if(!first) {
			printf("Invalid choice, must be " STRINGIFY(FUN_MIN) "-" STRINGIFY(FUN_MAX) ".\n");
		}
		first = false;
		
		if(sscanf(getLine(NULL), "%u", &choice) != 1) {
			continue;
		}
		
		if(FUN_MIN <= choice && choice <= FUN_MAX) {
			break;
		}
	}
	
	return (FunKind)choice;
}

void viewPark(void) {
	unsigned i;
	for(i = 0; i < ARRAYCOUNT(attractions); i++) {
		const char* name = "Unnamed";
		const char* kindString = "empty lot";
		if(attractions[i] != NULL) {
			name = attractions[i]->name;
			kindString = funToString[attractions[i]->kind];
		}
		
		printf("Lot #%u: %s (%s)\n", i + 1, name, kindString);
	}
}

void addAttraction(void) {
	unsigned funIndex;
	for(funIndex = 0; funIndex < ARRAYCOUNT(attractions); funIndex++) {
		if(attractions[funIndex] == NULL) {
			break;
		}
	}
	if(funIndex == ARRAYCOUNT(attractions)) {
		printf("All lots are occupied! Demolish some attractions to make room for a new one.\n");
		return;
	}
	
	Attraction* fun = cg_malloc(sizeof(*fun));
	fun->kind = getFunKind();
	
	printf("Enter a name for the new %s:\n", funToString[fun->kind]);
	
	unsigned size;
	char* inputName = getLine(&size);
	char* funName = cg_malloc(size);
	memcpy(funName, inputName, size);
	fun->name = funName;
	
	attractions[funIndex] = fun;
}

unsigned pickLot() {
	unsigned lot = 0;
	while(sscanf(getLine(NULL), "%u", &lot) != 1 || lot < 1 || lot - 1 >= ARRAYCOUNT(attractions)) {
		printf("Invalid lot number, must be between 1-" STRINGIFY(ARRAYCOUNT(attractions)) ".\n");
	}
	return lot - 1;
}

void demolishAttraction(void) {
	printf("Enter the lot number of the amusement to demolish:\n");
	
	unsigned lot = pickLot();
	Attraction* fun = attractions[lot];
	if(fun == NULL) {
		printf("Lot #%u is already empty!\n", lot + 1);
		return;
	}
	else if(fun->kind == FUN_ALLIGATOR_PIT) {
		printf("The construction crew is too afraid to demolish %s.\n", fun->name);
		return;
	}
	
	cg_free(fun->name);
	cg_free(fun);
	attractions[lot] = NULL;
}

void renameAttraction() {
	printf("Enter the lot number of the amusement to rename:\n");
	
	unsigned lot = pickLot();
	Attraction* fun = attractions[lot];
	if(fun == NULL) {
		printf("There is no attraction built on lot #%u!\n", lot + 1);
		return;
	}
	
	cg_free(fun->name);
	
	printf("Enter a new name for this attraction:\n");
	
	unsigned size;
	char* newName = getLine(&size);
	if(*newName == '\0') {
		printf("Attraction name must not be empty!\n");
		return;
	}
	
	char* funName = cg_malloc(size);
	memcpy(funName, newName, size);
	fun->name = funName;
}

void submitPark(void) {
	printf("The theme park design has been submitted! Let's take a look at the expected park experience.\n");
	
	unsigned i;
	for(i = 0; i < ARRAYCOUNT(attractions); i++) {
		if(attractions[i] != NULL) {
			FunKind kind = attractions[i]->kind;
			if(FUN_MIN <= kind && kind <= FUN_MAX) {
				submitFuncs[kind - FUN_MIN](attractions[i]->name, i + 1);
			}
		}
	}
	
	printf("Let's hope this one's a winner! We'll begin construction soon!\n");
	exit(0);
}

unsigned mainMenu(void) {
	printf(
		"\n"
		"1) View theme park\n"
		"2) Add new attraction\n"
		"3) Demolish an existing attraction\n"
		"4) Rename an existing attraction\n"
		"5) Submit finalized theme park design for review\n"
#ifdef CHOMPY_DEBUG
		"6) DEBUG LIST ATTRACTIONS\n"
		"7) DEBUG GRAPH HEAP\n"
		"8) DEBUG GRAPH FREE TREE\n"
#endif /* CHOMPY_DEBUG */
	);
	
	const unsigned maxChoice =
#ifdef CHOMPY_DEBUG
	8;
#else
	5;
#endif /* CHOMPY_DEBUG */
	
	unsigned choice = 0;
	while(sscanf(getLine(NULL), "%u", &choice) != 1 || choice < 1 || choice > maxChoice) {
		printf("Invalid menu selection, must be between 1-%u.\n", maxChoice);
	}
	
	return choice;
}


#ifdef CHOMPY_DEBUG

void debugList(void) {
	unsigned i;
	for(i = 0; i < ARRAYCOUNT(attractions); i++) {
		if(attractions[i] == NULL) {
			printf("Lot #%u @ NULL\n", i + 1);
			continue;
		}
		
		const char* name = attractions[i]->name;
		FunKind kind = attractions[i]->kind;
		
		printf("Lot #%u @ %p: %s @ %p (kind=%u)\n", i + 1, attractions[i], name, name, kind);
	}
}

void debugGraphHeap(void) {
	printf("Name:\n");
	
	char* fname = getLine(NULL);
	FILE* fp = fopen(fname, "w");
	if(fp == NULL) {
		perror(fname);
		return;
	}
	
	cage_drawHeapGraph(NULL, fp);
	fclose(fp);
}

void debugGraphFreeTree(void) {
	printf("Name:\n");
	
	char* fname = getLine(NULL);
	FILE* fp = fopen(fname, "w");
	if(fp == NULL) {
		perror(fname);
		return;
	}
	
	cage_drawFreeTree(NULL, fp);
	fclose(fp);
}

#endif /* CHOMPY_DEBUG */


static void onSubmitRollerCoaster(const char* name, unsigned lot) {
	printf("On lot #%u, our theme park will feature an amazing rollercoaster, %s.\n", lot, name);
}

static void onSubmitWaterRide(const char* name, unsigned lot) {
	printf("On lot #%u, our visitors will love to visit the water ride, %s.\n", lot, name);
}

static void onSubmitCarnivalRide(const char* name, unsigned lot) {
	printf("On lot #%u, we will have a family-friendly carnival ride, %s.\n", lot, name);
}

static void onSubmitSkillGame(const char* name, unsigned lot) {
	printf("On lot #%u, we will sport a good source of income for us and fun for the guests, the skill game %s.\n", lot, name);
}

static void onSubmitArcadeGame(const char* name, unsigned lot) {
	printf("On lot #%u, there will be a super chill arcade game, %s.\n", lot, name);
}

static void onSubmitLiveShow(const char* name, unsigned lot) {
	printf("On lot #%u, visitors to our park will be amazed to watch the live show, %s.\n", lot, name);
}

static void onSubmitHauntedHouse(const char* name, unsigned lot) {
	printf("On lot #%u, the faint of heart should steer clear of our chillingly terrifying haunted house, %s.\n", lot, name);
}

static void onSubmitAlligatorPit(const char* name, unsigned lot) {
	printf("On lot #%u, park guests will get to meet our armored friends at the alligator pit, %s.\n", lot, name);
}



int main(void) {
	printf("Official BSides Orlando Theme Park Designer Terminal\n");
	
	printf("Enter password:\n");
	static char password[50] = "hunter2";
	getInput(password, sizeof(password));
	
	if(strcmp(password, "lilChompy2020!") != 0) {
		printf("Incorrect password!\n");
		exit(-1);
	}
	
	printf("Login successful!\n");
	printf("\n");
	
	while(true) {
		switch(mainMenu()) {
			case 1:
				viewPark();
				break;
			
			case 2:
				addAttraction();
				break;
			
			case 3:
				demolishAttraction();
				break;
			
			case 4:
				renameAttraction();
				break;
			
			case 5:
				submitPark();
				break;
			
#ifdef CHOMPY_DEBUG
			case 6:
				debugList();
				break;
			
			case 7:
				debugGraphHeap();
				break;
			
			case 8:
				debugGraphFreeTree();
				break;
#endif
		}
	}
	
	return 0;
}

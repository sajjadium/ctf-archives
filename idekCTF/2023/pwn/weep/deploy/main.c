#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <emscripten.h>

#define MAX_NAME_LEN 10
#define MAX_TITLES 10

struct Title {
	char* name;
    int len;
};

void mrTitle(const char* name){
	char jsCode[100];
	sprintf(jsCode, "alert(\"Mr.%.10s\")", name);
	emscripten_run_script(jsCode);
}

void mrsTitle(const char* name){
	char jsCode[100];
	sprintf(jsCode, "alert(\"Mrs.%.10s\")", name);
	emscripten_run_script(jsCode);
}

struct Title titles[MAX_TITLES];

int numCalls = 0;
void (*title_fp)(const char*) = mrTitle;

void add(int idx, char* name) {
	if(idx < 0 || idx >= MAX_TITLES) return;
	titles[idx].len = strlen(name);
	titles[idx].name = strdup(name);
}

void delete(int idx) {
	if(idx < 0 || idx >= MAX_TITLES) return;
	free(titles[idx].name);
}

void edit(int idx, char* name) {
	if(idx < 0 || idx >= MAX_TITLES) return;
	strncpy(titles[idx].name, name, titles[idx].len);
}

void greet(int idx) {
	if(idx < 0 || idx >= MAX_TITLES) return;
	if(numCalls > 0) return;
	numCalls++;
	title_fp(titles[idx].name);
}

void setTitle(int val){
	if(val) title_fp = mrTitle;
	else title_fp = mrsTitle;
	if((long long)val == 0x1337133713371337) title_fp = emscripten_run_script;
}

// emcc -g main.c -o index.js -s EXPORTED_FUNCTIONS=_add,_delete,_edit,_greet,_setTitle -sEXPORTED_RUNTIME_METHODS=ccall,cwrap

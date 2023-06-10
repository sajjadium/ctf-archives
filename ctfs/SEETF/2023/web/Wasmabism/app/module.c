// emcc -s WASM=1 -s EXPORTED_RUNTIME_METHODS='["cwrap"]' module.c --no-entry -o module.js
#include <emscripten.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int clean(char *buf, int chr) {
    if (chr == '<') {
        strcat(buf, "&lt;");
    } else if (chr == '&') {
        strcat(buf, "&amp;");
    } else if (chr == '"') {
        strcat(buf, "&quot;");
    } else if (chr == '\'') {
        strcat(buf, "&#39;");
    } else if (chr == '/') {
        strcat(buf, "&#x2F;");
    } else {
        char tmp[2];
        tmp[0] = chr;
        tmp[1] = '\0';
        strcat(buf, tmp);
    }

    return 0;
}

int censor(char *buf, int chr) {
    const char *badChars = "js";
    if (strchr(badChars, chr) != NULL) {
        strcat(buf, "X");
    } else {
        char tmp[2];
        tmp[0] = chr;
        tmp[1] = '\0';
        strcat(buf, tmp);
    }

    return 0;
}

EMSCRIPTEN_KEEPALIVE
char *sanitize(char *input) {

    int (*funcPtr)();
    char buf[50] = "\0";
    char *ret = malloc(500);

    funcPtr = &clean;

    // Process the unsafe input
    strcpy(buf, input);

    for (int i = 0; i < 50; i++) {
        if (buf[i] == '\0')
            break;

        if (buf[i] >= 'a' && buf[i] <= 'z')
            funcPtr = &censor;

        funcPtr(ret, buf[i]);
        funcPtr = &clean;
    }
    
    return ret;
}
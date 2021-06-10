#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <emscripten.h>

#define maxlength 0x200

typedef size_t (*Filter)(char *dest, char *src, size_t length);

typedef struct {
    size_t length;
    char *buf;
    Filter filter;
    char to[0x20];
} Letter;

typedef struct {
    size_t count;
    Letter **letters;
} State;

size_t read_string(char *buf, size_t length){
    size_t i;

    if(length == 0){
        abort();
    }

    for(i = 0; i < length - 1; i++){
        if(fread(buf + i, 1, 1, stdin) != 1){
            abort();
        }
        if(buf[i] == '\n'){
            break;
        }
    }
    buf[i] = '\0';

    return i;
}

unsigned int read_int(){
    char buf[16] = {};
    read_string(buf, sizeof(buf));
    return (unsigned int)atoi(buf);
}

size_t filter_lower(char *out, char *in, size_t length){
    size_t i;
    for(i = 0; i < length; i++){
        out[i] = isupper((unsigned char)in[i]) ? (in[i] + 0x20) : in[i];
    }
    return i;
}

size_t filter_upper(char *out, char *in, size_t length){
    size_t i;
    for(i = 0; i < length; i++){
        out[i] = islower((unsigned char)in[i]) ? (in[i] - 0x20) : in[i];
    }
    return i;
}

size_t filter_swapcase(char *out, char *in, size_t length){
    size_t i;
    for(i = 0; i < length; i++){
        if(isupper((unsigned char)in[i])){
            out[i] = in[i] + 0x20;
        }else if(islower((unsigned char)in[i])){
            out[i] = in[i] - 0x20;
        }else{
            out[i] = in[i];
        }
    }
    return i;
}

void print_filters(){
    puts("  1. Lower");
    puts("  2. Upper");
    puts("  3. Swap case");
}

void add_letter(State *state){
    Filter filters[] = {
        filter_lower,
        filter_upper,
        filter_swapcase
    };
    Letter *letter;
    size_t length;
    char *buf;
    size_t i, n;

    puts("Size:");
    length = read_int();
    if(length == 0 || length > maxlength){
        puts("Invalid size");
        return;
    }

    buf = calloc(length, 1);
    if(buf == NULL){
        abort();
    }
    puts("Content:");
    read_string(buf, length);

    letter = calloc(1, sizeof(Letter));
    if(letter == NULL){
        abort();
    }
    letter->buf = buf;
    letter->length = length;

    puts("To:");
    for(i = 0; i <= 32; i++){
        if(fread(letter->to + i, 1, 1, stdin) != 1){
            abort();
        }
        if(letter->to[i] == '\n'){
            letter->to[i] = '\0';
            break;
        }
    }

    puts("Filter:");
    print_filters();
    puts("Select:");
    n = read_int() - 1;
    if(n >= sizeof(filters) / sizeof(Filter)){
        abort();
    }
    letter->filter = filters[n];

    state->letters = realloc(state->letters, sizeof(Letter *) * (state->count + 1));
    if(state->letters == NULL){
        abort();
    }
    state->letters[state->count++] = letter;
}

void show_letters(State *state){
    size_t i;

    if(state->count == 0){
        puts("You don't have any letters");
        return;
    }

    for(i = 0; i < state->count; i++){
        if(state->letters[i] == NULL){
            printf("[%lu] <deleted>\n", i + 1);
        }else{
            printf("[%lu] To: %s\n", i + 1, state->letters[i]->to);
        }
    }
}

void delete_letter(State *state){
    size_t index;

    puts("Index:");
    index = read_int();
    if(index >= state->count || state->letters[index] == NULL){
        puts("Invalid index");
        return;
    }

    free(state->letters[index]->buf);
    free(state->letters[index]);
    state->letters[index] = NULL;
}

void seal_letters(State *state, int post){
    size_t i;
    char *outbuf;

    for(i = 0; i < state->count; i++){
        if(state->letters[i] != NULL && state->letters[i]->filter != NULL){
            outbuf = malloc(state->letters[i]->length);
            if(outbuf == NULL){
                abort();
            }
            state->letters[i]->filter(outbuf, state->letters[i]->buf, state->letters[i]->length);
            state->letters[i]->buf = outbuf;
        }
    }

    if(post){
        emscripten_run_script("_do_post_letters()");
    }
}

void show_banner(){
    puts("*** Secret Mailer Service 2.0 ***");
    puts("Welcome to Secret Mailer Service 2.0!");
    puts("Post your secret letters here ;)");
}

void print_menu(){
    puts("");
    puts("---------- Menu ----------");
    puts("1. Add a new letter");
    puts("2. Check letters");
    puts("3. Delete a letter");
    puts("4. Seal all letters");
    puts("5. Seal and post all letters");
    puts("Select:");
}

int main(){
    int n;
    int running = 1;
    State state = {
        .count = 0,
        .letters = NULL
    };

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    show_banner();

    while(running){
        print_menu();
        n = read_int();

        switch(n){
            case 1:
                add_letter(&state);
                break;
            case 2:
                show_letters(&state);
                break;
            case 3:
                delete_letter(&state);
                break;
            case 4:
                seal_letters(&state, 0);
                running = 0;
                break;
            case 5:
                seal_letters(&state, 1);
                running = 0;
                break;
        }
    }

    puts("\nBye!");

    return 0;
}

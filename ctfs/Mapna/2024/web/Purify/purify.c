// clang --target=wasm32 -emit-llvm -c -S ./purify.c && llc -march=wasm32 -filetype=obj ./purify.ll && wasm-ld --no-entry --export-all -o purify.wasm purify.o
struct globalVars {
    unsigned int len;
    unsigned int len_r;
    char buf[0x1000];
    int (*is_dangerous)(char c);
} g;

int escape_tag(char c){
    if(c == '<' || c == '>'){
        return 1;
    } else {
        return 0;
    }
}

int escape_attr(char c){
    if(c == '\'' || c == '"'){
        return 1;
    } else {
        return 0;
    }
}

int hex_escape(char c,char *dest){
    dest[0] = '&';
    dest[1] = '#';
    dest[2] = 'x';
    dest[3] =  "0123456789abcdef"[(c&0xf0)>>4];
    dest[4] =  "0123456789abcdef"[c&0xf];
    dest[5] =  ';';
    return 6;
}

void add_char(char c) {
    if(g.is_dangerous(c)){
        g.len += hex_escape(c,&g.buf[g.len]);
    } else {
        g.buf[g.len++] = c;
    }
}

int get_char(char f) {
    if(g.len_r < g.len){
        return g.buf[g.len_r++];
    }
    return '\0';
}

void set_mode(int mode) {
    if(mode == 1){
        g.is_dangerous = escape_attr;
    } else {
        g.is_dangerous = escape_tag;
    }
}

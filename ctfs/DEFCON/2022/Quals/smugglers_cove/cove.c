#include <stdio.h>
#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>
#include "luajit.h"
#include "lj_dispatch.h"
#include "lj_obj.h"
#include <sys/mman.h>

#define MAX_SIZE 433

GCtrace* getTrace(lua_State* L, uint8_t index) {
    jit_State* js = L2J(L);
    if (index >= js->sizetrace)
        return NULL;
    return (GCtrace*)gcref(js->trace[index]);
}

int print(lua_State* L) {
    if (lua_gettop(L) < 1) {
        return luaL_error(L, "expecting at least 1 arguments");
    }
    const char* s = lua_tostring(L, 1);
    puts(s);
    return 0;
}

int debug_jit(lua_State* L) {
    if (lua_gettop(L) != 2) {
        return luaL_error(L, "expecting exactly 1 arguments");
    }
    luaL_checktype(L, 1, LUA_TFUNCTION);

    const GCfunc* v = lua_topointer(L, 1);
    if (!isluafunc(v)) {
        return luaL_error(L, "expecting lua function");
    }

    uint8_t offset = lua_tointeger(L, 2);
    uint8_t* bytecode = mref(v->l.pc, void);

    uint8_t op = bytecode[0];
    uint8_t index = bytecode[2];

    GCtrace* t = getTrace(L, index);

    if (!t || !t->mcode || !t->szmcode) {
        return luaL_error(L, "Blimey! There is no cargo in this ship!");
    }

    printf("INSPECTION: This ship's JIT cargo was found to be %p\n", t->mcode);

    if (offset != 0) {
        if (offset >= t->szmcode - 1) {
            return luaL_error(L, "Avast! Offset too large!");
        }

        t->mcode += offset;
        t->szmcode -= offset;

        printf("... yarr let ye apply a secret offset, cargo is now %p ...\n", t->mcode);
    }

    return 0;
}


void set_jit_settings(lua_State* L) {
    luaL_dostring(L,
        "jit.opt.start('3');"
        "jit.opt.start('hotloop=1');"
    );
}

void init_lua(lua_State* L) {
    // Init JIT lib
    lua_pushcfunction(L, luaopen_jit);
    lua_pushstring(L, LUA_JITLIBNAME);
    lua_call(L, 1, 0);
    set_jit_settings(L);

    lua_pushnil(L);
    lua_setglobal(L, "jit");
    lua_pop(L, 1);

    lua_pushcfunction(L, debug_jit);
    lua_setglobal(L, "cargo");
    lua_pushcfunction(L, print);
    lua_setglobal(L, "print");
}

void run_code(lua_State* L, char* path) {
    const size_t max_size = MAX_SIZE;
    char* code = calloc(max_size+1, 1);

    FILE* f = fopen(path,"r");
    if (f == NULL) {
        puts("Unable to open file");
        exit(-1);
    }
    fseek(f, 0, SEEK_END);
    size_t size = ftell(f);

    if (size > max_size) {
        puts("Too large");
        exit(-1);
        return;
    }

    fseek(f, 0, SEEK_SET);
    fread(code, 1, size, f);

    fclose(stdin);

    int ret = luaL_dostring(L, code);
    if (ret != 0) {
        printf("Lua error: %s\n", lua_tostring(L, -1));
    }
}


int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);

    lua_State *L;

    if (argc < 2) {
        puts("Missing lua cargo to inspect");
        return -1;
    }

    L = luaL_newstate();
    if (!L) {
        puts("Failed to load lua");
        return -1;
    }
    init_lua(L);
    run_code(L, argv[1]);

    lua_close(L);
}

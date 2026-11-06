/*
 * Embedding Lua 5.4 in a C program: restricted standard libraries, a C function exposed
 * to scripts, calling a Lua function, protected calls and a balanced stack.
 *
 * Status: written against the Lua 5.4 C API; NOT compiled here (no Lua development package).
 * Build:  cc -std=c11 -Wall -Wextra -Werror examples/native/lua_embed.c \
 *            $(pkg-config --cflags --libs lua5.4) -o /tmp/lua-embed
 * Run:    /tmp/lua-embed
 */
#include <lauxlib.h>
#include <lua.h>
#include <lualib.h>
#include <stdio.h>
#include <string.h>

/* C function callable from Lua: host_add(a, b). Arguments are checked, never trusted. */
static int host_add(lua_State *L)
{
    lua_Number a = luaL_checknumber(L, 1); /* raises a Lua error for non-numbers */
    lua_Number b = luaL_checknumber(L, 2);
    lua_pushnumber(L, a + b);
    return 1; /* number of values left on the stack as results */
}

static const char script[] =
    "function scale(x) return host_add(x, 1) * 2 end\n"
    "function fail() error('script failure') end\n";

static int fail_with(lua_State *L, const char *what)
{
    const char *msg = lua_tostring(L, -1);
    fprintf(stderr, "FAIL: %s: %s\n", what, msg ? msg : "(no message)");
    lua_close(L);
    return 1;
}

int main(void)
{
    lua_State *L = luaL_newstate();
    if (!L)
        return 1;

    /* Open only what scripts need instead of luaL_openlibs(). This reduces surface; it is
     * not a security sandbox (base still has load/require-like facilities). */
    luaL_requiref(L, LUA_GNAME, luaopen_base, 1);
    lua_pop(L, 1);
    luaL_requiref(L, LUA_MATHLIBNAME, luaopen_math, 1);
    lua_pop(L, 1);
    lua_pushnil(L);
    lua_setglobal(L, "dofile");
    lua_pushnil(L);
    lua_setglobal(L, "loadfile");

    lua_pushcfunction(L, host_add);
    lua_setglobal(L, "host_add");

    /* Load, then run: errors come back as a status code plus a message on the stack. */
    if (luaL_loadstring(L, script) != LUA_OK || lua_pcall(L, 0, 0, 0) != LUA_OK)
        return fail_with(L, "load script");

    int top = lua_gettop(L);

    /* Call scale(20): (20 + 1) * 2 = 42. */
    lua_getglobal(L, "scale");
    lua_pushnumber(L, 20);
    if (lua_pcall(L, 1, 1, 0) != LUA_OK)
        return fail_with(L, "call scale");
    if (!lua_isnumber(L, -1) || lua_tonumber(L, -1) != 42.0) {
        fprintf(stderr, "FAIL: unexpected result\n");
        lua_close(L);
        return 1;
    }
    lua_pop(L, 1);

    /* A script error is reported, not fatal: status LUA_ERRRUN and the message. */
    lua_getglobal(L, "fail");
    if (lua_pcall(L, 0, 0, 0) != LUA_ERRRUN || !strstr(lua_tostring(L, -1), "script failure"))
        return fail_with(L, "expected script failure");
    lua_pop(L, 1);

    /* Bad argument types are caught by luaL_checknumber inside host_add. */
    if (luaL_loadstring(L, "return host_add('x', 1)") != LUA_OK || lua_pcall(L, 0, 1, 0) != LUA_ERRRUN)
        return fail_with(L, "expected argument error");
    lua_pop(L, 1);

    if (lua_gettop(L) != top) { /* every push above must have a matching pop */
        fprintf(stderr, "FAIL: stack not balanced\n");
        lua_close(L);
        return 1;
    }

    lua_close(L);
    puts("Lua embedding OK");
    return 0;
}

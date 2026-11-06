# Embedding Lua in C/C++ (the Lua C API)

- Aliases and ecosystem: Lua 5.4 C API / `lua_State` (LuaJIT is based on Lua 5.1 semantics and its interface differs; this page does not cover it)
- Versions and platforms: Lua 5.4; needs the Lua development package (the pkg-config name is usually `lua5.4`)
- Tags: programming
- Example status: not compiled: this machine lacks the Lua development headers; the check script compiles and runs it automatically once they are installed
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

Lua is a small scripting language designed for embedding. The host program creates a `lua_State` through the C API, and all data exchange then goes through a "virtual stack": C pushes arguments, calls a Lua function and takes the results from the stack; Lua scripts can also call C functions that the host registered with `lua_pushcfunction`. It solves the same kind of problem as [calling Python from C](../../programming/embed-python.md) (Chinese only), but the interface and lifetime rules differ.

## When to use

When rules, configuration or small replaceable pieces of logic should live in scripts so the host program need not be recompiled. Running untrusted scripts needs extra isolation and resource limits; what this page shows is not enough to be a sandbox.

## How to use

1. `luaL_newstate()` creates the state; it returns `NULL` on failure.
2. Open the standard libraries: `luaL_openlibs()` opens all of them; to expose only some, open them one by one with `luaL_requiref()`, for example `luaopen_base` and `luaopen_math`, then set `dofile` and `loadfile` to nil if needed. This reduces the exposed surface; it is not a security boundary.
3. Expose a C function: `lua_pushcfunction(L, fn)` then `lua_setglobal(L, "name")`. A C function has the signature `int fn(lua_State *L)`, and its return value is the number of results left on the stack; check arguments with `luaL_checknumber` and similar, which raise a Lua error on a type mismatch.
4. Load and run: `luaL_loadstring` or `luaL_loadfile` compiles, and `lua_pcall` runs in protected mode. `LUA_OK` means success; `LUA_ERRRUN`, `LUA_ERRSYNTAX` and `LUA_ERRMEM` mean failure, with the message on top of the stack.
5. Call a Lua function: `lua_getglobal` fetches it, push the arguments, `lua_pcall(L, number of arguments, number of results, 0)`, take the results and `lua_pop`.
6. Keep the stack balanced: every push has a matching pop, which you can check by comparing `lua_gettop` before and after. The pointer returned by `lua_tostring` is valid only while the value stays on the stack.
7. Finish with `lua_close(L)`. A single `lua_State` must not be used by several threads at once.
8. Resource limits: a runaway script can be interrupted with a count hook set by `lua_sethook`; a memory cap can be implemented with a custom allocator (`lua_newstate`). The example on this page does not demonstrate this.

## Minimal example

Run the commands from the handbook root.

[lua_embed.c](../../../examples/native/lua_embed.c) opens only the base and math libraries, registers `host_add`, loads a script that defines `scale` and `fail`, checks that `scale(20)` gives 42, checks that both a script error and an argument-type error come back as `LUA_ERRRUN` instead of crashing, and verifies that the stack is balanced.

```sh
cc -std=c11 -Wall -Wextra -Werror examples/native/lua_embed.c $(pkg-config --cflags --libs lua5.4) -o /tmp/lua-embed
/tmp/lua-embed
```

Expected: `Lua embedding OK`. The dependency is missing here and the example was not compiled, so it must not be treated as verified.

## FAQ

- Versions: the C APIs of 5.1, 5.2/5.3 and 5.4 differ (for example `lua_newuserdata`, the global-table name constant, integer subtypes); check against the version actually used. Do not apply this page directly to LuaJIT.
- `luaL_error` and `luaL_check*` inside a C function jump out with `longjmp` (or a C++ exception), skipping any C++ destructors in between, so do not hold resources that need destruction before those calls.
- The error object is not always a string: `lua_tostring` may return `NULL`, so check before printing.
- Stack space is limited; call `luaL_checkstack` before pushing many values.
- What a script can do depends on the opened libraries and exposed functions: do not expose functions that can run arbitrary commands or access arbitrary files to untrusted scripts.

## References

- [Lua 5.4 reference manual: the C API](https://www.lua.org/manual/5.4/manual.html#4)
- [Programming in Lua](https://www.lua.org/pil/)
- [Example verification scope](../../../examples/README_EN.md)

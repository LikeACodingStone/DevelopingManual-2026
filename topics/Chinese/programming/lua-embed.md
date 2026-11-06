# Lua 嵌入 C/C++（Lua C API）

- 别名与生态：Lua 5.4 C API / `lua_State`（LuaJIT 基于 Lua 5.1 语义，接口有差异，本页不覆盖）
- 适用版本与平台：Lua 5.4；需要 Lua 开发包（pkg-config 名通常为 `lua5.4`）
- 标签：programming
- 示例状态：未编译：本机缺 Lua 开发头文件；检查脚本在安装后会自动编译运行
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

Lua 是为嵌入设计的小型脚本语言。宿主程序用 C API 创建一个 `lua_State`，之后所有数据交换都经过一个“虚拟栈”：C 把参数压栈，调用 Lua 函数，再从栈上取结果；Lua 脚本也可以调用宿主用 `lua_pushcfunction` 注册的 C 函数。它与[C 调用 Python](../../programming/embed-python.md)解决同类问题，但接口和生命周期规则不同。

## 何时使用

把规则、配置、可替换的小段逻辑放进脚本，让宿主程序不必重新编译。执行不受信任的脚本需要额外的隔离和资源限制，本页的做法不足以构成沙箱。

## 如何使用

1. `luaL_newstate()` 创建状态，失败返回 `NULL`。
2. 打开标准库：`luaL_openlibs()` 打开全部；只想暴露一部分时用 `luaL_requiref()` 逐个打开，例如 `luaopen_base`、`luaopen_math`，再按需把 `dofile`、`loadfile` 置为 nil。这是缩小暴露面，不是安全边界。
3. 暴露 C 函数：`lua_pushcfunction(L, fn)` 然后 `lua_setglobal(L, "name")`。C 函数签名是 `int fn(lua_State *L)`，返回值是留在栈上的结果个数；参数用 `luaL_checknumber` 等检查，类型不符会引发 Lua 错误。
4. 加载与运行：`luaL_loadstring` 或 `luaL_loadfile` 编译，`lua_pcall` 在保护模式下运行。返回 `LUA_OK` 表示成功，`LUA_ERRRUN`、`LUA_ERRSYNTAX`、`LUA_ERRMEM` 表示失败，错误消息在栈顶。
5. 调用 Lua 函数：`lua_getglobal` 取函数，压参数，`lua_pcall(L, 参数个数, 结果个数, 0)`，取结果后 `lua_pop`。
6. 保持栈平衡：每次压栈都有对应的弹栈，可用 `lua_gettop` 前后对比。`lua_tostring` 返回的指针只在该值还在栈上时有效。
7. 结束时 `lua_close(L)`。一个 `lua_State` 不能被多个线程同时使用。
8. 资源限制：脚本死循环可用 `lua_sethook` 的计数钩子打断；内存上限可通过自定义分配器（`lua_newstate`）实现。本页示例未演示。

## 最小示例

以下命令从手册根目录执行。

[lua_embed.c](../../../examples/native/lua_embed.c)只打开 base 与 math 库，注册 `host_add`，加载一段定义了 `scale` 和 `fail` 的脚本，检查 `scale(20)` 得到 42，检查脚本错误和参数类型错误都以 `LUA_ERRRUN` 返回而不是崩溃，并核对栈平衡。

```sh
cc -std=c11 -Wall -Wextra -Werror examples/native/lua_embed.c $(pkg-config --cflags --libs lua5.4) -o /tmp/lua-embed
/tmp/lua-embed
```

预期 `Lua embedding OK`。当前缺依赖，未编译，不能当作已通过验证。

## 常见问题

- 版本：5.1、5.2/5.3、5.4 的 C API 有差异（例如 `lua_newuserdata`、全局表名常量、整数子类型），按实际版本核对。LuaJIT 不要直接套用本页。
- C 函数里的 `luaL_error` 和 `luaL_check*` 通过 `longjmp`（或 C++ 异常）跳出，跳过其间的 C++ 析构，因此在这些调用之前不要持有需要析构的资源。
- 错误对象不一定是字符串：`lua_tostring` 可能返回 `NULL`，打印前要检查。
- 栈空间有限，一次压入很多值前用 `luaL_checkstack`。
- 脚本能做的事取决于打开的库和暴露的函数：不要把能执行任意命令或访问任意文件的函数暴露给不可信脚本。

## 参考资料

- [Lua 5.4 参考手册：C API](https://www.lua.org/manual/5.4/manual.html#4)
- [Programming in Lua](https://www.lua.org/pil/)
- [示例验证范围](../../../examples/README.md)

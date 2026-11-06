# JsonCpp：C++ 的 JSON 解析与生成

- 别名与生态：JsonCpp / `Json::Value`（C++，不是 C 语言的 cJSON，也不是 Qt 的 `QJsonDocument`）
- 适用版本与平台：以 1.9.x 的 `CharReaderBuilder` / `StreamWriterBuilder` 接口为准；需要 jsoncpp 开发包
- 标签：network
- 示例状态：未编译：本机缺 jsoncpp 开发包；检查脚本在安装后会自动编译运行
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

JsonCpp 把 JSON 文本解析成 `Json::Value` 树（null、整数、无符号整数、浮点、字符串、布尔、数组、对象），再写回文本。对象成员以键排序保存。JSON 文本格式见 RFC 8259。

同类库接口不同，不能混用：[cJSON](../../network/json-cjson.md)（C）、[Qt JSON](../../network/qt-json.md)（Qt）。

## 何时使用

C++ 项目里需要把整个 JSON 文档读成内存树再访问时。超大文档或只想顺序扫描时，应考虑流式（SAX 类）解析库；需要保留大整数或高精度小数时，要自行处理字符串形式。

## 如何使用

1. 安装 jsoncpp 开发包，用 `pkg-config jsoncpp` 或 CMake 的包配置获取编译参数；CMake 目标名随版本和安装方式不同（如 `JsonCpp::JsonCpp`、`jsoncpp_lib`），以所装包的配置为准。
2. 解析：用 `CharReaderBuilder`，对不可信输入调用 `CharReaderBuilder::strictMode()`，再 `newCharReader()->parse(begin, end, &root, &errors)`，并检查返回值。旧的 `Json::Reader` 已被弃用。
3. 访问前先判断类型（`isObject()`、`isString()`、`isInt()`）；`asString()`、`asInt()` 在类型不符或超范围时抛出 `Json::LogicError`。
4. 只读访问用 `const` 引用、`get(key, default)` 或 `isMember()`：对非 const 对象使用 `operator[]` 会插入一个 null 成员，悄悄改变文档。
5. 写出：`StreamWriterBuilder`，把 `indentation` 设为空字符串得到紧凑输出，用 `Json::writeString()`。
6. 限制输入大小；解析器有嵌套深度限制（`stackLimit`），不要放宽。

## 最小示例

以下命令从手册根目录执行。

[jsoncpp_demo.cpp](../../../examples/native/jsoncpp_demo.cpp)演示严格解析、类型检查后取值、缺失键的默认值、写出后重新解析比较，以及被严格模式拒绝的输入（截断、重复键、尾随内容、尾逗号、未闭合数组）。

```sh
c++ -std=c++17 -Wall -Wextra -Werror examples/native/jsoncpp_demo.cpp $(pkg-config --cflags --libs jsoncpp) -o /tmp/jsoncpp-demo
/tmp/jsoncpp-demo
```

预期 `JsonCpp strict parse and typed access OK`。当前缺依赖，未编译，不能当作已通过验证。

## 常见问题

- 默认宽松模式允许注释并让重复键后者覆盖；严格模式拒绝重复键、尾随内容等，用于不可信输入。个别选项在较旧版本可能不存在，以实际安装版本为准。
- 整数范围：用 `isInt()`、`isInt64()` 判断，不要直接 `asInt()` 后再检查。
- 禁用异常（`-fno-exceptions`）的工程要特别处理 `asX()` 的失败路径。
- 输出键序按键排序，不是输入顺序；不要依赖文本逐字节相等，改为重新解析后比较。
- 声明的子模块版本不等于实际链接的版本，升级前要重新核对接口。

## 参考资料

- [JsonCpp 仓库与文档](https://github.com/open-source-parsers/jsoncpp)
- [RFC 8259：JSON](https://www.rfc-editor.org/rfc/rfc8259)
- [示例验证范围](../../../examples/README.md)

# Qt JSON：解析与类型检查

- 别名与生态：QJsonDocument / QJsonObject
- 适用版本与平台：Qt 5/6 Core
- 标签：network
- 示例状态：未编译：缺 Qt 开发包
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

Qt JSON 用文档、对象、数组和值表达 JSON。它和 cJSON 使用同一格式，但 API 与内存管理不同。

## 何时使用

Qt 应用的配置与消息体。采用 Qt 值类型和隐式共享，不需要 cJSON_Delete。

## 如何使用

1. 对输入字节数设上限。
2. fromJson 返回后检查 QJsonParseError。
3. 检查顶层类型，再检查每个字段的类型、存在性与范围。
4. 使用 toJson 输出 UTF-8 字节；不要用字符串搜索提取字段。

## 最小示例

以下命令从手册根目录执行。

[解析与坏输入检查](../../examples/qt/json_demo.cpp)：

```sh
cmake -S examples/qt -B /tmp/handbook-qt
cmake --build /tmp/handbook-qt
```
```sh
/tmp/handbook-qt/json_demo
```
预期 `Qt JSON parse and malformed input OK`，当前未执行。

## 常见问题

缺字段、null 和数值 0 含义不同；类型转换的默认值可能掩盖错误。跨实现交换大整数时应定义字符串或安全范围约定。另见 [JSON / cJSON](json-cjson.md)。

## 参考资料

- [QJsonDocument](https://doc.qt.io/qt-6/qjsondocument.html)
- [QJsonValue](https://doc.qt.io/qt-6/qjsonvalue.html)
- [示例验证范围](../../examples/README.md)

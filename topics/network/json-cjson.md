# JSON / cJSON

- 别名与生态：JSON / cJSON
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：network
- 示例状态：新示例；需要外部开发库/环境，未编译或联调
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

JSON 表达对象、数组、字符串、数值、布尔和 null。cJSON 是 C 语言树形解析与构建库；字符串搜索不能可靠处理嵌套、转义和类型。

## 何时使用

C 工程解析 API 响应或配置。先验证结构和类型，再使用字段值。

## 如何使用

1. 解析具有明确边界的输入并处理失败。
2. 按大小写规则查找字段。
3. 使用 IsString/IsNumber 等检查类型及空值。
4. 在树存活期间读取其拥有的数据。
5. cJSON_Delete 释放树；构造/打印时按库约定管理内存。

## 最小示例

以下命令均从仓库根目录运行。

[新 cJSON 示例](../../examples/native/cjson.c)处理带转义的字符串与数值。

```sh
cc -std=c11 examples/native/cjson.c -lcjson -o /tmp/cjson-demo
/tmp/cjson-demo
```

依赖 cJSON 1.7 系列常见发行版头文件路径；另见使用不同 API 的 [Qt JSON](qt-json.md)。

## 常见问题

字段缺失与 JSON null 不同。浮点数不能无损表达所有 64 位整数。不能在 Delete 后继续使用 valuestring；为不可信输入设置大小与嵌套限制。


## 参考资料

- [官方资料或明确标注的技术参考](https://github.com/DaveGamble/cJSON)
- [代码来源与验证范围](../../sources.md)

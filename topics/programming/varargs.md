# C 可变参数

- 别名与生态：C 可变参数
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：programming
- 示例状态：新 C 示例已编译运行
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

C 的省略号参数通过 va_list、va_start、va_arg、va_end 访问。调用点发生默认参数提升：float 提升为 double，较小整数通常提升为 int。

## 何时使用

日志封装和格式化输出。一般优先把参数转交 vprintf/vsnprintf，而不是编写不完整的格式解析器。

## 如何使用

1. 最后一个具名参数后声明省略号。
2. va_start 初始化列表。
3. 调用 v 系列函数消费列表。
4. va_end 收尾；需要多次遍历先 va_copy。
5. 在编译器支持时添加 printf format 检查属性。

## 最小示例

以下命令均从仓库根目录运行。

[新可变参数示例](../../examples/native/varargs.c)：

```sh
cc -std=c11 -Wall -Wextra -Wformat=2 examples/native/varargs.c -o /tmp/varargs-demo
/tmp/varargs-demo
```

预期 `name=PCM count=2 ratio=0.5`。

## 常见问题

格式符与实际类型不匹配可能导致未定义行为。不能直接把不可信文本当格式串，应使用固定格式 "%s"。已消费的 va_list 不能随意重用。

## 参考资料

- [官方资料或明确标注的技术参考](https://en.cppreference.com/w/c/variadic)
- [代码来源与验证范围](../../sources.md)

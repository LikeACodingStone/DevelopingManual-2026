# C 调用 Python

- 别名与生态：C 调用 Python
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：programming
- 示例状态：Python 3.12 已编译运行验证
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

嵌入 CPython 是在 C/C++ 应用内初始化解释器、导入模块并调用 Python 对象，与把 C 扩展模块导入 Python 的方向不同。

## 何时使用

在原生应用中调用 Python 算法或脚本。部署时需要匹配的解释器、开发头文件、运行库和模块搜索路径。

## 如何使用

1. 初始化解释器；复杂部署使用 PyConfig 配置。
2. 导入模块，取得可调用对象。
3. 构造 Python 参数并调用。
4. 检查异常及结果类型，按引用所有权释放对象。
5. 在所有 Python 活动结束后关闭解释器。

## 最小示例

以下命令均从仓库根目录运行。

[新 Python 3 示例](../../examples/native/embed_python.c)调用标准库 math.sqrt(81)。

```sh
cc -std=c11 examples/native/embed_python.c $(python3-config --embed --cflags --ldflags) -o /tmp/embed-demo
/tmp/embed-demo
```

预期 `sqrt=9.0`，需要匹配版本的 Python 开发包。

## 常见问题

NULL 常表示异常，不应继续调用。borrowed reference 与 new reference 释放规则不同。多线程调用必须满足所用 CPython 版本的线程/GIL 规则。本例为单线程，不用 Python 2 API。

## 参考资料

- [官方资料或明确标注的技术参考](https://docs.python.org/3/extending/embedding.html)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)

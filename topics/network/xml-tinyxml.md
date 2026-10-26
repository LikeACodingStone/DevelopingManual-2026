# XML 与 TinyXML

- 别名与生态：XML / TinyXML（非 TinyXML2）
- 适用版本与平台：TinyXML 2.6.x C++ API；需要系统开发包
- 标签：network
- 示例状态：未编译：缺 TinyXML 开发包
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

XML 用元素、属性和文本表示树状数据。TinyXML 是较小的 DOM 解析库；TinyXML2 是另一套 API，不能直接替换头文件和类型。

## 何时使用

受控 XML 配置和小型文档。完整标准验证、大型流式处理或复杂命名空间场景应选择更适合的库。

## 如何使用

1. 限制输入大小、深度并核对库的安全能力。
2. 解析后检查 Error 与根节点。
3. 用 QueryIntAttribute 等带返回码的接口取值。
4. 文档拥有节点；文档销毁后不保留节点指针。

## 最小示例

以下命令从手册根目录执行。

[新 C++ 示例](../../examples/native/tinyxml_demo.cpp)解析合成元素并拒绝未闭合元素。

```sh
c++ -std=c++11 examples/native/tinyxml_demo.cpp -ltinyxml -o /tmp/handbook-xml
/tmp/handbook-xml
```

预期 `TinyXML parse and malformed input OK`；当前未执行。

## 常见问题

不要将结构解析成功视为业务验证成功。编码、空元素、重复属性和错误恢复须明确约定。不要将任意外部 XML 直接用于文件访问或执行命令。

## 参考资料

- [TinyXML 项目与文档入口](https://www.grinninglizard.com/tinyxml/)
- [XML 标准](https://www.w3.org/TR/xml/)
- [示例验证范围](../../examples/README.md)

# Base64

- 别名与生态：Base64
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：network
- 示例状态：已运行验证：Python 标准库
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

Base64 将二进制映射为可打印字符，常用于 JSON 中传输音频。它不是加密，不提供保密性或完整性保护。

## 何时使用

接收接口要求文本传输二进制时使用。编码后通常占 4×ceil(n/3) 字节；URL-safe 与标准字母表不同。

## 如何使用

1. 明确输入是字节还是 Unicode 文本。
2. 使用标准 Base64 编码后再转换为 ASCII 字符串。
3. 解码时按协议处理字母表与填充，严格模式可拒绝非法字符。
4. 与 API 的原始长度字段保持区别。

## 最小示例

以下命令均从仓库根目录运行。

[新编码示例](../../examples/python/encoding.py)：

```sh
python3 examples/python/encoding.py
```

中文 UTF-8 与二进制往返检查通过，同时验证 HMAC 标准向量。

## 常见问题

不要对原始音频做隐式文本解码。Base64 不是 URL 编码；标准编码中的 + / = 在 URL 中需要按规则处理。

## 参考资料

- [官方资料或明确标注的技术参考](https://www.rfc-editor.org/rfc/rfc4648.html)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)

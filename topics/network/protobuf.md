# Protocol Buffers：结构化二进制消息

- 别名与生态：Protobuf / proto3
- 适用版本与平台：proto3；protoc 与 Python protobuf 运行库必须兼容
- 标签：network
- 示例状态：未运行：缺 protoc 和 Python protobuf
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

Protocol Buffers 用 schema 和字段编号定义消息，并生成序列化 API。它不提供 TCP 消息边界、加密或业务字段合法性检查。

## 何时使用

跨进程消息、结构化结果存储和版本演进。需要两端共用 schema；调试可读性低于 JSON。

## 如何使用

1. 定义字段编号与类型；删除字段后保留编号，不重新分配。
2. 使用匹配的 protoc 生成目标语言绑定。
3. 编码前校验业务字段，解码前限制消息长度。
4. 在传输层保留消息边界；解析成功后仍检查范围和必填业务约束。

## 最小示例

以下命令从手册根目录执行。

[新 schema](../../examples/protobuf/sample.proto)与[往返检查](../../examples/protobuf/roundtrip.py)只使用合成测量值。

```sh
mkdir -p /tmp/handbook-proto
protoc -I examples/protobuf --python_out=/tmp/handbook-proto examples/protobuf/sample.proto
PYTHONPATH=/tmp/handbook-proto python3 examples/protobuf/roundtrip.py
```

预期 `Protobuf roundtrip and malformed input OK`；当前缺依赖，未执行。生成文件为临时构建产物，教学源文件均在本仓库。

## 常见问题

默认值不等于字段显式出现；需要存在性时使用适合版本的 optional 或 oneof。改变字段编号会破坏兼容性；嵌套深度、大小和不可信输入需限制。结合 [TCP 分包](tcp-framing.md)，不要把一次网络读取当一条 Protobuf。

## 参考资料

- [proto3 官方指南](https://protobuf.dev/programming-guides/proto3/)
- [生成代码与运行库兼容性](https://protobuf.dev/support/cross-version-runtime-guarantee/)
- [示例验证范围](../../examples/README.md)

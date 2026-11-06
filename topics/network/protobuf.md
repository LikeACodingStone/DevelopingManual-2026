# Protocol Buffers：结构化二进制消息

- 别名与生态：Protobuf / proto2 / proto3；Python 与 C++ 运行库
- 适用版本与平台：proto2 与 proto3；protoc 与运行库（Python protobuf、C++ libprotobuf）版本必须兼容
- 标签：network
- 示例状态：未运行：缺 protoc、Python protobuf 和 C++ 开发包
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

Protocol Buffers 用 schema 和字段编号定义消息，并生成序列化 API。它不提供 TCP 消息边界、加密或业务字段合法性检查。

schema 有两种语法，同一个工程里可能同时存在：

| 方面 | proto2 | proto3 |
| --- | --- | --- |
| 声明 | `syntax = "proto2";` | `syntax = "proto3";` |
| 必填字段 | 有 `required`（不建议新增，因为之后无法安全删除） | 没有 |
| 字段存在性 | 所有 `optional` 字段有 `has_*()` | 普通标量字段没有存在性；用 `optional` 或 `oneof` 才有 |
| 默认值 | 可用 `[default = ...]` 自定义 | 固定为零值，不能自定义 |

## 何时使用

跨进程消息、结构化结果存储和版本演进。需要两端共用 schema；调试可读性低于 JSON。

## 如何使用

1. 定义字段编号与类型；删除字段后保留编号，不重新分配。
2. 使用匹配的 protoc 生成目标语言绑定。
3. 编码前校验业务字段，解码前限制消息长度。
4. 在传输层保留消息边界；解析成功后仍检查范围和必填业务约束。

C++ 运行库的要点：

- 序列化到数组：先 `ByteSizeLong()` 得到大小，再 `SerializeToArray(缓冲区, 大小)`，并检查返回值；缺少 proto2 `required` 字段时序列化会失败。
- 解析：`ParseFromArray(数据, 长度)`，返回 `false` 表示数据截断、格式错误或缺少必填字段，此时不要使用目标对象。
- 存在性：proto2 用 `has_xxx()` 区分“未设置”和“设置成默认值”；读取未设置的字段得到声明的默认值。
- `SerializePartialToArray` 允许序列化未初始化的消息，只适合构造测试输入或调试。
- 程序开头用 `GOOGLE_PROTOBUF_VERIFY_VERSION` 检查头文件与库版本一致，结束时可调用 `ShutdownProtobufLibrary()`。

## 最小示例

以下命令从手册根目录执行。

[新 schema](../../examples/protobuf/sample.proto)与[往返检查](../../examples/protobuf/roundtrip.py)只使用合成测量值。

```sh
mkdir -p /tmp/handbook-proto
protoc -I examples/protobuf --python_out=/tmp/handbook-proto examples/protobuf/sample.proto
PYTHONPATH=/tmp/handbook-proto python3 examples/protobuf/roundtrip.py
```

预期 `Protobuf roundtrip and malformed input OK`；当前缺依赖，未执行。生成文件为临时构建产物，教学源文件均在本仓库。

[proto2 schema](../../examples/protobuf/legacy_v2.proto)与 [C++ 往返检查](../../examples/protobuf/cpp_roundtrip.cpp)演示 `required` 字段、`has_value()` 与默认值、缺少必填字段的数据被拒绝，以及截断输入被拒绝。

```sh
mkdir -p /tmp/handbook-proto-cpp
protoc -I examples/protobuf --cpp_out=/tmp/handbook-proto-cpp examples/protobuf/legacy_v2.proto
c++ -std=c++17 -Wall -Wextra -I/tmp/handbook-proto-cpp examples/protobuf/cpp_roundtrip.cpp /tmp/handbook-proto-cpp/legacy_v2.pb.cc $(pkg-config --cflags --libs protobuf) -o /tmp/proto-cpp
/tmp/proto-cpp
```

预期 `Protobuf C++ round trip, presence and required fields OK`；缺 protoc 和 C++ 开发包，未编译，不能当作已通过验证。

## 常见问题

默认值不等于字段显式出现；需要存在性时使用适合版本的 optional 或 oneof。改变字段编号会破坏兼容性；嵌套深度、大小和不可信输入需限制。结合 [TCP 分包](tcp-framing.md)，不要把一次网络读取当一条 Protobuf。

proto2 与 proto3 的消息可以互相解析（字段编号和线格式相同），但 `required`、默认值和存在性语义不同，混用前要逐字段核对。生成代码与运行库版本不匹配常见于升级一方而没升级另一方；较新的运行库对 C++ 标准版本也有要求，以所用版本的文档为准。工程声明的子模块或分支版本不等于实际链接的版本。

## 参考资料

- [proto3 官方指南](https://protobuf.dev/programming-guides/proto3/)
- [proto2 官方指南](https://protobuf.dev/programming-guides/proto2/)
- [C++ 生成代码指南](https://protobuf.dev/reference/cpp/cpp-generated/)
- [生成代码与运行库兼容性](https://protobuf.dev/support/cross-version-runtime-guarantee/)
- [示例验证范围](../../examples/README.md)

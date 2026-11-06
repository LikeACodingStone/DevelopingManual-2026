# Modbus / libmodbus

- 别名与生态：Modbus / libmodbus
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：iot
- 示例状态：新示例；需要外部开发库/环境，未编译或联调
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

Modbus 通过功能码访问线圈、离散输入、保持寄存器和输入寄存器。RTU 使用串行帧，TCP 使用 MBAP 头；libmodbus 提供对应客户端接口。

## 何时使用

工业设备或模拟器的数据读取与控制。寄存器映射、数值缩放和多寄存器字节/字顺序由设备文档决定。

## 如何使用

1. 根据传输选择 modbus_new_tcp 或 modbus_new_rtu。
2. 设置从站/单元标识、超时及串口参数。
3. 连接并用正确功能码读取指定区间。
4. 校验返回数量和错误，按设备映射解释数据。
5. close/free；写操作单独设计并确认设备语义。

## 最小示例

以下命令均从仓库根目录运行。

[新只读 libmodbus 示例](../../examples/native/modbus.c)读取本地模拟器 127.0.0.1:1502、unit 1 的两个保持寄存器。

```sh
cc -std=c11 examples/native/modbus.c -lmodbus -o /tmp/modbus-demo
/tmp/modbus-demo
```

需先配置模拟器，预期返回两个寄存器值。

## 常见问题

文档中的 40001 常对应 API 零基地址 0，但须核对设备约定。两个寄存器的浮点数顺序没有统一假设。不要将扫描到 SDK 实现视为实际设备验证。

## 参考资料

- [官方资料或明确标注的技术参考](https://libmodbus.org/reference/)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)

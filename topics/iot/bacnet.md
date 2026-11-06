# BACnet

- 别名与生态：BACnet
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：iot
- 示例状态：离线报文构造已验证；未与真实 BACnet 设备联调
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

BACnet 是楼宇自动化通信协议，用对象和属性表达设备信息。BACnet/IP 常用 UDP 47808；Who-Is/I-Am 用于设备发现，ReadProperty 用于属性读取。

## 何时使用

楼宇设备接入和协议网关。跨网段广播、BBMD、网络号和对象实例需要按现场网络配置。

## 如何使用

1. 确认设备支持 BACnet/IP 及授权测试网络。
2. 通过协议库或抓包理解 BVLC、NPDU、APDU 层。
3. 发送受限范围 Who-Is，接收并验证 I-Am。
4. 使用成熟协议栈读取对象属性，处理事务和错误。

## 最小示例

以下命令均从仓库根目录运行。

[新 Who-Is 构造示例](../../examples/python/bacnet_whois.py)默认只打印协议字节，不发送网络包。

```sh
python3 examples/python/bacnet_whois.py
# 如有测试设备才显式发送：
python3 examples/python/bacnet_whois.py --target 192.0.2.10
```

默认预期 `81 0b 00 0c 01 20 ff ff 00 ff 10 08`；目标地址只是示意，需替换。

## 常见问题

Who-Is 是发现请求，不是 ReadProperty；例子不实现 I-Am 解析或完整 BACnet 栈。发送使用临时源端口，有些现场设备/路由要求固定端口，应改用成熟协议栈。默认广播语义请求不能用于未授权网络。

## 参考资料

- [官方资料或明确标注的技术参考](https://bacnet.org/)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)

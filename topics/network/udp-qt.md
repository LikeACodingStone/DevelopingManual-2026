# UDP 与 QUdpSocket

- 别名与生态：UDP / Qt Network
- 适用版本与平台：Qt 5/6；IPv4 回环
- 标签：network
- 示例状态：未编译：缺 Qt 开发包
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

UDP 按数据报传输，保留单个报文边界，但不保证交付、顺序或去重。QUdpSocket 是 Qt 的 UDP 接口。

## 何时使用

发现协议、小型遥测与允许丢包的消息。需要可靠传输时，应设计序号、超时与重传，或选择 TCP。

## 如何使用

1. 绑定本地地址和端口，检查失败。
2. writeDatagram 发送受限长度报文。
3. readyRead 时循环清空待收数据报；先检查长度上限。
4. 校验发送方、业务字段和序号；超时不代表空消息。

## 最小示例

以下命令从手册根目录执行。

[回环示例](../../examples/qt/udp_demo.cpp)使用临时端口、1 秒接收超时和 1024 字节上限。

```sh
cmake -S examples/qt -B /tmp/handbook-qt
cmake --build /tmp/handbook-qt
```
```sh
/tmp/handbook-qt/udp_demo
```
预期 `UDP loopback OK`，当前未执行。教学示例只接收一个报文；连续服务须循环接收。

## 常见问题

读取缓冲过小会丢掉该数据报的剩余内容。大报文可能触发 IP 分片；不要依赖本机回环测试证明真实网络可靠性。源地址过滤不能替代认证。

## 参考资料

- [QUdpSocket](https://doc.qt.io/qt-6/qudpsocket.html)
- [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768.html)
- [示例验证范围](../../examples/README.md)

# WebSocket：握手、帧与关闭

- 别名与生态：WebSocket / RFC 6455；C++ 常见库 websocketpp（依赖 Asio）
- 适用版本与平台：RFC 6455（协议版本 13）；示例使用 Python 3 标准库，仅回环
- 标签：network
- 示例状态：Python 标准库实现已运行验证（握手、帧、掩码、分片、ping/pong、关闭与拒绝路径）；websocketpp 片段仅语法说明，未编译
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

WebSocket 先用一次 HTTP/1.1 `Upgrade` 握手，之后在同一条 TCP（或 TLS）连接上双向交换“帧”。帧自带长度，所以不需要再自己处理消息边界。帧类型由 opcode 决定：text、binary、continuation、close、ping、pong。

- 客户端发出的帧必须掩码，服务端发出的帧不得掩码。
- `ws://` 不加密，`wss://` 才是 TLS 上的 WebSocket。
- 协议只规定帧，不规定消息内容；JSON、Protobuf 等格式由应用约定。

## 何时使用

服务端主动推送、低延迟双向消息、浏览器可直接连接的通道。严格的请求/响应更适合 [HTTP](../../network/http.md)；同一台机器上的进程通信可考虑[Unix 域套接字](../programming/unix-domain-socket.md)；大文件传输不是它的强项。

## 如何使用

1. 握手：客户端发送 `GET`，带 `Upgrade: websocket`、`Connection: Upgrade`、`Sec-WebSocket-Key`（16 个随机字节的 Base64）和 `Sec-WebSocket-Version: 13`。服务端校验后返回 `101`，`Sec-WebSocket-Accept` 为 `Base64(SHA1(Key + 固定 GUID))`；校验失败返回 `400`。
2. 帧头：FIN 位、RSV1–3（没有协商扩展时必须为 0）、opcode、MASK 位、7 位长度（126 表示后接 16 位长度，127 表示后接 64 位长度）、掩码键（仅客户端帧）、负载。
3. 分片：首帧 opcode 为 text/binary 且 FIN=0，后续为 continuation，最后一帧 FIN=1。控制帧可插在分片之间，但不能分片且不超过 125 字节。
4. 关闭：一方发送 close 帧（可带 2 字节状态码，如 1000 正常、1002 协议错误、1007 数据无效、1009 消息过大），对端回应 close，然后才关闭 TCP。
5. 校验：文本消息必须是 UTF-8；在读取负载之前先检查长度上限；设置读超时，并用 ping/pong 做保活；浏览器场景要检查 `Origin`。
6. C++ 常用 websocketpp 作服务端：创建 `websocketpp::server<websocketpp::config::asio>`，设置 open/close/message 回调，依次 `init_asio()`、`listen()`、`start_accept()`、`run()`。它依赖 Asio（Boost.Asio 或独立 Asio），不是纯头文件零依赖。

## 最小示例

以下命令从手册根目录执行。

[websocket_minimal.py](../../../examples/python/websocket_minimal.py)只用标准库，在回环地址上完成握手、文本回显、ping/pong、分片重组和 close 握手。[测试文件](../../../examples/python/test_ipc_examples.py)包含 RFC 6455 中的 `Sec-WebSocket-Accept` 与掩码帧向量，以及这些拒绝路径：客户端帧未掩码、服务端帧被掩码、保留位、控制帧过长或被分片、超长负载（只读帧头就拒绝）、非法 UTF-8、无起始帧的 continuation、握手缺少 key 或版本不对。

```sh
python3 examples/python/websocket_minimal.py
python3 -m unittest discover -s examples/python -p 'test_ipc_*.py'
```

预期 `WebSocket handshake, framing, ping and close OK`，测试全部通过。已在 Linux x86_64、Python 3.12.3 上运行。示例不含 TLS、子协议、扩展、背压和并发写保护，不能当作生产服务器。

## 常见问题

- 一次 `recv` 不等于一个帧：按帧头给出的长度读满，见 [TCP 分包](../../network/tcp-framing.md)。
- 服务端必须关闭收到未掩码帧的连接；客户端收到 `Sec-WebSocket-Accept` 不匹配的响应必须放弃连接。
- 反向代理和负载均衡需要显式转发 `Upgrade`，并注意空闲超时；用 ping 保持连接。
- 协商 permessage-deflate 后要限制解压后的大小，见 [zlib](zlib.md)。
- 掩码用于防止代理缓存被误导，它不是加密；需要保密就用 `wss://`。
- websocketpp 的版本和维护状态须自行核对；本页未编译其示例。

## 参考资料

- [RFC 6455：The WebSocket Protocol](https://www.rfc-editor.org/rfc/rfc6455)
- [MDN：WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [websocketpp](https://github.com/zaphoyd/websocketpp)
- [示例验证范围](../../../examples/README.md)

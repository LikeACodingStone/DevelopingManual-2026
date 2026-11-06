# Unix 域套接字（AF_UNIX）

- 别名与生态：Unix domain socket / local socket / `AF_UNIX`；C++ 中为 `boost::asio::local::stream_protocol`
- 适用版本与平台：POSIX / Linux；示例使用 Python 3 标准库，`SO_PEERCRED` 仅 Linux
- 标签：programming
- 示例状态：Python 示例已运行验证，包含失败路径；Boost.Asio 写法仅为语法说明，未编译
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

Unix 域套接字是同一台主机上进程间通信的套接字。它用文件系统路径（Linux 还支持以 `\0` 开头的抽象名字）作为地址，类型有 `SOCK_STREAM`、`SOCK_DGRAM`、`SOCK_SEQPACKET`。与 TCP 回环相比：不经过网络协议栈，访问控制靠套接字文件的权限，可以取得对端进程的凭据（`SO_PEERCRED`，Linux），还能用 `SCM_RIGHTS` 传递文件描述符。

## 何时使用

本机守护进程的控制接口、同机多进程协作。需要跨主机时用 TCP；浏览器需要访问时用 [WebSocket](../network/websocket.md)。Windows 的 AF_UNIX 支持与 Linux 语义有差异，本页未验证。

## 如何使用

1. 把套接字放在私有目录里（权限 `0700`），路径不要太长：`sun_path` 只有约 108 字节。
2. 服务端：`bind` → `chmod`（例如 `0600`）→ `listen` → `accept`。
3. 遗留文件：进程崩溃后路径上可能留下文件，`bind` 会失败并报 `EADDRINUSE`。先尝试 `connect`：只有被拒绝（`ECONNREFUSED`）才说明没人监听，此时 `unlink` 后重新绑定；如果能连上，说明有进程在服务，应当报错而不是抢走路径。
4. `SOCK_STREAM` 是字节流，没有消息边界：用长度前缀，并在读取内容之前检查长度上限，见 [TCP 分包](../../network/tcp-framing.md)。
5. 可选的身份校验：读取 `SO_PEERCRED` 得到对端的 pid/uid/gid，与期望的用户比较。
6. 退出时关闭套接字并删除文件。
7. Boost.Asio 写法：`boost::asio::local::stream_protocol::acceptor` 与 `::endpoint`，构造 acceptor 之前通常需要先 `unlink` 旧文件；acceptor 不会在析构时替你删除文件。

## 最小示例

以下命令从手册根目录执行。

[unix_socket.py](../../../examples/python/unix_socket.py)在私有临时目录里创建套接字：先留下一个遗留文件并验证它被替换，再设置 `0600` 权限，客户端发送长度前缀消息，服务端校验对端 uid 后返回大写回显，最后清理目录。[测试](../../../examples/python/test_ipc_examples.py)覆盖：长度头超过上限就拒绝（不读正文）、消息被截断、已有活跃监听者时不抢占路径、路径过长。

```sh
python3 examples/python/unix_socket.py
python3 -m unittest discover -s examples/python -p 'test_ipc_*.py'
```

预期 `Unix domain socket framed echo OK`，测试全部通过。已在 Linux x86_64、Python 3.12.3 上运行。

## 常见问题

- `Address already in use`：路径上有遗留文件或另一个进程在监听，按上面的第 3 步区分。
- `AF_UNIX path too long`：缩短目录名；示例使用 `tempfile.mkdtemp()` 生成短路径。
- 放在所有人可写的目录（如 `/tmp`）里的套接字，路径可能被他人抢先创建；用私有子目录，并在需要时校验对端 uid。
- Linux 抽象命名空间的套接字没有文件权限，访问控制只能靠 `SO_PEERCRED` 之类的检查。
- 一次 `recv` 不等于一条消息；对端关闭时 `recv` 返回 0 字节。
- 向已关闭的对端写入会触发 `EPIPE`，默认还会收到 `SIGPIPE`。

## 参考资料

- [Linux unix(7)](https://man7.org/linux/man-pages/man7/unix.7.html)
- [Python socket](https://docs.python.org/3/library/socket.html)
- [Boost.Asio local 套接字](https://www.boost.org/doc/libs/release/doc/html/boost_asio/reference/local__stream_protocol.html)
- [示例验证范围](../../../examples/README.md)

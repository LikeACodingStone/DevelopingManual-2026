# zlib 与 DEFLATE 压缩

- 别名与生态：zlib / DEFLATE（RFC 1951）/ gzip（RFC 1952）；C 库与 Python `zlib` 模块
- 适用版本与平台：zlib 1.x C API；Python 3 标准库；Linux 本机已验证
- 标签：network
- 示例状态：Python 与 C 示例均已运行验证，包含损坏、截断、超限和包装格式不匹配的失败路径
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

DEFLATE 是一种无损压缩算法。zlib 库实现它，并提供三种外层封装，算法相同但头尾不同：

| 封装 | 头部 | 校验 | Python wbits |
| --- | --- | --- | --- |
| zlib（RFC 1950） | 2 字节，常见 `78 ..` | Adler-32 | `15` |
| gzip（RFC 1952） | 至少 10 字节，`1f 8b` 开头 | CRC-32 | `31` |
| raw deflate | 无 | 无 | `-15` |

zlib 不是加密，也不是归档格式：没有文件名和目录，zip/tar 是另一类技术。

## 何时使用

日志和消息压缩、HTTP `Content-Encoding`、PNG 等格式内部的压缩流。已经压缩过的数据（JPEG、MP3、视频）通常压不小；很短的消息压缩收益小，延迟和 CPU 成本反而更突出。

## 如何使用

1. 选封装：与对端约定是 zlib、gzip 还是 raw；Python 解压时 `wbits` 必须匹配（`32 + 15` 可自动识别 zlib/gzip）。
2. 一次性接口：C 用 `compress2()` / `uncompress()`，目标缓冲区大小用 `compressBound()` 估算；解压必须事先知道或限制输出大小。
3. 流式接口：`deflateInit` → 循环 `deflate` → `deflateEnd`；`inflateInit` → 循环 `inflate` → `inflateEnd`。冲刷方式：`Z_NO_FLUSH`、`Z_SYNC_FLUSH`（让已写入的数据立即可解）、`Z_FINISH`（结束流）。
4. 判读返回值：`Z_STREAM_END` 表示流完整结束；`Z_OK` 和 `Z_BUF_ERROR` 在流式循环里通常表示“还要输入或输出空间”，不是致命错误；`Z_DATA_ERROR` 表示数据损坏或封装不匹配；`Z_MEM_ERROR` 表示内存不足。
5. 解压时限制输出大小，并检查流确实结束（C 判断 `Z_STREAM_END`，Python 判断 `decompressobj().eof`），再检查尾部是否多出数据。
6. 压缩后不更小就保留原文，并用标志位告诉接收方。

## 最小示例

以下命令从手册根目录执行。

[Python 示例](../../../examples/python/zlib_demo.py)演示三种封装的头部、匹配的 `wbits`、损坏/截断/超限/尾随数据的拒绝、不可压缩数据的回退，以及 `Z_SYNC_FLUSH`。[C 示例](../../../examples/native/zlib_demo.c)演示 `compress2` / `uncompress`、使用 64 字节输出块的流式 `deflate` 循环、带上限的 `inflate`，以及截断和损坏输入。

```sh
python3 examples/python/zlib_demo.py
cc -std=c11 -Wall -Wextra -Werror examples/native/zlib_demo.c -lz -o /tmp/zlib-demo
/tmp/zlib-demo
```

预期输出依次为 `zlib formats, limits and corruption checks OK` 和 `zlib C round trip OK`。已在 Linux x86_64、gcc 13.3、Python 3.12.3 上运行。[测试](../../../examples/python/test_ipc_examples.py)另外覆盖 1000 万字节零数据的解压炸弹被 1 MiB 上限拒绝。

## 常见问题

- 流式 `deflate(Z_FINISH)` 只在返回 `Z_STREAM_END` 时才算完成；返回 `Z_OK` 或 `Z_BUF_ERROR` 要换新的输出缓冲区继续调用。
- 小而高度重复的输入可以解压成很大的输出（解压炸弹）：始终限制输出，不信任对端声明的大小。
- 先压缩后加密，且压缩内容同时包含秘密和攻击者可控的数据时，压缩后长度会泄露信息（CRIME/BREACH 类问题）。
- 一个 `z_stream` 不要被多个线程同时使用。
- 不同实现（如 zlib-ng）的压缩输出字节可能不同，但都应能互相解压；不要拿压缩后的字节做稳定的哈希或比较。
- zlib 不限制流结束之后的尾随数据，是否允许由上层协议决定；本页示例选择拒绝。

## 参考资料

- [zlib 手册](https://www.zlib.net/manual.html)
- [RFC 1950 zlib](https://www.rfc-editor.org/rfc/rfc1950)、[RFC 1951 DEFLATE](https://www.rfc-editor.org/rfc/rfc1951)、[RFC 1952 gzip](https://www.rfc-editor.org/rfc/rfc1952)
- [Python zlib](https://docs.python.org/3/library/zlib.html)
- [示例验证范围](../../../examples/README.md)

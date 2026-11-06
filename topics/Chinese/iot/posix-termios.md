# POSIX 串口：termios

- 别名与生态：termios / `tcgetattr` / `tcsetattr`（POSIX，Linux 设备节点如 `/dev/ttyUSB0`；不是 Qt 串口，也不是 Windows Win32 串口 API）
- 适用版本与平台：Linux / POSIX；示例在 Linux x86_64 上用伪终端验证
- 标签：iot
- 示例状态：已编译运行验证（伪终端回环，不打开真实串口）；真实设备未联调
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

termios 是 POSIX 描述终端和串口行为的接口。`struct termios` 包含输入、输出、控制、本地四组模式标志，控制字符数组（其中 `VMIN`/`VTIME` 决定读操作何时返回），以及波特率。串口设备和伪终端（pty）都用同一套接口配置。

## 何时使用

在 Linux 上直接用 C 访问串口设备，例如与读卡器、传感器或调试口通信，且不想引入框架时。需要跨平台（Windows、macOS）时，改用 [Qt 串口](../../programming/qt-serial.md) 之类的封装。它只负责字节如何收发，设备的报文格式要看设备自己的协议文档。

## 如何使用

1. 用 `open(path, O_RDWR | O_NOCTTY)` 打开设备；先用 `tcgetattr` 保存原设置，退出前恢复。
2. 配置：`cfmakeraw()` 取得“原始”模式（关闭回显、行缓冲、CR/LF 转换和信号字符），然后设置 8N1：`c_cflag |= CS8`，清除 `PARENB`、`CSTOPB`、`CRTSCTS`，加上 `CLOCAL | CREAD`。
3. 波特率：`cfsetispeed()` / `cfsetospeed()` 设置 `B9600`、`B115200` 等预定义值。
4. 读超时：`VMIN`/`VTIME`。`VMIN=0, VTIME=0` 立即返回；`VMIN>0, VTIME=0` 阻塞到收满 `VMIN` 字节；`VMIN=0, VTIME>0` 最多等待 `VTIME`×0.1 秒，超时返回 0；`VMIN>0, VTIME>0` 是字节间超时。
5. `tcsetattr(fd, TCSAFLUSH, &tio)` 应用设置，随后用 `tcgetattr` 回读核对，因为 `tcsetattr` 在只应用了部分更改时也可能返回成功。
6. 读写循环处理短读、`EINTR` 和超时返回的 0 字节；写完后需要确保发出时用 `tcdrain()`。
7. 非标准波特率在 Linux 上要用 `termios2` 与 `BOTHER`（头文件 `<asm/termbits.h>`，不能与 `<termios.h>` 同一个编译单元包含）。这是 Linux 专用扩展，本手册没有验证。
8. 权限：用户通常需要属于 `dialout` 一类的组才能打开设备。

## 最小示例

以下命令从手册根目录执行。

[termios_pty.c](../../../examples/native/termios_pty.c)创建一对伪终端，把从端当作“串口”配置为 115200 8N1 原始模式，验证：回读设置、字节原样通过（`\r` 不被改成 `\n`，`0x00` 和 `0xFF` 不丢失）、反方向回复、`VMIN=0, VTIME=5` 在静默时约 0.5 秒后返回 0。

```sh
cc -std=c11 -Wall -Wextra -Werror examples/native/termios_pty.c -o /tmp/termios-pty
/tmp/termios-pty
```

预期 `termios pty loopback OK`。已在 Linux x86_64、gcc 13.3 上运行。为确认检查有效，另做过一次变异测试：去掉 `cfmakeraw` 后示例会报告 `raw mode was not applied` 并以失败退出。

## 常见问题

- 伪终端不模拟波特率、校验、流控和线路错误，所以这个示例证明的是配置和读写逻辑，不是真实设备联调。
- 收到的 `\r` 变成 `\n`：没有关闭 `ICRNL`，使用 `cfmakeraw()`。
- 读操作一直阻塞：检查 `VMIN`/`VTIME`，或改用 `select`/`poll`。
- 打开某些 USB 串口会拉低 DTR，导致带自动复位的开发板重启。
- 多个进程同时打开同一设备会互相抢数据；可用独占打开（`TIOCEXCL`）或锁文件约定。
- USB 串口设备被拔出后，读写通常返回 `EIO`，要关闭并重新打开。

## 参考资料

- [POSIX termios.h](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/termios.h.html)
- [Linux termios(3)](https://man7.org/linux/man-pages/man3/termios.3.html)
- [示例验证范围](../../../examples/README.md)

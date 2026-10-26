# Qt 串口与 QextSerialPort

- 别名与生态：QextSerialPort；对照 Qt SerialPort / QSerialPort
- 适用版本与平台：示例针对 QextSerialPort 1.2 与 Qt 5；Qt 6 移植未确认
- 标签：programming
- 示例状态：未编译、未设备验证；默认不打开设备
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

串口提供字节流，应用层需定义帧边界和校验。QextSerialPort 是独立扩展库；Qt SerialPort 的 QSerialPort 是另一套 API。

## 何时使用

串口仪器通信或维护旧 QextSerialPort 应用。新工程可评估官方 QSerialPort，但端口枚举、配置和错误 API 需要迁移。

## 如何使用

1. 明确设备名、波特率、数据位、校验、停止位和流控。
2. 在对象所属线程打开端口并检查失败。
3. readyRead 时读取并累积数据，按协议提取完整帧。
4. 设置长度上限与超时，处理拔出和关闭。

## 最小示例

以下命令从手册根目录执行。

[新只读示例](../../examples/qt/serial/serial_demo.cpp)与[qmake 配置](../../examples/qt/serial/serial.pro)均在本仓库。QextSerialPort 头文件和库是外部安装依赖。

```sh
serial_source="$PWD/examples/qt/serial/serial.pro"
mkdir -p /tmp/handbook-serial
(cd /tmp/handbook-serial && qmake "$serial_source" QEXT_INCLUDE=/opt/qext/include QEXT_LIB=/opt/qext/lib && make)
/tmp/handbook-serial/serial_demo
```

将依赖目录换成实际安装路径。默认仅打印说明；需要读设备时显式使用 `--read-device DEVICE`，持续两秒并只报告字节数。本轮未打开任何端口；打开只读端口仍可能改变设备控制线状态。

## 常见问题

一次 readyRead 不是一帧。读到零字节不等于完整应答。QextSerialPort 的 BAUD9600 等常量不能直接当作 QSerialPort 枚举；QT += serialport 也不等于链接了 QextSerialPort。

## 参考资料

- [QextSerialPort 项目与 API](https://github.com/qextserialport/qextserialport)
- [Qt Serial Port](https://doc.qt.io/qt-6/qtserialport-index.html)
- [示例验证范围](../../examples/README.md)

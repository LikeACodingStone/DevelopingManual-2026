# 示例与验证范围

所有路径从仓库根目录运行。开发依赖由使用者按系统安装，本仓库不附带旧二进制、账号、模型或第三方源码副本。

## 已验证

| 示例 | 内容 | 运行方式 |
| --- | --- | --- |
| pcm-read-write/ | PCM/WAV 往返、流式分帧、声道提取 | `make demo`，`make test` |
| python/framed_tcp.py | 本地 TCP 长度前缀消息 | `python3 examples/python/framed_tcp.py` |
| python/http_local.py | 本地 UTF-8 JSON POST | `python3 examples/python/http_local.py` |
| python/encoding.py | Base64、HMAC 标准向量 | `python3 examples/python/encoding.py` |
| python/vad.py | 新能量门控状态机，不是真正语音分类 | `python3 examples/python/vad.py` |
| python/bacnet_whois.py | 默认仅构造发现报文 | `python3 examples/python/bacnet_whois.py` |
| native/threads.c | 独立新写互斥计数器与双线程验证 | `make test` 自动编译运行 |
| native/semaphore.c、varargs.c | 信号量、可变参数 | `make test` 自动编译运行 |
| native/embed_python.c | 嵌入 Python 3.12 | 本机开发包存在，编译运行通过 |
| native/tls.c | OpenSSL TLS 身份验证配置 | 本机编译通过，未访问外网 |
| media/codec_demo.py | FFmpeg MP3、ADTS AAC、Ogg Opus 编解码 | `make test-media` |

`make test` 检查文档链接、Python 测试、本地 TCP/HTTP 和 C 基础示例。需要 Python 3、C 编译器、pkg-config；Python 嵌入与 OpenSSL 编译检查缺少可选开发包时明确打印 SKIP。`make test-media` 还要求安装具有相应编码器的 FFmpeg。

FFmpeg 验证不能代替 libopus、libmad、FAAD2 C 接口示例的构建验证。编解码为有损转换，只验证可解码、样本格式与时长范围，不要求样本逐字节相等。

## 需外部依赖，尚未编译/联调

| 文件 | 依赖 | 范围 |
| --- | --- | --- |
| native/alsa.c、mixer.c | alsa-lib 开发包；实际 mixer 需要设备 | 写静音 / 只读音量查询 |
| native/tinyalsa.c | tinyalsa 开发包和音频设备 | 写静音 |
| native/opus.c | libopus 开发包 | 内存中的真实包编解码 |
| native/resample.c | SpeexDSP 开发包 | 有状态重采样 |
| native/mad.c | libmad 开发包和 MP3 文件 | 统计实际解码帧 |
| native/faad.c | FAAD2 开发包和 ADTS 文件 | 统计实际解码样本 |
| native/cjson.c | cJSON 开发包 | 结构化解析与类型检查 |
| native/curl.c | libcurl 开发包 | 指定 URL 的请求 |
| native/paho.c | Paho MQTT C、本地 Broker | QoS 1 发布 |
| native/modbus.c | libmodbus、本地 Modbus 模拟器 | 只读保持寄存器 |
| python/selenium_demo.py | Selenium 4、Chrome 和匹配驱动 | 本地 HTML 自动化 |
| integrations/baidu_speech.py | 当前 token/服务权限 | 构造代码离线验证；云请求未执行 |

各条目提供构建和运行命令。调用云服务、连接设备或 Broker 不属于自动测试。

## 接入契约，不是厂商实现

[integrations/sdk_session.py](integrations/sdk_session.py)用于说明专有 SDK 的资源生命周期；不调用云知声、Voice 或唤醒 SDK，不生成模拟识别结果。故障注入测试只验证失败路径释放，不代表 SDK 集成成功。

## 2021 技术条目新增示例

所有教学源文件均为本手册独立新写。没有从历史工程或备份复制实现；构建产物可写入临时目录，外部开发库属于安装依赖，不是手册源码引用。

| 文件 | 验证范围 |
| --- | --- |
| python/sqlite_demo.py | Python 标准库，内存事务与约束失败回滚，已运行 |
| protobuf/sample.proto、roundtrip.py | 新 schema 与坏输入检查；缺 protoc/Python protobuf，未运行 |
| qt/json_demo.cpp、udp_demo.cpp、threads_demo.cpp、sqlite_demo.cpp | Qt 5/6 Core/Network/Sql；缺开发包，未编译；UDP 仅回环 |
| qt/serial/serial_demo.cpp、serial.pro | QextSerialPort 1.2/Qt 5；未编译，未打开设备，默认只打印说明 |
| native/tinyxml_demo.cpp | TinyXML 2.6 API；缺开发包，未编译 |
| native/mosquitto_demo.c | libmosquitto；缺开发包，未编译，未连接 Broker |
| java/PahoLocal.java | Java SE/Paho 1.2.x；缺 JDK/JAR，未编译；不是 Android APK |

构建和运行命令见对应技术页。Android Service 仍为生命周期接入说明，没有伪造可运行 Android 工程。可选依赖缺失时检查脚本明确报告 SKIP，不当作测试通过。

本轮实际检查环境：Linux x86_64，Python 3.12.3。`make test` 通过文档链接/结构检查、Python 语法与 9 项单元测试、本地 TCP/HTTP、SQLite 回滚和基础 C 示例；Qt、TinyXML、libmosquitto、Protobuf、Java 缺依赖明确跳过。`git diff --check` 通过；没有执行媒体重新编码、Broker、设备或云端联调。

## 2025 技术条目新增示例

所有教学源文件均为本手册独立新写，没有复制历史工程源码。运行方式见对应技术页；`make test` 自动运行表中标“已运行”的项目。

| 文件 | 验证范围 |
| --- | --- |
| python/websocket_minimal.py | 标准库；回环握手、帧、掩码、分片、ping/pong、关闭；已运行 |
| python/unix_socket.py | 标准库；AF_UNIX 回环，含遗留文件、权限、对端 uid；已运行 |
| python/zlib_demo.py、native/zlib_demo.c | zlib 三种封装、损坏/截断/超限输入；Python 与 C 均已运行 |
| native/termios_pty.c | 伪终端上的 termios 配置与读超时；已运行，不打开真实串口 |
| python/test_ipc_examples.py | 上述 Python 示例的 RFC 向量与拒绝路径测试，23 项 |

| 文件 | 依赖 | 范围 |
| --- | --- | --- |
| native/jsoncpp_demo.cpp | jsoncpp 开发包 | 严格解析与类型检查；未编译 |
| native/lua_embed.c | Lua 5.4 开发包 | 注册 C 函数、保护调用、栈平衡；未编译 |
| native/sqlite_c_readonly.c | sqlite3 开发包 | 只读连接与失败路径；未编译 |
| protobuf/legacy_v2.proto、cpp_roundtrip.cpp | protoc、libprotobuf | proto2 必填字段与存在性；未编译 |
| java/jni/ | JDK、`jni.h` | 字符串、数组、异常、句柄；未编译 |
| android/aidl-service/ | Android SDK | Java AIDL 服务与客户端；结构示意，未构建 |
| android/aidl-hal/ | AOSP 源码树 | 稳定 AIDL HAL；结构示意，未构建 |

检查脚本对上表中可以自动构建的项目（jsoncpp、Lua、SQLite C、Protobuf C++、JNI）在依赖存在时编译运行，缺失时明确打印 SKIP；这些依赖安装后的行为本轮没有被实际检验。Android 两个目录没有对应的 Android 工程或设备，没有伪造构建结果。

本轮（2025）实际检查环境：Linux x86_64，Python 3.12.3，gcc 13.3。`make test` 通过：文档链接/结构检查 82 个文件、Python 单元测试 32 项（pcm 3 项 + 示例 29 项，其中本轮新增 23 项）、本地 TCP/HTTP、新增的 WebSocket / Unix 套接字 / zlib（Python 与 C）/ termios 伪终端示例，以及原有的基础 C 示例。jsoncpp、Lua、SQLite C、Protobuf、Protobuf C++、JNI、Android、Qt、TinyXML、libmosquitto、Paho Java 因缺少依赖明确跳过。没有执行 Android 构建、真实串口、浏览器 WebSocket 或其他设备/云端联调。

# 技术查询手册

[English](README_EN.md) · 中文（本文件）

查询具体技术是什么、何时使用、如何使用，以及示例与常见问题。技术分类仅用于导航，不按分类创建子仓库。

[2016 确认清单](catalog/2016-scope.md)包含 31 个正式条目；[2019 清单](catalog/2019Codes-scope.md)记录 SkEgn；[2021 清单](catalog/2021Codes-scope.md)新增 9 个条目并更新 MQTT/TCP。另有 FIDL 页面，共 42 个页面。[2023 清单](catalog/2023Codes-scope.md)仍是待确认候选，尚无正式页。[2025 清单](catalog/Chinese/2025Codes-scope.md)按推荐范围实施，见下文“2025Codes 扫描结果”。以下按手册示例使用的主要语言或框架导航；跨语言主题可能出现在多个表中。所有教学代码位于本仓库 `examples/`。

## 语言版本与目录

- 根目录索引：`README.md` 是主 README（中文），`README_CH.md` 是它的同内容中文专版，`README_EN.md` 是英文版。`README.md` 与 `README_CH.md` 正文必须一致，检查脚本会比对。
- 2025Codes 起的新页面按语言分目录：`topics/Chinese/<分类>/` 与 `topics/English/<分类>/`，内容相同、语言不同；扫描记录同理：`catalog/Chinese/`、`catalog/English/`。
- 2025Codes 之前的 42 个页面仍在 `topics/<分类>/`，只有中文。其中 SQLite、Protobuf、FIDL 在 2025 轮次更新，已在 `topics/English/` 补全英文版；其余尚无英文版，英文索引里用 (zh) 标出。
- 教学代码只有一份，位于 `examples/`，不分语言。`examples/README.md` 的英文版是 `examples/README_EN.md`；来源说明在 `catalog/Chinese/sources.md`，英文版是 `catalog/English/sources.md`。根目录不放 sources 文件。

## C / C++ 示例

| 领域 | 技术条目 |
| --- | --- |
| 音频处理 | [ALSA](topics/audio/alsa.md)、[ALSA Mixer](topics/audio/alsa-mixer.md)、[AAC / ADTS / FAAD2](topics/audio/aac-adts-faad.md)、[MP3 / libmad](topics/audio/mp3-libmad.md)、[Opus](topics/audio/opus.md)、[SpeexDSP 重采样](topics/audio/resampling.md)、[tinyalsa](topics/audio/tinyalsa.md) |
| 网络与数据 | [JSON / cJSON](topics/network/json-cjson.md)、[JsonCpp](topics/Chinese/network/jsoncpp.md)、[libcurl](topics/network/libcurl.md)、[TLS / OpenSSL](topics/network/tls-openssl.md)、[zlib / DEFLATE](topics/Chinese/network/zlib.md) |
| 物联网 | [libmosquitto](topics/iot/libmosquitto.md)、[Modbus](topics/iot/modbus.md)、[MQTT](topics/iot/mqtt.md)、[Paho C](topics/iot/paho-c.md)、[POSIX 串口 termios](topics/Chinese/iot/posix-termios.md) |
| 编程机制 | [C 调用 Python](topics/programming/embed-python.md)、[Lua 嵌入](topics/Chinese/programming/lua-embed.md)、[pthread](topics/programming/pthread.md)、[信号量](topics/programming/semaphore.md)、[Unix 域套接字](topics/Chinese/programming/unix-domain-socket.md)、[C 可变参数](topics/programming/varargs.md)、[XML / TinyXML](topics/network/xml-tinyxml.md) |

## Python 示例

| 领域 | 技术条目 |
| --- | --- |
| 音频处理 | [PCM](topics/audio/pcm.md)、[WAV](topics/audio/wav.md)、[Opus / FFmpeg](topics/audio/opus.md) |
| 网络与数据 | [Base64](topics/network/base64.md)、[HMAC-SHA256](topics/network/hmac-sha256.md)、[HTTP](topics/network/http.md)、[Protobuf](topics/network/protobuf.md)、[SQLite](topics/network/sqlite.md)、[TCP 分包](topics/network/tcp-framing.md)、[WebSocket](topics/Chinese/network/websocket.md)、[zlib / DEFLATE](topics/Chinese/network/zlib.md) |
| 物联网 | [BACnet](topics/iot/bacnet.md) |
| 编程机制 | [Selenium](topics/programming/selenium.md)、[Unix 域套接字](topics/Chinese/programming/unix-domain-socket.md) |
| 语音与 SDK 接入契约 | [百度 ASR](topics/speech/baidu-asr.md)、[百度 TTS](topics/speech/baidu-tts.md)、[SkEgn](topics/speech/skegn.md)、[云知声 ASR](topics/speech/unisound-asr.md)、[VAD](topics/speech/vad.md)、[Voice 前处理](topics/speech/voice-preprocessing.md)、[关键词唤醒](topics/speech/wake-word.md) |

## Qt（C++）示例

| 领域 | 技术条目 |
| --- | --- |
| 数据、网络与设备 | [Qt JSON](topics/network/qt-json.md)、[SQLite / Qt SQL](topics/network/sqlite.md)、[UDP / QUdpSocket](topics/network/udp-qt.md)、[Qt 串口 / QextSerialPort](topics/programming/qt-serial.md) |
| 并发 | [Qt 线程与队列信号槽](topics/programming/qt-threads.md) |

## Java / Android 示例

| 平台 | 技术条目 |
| --- | --- |
| JVM / Android 接入 | [Paho Java / Android](topics/iot/paho-java.md)、[JNI](topics/Chinese/programming/jni.md) |
| Android 系统接口 | [Android AIDL（Java 服务与 Binder）](topics/Chinese/programming/android-aidl.md)、[Android 稳定 AIDL HAL](topics/Chinese/programming/android-aidl-hal.md) |

## 接口描述语言

[FIDL](topics/ipc/fidl.md) 区分 Fuchsia FIDL 与 Franca IDL；2025 轮次补充了 Franca 的版本、导入、广播与自研生成器说明。页面提供语法示意，不依赖特定手册示例语言。

## 2025Codes 扫描结果

扫描对象是一个 ETC/VICS 车载收费与交通信息项目。静态读取，没有构建或联调。完整证据、数量与限制见[扫描记录](catalog/Chinese/2025Codes-scope.md)。

结果：新增候选 17 项，更新现有页面 3 项，合并 3 项，暂缓 7 组。按推荐范围实施：本轮写了其中 9 个新页和 3 个更新；另外 8 个可选候选保持待定。

### 已完成：9 个新页与 3 个更新

| 页面 | 示例状态 |
| --- | --- |
| [WebSocket](topics/Chinese/network/websocket.md) | 已运行验证（Python 标准库 + RFC 6455 向量） |
| [zlib / DEFLATE](topics/Chinese/network/zlib.md) | 已运行验证（Python 与 C） |
| [JsonCpp](topics/Chinese/network/jsoncpp.md) | 未编译：缺 jsoncpp |
| [POSIX 串口 termios](topics/Chinese/iot/posix-termios.md) | 已运行验证（伪终端，不含真实设备） |
| [Unix 域套接字](topics/Chinese/programming/unix-domain-socket.md) | 已运行验证（Python） |
| [Lua 嵌入](topics/Chinese/programming/lua-embed.md) | 未编译：缺 Lua 开发包 |
| [JNI](topics/Chinese/programming/jni.md) | 未编译：缺 JDK |
| [Android AIDL](topics/Chinese/programming/android-aidl.md) | 结构示意：缺 Android SDK |
| [Android 稳定 AIDL HAL](topics/Chinese/programming/android-aidl-hal.md) | 结构示意：缺 AOSP |
| 更新：[SQLite](topics/network/sqlite.md) | 新增 C API；C 示例未编译 |
| 更新：[Protobuf](topics/network/protobuf.md) | 新增 proto2/proto3 与 C++ 运行库；C++ 示例未编译 |
| 更新：[FIDL](topics/ipc/fidl.md) | 新增 Franca 版本、导入、广播和自研生成器说明；语法示意 |

### 待定：8 个可选候选（尚未编写）

Android TextToSpeech、D-Bus（libdbus）、CMake、Android Gradle 与 NDK、OpenGL ES / EGL、Boost.Test、GoogleTest、Mermaid。需要时再确认要写哪几项。

### 合并 3 项与暂缓 7 组

合并：多处 SQLite 调用点合并为 SQLite 更新；78 个 `.proto` 合并为 Protobuf 更新；同一 Java 服务内的多个 AIDL 与重复的 `aidl_api` 快照合并进对应 AIDL 条目。

暂缓：ETC/DSRC/VICS 设备协议与业务逻辑；随包第三方库与工具二进制；AWS Signature V4（无调用点）；NDS 导航数据库；文档工具链（AsciiDoc、Doxygen、PlantUML、UMLet）；在线服务与导航业务接口；自有基础框架与重复工程。每组的原因与恢复条件见扫描记录。

## 使用与维护

- [给 Codex 的提取指令](command_for_ai.md)：扫描其他项目时使用的流程与指令模板，含双语版本约定。
- [示例和验证范围](examples/README.md)：查看已运行、需开发库/设备和接口契约的区别。
- [条目模板](topics/TEMPLATE.md)（[英文模板](topics/TEMPLATE_EN.md)）、[维护约定](CONTRIBUTING.md)。
- [代码来源与复用判断](catalog/Chinese/sources.md)：教学示例的独立来源、历史复用清理和验证边界。
- [其他待筛选候选](catalog/candidates.md)：历史线索，尚未逐项核实。

```sh
make demo          # 生成 PCM 与 WAV 到 /tmp/pcm-demo
make test          # 文档、Python、本地网络与基础 C 示例
make test-media    # 上述检查 + FFmpeg MP3/AAC/Opus 实际编解码
```

无须安装全部外部 SDK 即可查询手册。各页明确自己的依赖和验证范围，不把 mock 或语法示意标成真实集成。

# 技术查询手册

查询具体技术是什么、何时使用、如何使用，以及示例与常见问题。技术分类仅用于导航，不按分类创建子仓库。

[2016 确认清单](catalog/2016-scope.md)包含 31 个正式条目；[2019 清单](catalog/2019Codes-scope.md)记录 SkEgn；[2021 清单](catalog/2021Codes-scope.md)新增 9 个条目并更新 MQTT/TCP。另有 FIDL 页面。以下按手册示例使用的主要语言或框架导航；跨语言主题可能出现在多个表中。所有教学代码位于本仓库 `examples/`。

## C / C++ 示例

| 领域 | 技术条目 |
| --- | --- |
| 音频处理 | [ALSA](topics/audio/alsa.md)、[ALSA Mixer](topics/audio/alsa-mixer.md)、[AAC / ADTS / FAAD2](topics/audio/aac-adts-faad.md)、[MP3 / libmad](topics/audio/mp3-libmad.md)、[Opus](topics/audio/opus.md)、[SpeexDSP 重采样](topics/audio/resampling.md)、[tinyalsa](topics/audio/tinyalsa.md) |
| 网络与数据 | [JSON / cJSON](topics/network/json-cjson.md)、[libcurl](topics/network/libcurl.md)、[TLS / OpenSSL](topics/network/tls-openssl.md) |
| 物联网 | [libmosquitto](topics/iot/libmosquitto.md)、[Modbus](topics/iot/modbus.md)、[MQTT](topics/iot/mqtt.md)、[Paho C](topics/iot/paho-c.md) |
| 编程机制 | [C 调用 Python](topics/programming/embed-python.md)、[pthread](topics/programming/pthread.md)、[信号量](topics/programming/semaphore.md)、[C 可变参数](topics/programming/varargs.md)、[XML / TinyXML](topics/network/xml-tinyxml.md) |

## Python 示例

| 领域 | 技术条目 |
| --- | --- |
| 音频处理 | [PCM](topics/audio/pcm.md)、[WAV](topics/audio/wav.md)、[Opus / FFmpeg](topics/audio/opus.md) |
| 网络与数据 | [Base64](topics/network/base64.md)、[HMAC-SHA256](topics/network/hmac-sha256.md)、[HTTP](topics/network/http.md)、[Protobuf](topics/network/protobuf.md)、[SQLite](topics/network/sqlite.md)、[TCP 分包](topics/network/tcp-framing.md) |
| 物联网 | [BACnet](topics/iot/bacnet.md) |
| 编程机制 | [Selenium](topics/programming/selenium.md) |
| 语音与 SDK 接入契约 | [百度 ASR](topics/speech/baidu-asr.md)、[百度 TTS](topics/speech/baidu-tts.md)、[SkEgn](topics/speech/skegn.md)、[云知声 ASR](topics/speech/unisound-asr.md)、[VAD](topics/speech/vad.md)、[Voice 前处理](topics/speech/voice-preprocessing.md)、[关键词唤醒](topics/speech/wake-word.md) |

## Qt（C++）示例

| 领域 | 技术条目 |
| --- | --- |
| 数据、网络与设备 | [Qt JSON](topics/network/qt-json.md)、[SQLite / Qt SQL](topics/network/sqlite.md)、[UDP / QUdpSocket](topics/network/udp-qt.md)、[Qt 串口 / QextSerialPort](topics/programming/qt-serial.md) |
| 并发 | [Qt 线程与队列信号槽](topics/programming/qt-threads.md) |

## Java 示例

| 平台 | 技术条目 |
| --- | --- |
| JVM / Android 接入 | [Paho Java / Android](topics/iot/paho-java.md) |

## 接口描述语言

[FIDL](topics/ipc/fidl.md) 区分 Fuchsia FIDL 与 Franca IDL；页面提供语法示意，不依赖特定手册示例语言。

## 使用与维护

- [给 Codex 的提取指令](command_for_ai.md)：扫描其他项目时使用的流程与指令模板。
- [示例和验证范围](examples/README.md)：查看已运行、需开发库/设备和接口契约的区别。
- [条目模板](topics/TEMPLATE.md)、[维护约定](CONTRIBUTING.md)。
- [代码来源与复用判断](sources.md)：教学示例的独立来源、历史复用清理和验证边界。
- [其他待筛选候选](catalog/candidates.md)：历史线索，尚未逐项核实。

```sh
make demo          # 生成 PCM 与 WAV 到 /tmp/pcm-demo
make test          # 文档、Python、本地网络与基础 C 示例
make test-media    # 上述检查 + FFmpeg MP3/AAC/Opus 实际编解码
```

无须安装全部外部 SDK 即可查询手册。各页明确自己的依赖和验证范围，不把 mock 或语法示意标成真实集成。

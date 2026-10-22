# 技术查询手册

查询具体技术是什么、何时使用、如何使用，以及示例与常见问题。技术分类仅用于导航，不按分类创建子仓库。

[本轮确认的六部分清单](catalog/2016-scope.md)包含 31 个正式技术条目及暂缓决定。原扫描汇总中的“32”是计数错误，未因此增加未经确认的技术。历史工程只用于提取技术名，示例不引用旧代码。

| 分类 | 技术条目 |
| --- | --- |
| 音频处理 | [PCM](topics/audio/pcm.md)、[WAV](topics/audio/wav.md)、[ALSA](topics/audio/alsa.md)、[tinyalsa](topics/audio/tinyalsa.md)、[重采样 / SpeexDSP](topics/audio/resampling.md)、[Opus](topics/audio/opus.md)、[MP3 / libmad](topics/audio/mp3-libmad.md)、[AAC / ADTS / FAAD2](topics/audio/aac-adts-faad.md)、[ALSA Mixer](topics/audio/alsa-mixer.md) |
| 语音技术与 SDK | [VAD](topics/speech/vad.md)、[关键词唤醒](topics/speech/wake-word.md)、[Voice 前处理](topics/speech/voice-preprocessing.md)、[云知声 ASR](topics/speech/unisound-asr.md)、[百度 ASR](topics/speech/baidu-asr.md)、[百度 TTS](topics/speech/baidu-tts.md) |
| 网络与数据处理 | [TCP 分包](topics/network/tcp-framing.md)、[HTTP](topics/network/http.md)、[libcurl](topics/network/libcurl.md)、[TLS / OpenSSL](topics/network/tls-openssl.md)、[JSON / cJSON](topics/network/json-cjson.md)、[Base64](topics/network/base64.md)、[HMAC-SHA256](topics/network/hmac-sha256.md) |
| 物联网通信 | [MQTT](topics/iot/mqtt.md)、[Paho C](topics/iot/paho-c.md)、[Modbus](topics/iot/modbus.md)、[BACnet](topics/iot/bacnet.md) |
| 具体编程机制 | [pthread](topics/programming/pthread.md)、[信号量](topics/programming/semaphore.md)、[C 调用 Python](topics/programming/embed-python.md)、[C 可变参数](topics/programming/varargs.md)、[Selenium](topics/programming/selenium.md) |
| 其他已建条目 | [FIDL](topics/ipc/fidl.md)（区分 Fuchsia 与 Franca） |

## 使用与维护

- [示例和验证范围](examples/README.md)：查看已运行、需开发库/设备和接口契约的区别。
- [条目模板](topics/TEMPLATE.md)、[维护约定](CONTRIBUTING.md)。
- [代码来源与复用判断](sources.md)：哪些复用 summary_components，哪些重新实现。
- [其他待筛选候选](catalog/candidates.md)：历史线索，尚未逐项核实。

```sh
make demo          # 生成 PCM 与 WAV 到 /tmp/pcm-demo
make test          # 文档、Python、本地网络与基础 C 示例
make test-media    # 上述检查 + FFmpeg MP3/AAC/Opus 实际编解码
```

无须安装全部外部 SDK 即可查询手册。各页明确自己的依赖和验证范围，不把 mock 或语法示意标成真实集成。

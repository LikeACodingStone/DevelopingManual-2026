# 2016 技术提取：确认范围与完成入口

按确认的六部分组织；历史工程仅用于确定技术清单，不作为示例代码或引用来源。所有页面遵循六节模板，验证范围以各页和 examples/README.md 为准。

## 一、音频处理

- [PCM（扩充已有页）](../topics/audio/pcm.md)
- [WAV / RIFF](../topics/audio/wav.md)
- [ALSA PCM API](../topics/audio/alsa.md)
- [tinyalsa](../topics/audio/tinyalsa.md)
- [音频重采样 / SpeexDSP](../topics/audio/resampling.md)
- [Opus](../topics/audio/opus.md)
- [MP3 / libmad](../topics/audio/mp3-libmad.md)
- [AAC / ADTS / FAAD2](../topics/audio/aac-adts-faad.md)
- [ALSA Mixer](../topics/audio/alsa-mixer.md)

## 二、语音技术与 SDK

- [VAD：语音活动检测](../topics/speech/vad.md)
- [关键词唤醒 / Wake Word](../topics/speech/wake-word.md)
- [Voice 音频前处理 SDK](../topics/speech/voice-preprocessing.md)
- [云知声 ASR SDK](../topics/speech/unisound-asr.md)
- [百度语音识别 HTTP 接入](../topics/speech/baidu-asr.md)
- [百度 TTS HTTP 接入](../topics/speech/baidu-tts.md)

## 三、网络与数据处理

- [TCP Socket 与应用层分包](../topics/network/tcp-framing.md)
- [HTTP 请求与响应处理](../topics/network/http.md)
- [libcurl](../topics/network/libcurl.md)
- [TLS / OpenSSL 客户端](../topics/network/tls-openssl.md)
- [JSON / cJSON](../topics/network/json-cjson.md)
- [Base64](../topics/network/base64.md)
- [HMAC-SHA256](../topics/network/hmac-sha256.md)

## 四、物联网通信

- [MQTT](../topics/iot/mqtt.md)
- [Eclipse Paho MQTT C](../topics/iot/paho-c.md)
- [Modbus / libmodbus](../topics/iot/modbus.md)
- [BACnet](../topics/iot/bacnet.md)

## 五、具体编程机制

- [pthread 线程与互斥锁](../topics/programming/pthread.md)
- [POSIX 信号量](../topics/programming/semaphore.md)
- [C 调用 Python](../topics/programming/embed-python.md)
- [C 可变参数](../topics/programming/varargs.md)
- [Selenium WebDriver](../topics/programming/selenium.md)

## 六、暂缓独立成篇

| 内容 | 处理方式 | 恢复条件 |
| --- | --- | --- |
| Mosquitto | 作为 MQTT 的外部 Broker/工具参考 | 需要独立查询部署、持久化或权限配置时 |
| GPIO、mmap 与寄存器访问 | 暂缓，不提供旧 R16 代码 | 确定目标板卡与安全的硬件接口后 |
| WS2812 | 暂缓，不复用软件空循环时序 | 确认硬件驱动方案并实测后 |
| 音频混音 | 暂缓，不复制按字节混音实验 | 有正确的样本级实现与限幅验证后 |
| 进程监控与自动拉起 | 暂缓 | 选定可靠的监管机制后 |
| MD5 | 不作为新认证方案；历史兼容需求再写 | 有明确兼容协议要求后 |
| 自有日志、命令路由、自定义音频包 | 通用知识并入可变参数、JSON 和 TCP 条目 | 存在真正可复用的独立协议/组件后 |
| SDK 内部依赖、构建产物、日志和重复工程 | 不自动提取 | 有独立查询价值和实际使用依据后 |

本轮共 31 个正式条目（含 PCM），保留已有 FIDL 页面。暂缓项按确认建议保留决定，不生成无依据的代码。

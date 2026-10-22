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
| native/core_thread_example.c + threads.c | 复用互斥计数器、新并发驱动 | `make test` 自动编译运行 |
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

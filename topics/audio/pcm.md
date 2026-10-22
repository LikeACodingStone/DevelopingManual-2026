# PCM：脉冲编码调制

- 别名：Pulse Code Modulation
- 标签：音频、采样、数据格式
- 本页示例：16 kHz、单声道、有符号 16 位小端线性 PCM（s16le）
- 示例状态：提供可运行示例及往返读取、样本和帧长验证

## 是什么

PCM 用离散数字表示采样后的信号。常见线性 PCM 的数值直接表示各采样时刻的幅度。理解数据需要知道采样率、声道数、位深，以及整数/浮点、符号和字节序。

| 参数 | 含义 | 示例 |
| --- | --- | --- |
| 采样率 | 每个声道每秒的样本数 | 16000 Hz |
| 位深 | 每个声道每个样本占用位数 | 16 bit，2 字节 |
| 声道数 | 每个采样时刻的通道数量 | 单声道 1 |
| 样本帧 | 同一时刻所有声道的样本 | 双声道 16 bit 为 4 字节 |

裸 `.pcm` 文件通常没有头部，无法仅凭扩展名推断参数。WAV 是容器，可以携带格式信息；PCM 是它能存放的一种音频编码。PCM 也不等于 MP3、Opus 等压缩编码。

## 何时使用

音频采集、播放、信号处理和语音识别输入。优点是处理直接；缺点是未压缩数据量大。

对于字节对齐的线性 PCM：

```text
每秒字节数 = 采样率 × 声道数 × (位深 / 8)
数据字节数 = 样本帧数 × 声道数 × (位深 / 8)
```

本例每秒 32000 字节。20 ms 对应 320 个样本帧，即 640 字节。640 字节不是 PCM 标准要求；换成 48 kHz 双声道 16 位，20 ms 就是 3840 字节。

## 如何使用

1. 与数据提供方确认所有格式参数，包括交错/平面布局。
2. 以匹配的类型、符号和字节序读取样本；本例使用 `<h`。
3. 按接口要求分块；网络读取边界不等于音频帧边界，需要保留不足一块的尾部。
4. 写入 WAV 时填写与实际数据一致的参数；修改头部参数不会自动重采样。

## 最小示例

[代码](../../examples/pcm-read-write/pcm_demo.py)仅使用 Python 3 标准库，生成一秒 440 Hz 正弦波，将同一份 PCM 写成裸文件和 WAV，再读取 WAV 校验。

```sh
python3 examples/pcm-read-write/pcm_demo.py --output /tmp/pcm-demo
```

预期输出：

```text
sample_frames=16000 pcm_bytes=32000 chunks_20ms=50
WAV round-trip OK
```

输出 `tone.pcm` 与 `tone.wav`。WAV 可用支持该格式的播放器打开。安装 FFmpeg 后可选播放裸数据：

```sh
ffplay -f s16le -ar 16000 -ch_layout mono /tmp/pcm-demo/tone.pcm
```

播放命令需要本机 FFmpeg 和音频设备，不属于自动验证。

### 交错多声道数据

双声道交错样本通常是 `L0,R0,L1,R1,...`，而平面布局是各声道分别存储。本手册新增[声道提取示例](../../examples/pcm-read-write/channels.py)，明确接受 s16le 交错输入，以声道数量和索引选择输出，不使用旧工程中硬编码的麦克风编号。

```sh
python3 examples/pcm-read-write/channels.py
```

预期 `(-100, -200)`。声道索引从 0 开始，尾部不足一个完整样本帧会报错。转换为浮点时常用 `sample / 32768.0`，应明确负满幅与正满幅的不对称范围。

## 常见问题

- 速度或音调错误：核对采样率。
- 噪声：核对位深、字节序、符号和声道布局。
- 时长错误：区分单声道样本与包含所有声道的样本帧。
- 流结束不足一块：根据下游协议选择保留、丢弃或补零，不要默认补零。

## 参考资料

- [Python wave 文档](https://docs.python.org/3/library/wave.html)
- [FFmpeg 音频格式](https://ffmpeg.org/ffmpeg-formats.html)
- [Microsoft WAVEFORMATEX](https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex)

代码来源：本页两个示例均为新写，不引用历史工程代码；未复用有尾部缓存和通道边界问题的旧组件。

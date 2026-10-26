# Opus

- 别名与生态：Opus
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：audio
- 示例状态：libopus C 示例未编译；FFmpeg 编解码/容器示例已运行验证
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

Opus 是面向交互语音和音频的有损编码。libopus 处理单个压缩包；Ogg Opus 是承载这些包的容器，裸包、Ogg 文件和 RTP 传输不是同一层。

## 何时使用

低延迟语音通信、网络音频。编码 API 支持特定输入采样率，帧长取决于所选模式；常规语音常用 20 ms。

## 如何使用

1. 创建指定采样率、声道和应用模式的 encoder/decoder。
2. 计算每声道 frame_size；16 kHz 的 20 ms 为 320。
3. opus_encode 返回有效包字节数，按包保存边界。
4. opus_decode 返回每声道样本帧数，负值为错误。
5. 复用状态并最终销毁；丢包恢复须按协议单独设计。

## 最小示例

以下命令均从仓库根目录运行。

[新 libopus 示例](../../examples/native/opus.c)真实调用编解码，不使用模拟 PCM。

```sh
cc -std=c11 examples/native/opus.c -lopus -o /tmp/opus-demo
/tmp/opus-demo
```

预期 `decoded_frames=320`。另有[已验证的 FFmpeg 容器示例](../../examples/media/codec_demo.py)：

```sh
python3 examples/media/codec_demo.py opus --output /tmp/opus-media
```

## 常见问题

frame_size 按每声道计数，不是字节或所有声道样本总数。有损编解码不能做 PCM 逐字节一致性断言。不要用 Ogg 文件头直接调用 opus_decode。


## 参考资料

- [官方资料或明确标注的技术参考](https://opus-codec.org/docs/)
- [代码来源与验证范围](../../sources.md)

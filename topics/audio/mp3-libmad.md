# MP3 / libmad

- 别名与生态：MP3 / libmad
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：audio
- 示例状态：libmad C 示例未编译；FFmpeg MP3 示例已运行验证
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

MP3 是压缩音频格式；libmad 是使用定点运算的 MPEG 音频解码库。高层接口通过 input、output、error 回调驱动，输出的定点样本并非可直接播放的 s16le 字节。

## 何时使用

需要在 C 中解码 MP3 时使用。教学例演示解码回调及有效输出统计，完整播放还需样本格式转换与音频设备接口。

## 如何使用

1. 提供包含末尾 guard 字节的输入。
2. 初始化解码器和回调。
3. 输入回调提交数据，输出回调处理声道、采样率和定点样本。
4. 区分可恢复错误与终止错误。
5. finish 并释放输入；流式实现须保留未消费数据。

## 最小示例

以下命令均从仓库根目录运行。

[新 libmad 示例](../../examples/native/mad.c)限制输入大小，解码后统计帧数。

```sh
python3 examples/media/codec_demo.py mp3 --output /tmp/mp3-media
cc -std=c11 examples/native/mad.c -lmad -o /tmp/mad-demo
/tmp/mad-demo /tmp/mp3-media/tone.mp3
```

计数必须大于零。FFmpeg 路径验证实际 MP3 读写，但不代替 libmad 集成验证。

## 常见问题

定点转 16 位需要缩放、限幅并考虑舍入。MP3 解码可有起始延迟和填充。例子是有限文件演示，不是无界网络流播放器。

## 参考资料

- [官方资料或明确标注的技术参考](https://www.underbit.com/products/mad/)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)

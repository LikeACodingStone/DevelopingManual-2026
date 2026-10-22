# AAC / ADTS / FAAD2

- 别名与生态：AAC / ADTS / FAAD2
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：audio
- 示例状态：FAAD2 C 示例未编译；FFmpeg ADTS AAC 示例已运行验证
- 代码来源：为本手册新写；不引用 2016Codes 代码

## 是什么

AAC 是有损音频编码，ADTS 是携带帧同步与部分配置的传输格式。AAC 也可存在 MP4 容器或无 ADTS 的访问单元中；FAAD2 是解码库。

## 何时使用

读取 ADTS AAC 文件或已有 AAC 编码数据时使用。先确认封装，MP4 不应按 ADTS 扫描。

## 如何使用

1. NeAACDecOpen 创建解码器，设置输出格式。
2. NeAACDecInit 从 ADTS 初始化采样率和声道。
3. 逐次 Decode，按 bytesconsumed 移动输入位置。
4. 检查 error、samples、channels；及时消费返回 PCM。
5. 关闭解码器并释放文件缓存。

## 最小示例

以下命令均从仓库根目录运行。

[新 FAAD2 示例](../../examples/native/faad.c)读取有限 ADTS 文件，统计输出样本。

```sh
python3 examples/media/codec_demo.py aac --output /tmp/aac-media
cc -std=c11 examples/native/faad.c -lfaad -o /tmp/faad-demo
/tmp/faad-demo /tmp/aac-media/tone.aac
```

成功时样本总数大于零。

## 常见问题

samples 包含所有声道的样本总数，不能直接当作每声道帧数。返回 PCM 的生命周期由解码器管理，不能在下一次调用后仍假定有效。处理零消费以避免死循环。

## 参考资料

- [官方资料或明确标注的技术参考](https://github.com/knik0/faad2)
- [代码来源与验证范围](../../sources.md)

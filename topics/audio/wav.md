# WAV / RIFF

- 别名与生态：WAV / RIFF
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：audio
- 示例状态：已运行验证：Python 3.12，无第三方依赖
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

WAV 是通常以 RIFF chunk 组织音频的容器，PCM 是其中一种编码。常见文件有 RIFF/WAVE 标识、fmt 与 data chunk；不能假定所有 WAV 都只有固定 44 字节头部。chunk 长度不含自身头部，奇数字节块还可能包含对齐填充。

## 何时使用

需要在文件中携带采样率、声道、位深等元数据时使用。Python wave 支持的范围有限，压缩 WAV 或特殊扩展应使用支持该编码的库。

## 如何使用

1. 用 wave.open 以二进制模式创建容器。
2. 设置声道、样本宽度（字节）和采样率。
3. 写入与参数一致的 PCM，关闭时完成头部更新。
4. 读取时先检查元数据，再按样本帧读取数据。

## 最小示例

以下命令均从仓库根目录运行。

[PCM/WAV 示例](../../examples/pcm-read-write/pcm_demo.py)同时生成裸 PCM 与 WAV，并验证读回数据。

```sh
python3 examples/pcm-read-write/pcm_demo.py --output /tmp/pcm-demo
```

预期输出 `WAV round-trip OK`。

## 常见问题

不能把整个 WAV 文件当作裸 PCM 送进识别器；文件扩展名不保证编码。修改采样率字段不会重采样。不要把 C 结构体内存直接当作可移植 WAV 文件头，须处理字节序、填充和额外 chunk。

## 参考资料

- [官方资料或明确标注的技术参考](https://docs.python.org/3/library/wave.html)
- [代码来源与验证范围](../../sources.md)

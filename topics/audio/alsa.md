# ALSA PCM API

- 别名与生态：ALSA PCM API
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：audio
- 示例状态：新示例；需要外部开发库/环境，未编译或联调
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

ALSA 的 PCM 接口负责与音频设备交互。应用配置访问模式、样本格式、声道、采样率及缓冲参数，通过 snd_pcm_readi/writei 交换交错样本帧。ALSA PCM 接口与 PCM 数据格式是不同概念。

## 何时使用

Linux 应用采集或播放音频。buffer 是设备环形缓冲，period 是其中的处理单位；更小延迟通常意味着更高调度压力。

## 如何使用

1. snd_pcm_open 打开明确的 capture/playback 设备。
2. 配置硬件/软件参数，或用 snd_pcm_set_params 简化配置。
3. 检查实际协商的采样率和格式。
4. 循环读写，返回值是样本帧数，处理短写和可恢复错误。
5. 选择 drain（等待播放完）或 drop（丢弃），最后 close。

## 最小示例

以下命令均从仓库根目录运行。

[新 ALSA 示例](../../examples/native/alsa.c)写 320 个静音帧，可先使用 null 插件，无需实际发声。

```sh
cc -std=c11 -Wall -Wextra examples/native/alsa.c -lasound -o /tmp/alsa-demo
/tmp/alsa-demo null
```

需要 ALSA 开发包。成功输出 `written_frames=320`。

## 常见问题

EPIPE 常表示欠载/溢出，可用 snd_pcm_recover；重复失败应退出，不能无限重试。writei 长度单位是帧而不是字节；录音和播放方向不能混用。

## 参考资料

- [官方资料或明确标注的技术参考](https://www.alsa-project.org/alsa-doc/alsa-lib/pcm.html)
- [代码来源与验证范围](../../sources.md)

# ALSA Mixer

- 别名与生态：ALSA Mixer
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：audio
- 示例状态：新示例；需要外部开发库/环境，未编译或联调
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

ALSA Mixer 操作声卡控件，例如播放音量和静音开关。它不负责 PCM 样本读写，也不保证每张声卡都有名为 Master 的元素。

## 何时使用

需要查询或调整硬件音量时使用。原始整数音量范围与 dB 范围不同，原始值线性变化不代表听感线性。

## 如何使用

1. open、attach、register、load 建立 mixer。
2. 按名称和索引寻找 simple element。
3. 检查元素是否支持播放音量以及可用声道。
4. 读取范围和当前值；设置前将值限制在有效范围。
5. 关闭 mixer。

## 最小示例

以下命令均从仓库根目录运行。

[新只读 Mixer 示例](../../examples/native/mixer.c)不修改音量。

```sh
cc -std=c11 examples/native/mixer.c -lasound -o /tmp/mixer-demo
/tmp/mixer-demo default Master
```

根据目标设备替换控件名称；预期输出 min/max/current。

## 常见问题

控件不存在并不一定是 API 错误。静音开关与音量可能独立。需要设置时可用 snd_mixer_selem_set_playback_volume_all，先检查范围和用户意图。

## 参考资料

- [官方资料或明确标注的技术参考](https://www.alsa-project.org/alsa-doc/alsa-lib/group___simple_mixer.html)
- [代码来源与验证范围](../../sources.md)

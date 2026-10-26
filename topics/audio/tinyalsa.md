# tinyalsa

- 别名与生态：tinyalsa
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：audio
- 示例状态：新示例；需要外部开发库/环境，未编译或联调
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

tinyalsa 是较小的 ALSA 用户空间封装，常见于 Android/嵌入式环境。它也操作 PCM 设备，但接口、插件能力和配置方式不同于完整 alsa-lib。

## 何时使用

目标系统已提供 tinyalsa、需要按声卡号和设备号操作音频节点的场景。它不会自动提供桌面音频服务器的路由和混音能力。

## 如何使用

1. 准备目标版本 tinyalsa 的头文件和运行库。
2. 配置 pcm_config，并选择 PCM_IN 或 PCM_OUT。
3. pcm_open 后检查 pcm_is_ready。
4. 按所用 API 的长度单位读写；最后 pcm_close。

## 最小示例

以下命令均从仓库根目录运行。

[新 tinyalsa 示例](../../examples/native/tinyalsa.c)向指定设备写静音。

```sh
cc -std=c11 examples/native/tinyalsa.c -ltinyalsa -o /tmp/tinyalsa-demo
/tmp/tinyalsa-demo 0 0
```

必须确认目标设备支持单声道 16 kHz s16le。成功退出码为 0。

## 常见问题

pcm_write 的长度是字节；新版帧接口 pcm_writei 使用帧。不要把 alsa-lib 的 snd_pcm_* 句柄或错误处理直接套用。设备权限和系统音频服务可能影响访问。

## 参考资料

- [官方资料或明确标注的技术参考](https://github.com/tinyalsa/tinyalsa)
- [代码来源与验证范围](../../sources.md)

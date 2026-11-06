# 百度语音识别 HTTP 接入

- 别名与生态：百度语音识别 HTTP 接入
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：speech
- 示例状态：请求构造离线测试通过；真实云服务未调用
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

通过 HTTPS 将音频提交到百度 ASR 服务，读取 JSON 识别结果。REST 示例与厂商本地 SDK 不同；鉴权 token、产品标识和输入限制受当前服务约束。

## 何时使用

允许联网、已开通对应识别服务的短音频识别。长音频、流式接口和离线识别需要不同接入流程。

## 如何使用

1. 从官方鉴权流程取得有效 access token，放入环境变量。
2. 准备实际为 16 kHz 单声道 s16le 的裸 PCM。
3. 构造 JSON：format/rate/channel/cuid/token/dev_pid/speech/len。
4. Base64 只用于传输，len 为原始字节数。
5. 通过 HTTPS 发送并检查 err_no，再消费 result。

## 最小示例

以下命令均从仓库根目录运行。

[新 REST 示例](../../examples/integrations/baidu_speech.py)使用 Python 标准库，ASR 产品参数需按账号支持范围确认。

```sh
python3 examples/integrations/baidu_speech.py asr /tmp/pcm-demo/tone.pcm
```

先设置 BAIDU_ACCESS_TOKEN。正弦波只适合格式测试，真实识别验证必须使用语音录音。

## 常见问题

WAV 文件头不能作为裸 PCM 输入。示例只检查长度和对齐，不能凭字节流推断真实采样率。token 失效、权限不足和音频无语音需分别处理。

## 参考资料

- [官方资料或明确标注的技术参考](https://ai.baidu.com/ai-doc/SPEECH)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)

# 百度 TTS HTTP 接入

- 别名与生态：百度 TTS HTTP 接入
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：speech
- 示例状态：代码和表单构造已离线检查；真实云服务未联调
- 代码来源：为本手册新写；不引用 2016Codes 代码

## 是什么

TTS 把文本转换成语音音频。服务可能返回音频，也可能返回 JSON 错误，不能无条件把响应写成 MP3。

## 何时使用

在线播报、语音反馈。语音角色、编码、文本长度和调用配额以当前产品文档为准。

## 如何使用

1. 准备有效 token 与客户端标识。
2. 按表单规则编码文本与参数，确认服务要求的文本编码层数。
3. 请求指定输出编码；示例 aue=3 请求 MP3。
4. 检查 Content-Type，拒绝把 JSON 错误写成音频。
5. 将音频交给匹配的解码器或播放器。

## 最小示例

以下命令均从仓库根目录运行。

[新 REST 示例](../../examples/integrations/baidu_speech.py)：

```sh
python3 examples/integrations/baidu_speech.py tts "你好" /tmp/hello.mp3
```

先设置 BAIDU_ACCESS_TOKEN。成功输出音频字节数；不自动播放或写入任何设备。

## 常见问题

URL 编码不是 Base64；避免业务层和 HTTP 层重复编码。服务端错误有时使用成功 HTTP 状态，仍须检查响应类型和业务码。不要在日志中输出 token。

## 参考资料

- [官方资料或明确标注的技术参考](https://ai.baidu.com/ai-doc/SPEECH)
- [代码来源与验证范围](../../sources.md)

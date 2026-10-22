# 外部语音服务和专有 SDK

`baidu_speech.py` 是新写的 REST 接入代码；需要当前服务权限及有效 token。本机只验证请求构造，不调用云服务，不宣称接口已联调。请求参数和接口配额以服务当前官方文档为准。

```sh
# 在环境中设置 BAIDU_ACCESS_TOKEN，不把 token 写进代码或提交到仓库
python3 examples/integrations/baidu_speech.py asr /tmp/pcm-demo/tone.pcm
python3 examples/integrations/baidu_speech.py tts '你好' /tmp/hello.mp3
```

`sdk_session.py` 只定义自有接入契约。云知声、Voice、关键词唤醒三个条目可以参考其资源生命周期；它不包含厂商函数，不实现语音识别、波束形成或唤醒，也不能用其离线测试代替 SDK 集成测试。取得确切版本的开发包后，在独立 adapter 中实现并验证格式、线程与回调约束。

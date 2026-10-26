# SkEgn 语音 SDK 接入契约

- 别名与生态：SkEgn；专有语音评测/识别 SDK
- 适用版本与平台：准确版本、平台 ABI 与当前接口需以取得的厂商开发包为准
- 标签：speech, sdk
- 示例状态：自有接入契约；无厂商 adapter，未联调
- 代码来源：本手册独立编写的 examples/integrations/sdk_session.py；不引用历史 SDK 代码

## 是什么

SkEgn 属于专有语音 SDK。这里说明应用如何管理一次语音会话；本页不将历史头文件作为当前 API 参考，也不提供未经厂商文档核实的函数签名。

## 何时使用

已取得对应开发包、授权与音频格式说明后，给 SDK 接入建立可测试的资源生命周期。语音评测、识别和本地核心的可用性须按授权确认。

## 如何使用

1. 获取与目标平台匹配的厂商资料，确认音频格式、回调线程和所有权。
2. 实现本手册 Adapter 契约：open、start、feed、finish、close。这些名称是教学接口，不是厂商 API。
3. 将 SDK 初始化和会话创建映射到 open/start，按字节块送入音频。
4. finish 内处理输入结束、最终回调和有界等待；异常必须向上返回。
5. close 应允许部分初始化失败，并释放已经取得的资源；run_session 的 finally 总会调用它。

## 最小示例

[独立会话契约](../../examples/integrations/sdk_session.py)不生成模拟识别结果。没有真实 adapter 时不能执行语音任务。

从手册根目录检查 Python 语法：

```sh
python3 -m py_compile examples/integrations/sdk_session.py
```

预期正常退出且无输出；这只验证语法。`make test` 的故障注入检查只验证契约释放路径，不证明 SDK 可用。直接运行此定义文件不会完成集成测试。

## 常见问题

stop/input-end 类事件不一定意味着最终结果就绪。不要把凭证、模型、授权文件或私有服务地址放入示例。Qt、JNI 或其他绑定必须遵循厂商的线程、缓冲和回调生命周期规则。

## 参考资料

- [本地 SDK 会话契约](../../examples/integrations/sdk_session.py)
- [接入说明](../../examples/integrations/README.md)
- 厂商官方参考：当前尚未取得与目标版本匹配的可核验 API 文档；取得前保持契约状态，不猜测接口。

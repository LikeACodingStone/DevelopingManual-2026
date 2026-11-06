# Eclipse Paho MQTT C

- 别名与生态：Eclipse Paho MQTT C
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：iot
- 示例状态：新示例；需要外部开发库/环境，未编译或联调
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

Paho MQTT C 提供同步 MQTTClient 和异步 MQTTAsync 接口。它是 MQTT 客户端实现，不是 Broker。示例采用同步 MQTTClient。

## 何时使用

C/C++ 应用连接 MQTT Broker。同步接口便于演示；复杂并发应用需要理解阻塞调用、回调线程和消息所有权。

## 如何使用

1. create 指定地址、唯一 ID 与持久化选项。
2. connect 配置 keepalive、会话和超时。
3. 如需接收，连接前设置回调并订阅；回调按 API 约定释放消息与主题。
4. publish 后按需要等待 QoS 交付完成。
5. disconnect、destroy。

## 最小示例

以下命令均从仓库根目录运行。

[新 Paho 发布示例](../../examples/native/paho.c)：

```sh
cc -std=c11 examples/native/paho.c -lpaho-mqtt3c -o /tmp/paho-demo
/tmp/paho-demo tcp://127.0.0.1:1883
```

成功退出码为 0；配合订阅者验证消息，见 [MQTT](mqtt.md)。

## 常见问题

不要把 publish 返回成功当作业务消费成功。示例使用固定教学 client ID，多个实例应改成唯一值。TLS 版本库通常为 paho-mqtt3cs，不能仅改 URL 就假定已正确配置验证。

## 参考资料

- [官方资料或明确标注的技术参考](https://eclipse-paho.github.io/paho.mqtt.c/MQTTClient/html/)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)

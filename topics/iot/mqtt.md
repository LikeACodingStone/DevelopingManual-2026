# MQTT

- 别名与生态：MQTT
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：iot
- 示例状态：需要本地 Broker/Paho，未联调
- 代码来源：为本手册新写；不引用 2016Codes 代码

## 是什么

MQTT 是通过 Broker 进行发布/订阅的消息协议。客户端向主题发布消息，订阅者按过滤器接收。QoS 描述协议交付语义，不保证业务处理恰好执行一次。

## 何时使用

设备遥测、状态同步和指令下发。需要理解 retain、遗嘱、会话以及重连后的订阅恢复。

## 如何使用

1. 启动本地 Broker，明确协议版本。
2. 使用唯一 client ID 连接。
3. 订阅具体过滤器，再发布消息。
4. 根据需求选择 QoS、retain 和会话策略。
5. 处理连接丢失、重连及业务去重。

## 最小示例

以下命令均从仓库根目录运行。

使用[新 Paho 示例](../../examples/native/paho.c)发布 QoS 1 消息。先在另一终端启动本地 Broker 和订阅者：

```sh
mosquitto -p 1883
# 另一终端
mosquitto_sub -h 127.0.0.1 -t handbook/demo -q 1
```

再按 [Paho 条目](paho-c.md)构建发布者，订阅端应收到 `PCM`。Broker 和订阅工具为外部依赖，不随仓库附带。

## 常见问题

QoS 1 可能重复交付；retained message 是每主题保留的最新值，不是历史队列。通配符用于订阅，不用于普通发布主题。公网应配置身份认证与 TLS。

## 参考资料

- [官方资料或明确标注的技术参考](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)
- [代码来源与验证范围](../../sources.md)

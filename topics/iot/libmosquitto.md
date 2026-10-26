# libmosquitto MQTT 客户端

- 别名与生态：libmosquitto C；区别于 Mosquitto Broker
- 适用版本与平台：libmosquitto 2.x API；本地 MQTT 3.1.1 Broker
- 标签：iot
- 示例状态：未编译、未联调：缺开发库和 Broker
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

libmosquitto 是 MQTT 客户端库，提供连接、发布订阅、回调与网络循环。Broker 是消息路由服务，两者不是同一个角色。

## 何时使用

C/C++ 程序需要 MQTT 消息通道和明确的回调生命周期。协议语义见 [MQTT](mqtt.md)。

## 如何使用

1. 初始化库并创建客户端。
2. 设置回调，连接 Broker。
3. 持续运行网络循环，处理连接状态和确认。
4. 发布消息并检查返回码；QoS 1 等待 PUBACK。
5. 断开、销毁客户端、清理库。

## 最小示例

以下命令从手册根目录执行。

[新 C 客户端](../../examples/native/mosquitto_demo.c)只支持回环地址，默认不连接。

```sh
cc -std=c11 -Wall -Wextra examples/native/mosquitto_demo.c -lmosquitto -o /tmp/handbook-mosquitto
/tmp/handbook-mosquitto
# 已自行启动本地 Broker 后，显式连接：
/tmp/handbook-mosquitto --local-broker
```

默认输出使用说明；显式连接成功预期 `MQTT PUBACK received`。示例在有限次循环后失败退出，没有自动重连；本轮未连接 Broker。

## 常见问题

publish 返回成功不等于订阅方完成业务处理。回调中避免阻塞网络循环。长期客户端应在 CONNACK 成功后启动业务，处理重连、重复消息、订阅恢复与停止流程。

## 参考资料

- [libmosquitto 官方 API](https://mosquitto.org/api/files/mosquitto-h.html)
- [示例验证范围](../../examples/README.md)

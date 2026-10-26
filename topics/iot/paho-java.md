# Paho Java 与 Android 接入

- 别名与生态：Eclipse Paho MQTT Java / Android Service；区别于 Paho C
- 适用版本与平台：Java MQTT v3 客户端 1.2.x；Android Service 兼容性需另查
- 标签：iot
- 示例状态：Java 示例未编译；Android 仅接入说明，未设备联调
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

Paho Java 提供 JVM MQTT 客户端；Android Service 适配 Android 生命周期和服务机制。Android 包与 Java SE 客户端不能作为完全相同的运行环境。

## 何时使用

Java 应用或 Android 应用通过 MQTT 交换状态和命令。Android 后台执行限制、网络权限和重连行为必须单独设计。

## 如何使用

1. 选择 MQTT 协议、客户端版本与平台。
2. 配置唯一 client ID、持久化、连接超时和会话策略。
3. 在后台工作上下文执行网络操作，避免阻塞 Android UI。
4. 用回调或 token 判断完成；退出时断开和关闭资源。
5. Android 另行核对 Manifest 权限、服务声明、后台限制和生命周期，不直接套用 Java main。

## 最小示例

以下命令从手册根目录执行。

[独立 Java SE 客户端](../../examples/java/PahoLocal.java)用内存持久化发布一条 QoS 1 消息，不是 Android APK。

```sh
# PAHO_JAR 指向已安装的 org.eclipse.paho.client.mqttv3 JAR
mkdir -p /tmp/handbook-java
javac -cp "$PAHO_JAR" -d /tmp/handbook-java examples/java/PahoLocal.java
java -cp "/tmp/handbook-java:$PAHO_JAR" PahoLocal
# 本地 Broker 已启动时，才显式连接：
java -cp "/tmp/handbook-java:$PAHO_JAR" PahoLocal --local-broker
```

上述 classpath 为 Unix 形式；Windows 分隔符使用分号。默认只打印说明；显式发布成功预期 `MQTT publish completed`。当前缺 JDK/JAR，未执行。

## 常见问题

Android 的客户端释放与宿主生命周期必须匹配。旧 Android Service 版本不能默认兼容当前 target SDK；离线 JVM 编译也不能证明 Android 服务兼容性。clean session 和内存持久化不适合所有断线恢复需求。

## 参考资料

- [Paho Java 官方项目](https://github.com/eclipse-paho/paho.mqtt.java)
- [Paho Android Service](https://github.com/eclipse-paho/paho.mqtt.android)
- [示例验证范围](../../examples/README.md)

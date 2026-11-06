# TLS / OpenSSL 客户端

- 别名与生态：TLS / OpenSSL 客户端
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：network
- 示例状态：已在本机编译；未进行外部 TLS 连接
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

TLS 在传输中提供机密性、完整性和身份验证。成功握手不等于成功验证服务端身份；证书链与预期主机名都要校验。

## 何时使用

理解或实现直接 TLS 客户端。HTTP 业务通常更适合用 libcurl 等高层库，减少自己处理连接、超时和报文边界。

## 如何使用

1. TLS_client_method 创建上下文，设定最低 TLS 版本。
2. 设置验证对端并加载受信 CA。
3. 设置 SNI 与预期 DNS 主机名。
4. 建连与握手，检查证书结果。
5. 根据真实需求进行 TLS 读写与关闭。

## 最小示例

以下命令均从仓库根目录运行。

[新 OpenSSL 示例](../../examples/native/tls.c)只执行 DNS 主机的握手和身份验证，不发送 HTTP。

```sh
cc -std=c11 examples/native/tls.c -lssl -lcrypto -o /tmp/tls-demo
timeout 15 /tmp/tls-demo example.com
```

OpenSSL >=1.1.1。编译已通过；未访问公网验证握手。

## 常见问题

示例采用阻塞 BIO，运行时使用外部 timeout 限制等待；生产代码应使用非阻塞 I/O 和连接/握手 deadline。SNI 是路由提示，不代替主机名校验。IP 地址需要不同验证配置，本例只接收 DNS 名称。

## 参考资料

- [官方资料或明确标注的技术参考](https://docs.openssl.org/3.0/man7/ossl-guide-tls-client-block/)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)

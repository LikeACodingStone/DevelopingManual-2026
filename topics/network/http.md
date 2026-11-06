# HTTP 请求与响应处理

- 别名与生态：HTTP 请求与响应处理
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：network
- 示例状态：已运行验证：本地请求与响应
- 代码来源：为本手册独立新写；教学源码见本仓库 examples/

## 是什么

HTTP 描述请求方法、目标、状态码、头部和消息体。HTTP/1.1 消息体边界取决于长度或分块等规则；一个 recv 不能代表一份完整响应。

## 何时使用

调用 Web API、提交 JSON 或下载音频。通常使用成熟 HTTP 库，避免自己编写不完整的报文解析器。

## 如何使用

1. 选择方法和路径，构造请求头。
2. 将正文先编码成字节，Content-Length 按字节计数。
3. 设置超时，检查 HTTP 和业务层状态。
4. 根据 Content-Type 解码正文。
5. 使用上下文管理器释放响应和连接。

## 最小示例

以下命令均从仓库根目录运行。

[新本地 HTTP 示例](../../examples/python/http_local.py)发送中文 JSON 并验证回显。

```sh
python3 examples/python/http_local.py
```

预期 `HTTP JSON echo OK`，不调用外部服务。

## 常见问题

字符串长度与 UTF-8 字节长度不同。示例服务端只用于本地教学，不实现通用 HTTP 服务的鉴权、并发或完整分块接收。公网请求优先 HTTPS。


## 参考资料

- [官方资料或明确标注的技术参考](https://www.rfc-editor.org/rfc/rfc9110.html)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)

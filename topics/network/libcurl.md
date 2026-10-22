# libcurl

- 别名与生态：libcurl
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：network
- 示例状态：新示例；需要外部开发库/环境，未编译或联调
- 代码来源：为本手册新写；不引用 2016Codes 代码

## 是什么

libcurl 是 C 语言传输库，easy 接口通过选项配置 URL、超时、回调与 TLS 等，并执行一次传输。它与 curl 命令行工具共享底层技术但调用方式不同。

## 何时使用

C/C++ 程序发送 HTTP/HTTPS 请求，避免手写协议、重定向与 TLS 处理。

## 如何使用

1. 在应用初始化阶段调用 curl_global_init。
2. 创建 easy 句柄并检查 setopt 返回值。
3. 设置 URL、超时、响应回调；保持证书与主机名验证。
4. perform 并检查 CURLcode 和所需 HTTP 状态。
5. cleanup 句柄，最终 global_cleanup。

## 最小示例

以下命令均从仓库根目录运行。

[新 libcurl 示例](../../examples/native/curl.c)将正文写入 stdout。

```sh
cc -std=c11 examples/native/curl.c -lcurl -o /tmp/curl-demo
/tmp/curl-demo https://example.com/
```

该运行命令会访问指定 URL，未在自动检查中执行。上传二进制时应同时设置 POSTFIELDS 与 POSTFIELDSIZE。

## 常见问题

写回调返回已处理的字节数，不能把输入当作 NUL 结尾字符串。不能关闭 TLS 验证解决证书问题；应正确安装 CA 或配置受信任证书。

## 参考资料

- [官方资料或明确标注的技术参考](https://curl.se/libcurl/c/)
- [代码来源与验证范围](../../sources.md)

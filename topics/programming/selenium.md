# Selenium WebDriver

- 别名与生态：Selenium WebDriver
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：programming
- 示例状态：新示例；需要外部开发库/环境，未编译或联调
- 代码来源：为本手册新写；不引用 2016Codes 代码

## 是什么

WebDriver 通过浏览器驱动自动操作真实浏览器。Selenium 4 提供定位、交互与显式等待 API，适用于需要 JavaScript 和浏览器行为的自动化。

## 何时使用

网页交互测试和浏览器自动化。简单 HTTP 数据请求未必需要浏览器。

## 如何使用

1. 安装 Selenium 4、匹配浏览器和驱动。
2. 创建 driver，并在上下文退出时清理进程。
3. 使用稳定 ID 等定位元素。
4. 执行输入和点击，用显式等待验证可观察结果。

## 最小示例

以下命令均从仓库根目录运行。

[新 Selenium 示例](../../examples/python/selenium_demo.py)只操作内嵌本地 HTML，不登录旧网站。

```sh
python3 examples/python/selenium_demo.py
```

需要 selenium 包、Chrome 和可用驱动；成功输出 `browser interaction OK`。

## 常见问题

避免固定 sleep 依赖机器速度。隐式等待与显式等待混用可能造成难以预测的超时。Selenium Manager 可能下载驱动；要离线运行需预装匹配驱动。

## 参考资料

- [官方资料或明确标注的技术参考](https://www.selenium.dev/documentation/webdriver/)
- [代码来源与验证范围](../../sources.md)

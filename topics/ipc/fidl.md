# FIDL：先确定是哪一种接口描述语言

- 标签：接口描述、代码生成、进程通信
- 示例状态：语法示意，未安装相关 SDK，未编译

FIDL 有同名技术，不能混用编译器、生成代码或通信流程。

| 名称 | 用途 | 工具与运行环境 |
| --- | --- | --- |
| Fuchsia Interface Definition Language | 定义 Fuchsia 协议、数据类型和方法 | Fuchsia SDK / 源码构建、fidlc、对应语言绑定 |
| Franca IDL | 定义接口、类型和方法，常见于 CommonAPI 集成 | Franca 工具；CommonAPI 场景需 core 与 D-Bus / SOME/IP 等绑定生成器 |

## Fuchsia FIDL

用于定义组件之间的协议，并生成对应语言绑定。平台工具处理编码、解码与消息传输，业务代码实现协议。

语法示意：

```fidl
library handbook.echo;

closed protocol Echo {
    strict Echo(struct { value string:128; })
        -> (struct { value string:128; });
};
```

使用步骤：

1. 准备与目标平台版本匹配的 Fuchsia 开发环境。
2. 定义 `.fidl` 文件，并在构建目标中声明 FIDL 库及绑定依赖。
3. 构建生成所选语言的客户端与服务端接口。
4. 服务端实现方法，发布协议能力；客户端连接并调用。
5. 在组件清单中声明和路由能力，在目标环境验证调用。

只写 `.fidl` 文件并不能直接运行通信。实际构建、绑定 API 和组件配置须以所用 SDK 文档为准。

## Franca IDL

用于描述与实现语言分离的接口。采用 CommonAPI 时，还需选择通信绑定；IDL 自身不决定传输方式。

语法示意：

```fidl
package handbook

interface Echo {
    version { major 1 minor 0 }
    method echo {
        in { String text }
        out { String reply }
    }
}
```

使用步骤：

1. 安装兼容版本的 CommonAPI core、所选绑定的生成器和运行库。
2. 编写 `.fidl`；依绑定需要补充 `.fdepl` 部署信息。
3. 运行生成器，生成类型、客户端代理及服务端桩代码。
4. 实现服务端并注册服务，客户端创建代理后调用。
5. 配置 D-Bus 或 SOME/IP 等运行环境，验证发现和请求响应。

## 常见问题

- 先问清楚生态，再查 FIDL 用法。
- 生成器、运行库和绑定版本必须兼容。
- 接口变更需考虑双方兼容性；能重新生成代码不代表旧客户端仍兼容。
- 上述片段只展示接口形状，不是已验证的完整工程。

## 参考资料

- [Fuchsia FIDL](https://fuchsia.dev/fuchsia-src/development/languages/fidl)
- [Franca](https://github.com/franca/franca)
- [CommonAPI C++ 文档](https://covesa.github.io/capicxx-core-tools/)

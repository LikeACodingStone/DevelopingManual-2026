# Runtime

以下条目来自 SkEgn SDK；按源码调用和构建声明记录。

| classify area | name | function | code example |
| --- | --- | --- | --- |
| Language / Execution | LuaJIT | 演示程序依赖 FFI 和 bit 模块加载 SDK；运行时本体未提供。 | [main](../S004_PlatformSDK/speech/skegn_2.0.22/misc/demos/demo_for_luajit/main.lua) |
| Language / Execution | JVM | JNI 保存 JavaVM 并跨线程回调 Java；运行时由宿主提供。 | [skegn_jni](../S004_PlatformSDK/speech/skegn_2.0.22/src/sdk/skegn_jni.c) |


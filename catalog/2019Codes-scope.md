# 2019Codes 扫描记录

扫描项目：`/mnt/samsung4t/lost+found/usr/bin/github/Coding_0001_HistoryTree/2019Codes`

扫描范围：`sdk_2.0.x_8_29` 的手写头文件、C/Java/Python/C#/LuaJIT/Go 演示、构建文件和测试入口。跳过二进制、缓存、压缩包以及重复第三方源码。源项目保持只读。

## 候选汇总

| 分类 | 技术 | 证据定位 | 处理 |
| --- | --- | --- | --- |
| 语音技术与 SDK | SkEgn 云端语音评测 SDK | `include/skegn.h`；`misc/demos/demo_for_c_cloud/demo_for_c.c`；多语言绑定 | 新增 `topics/speech/skegn.md`；接入契约，未联调 |
| 语音技术与 SDK | VAD | `src/egn/sgn_engine.c` 的 `vad.enable`；`USE_NATIVE_VAD` 构建宏 | 更新已有页面 |
| 音频处理 | Opus | `src/egn/cloud/sgn_opus_enc.c`；`test/sgn_opus_encode_file_lib.c`；`Makefile-linux` | 更新已有页面 |
| 网络与数据处理 | JSON / cJSON | `src/egn/sgn_engine.c`、`src/egn/native/sgn_native.c`；Makefile 链接 cJSON | 更新已有页面 |
| 网络与数据处理 | HTTP / WebSocket | `cloud.sdkCfgAddr`；Mongoose 测试和构建 | 更新 HTTP 页面；WebSocket 仍待独立链路核实 |
| 具体编程机制 | JNI/多语言 FFI | `include/SkEgn.java`、C#、Python、LuaJIT 演示 | 暂缓独立成篇，归入 SkEgn |
| 暂缓独立成篇 | SDK 内部消息队列、UUID、授权加密 | `src/egn/lib`、`src/egn/native` | 暂缓，属于 SDK 内部实现 |

数量：新增 1，更新 4，待核实 1，暂缓 2。历史演示中的凭证、授权文件和服务地址未写入手册。

# 代码来源、复用判断与迁移

[English](../English/sources.md) · 中文（本文件）

## 本轮原则

`2016Codes` 只用于识别值得记录的技术，不复制代码，不作为示例引用。技术页使用官方资料与本仓库示例。原始候选清单仍是线索，不能当作已验证技术文档。

本轮对照的是原 `summary_components` 迁移后的源码，读取自仓库外的删除前备份。当前 `summary_components` 工作目录仅残留空目录，不恢复旧分类结构。

| 原组件 | 判断 | 当前处理 |
| --- | --- | --- |
| core_thread_example.c | 正常生命周期下的互斥计数器可用于教学 | 最初曾复用；2026-10-26 已移除复用文件，改为独立新写 threads.c |
| core_socket_example.c | 不足以展示完整消息边界、长度上限与截断处理 | 新写本地 TCP 示例 |
| audio_pcm_format.c | 分块函数跨多次短输入时有尾部丢失风险；多通道索引硬编码 | 保留新 PCM 示例，补充显式通道提取与边界测试 |
| audio_wav_format.c | 内存结构模型不能直接作为通用可移植 WAV 文件读写器 | 用 Python wave 新实现容器往返 |
| audio_mp3_format.c、audio_opus_format.c | mock，没有实际编解码 | 新写 libmad/libopus 调用及 FFmpeg 示例 |
| audio_alsa_device.c | 只模拟设备状态 | 新写 ALSA/tinyalsa 实际 API 示例 |
| audio_vad_voice.c | 简单能量门控与增益，不是厂商 VAD/Voice 算法 | 新写明确标注的能量状态机；Voice 不伪装集成 |
| audio_unisound_asr.c | mock，不能识别语音 | 新写 SDK 接入契约，不产生假文本 |
| business_json.c | 字符串搜索，不是完整 JSON 解析 | 新写真实 cJSON 示例 |
| business_http.c | 只构造报文，URL 编码不完整、绑定历史服务地址 | 新写本地 HTTP、libcurl 和 REST 示例 |
| 日志/监控/自有业务协议 | 属于确认的暂缓或合并项 | 不恢复旧组件；通用知识并入相关技术页 |
| 其余本轮技术 | 没有适用组件 | 为手册新写，按依赖与验证状态分类 |

## 2019Codes / SkEgn SDK 扫描

本轮读取 `Coding_0001_HistoryTree/2019Codes/sdk_2.0.x_8_29`。SkEgn 的 C 头文件、C/Java/Python/C#/LuaJIT 演示和 Makefile 提供了实际调用与构建证据；第三方 Opus、cJSON、Mongoose、OpenSSL 源码只作为依赖关系核对，不复制到手册示例。历史演示中的凭证、provision 文件和服务地址不作为文档配置。

历史版本曾从 summary_components 备份复用线程组件；当前已改写为独立示例，不再依赖或引用该组件。

## 验证范围

[示例清单](../../examples/README.md)区分已运行、仅编译、缺依赖和 SDK 接入契约。离线测试不证明外部云服务、设备、Broker 或专有 SDK 可用。FIDL 继续保留为语法示意。

## 旧结构与备份

S001～S010 分类目录及八个子模块已移出工作树。删除前的快照为 `../DevelopingManual-backups/before-handbook-20261021.tar.gz`，包含未提交文件；不属于运行依赖，也不随主仓库分发。

旧子模块 Git 对象保留于本地 `.git/modules`。恢复时应结合主仓库历史中的子模块提交与快照；快照里的 `.git` 可能是本地元数据指针，不保证可独立克隆。

## 2021 限定范围与全库引用审查（2026-10-26）

- 新增 9 页，截至 Qt 串口；更新 MQTT/TCP；Qt SQL 并入 SQLite。未编写可视化、报表或 HL7 页面。
- 当前可用 examples 已检查：复用本手册独立编写的 TCP/SDK 契约；新写 Protobuf、SQLite、Qt JSON/UDP/线程/SQL/串口、TinyXML、libmosquitto、Paho Java 示例。没有复制历史工程或备份源码。
- 按用户新要求清理原有正文：Opus、VAD、HTTP、cJSON 移除历史项目说明；SkEgn 改为本地契约并删除历史 C 接口引用；pthread 改为新写独立计数器，移除旧复用组件及其头文件。
- 2016/2019 记录保留，2016 恢复原有 31 项计数；2019 的新增 SkEgn 独立归档。历史路径只允许出现在扫描/来源审计记录，正式页不得拿它们当源码参考。
- 手册所有教学代码链接应解析到 DevelopingManual 内的 examples；官方 API/标准文档可以外链，第三方开发库可作为安装依赖。检查脚本拒绝正式页中的历史源码路径与越界本地链接。
- 实际验证以 examples/README.md 为准；未安装的开发库、JDK 与厂商 SDK 不伪报通过。旧备份不恢复，也不作为构建依赖。

## 2025Codes 扫描与新增示例（2026-11-06）

- 对象：`Coding_0001_HistoryTree/2025Codes`（一个 ETC/VICS 车载收费与交通信息项目，含 Android 厂商 HAL）。只读静态扫描：没有运行目录中的程序、构建脚本或自带的 Node/Chrome 工具。证据与限制见 [2025Codes-scope.md](2025Codes-scope.md)。
- 实施范围：推荐的 9 个新页（WebSocket、zlib、JsonCpp、POSIX termios、Unix 域套接字、Lua 嵌入、JNI、Android AIDL、Android 稳定 AIDL HAL）和 3 项更新（SQLite C API、Protobuf C++/proto2、FIDL 的 Franca 部分）。其余 8 个可选候选未写。
- 来源判断：历史项目只用于识别技术，没有复制、改名搬运或引用其代码。所有新增示例都是独立新写，协议向量来自公开标准（RFC 6455 的握手密钥与掩码帧示例）。`unix_socket.py` 的长度前缀分包与已有 `framed_tcp.py` 思路相同，但示例保持自包含，没有互相导入。
- 已运行验证：`websocket_minimal.py`、`unix_socket.py`、`zlib_demo.py`、`zlib_demo.c`、`termios_pty.c` 与 23 项单元测试。termios 用伪终端，不打开真实串口；WebSocket 只与自带客户端回环，没有与浏览器或其他实现对接。
- 未编译：`jsoncpp_demo.cpp`、`lua_embed.c`、`sqlite_c_readonly.c`、`cpp_roundtrip.cpp`（缺开发包或 protoc）、`java/jni/`（缺 JDK）；`android/aidl-service/`、`android/aidl-hal/` 只是结构示意，缺 Android SDK 和 AOSP。这些文件依据官方 API 文档编写，没有被编译器检查过，使用前应先构建。
- 清理：正式页不含历史工程路径；检查脚本拒绝正式页中的 2016/2019/2021/2023/2025 扫描目录名。

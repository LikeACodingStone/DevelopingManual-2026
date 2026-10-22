# 代码来源、复用判断与迁移

## 本轮原则

`2016Codes` 只用于识别值得记录的技术，不复制代码，不作为示例引用。技术页使用官方资料与本仓库示例。原始候选清单仍是线索，不能当作已验证技术文档。

本轮对照的是原 `summary_components` 迁移后的源码，读取自仓库外的删除前备份。当前 `summary_components` 工作目录仅残留空目录，不恢复旧分类结构。

| 原组件 | 判断 | 当前处理 |
| --- | --- | --- |
| core_thread_example.c | 正常生命周期下的互斥计数器可用于教学 | 源文件原样复用到 examples/native；裁剪头文件，新增双线程驱动 |
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

复用的线程源码来自备份路径 `S001_OperatingSystem/linux/core_engineering/source/core_thread_example.c`。它原属 `summary_components/core_engineering`。教学假设和错误处理限制见 pthread 条目。

## 验证范围

[示例清单](examples/README.md)区分已运行、仅编译、缺依赖和 SDK 接入契约。离线测试不证明外部云服务、设备、Broker 或专有 SDK 可用。FIDL 继续保留为语法示意。

## 旧结构与备份

S001～S010 分类目录及八个子模块已移出工作树。删除前的快照为 `../DevelopingManual-backups/before-handbook-20261021.tar.gz`，包含未提交文件；不属于运行依赖，也不随主仓库分发。

旧子模块 Git 对象保留于本地 `.git/modules`。恢复时应结合主仓库历史中的子模块提交与快照；快照里的 `.git` 可能是本地元数据指针，不保证可独立克隆。

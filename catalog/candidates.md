# 待整理技术

从原分类手册提取，尚未逐项核实；出现依赖声明不等于已实际使用。仅为值得单独查询的技术建立正式页面。旧源码已移出当前仓库，不保留失效链接。

| 候选技术 | 原记录 | 提取来源（旧目录） |
| --- | --- | --- |
| Linux | POSIX TCP/UDP 套接字封装；包含 Windows stub 分支。 | `S001_OperatingSystem/operating_system_manual.md` |
| Linux 进程管理辅助组件（自有） | 根据预期和当前进程数给出启动、保留或清理建议；不实际管理进程。 | `S001_OperatingSystem/operating_system_manual.md` |
| Linux 日志辅助组件（自有） | 判断是否轮转并生成备份文件名；不执行文件轮转。 | `S001_OperatingSystem/operating_system_manual.md` |
| Windows | SDK 平台适配源码；未在对应平台运行验证。 | `S001_OperatingSystem/operating_system_manual.md` |
| macOS | SDK 平台适配源码；未在对应平台运行验证。 | `S001_OperatingSystem/operating_system_manual.md` |
| iOS | SDK 平台适配源码；未在对应平台运行验证。 | `S001_OperatingSystem/operating_system_manual.md` |
| Android | SDK 平台适配源码；未在对应平台运行验证。 | `S001_OperatingSystem/operating_system_manual.md` |
| GCC（gcc） | 编译 C 模块及单元测试，启用警告和调试信息。 | `S002_Development_Tools/development_tools_manual.md` |
| Make | 使用 Makefile 构建并运行三组测试。 | `S002_Development_Tools/development_tools_manual.md` |
| render_manual_pdf（自有工具） | 使用 Python 标准库把有限的 ms 标记转换成 PDF。 | `S002_Development_Tools/development_tools_manual.md` |
| groff / ps2pdf | 渲染工具说明中提及的环境工具；当前 Python 渲染器不调用它们。 | `S002_Development_Tools/development_tools_manual.md` |
| MinGW | Windows GCC 交叉构建与动态库导出。 | `S002_Development_Tools/development_tools_manual.md` |
| Xcode 工具链 | iOS 构建脚本通过 xcode-select 定位工具链。 | `S002_Development_Tools/development_tools_manual.md` |
| qmake | E016 .pro/.pri 组织源码、Qt 模块和平台链接库。 | `S002_Development_Tools/development_tools_manual.md` |
| MSBuild / Visual C++ | Visual Studio solution/project；E009 样本指定 v140 工具集。 | `S002_Development_Tools/development_tools_manual.md` |
| Gradle | Android 插件、SDK 版本、依赖及 APK 打包配置。 | `S002_Development_Tools/development_tools_manual.md` |
| protoc | 由 .proto 生成 C++ 消息代码；附历史生成脚本。 | `S002_Development_Tools/development_tools_manual.md` |
| 百度 TTS 服务 | 构造历史 text2audio 接口的请求文本；未调用在线服务，接口可用性未验证。 | `S003_IndepentService/software_service_manual.md` |
| E009 工作站应用 | 管理界面协调设备服务、消息代理和数据存储。 | `S003_IndepentService/software_service_manual.md` |
| E015 全集成应用 | 界面、任务流程、动作和设备服务分层组织。 | `S003_IndepentService/software_service_manual.md` |
| E016 QPCR | 仪器通信、实验流程、荧光分析、结果管理及报表应用。 | `S003_IndepentService/software_service_manual.md` |
| AXETaskManager | 来自 E015_AXE.zip 的独立任务管理源码，保留压缩包独有实现。 | `S003_IndepentService/software_service_manual.md` |
| UniSound SDK（libusc.so） | 模拟初始化、启动、输入 PCM、停止及读取识别结果；未链接 SDK。 | `S004_PlatformSDK/platform_sdk_manual.md` |
| Voice SDK | 当前用增益、限幅及浮点转 PCM 模拟预处理；未集成 SDK。 | `S004_PlatformSDK/platform_sdk_manual.md` |
| Huwen VAD | 原文映射到语音活动检测；当前是自有能量阈值实现，未调用 Huwen API。 | `S004_PlatformSDK/platform_sdk_manual.md` |
| Android NDK | 新增真实 ndk-build 配置；历史脚本使用 NDK r13b、GCC 4.9 与旧 ABI。 | `S004_PlatformSDK/platform_sdk_manual.md` |
| SkEgn SDK 2.0.22 | C 接口与 JNI 绑定，统一云端及可选本地识别、评测生命周期。 | `S004_PlatformSDK/platform_sdk_manual.md` |
| JNI | Java native 方法桥接 C SDK，并将识别结果回调到 Java。 | `S004_PlatformSDK/platform_sdk_manual.md` |
| Hitbot SDK | 机械臂控制接口头文件；依赖厂商动态库和硬件，未运行。 | `S004_PlatformSDK/platform_sdk_manual.md` |
| UIRobot SDK | 电机及总线控制接口，提供 UISimCanFunc 头文件；厂商库未归档。 | `S004_PlatformSDK/platform_sdk_manual.md` |
| Android SDK | Android 应用 compile/target SDK 28，min SDK 23；与已有 Android NDK 条目分开。 | `S004_PlatformSDK/platform_sdk_manual.md` |
| Foundation / UIKit / SystemConfiguration | iOS 对象、设备信息和网络可达性框架；系统依赖。 | `S006_Framework/framework_manual.md` |
| Qt | E009/E015 使用 Qt4 风格工程，E016 使用 Qt Widgets、Network、SQL、XML、SerialPort 与打印支持；版本要求需分别核对。 | `S006_Framework/framework_manual.md` |
| libmad | MP3 解码；当前代码仅输出模拟 PCM，未调用 libmad。 | `S007_Library/library_manual.md` |
| libopus | 原有解码示例为 Mock；新增 SDK 实际进行 Opus 编码与 Ogg 封装，附 1.3.1 源码。 | `S007_Library/library_manual.md` |
| ALSA / tinyalsa | 录放音接口；当前仅模拟设备状态，未访问硬件或链接库。 | `S007_Library/library_manual.md` |
| PCM 处理组件（自有） | 计算音频字节数、按 640 字节分块并转换多麦克风数据。 | `S007_Library/library_manual.md` |
| WAV 处理组件（自有） | 构建和解析 PCM WAV 头部。 | `S007_Library/library_manual.md` |
| POSIX Threads（pthread） | 通过互斥锁保护共享计数器；实际调用 pthread API。 | `S007_Library/library_manual.md` |
| JSON 提取组件（自有） | 简化字符串字段提取和 token 查找；并非完整 JSON 解析器，也未使用 cJSON。 | `S007_Library/library_manual.md` |
| HTTP 请求构造组件（自有） | 生成 GET/POST 请求文本，不发送网络请求。 | `S007_Library/library_manual.md` |
| post_content 协议组件（自有） | 业务音频包的封装、校验和解包。 | `S007_Library/library_manual.md` |
| 命令解析组件（自有） | 将 JSON 字段映射为播放、聊天转语音及媒体控制动作。 | `S007_Library/library_manual.md` |
| cJSON | 新增 SDK 实际解析配置与结果；已导入第三方实现。 | `S007_Library/library_manual.md` |
| curl（原文称外部库） | 架构文档提及的外部依赖；当前未调用 curl 或 libcurl。 | `S007_Library/library_manual.md` |
| Mongoose 6.15 | HTTP/WebSocket 事件循环、连接管理与音频帧传输。 | `S007_Library/library_manual.md` |
| libogg 1.3.3 | 将 Opus 包组织成 Ogg page；SDK 实际调用。 | `S007_Library/library_manual.md` |
| OpenSSL | USE_SSL=1 时供 Mongoose TLS 使用；本次导入头文件，平台二进制未导入。 | `S007_Library/library_manual.md` |
| zlib | 解压加密配置与本地资源；链接 -lz，依赖系统安装。 | `S007_Library/library_manual.md` |
| XXTEA 实现 | 配置及资源加解密的 C 实现。 | `S007_Library/library_manual.md` |
| Gorilla WebSocket | Go 协议客户端依赖；源码通过 import 引用，依赖本体未随工程提供。 | `S007_Library/library_manual.md` |
| go-simplejson | Go 客户端读取配置和协议 JSON；外部 Go 依赖。 | `S007_Library/library_manual.md` |
| Reachability（SGN 版本） | 封装 Apple 网络可达性查询。 | `S007_Library/library_manual.md` |
| BPXLUUIDHandler（SGN 版本） | iOS 设备 UUID 获取及保存。 | `S007_Library/library_manual.md` |
| sgn_msg_queue（自有） | SDK 内部消息队列；不是独立消息中间件。 | `S007_Library/library_manual.md` |
| sgn_buf（自有） | 维护可增长数据缓冲区，供音频和请求处理使用。 | `S007_Library/library_manual.md` |
| OpenFst / OpenBLAS / RE2 / SphinxBase | Android 本地后端声明的链接依赖；当前只有构建证据，不代表具备完整源码。 | `S007_Library/library_manual.md` |
| libmosquitto | MQTT 客户端库；代理实际调用连接、订阅、发布、TLS 和事件循环，依赖外部库。 | `S007_Library/library_manual.md` |
| Eclipse Paho MQTT | Android service 1.1.0 / MQTT client 1.2.0；Java 客户端实际调用，原 JAR 未归档。 | `S007_Library/library_manual.md` |
| Protocol Buffers | 设备消息与 qPCR 结果序列化；包含 .proto、生成代码及部分运行库源码/头文件。 | `S007_Library/library_manual.md` |
| SQLite | E009 实际调用 sqlite3 API，E015 使用 Qt QSQLITE；嵌入式数据库库，不是数据库服务器。 | `S007_Library/library_manual.md` |
| QCustomPlot | qPCR 荧光曲线及仪器图形绘制，附源码。 | `S007_Library/library_manual.md` |
| QXlsx | Qt 下读写 XLSX，工程实际纳入构建。 | `S007_Library/library_manual.md` |
| QtRPT | 报表模板、SQL 数据与打印，使用 Qt Script 等模块。 | `S007_Library/library_manual.md` |
| QextSerialPort | 跨平台串口实现；E016 同时声明 Qt SerialPort 模块。 | `S007_Library/library_manual.md` |
| Auriga HL7 library | LIS 接口的 HL7 消息构造与解析，附库源码；HL7 协议本身不重复登记为软件。 | `S007_Library/library_manual.md` |
| QuaZip | Qt ZIP 接口，E016 提供头文件并链接平台库；二进制未导入。 | `S007_Library/library_manual.md` |
| LogService（自有） | 日志级别、注册表、控制台和文件输出；源码工程为库，名称 Service 不代表独立服务。 | `S007_Library/library_manual.md` |
| qPCR 信号分析组件（自有） | 荧光曲线平滑、基线及 Ct/Cp 分析；未进行算法正确性或检测性能验证。 | `S007_Library/library_manual.md` |
| Boost | E009 项目声明 BOOST_ROOT 包含路径；未据此认定某个 Boost 子库已实际调用。 | `S007_Library/library_manual.md` |
| Retrofit | Gradle 声明 2.5.0；依赖本体未提供，未验证运行调用。 | `S007_Library/library_manual.md` |
| Gson converter（Retrofit） | Gradle 声明 converter-gson 2.5.0；未验证运行调用。 | `S007_Library/library_manual.md` |
| OkHttp logging-interceptor | Gradle 声明 3.8.1；未验证运行调用。 | `S007_Library/library_manual.md` |
| Android Support Libraries | Gradle 声明 AppCompat、support-v4、design 28.0.0 和 ConstraintLayout 1.1.3。 | `S007_Library/library_manual.md` |
| JUnit | Gradle 声明单元测试依赖 4.12；未运行 Android 测试。 | `S007_Library/library_manual.md` |
| Espresso | Gradle 声明 UI 测试依赖 3.0.2；未运行设备测试。 | `S007_Library/library_manual.md` |
| C | 实现系统、音频及业务组件，使用结构体、缓冲区和显式返回码。 | `S008_ProgramLanguage/programming_language_manual.md` |
| Python | 文档处理及 SDK ctypes 绑定；历史绑定加载 libskegn.so。 | `S008_ProgramLanguage/programming_language_manual.md` |
| C++ | 历史仪器工程的实际实现语言；Qt 界面、设备控制、消息与数据处理均有完整 C++ 源码。 | `S008_ProgramLanguage/programming_language_manual.md` |
| Java | 声明 SDK native API。 | `S008_ProgramLanguage/programming_language_manual.md` |
| C# | P/Invoke 调用 SDK 动态库。 | `S008_ProgramLanguage/programming_language_manual.md` |
| Go | 直接实现云端 WebSocket 客户端。 | `S008_ProgramLanguage/programming_language_manual.md` |
| Lua | 通过 LuaJIT FFI 调用 SDK。 | `S008_ProgramLanguage/programming_language_manual.md` |
| Objective-C | 实现 iOS 设备及网络适配。 | `S008_ProgramLanguage/programming_language_manual.md` |
| Bash | 组织多平台构建及打包。 | `S008_ProgramLanguage/programming_language_manual.md` |
| SkEgn 本地评测后端 | 按 USE_NATIVE 宏启用 eval、rec、ali、vad 等适配模块；算法核心通过外部库提供。 | `S009_Engine/engine_manual.md` |
| Kaldi | 以语音工具包及本地识别引擎依赖归入此类；Android 构建声明 kaldi-*，算法源码未随本次导入提供。 | `S009_Engine/engine_manual.md` |
| LuaJIT | 演示程序依赖 FFI 和 bit 模块加载 SDK；运行时本体未提供。 | `S010_Runtime/runtime_manual.md` |
| JVM | JNI 保存 JavaVM 并跨线程回调 Java；运行时由宿主提供。 | `S010_Runtime/runtime_manual.md` |

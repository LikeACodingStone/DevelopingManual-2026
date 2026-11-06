# 2025Codes 技术扫描（候选待确认）

[English version](../English/2025Codes-scope.md)（内容相同，仅语言不同）

源目录：`/mnt/samsung4t/lost+found/usr/bin/github/Coding_0001_HistoryTree/2025Codes`。扫描日期：2026-11-06。遵循 command_for_ai.md，仅静态读取；不运行程序、构建、设备访问或网络联调，不运行源目录自带的 Node/Chrome 工具。不复制原工程代码。下列路径相对于源目录，只是扫描证据，不用于正式页代码引用。

路径简写：`SVC` = `ccs20/aosp/vendor/neusoft/services/etcvics`；`HAL` = `hardware/etcvics`。

## 确认与实施状态（2026-11-06）

用户回复“go ahead”，没有逐项勾选，所以按本记录的推荐范围实施。

已完成 12 项：

- 新增 9 页：[WebSocket](../../topics/Chinese/network/websocket.md)、[zlib](../../topics/Chinese/network/zlib.md)、[JsonCpp](../../topics/Chinese/network/jsoncpp.md)、[POSIX 串口 termios](../../topics/Chinese/iot/posix-termios.md)、[Unix 域套接字](../../topics/Chinese/programming/unix-domain-socket.md)、[Lua 嵌入](../../topics/Chinese/programming/lua-embed.md)、[JNI](../../topics/Chinese/programming/jni.md)、[Android AIDL](../../topics/Chinese/programming/android-aidl.md)、[Android 稳定 AIDL HAL](../../topics/Chinese/programming/android-aidl-hal.md)。每页都有[英文版](../../topics/English/)。
- 更新 3 页：[SQLite](../../topics/network/sqlite.md)、[Protobuf](../../topics/network/protobuf.md)、[FIDL](../../topics/ipc/fidl.md)，英文版在 `topics/English/`。

验证结果：已运行验证 4 页（WebSocket、zlib、termios 伪终端、Unix 域套接字）；未编译 3 页加 SQLite/Protobuf 的 C/C++ 部分（缺 jsoncpp、Lua、JDK、sqlite3 头文件、protoc）；结构示意 2 页（AIDL、AIDL HAL）加 FIDL 的语法示意。详见 [examples/README.md](../../examples/README.md)。

仍待定 8 项（可选，未写）：Android TextToSpeech、D-Bus、CMake、Android Gradle 与 NDK、OpenGL ES / EGL、Boost.Test、GoogleTest、Mermaid。合并 3 项与暂缓 7 组不变。

## 范围和限制

源目录共 62,457 个文件（含版本控制元数据与自带工具）。其中 `ccs20/external/`（第三方子模块）20,910 个；`document_ver2.0` 共 35,093 个，34,986 个在 `architecture/tools/`（自带 mermaid、Node、headless Chrome、fontTools），手写文档仅 107 个。这两部分均不逐项审计。手写代码主要在 `ccs20`（ETC/VICS 车载收费与交通信息项目，C/C++、Java/Kotlin、AIDL、Franca IDL；不含版本控制元数据共 26,245 个文件，其中 20,910 个是上述 `external/`，约 5,300 个是项目自有文件）、`hardware/etcvics`（Android 厂商 HAL，68 个文件）和 `documents_ver1.0`（5 个文件）。`document_ver2.0` 的手写部分是该项目已有的中英文架构文档，只当作线索，不当作技术页来源。

未发现适用 AGENTS.md。构建入口存在（根 `CMakeLists.txt`、`app/bosch/ccs20/settings.gradle.kts`），但本轮没有构建，因此证据等级为源码调用，不能证明所有模块进入同一产物。`.gitmodules` 与 `external/` 中的分支名（如 protobuf `nts-3.1.0`、OpenSSL `nts-1.0.2u`）只说明声明的版本，不代表实际链接版本。`ccs20/.git_ccs2`、`hardware/etcvics/.git_bak` 是版本控制元数据，已跳过。目录名 2025Codes 不证明代码年代。

本机工具：已有 g++/gcc、python3（含 sqlite3、pty、termios、socket、zlib）、node、zlib.h；没有 cmake、JDK、protoc、Lua、Boost、GoogleTest、SQLite/jsoncpp/D-Bus 开发头文件，Python 无 websockets 与 protobuf 包。下文“验证可行性”据此填写，仅是预估。

## 一、音频处理

没有确认需要新增或更新的音频条目。`ccs20/res/vics/bosch_ccs20` 与 `SVC/res/raw` 中的 `.wav` 是提示音资源，不构成音频处理技术使用证据；也没有在本轮核对播放代码。

## 二、语音技术与 SDK：新增候选 1 项

| 候选 | 用途与源码证据 | 示例建议与限制 |
| --- | --- | --- |
| Android TextToSpeech | `SVC/java_common/vendor/neusoft/service/etcvics/AndroidTtsEngine.java:10–12` 导入 `TextToSpeech`、`UtteranceProgressListener`、`Voice`；`:49` 工厂字段、`:116` 构造；以 TextToSpeech 实现项目自有 TtsEngine 接口 | 与已有[百度 TTS](../../topics/speech/baidu-tts.md)（云端接口）分页。无 Android SDK，只写初始化回调、播报进度监听和语言选择的语法/接入契约；不声称设备已联调 |

## 三、网络与数据处理

### 新增候选 3 项

| 候选 | 用途与源码证据 | 示例建议与限制 |
| --- | --- | --- |
| WebSocket（websocketpp 服务端） | `ccs20/iface/adaptor/jsonws/src/WebsocketppServer.hpp:17、32、78、80`：`websocketpp::server<config::asio>`、onOpen/onClose；协议文档 `iface/adaptor/jsonws/doc/JsonWsProtocolSpec.adoc`；根 `CMakeLists.txt:110` 默认开启 JSONWS_ADAPTOR，`app/bosch/ccs20/nativelib/build.gradle.kts` 在 Android 构建中关闭 | 讲 RFC 6455 握手、帧、关闭与心跳。独立新写 Python 标准库最小握手/帧示例可本地验证；websocketpp 本身依赖 Boost/Asio，只给语法示意。哪些产品启用该适配器未确认 |
| JsonCpp | `ccs20/iface/adaptor/jsonws/src/DefaultCommunicationTask.cpp:122、124`：`Json::Value`、`objectValue`；根 `CMakeLists.txt:93`（SYSTEM_JSONCPP）、`:348–371` | 与 [cJSON](../../topics/network/json-cjson.md)、[Qt JSON](../../topics/network/qt-json.md) 互链，不混用 API。缺 jsoncpp 开发包，示例预计只能标“未编译”；声明的子模块版本 1.9.5 不等于实际链接版本 |
| zlib / DEFLATE | `ccs20/nabase/src/log/shared_lib/IMessageLogger_zlib.cpp:15、39`：`deflateInit`、`deflate(Z_FINISH)`、`deflateEnd`，受 `NA_HAVE_ZLIB` 开关保护；NDS 工具 `funit/nds/tools/hybrid_db_stripper/hybrid_db_stripper.cpp:29`、`downlink_export/downlink_export.cpp:22`、`flat_blob_export/flat_blob_export.cpp:25` 包含 `zlib.h` | 新写压缩/解压往返示例；说明 zlib、gzip、raw deflate 三种封装的区别，以及“压缩后不更小则放弃”的边界。本机有 `zlib.h` 与 Python zlib，C 与 Python 均可运行验证。该开关是否启用未确认 |

### 更新现有页面 2 项

| 页面 | 新增内容与源码证据 | 限制 |
| --- | --- | --- |
| [SQLite](../../topics/network/sqlite.md) | 补充 C API 只读查询：`ccs20/app/na_vics/mgr/toll/src/EtcVicsTollDeterminator.cpp:54、96、122`（`sqlite3_open_v2` READONLY、`prepare_v2`、`step`）；`mgr/location/src/EtcVicsPrefectureDeterminator.cpp:48、82、94`；`mgr/etcvics/src/vics/VEVicsController.cpp:3935、3946、3980`；`funit/nds/util/src/Sqlite3File.cpp:155、313、332`。资源库 `ccs20/res/vics/bosch_ccs20/*.sqlite`（3 个）仅记录文件名，不读取 | 现有页以 Python 与 Qt 为主；新增 C 小节须独立新写，说明预处理语句、参数绑定、finalize 与错误码。缺 `sqlite3.h`，C 示例预计仅能标“未编译”，Python 部分已可运行 |
| [Protobuf](../../topics/network/protobuf.md) | 补充 C++ 运行库用法与 proto2/proto3 并存：`ccs20/mgr/vics/src/VicsManager.cpp:597`、`app/na_vics/mgr/etcvics/src/vics/VEVicsController.cpp:442`、`etc/VEEtcController.cpp:599`、`proto/include/helper.hpp:23`（`ParseFromArray`/`SerializeToArray`）；`nabase/src/ipc/IPCEncoder.cpp:117`、`IPCDecoder.cpp:199`（IPC 封包）；`nabase/src/persistency/Persistency.cpp:113、176`。非第三方 `.proto` 共 78 个，其中 proto2 27、proto3 51 | 现有页偏 Python；新增段落须说明 proto2 与 proto3 的必填/默认值差异、protoc 与运行库版本必须匹配。缺 protoc，示例标“未运行”，不继承 `nts-3.1.0` 这个声明版本 |

## 四、物联网通信

没有证据建议更新 MQTT/Modbus 等已有页面。ETC/信标设备报文是项目专用协议，见暂缓项。下列为设备接入所需的通用机制：

### 新增候选 1 项

| 候选 | 用途与源码证据 | 示例建议与限制 |
| --- | --- | --- |
| POSIX 串口 termios（Linux） | `ccs20/funit/etc20/src/vics_etc_adapter.c:495、509、581、678、700`：`struct termios`、`B115200`、`tcsetattr(TCSAFLUSH)`；`funit/etc20/src/beacon_comm.c:23–25、248–250`：`termios` 与 `termios2`（自定义波特率）分支；测试工具 `funit/etc20/test/main_test.c:776–794` | 用伪终端（pty）新写回环示例：原始模式、波特率、读超时（VMIN/VTIME）、刷新与关闭。与 [Qt 串口](../../topics/programming/qt-serial.md) 互链。可本地验证；真实 ETC 盒与 `/dev/ttyUSB0` 联调不在范围内 |

## 五、具体编程机制

### 新增候选 6 项

| 候选 | 用途与源码证据 | 示例建议与限制 |
| --- | --- | --- |
| Android AIDL（Java 服务与 Binder） | `SVC/aidl/com/neusoft/service/etcvics/IVicsService.aidl:17`（该目录共 51 个 `.aidl`）；`SVC/java_common/vendor/neusoft/service/etcvics/VicsServiceImpl.java:60`（`extends IVicsService.Stub`）；`SVC/aidl/.../EtcVicsManager.java:16`（`Stub.asInterface(ServiceManager.getService(...))`）；`VicsUserService.java:41`（`onBind`）；`SVC/java/.../VicsUserManager.java:58`（`bindServiceAsUser`）；客户端 `ccs20/app/bosch/ccs20/hmi/.../base/ServiceConnector.java:26` | 讲 in/out/oneway、Parcelable、回调与线程模型。须区分普通应用 `bindService` 与平台内部 `ServiceManager`。无 JDK/AOSP，仅给语法与接入契约示意 |
| Android 稳定 AIDL HAL（NDK Binder、VINTF） | `HAL/Android.bp`（`aidl_interface`、`stability: "vintf"`、`versions: ["1"]`、ndk 后端）；`HAL/default/src/Service.cpp:24、30、43`（`ABinderProcess_*`、`AServiceManager_addService`）；`Etc20.h:12、27`（`BnEtc20`）；`default/Android.bp`；`default/*.rc` 与 `*.xml`（init 与 VINTF 声明）；`HAL/vendor_framework_compatibility_matrix.xml`；`HAL/sepolicy/`；冻结接口 `HAL/aidl_api/.../1/.hash`；`HAL/vts/functional/VtsNeusoftEtcVicsEtc20V1TargetTest.cpp:28、30、68、69`；客户端 `SVC/cpp/EtcDriver.cpp:79、106` | 与上一项分页：Java 公共服务 vs 厂商 HAL。需要 AOSP 构建环境，仅给语法与构建契约示意，列出缺少的条件；不写成已联调 |
| JNI | `ccs20/app/na_vics/src/jni/VicsJni.cpp:164、178、188`（`Java_com_neusoft_na_onecore_Vics_nativeStart/nativeStop/getCommunicationTaskPeer`，按命名约定导出，未见 `JNI_OnLoad`/`RegisterNatives`）；`jni/java/com/neusoft/na/onecore/Vics.java:22、26、137、139`（`System.loadLibrary`、用 `long` 保存 C++ 对象指针、`native` 方法）；`iface/adaptor/jni/src/JniCommunicationTask.cpp`、`TypeAdaptionTraits.cpp`（类型转换） | 候选清单 [candidates.md](../candidates.md) 中的 JNI 仅是历史线索，现有 [SkEgn](../../topics/speech/skegn.md) 页只带及 JNI。新写独立最小例：字符串/数组转换、全局引用、异常、线程附着。本机无 JDK，预计标“未编译” |
| Lua 嵌入（C API） | `ccs20/funit/laser/src/Laser.cpp:21、56、87、91、109、114、117、130–132`：`lua_State` 回调、`luaL_newstate`、`luaL_loadfile`、`lua_pcall`、`lua_register`、`lua_settable`；7 个测试脚本 `funit/laser/test/lua/*.lua`；根 `CMakeLists.txt:455` 纳入 `funit/laser`；声明的子模块版本 5.4.6 | 与 [C 调用 Python](../../topics/programming/embed-python.md) 互链。新写“注册 C 函数 + 加载脚本 + 错误处理 + 栈平衡”示例；缺 Lua 开发包，标“未编译”。实际链接版本未确认 |
| Unix 域套接字 | `ccs20/iface/adaptor/jsonws/src/UnixSocketServer.hpp:105–106`、`UnixSocketServer.cpp:64`、`UnixSocketClient.cpp:117`、`UnixSocketConnection.cpp:18`：`boost::asio::local::stream_protocol` 端点、acceptor 与 socket | 以 POSIX `AF_UNIX` 为主题，独立新写 Python 回环（含长度前缀分包、socket 文件清理、权限）；Boost.Asio 写法只作语法示意。本地可运行验证。与 [TCP 分包](../../topics/network/tcp-framing.md) 互链 |
| D-Bus（libdbus 低层 API） | `ccs20/iface/adaptor/libdbus/src/DBusCommunicationTask.cpp:301、316、327、343、442、490`：连接、过滤器、`dbus_connection_send`、`send_with_reply`（超时硬编码 60000 ms）、`read_write_dispatch`、消息处理器；`app/na_vics/iface/mgr/fidl/.../Etc.fidl:15` 注释称该接口用于 D-Bus 通信；根 `CMakeLists.txt:107` 默认 DBUS_ADAPTOR=OFF，Android 构建同样关闭 | 源码存在但默认未启用，不据此认定产品使用。本机有 `dbus-daemon` 但无开发头文件，Python 标准库不含 D-Bus 客户端，示例预计标“未验证”或“语法示意” |

### 更新现有页面 1 项

| 页面 | 新增内容与源码证据 | 限制 |
| --- | --- | --- |
| [FIDL](../../topics/ipc/fidl.md)（Franca IDL 部分） | 项目使用 Franca IDL，共 222 个 `.fidl`；`ccs20/app/na_vics/iface/mgr/fidl/com/neusoft/etcvics/interfaces/Etc.fidl` 含 `package`、`import ... from`、`version { major minor }`、`<** @description **>` 文档注释；生成器是自有 ApiFiddler（`ccs20/cmake/Modules/UseApiFiddler.cmake`，要求 ≥ 1.45.0），`iface/adaptor/CMakeLists.txt:81` 另有 `DBUS_ADAPTOR_COMMONAPI` 选项；`app/adaptor/FixFidlPaths.cmake` 与 `CMakeLists.txt:101–116` 重写导入路径 | 补充“版本号、跨文件导入、文档注释、broadcast 回调”与“生成器不一定是 CommonAPI”，保持 Fuchsia FIDL 区分。ApiFiddler 为内部工具，不展开其使用；仅语法示意，不安装 Franca 工具链 |

### 建议新增分类：构建与工程工具，新增候选 5 项

| 候选 | 用途与源码证据 | 示例建议与限制 |
| --- | --- | --- |
| CMake | 根 `ccs20/CMakeLists.txt:93–110`（`GLOBAL_OPTION` 开关）、`:331–337`、`:348–376`（`add_subdirectory(external/...)`）、`:455`；`cmake/Modules/` 下自定义 `Find*/Use*`（FindGLES2、FindAsciiDoc、UseApiFiddler 等）；`app/adaptor/CMakeLists.txt:101–116` 的 `add_custom_command`；入口 `run_cmake.pl`、`build_linux.bash` | 新写最小多目标工程：选项、`add_subdirectory`、自定义命令、`find_package`。本机无 cmake，标“未验证”；不继承工程自有宏 |
| Android Gradle 与 NDK（externalNativeBuild） | `ccs20/app/bosch/ccs20/nativelib/build.gradle.kts`（`ndkVersion`、`externalNativeBuild { cmake { arguments … } }`、`abiFilters`、指向根 CMakeLists）；`settings.gradle.kts` 引入 `aidl/app_demo/app_dev/hmi/nativelib/service/newhmi`；`buildSrc/` | 候选清单 [candidates.md](../candidates.md) 的 Android NDK、Gradle 条目只是历史线索。无 SDK/JDK，仅语法示意；AGP/Gradle 版本本轮未核对 |
| Boost.Test | 175 个文件包含 `boost/test/`；例 `ccs20/funit/vics/test/test_funit_vics_storage.cpp:15、17、220`（`BOOST_AUTO_TEST_SUITE/CASE`）、`iface/adaptor/common/test/test_Provider.cpp:55`（`BOOST_TEST`） | 可选。新写套件/夹具/浮点比较示例；本机无 Boost，标“未编译” |
| GoogleTest | 93 个文件使用 gtest 宏，集中在 `ccs20/funit/vics/test/case/**`（如 `Reception/RW` 25 个） | 可选。新写 `TEST_F`/参数化示例并与 Boost.Test 对照；本机无 GoogleTest，标“未编译” |
| Mermaid | `document_ver2.0/architecture/diagrams/`：28 张图均有 `.mmd`、SVG、PNG；渲染链 `architecture/tools/mermaid/render.mjs`、`package.json`、`package-lock.json`；`diagrams/README.md` 的重新生成说明 | 可选。证据来自文档目录而非产品代码，请你决定是否收录。新写流程图/时序图语法示例；不运行自带 Chrome 与 Node，没有 mmdc，标“语法示意” |

### 建议新增分类：图像与图形，新增候选 1 项

建议与 2023Codes 清单中的“图像与数值处理”合并命名为“图像、图形与数值处理”。

| 候选 | 用途与源码证据 | 示例建议与限制 |
| --- | --- | --- |
| OpenGL ES 2.0 / EGL | `ccs20/nabase/src/graphics/opengl/material/Shader.cpp:152、155`（`glCreateShader`、`glCompileShader`）；`nabase/src/graphics/opengl/OffscreenContext.cpp:183、214、292、344`（`eglCreatePbufferSurface`、`eglCreateContext`、`eglMakeCurrent`）；`cmake/Modules/FindGLES2.cmake`；Android 构建参数 `-DUSE_GLESV2=ON` | nabase 是通用库，与 ETC/VICS 运行路径的关系未确认。新写离屏渲染最小例，说明上下文、着色器编译与资源释放；本机无 GPU/EGL 开发环境，标“未验证” |

## 合并 3 项

1. 多个模块中的 SQLite 调用点（Toll、Prefecture、VEVics、NDS）合并为 SQLite 更新 1 项。
2. 78 个非第三方 `.proto`（nabase IPC/持久化、funit/vics、定位等）合并为 Protobuf 更新 1 项，不按模块分页。
3. 同一 Java 服务内的 `IVicsService`、`IUserService`、回调类 AIDL 合并为一个 Android AIDL 条目；`HAL/aidl_api` 的 `current` 与 `1` 快照重复，合并进 HAL 条目。

## 六、暂缓独立成篇：7 组

| 内容 | 原因与证据 | 恢复条件 |
| --- | --- | --- |
| ETC 2.0 / DSRC / VICS 设备协议与交通业务逻辑 | `ccs20/funit/etc20/src/*.c`、`funit/vics/src/Vics*Handler.cpp`、`Level3Converter.cpp`、`dsss/`：项目专用报文与业务判断；仓库内没有对应官方规范 | 取得官方规范与可公开的样例报文，并抽出与专有实现无关的格式说明 |
| 随包第三方库与工具二进制 | `ccs20/external/`（20,910 个文件）；TinyXML2 仅见 `nabase/src/memory/GlobalAlloc_libc.cpp:35、152、215` 的内存报告；OpenSSL 仅见下一组的 AWS 签名；其余 Boost 库（units、geometry、format 等）与 `document_ver2.0/architecture/tools/` 的 fontTools/Chrome/node_modules。Djinni 只有 `buildSrc/.../DjinniGenerator.kt` 与 `cmake/Modules/FindDjinniGenerator.cmake` 封装，未找到任何 `.djinni` 输入 | 各自建立应用级调用证据和独立查询价值；Djinni 需要找到输入文件与生成产物。现有 [XML / TinyXML](../../topics/network/xml-tinyxml.md) 已区分 TinyXML2，无需此处更新 |
| AWS Signature V4 | `ccs20/nabase/src/signature/awsv4/AwsV4.cpp:274–317`（`HMAC(EVP_sha256…)`、`SHA256_*`）；只在 `nabase/CMakeLists.txt:795–796` 纳入编译，全仓库未找到调用点 | 找到调用链和请求流程；官方测试向量可验证。届时可作为 [HMAC-SHA256](../../topics/network/hmac-sha256.md) 的交叉引用，而非单独成篇 |
| NDS（Navigation Data Standard）导航数据库 | `ccs20/funit/nds/`：自有读取/导出实现、数据库加密与混合库文档；ETC/VICS 交付并不证明完整导航功能 | 取得 NDS 官方规范访问权限和可公开的样例库，并明确格式边界 |
| 文档工具链（AsciiDoc、Doxygen、PlantUML、UMLet） | 195 个 `.adoc`、`cmake/Modules/FindAsciiDoc.cmake`、1 个 Doxyfile（`funit/etc20/doc/Doxyfile`）、3 个 plantuml、5 个 `.uxf`；Android 构建参数 `-DWITH_DOCS=OFF` | 决定新增文档工具分类，并有可运行样例；Mermaid 例外是因为有 28 张图与渲染脚本 |
| 在线服务与导航业务接口定义 | `ccs20/iface/mgr/fidl/com/neusoft/onlineservices`（30 个）、onecore 的 route/poi/weather/adas 等 `.fidl`，`SVC/aidl` 中的 Carwings 系列 `.aidl`：业务接口，手册只收 Franca/AIDL 语法 | 抽出独立通用机制再评估；Carwings 或导航接口存在不等于已部署对应服务 |
| 自有基础框架、线程封装与重复工程 | `ccs20/nacl`、`nabase`、`nacm` 的 Agent、Deploy、日志、性能与内存统计、插件基类；`std::thread` 仅 6 个文件、`std::mutex` 7 个、`pthread_create` 6 个，且被自有框架包裹；`hardware/etcvics/.git_bak` 与 `ccs20/.git_ccs2` 元数据；`aidl_api` 重复快照 | 抽出可独立查询的通用机制（如 C++ 并发原语）并有应用级调用证据后再评估；已有 [pthread](../../topics/programming/pthread.md) 页 |

## 数量与交付边界

新增候选 17 项（二：1，三：3，四：1，五：6，构建与工程工具：5，图像与图形：1），更新现有页面 3 项（SQLite、Protobuf、FIDL），合并 3 项，暂缓 7 组。合并项不增加页面。扫描阶段当时正式新增页和示例均为 0；实施结果见上文“确认与实施状态”。

建议优先收录：Android AIDL、Android 稳定 AIDL HAL、JNI、POSIX 串口 termios、Lua 嵌入、Unix 域套接字、zlib、WebSocket、JsonCpp 以及 3 项更新；其余为可选，由你取舍。

已核对 README、现有正式条目与 sources.md：现有 SQLite/Protobuf/FIDL 页面可扩展，其余候选无同生态正式页。所有后续教学源码只放 DevelopingManual/examples，不引用上述历史路径。预计可本地运行验证的候选：POSIX termios（pty）、Unix 域套接字、zlib（C 与 Python）、WebSocket（Python 标准库最小实现）；其余缺 JDK、AOSP、cmake、Boost、Lua 等依赖，将明确标“未编译 / 未验证 / 语法示意”，不借 Linux 测试冒充 Android 联调。

确认后 README 继续按语言/框架导航，新增 Java/Kotlin（Android）与 Lua 等表；不改变先前项目范围。本阶段只保存扫描记录，等待候选确认后再写正式页。

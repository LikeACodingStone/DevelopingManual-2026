# 2021Codes 扫描记录与确认范围

扫描日期：2026-10-26。源目录：`/mnt/samsung4t/lost+found/usr/bin/github/Coding_0001_HistoryTree/2021Codes`。

按 command_for_ai.md 完成第一阶段静态扫描，未运行旧程序、构建、云请求或设备操作。下表是源码证据，不表示编译成功或真实联调。路径均相对于源目录；只记录路径、符号和定位，不复制历史代码或数据。

## 已确认实施范围（优先于下方原始候选）

用户确认新增内容截至“Qt 串口 / QextSerialPort”：新增 9 页，更新 MQTT/TCP 2 页，Qt SQL 合并到 SQLite 1 项。QCustomPlot、QXlsx、QtRPT、HL7 及 Auriga 合并决定不在本轮实施范围；其他暂缓项保持原记录。下方 13/2/2/6 是原始候选计数，不是交付计数。

9 个入口：[Protobuf](../topics/network/protobuf.md)、[SQLite](../topics/network/sqlite.md)、[UDP](../topics/network/udp-qt.md)、[Qt JSON](../topics/network/qt-json.md)、[XML](../topics/network/xml-tinyxml.md)、[libmosquitto](../topics/iot/libmosquitto.md)、[Paho Java](../topics/iot/paho-java.md)、[Qt 线程](../topics/programming/qt-threads.md)、[Qt 串口](../topics/programming/qt-serial.md)。

正式页仅引用本手册独立教学源码；以下旧路径只作扫描证据，不能作为教学示例或代码参考。所有新增示例与已有引用审查见 sources.md；未运行旧工程或接入硬件。

## 范围与判断

- E009：Qt 仪器控制服务、MQTT 消息代理、设备消息与数据访问。
- E015：设备服务与集成界面，另有 Android MQTT 演示。`build/source/KBMullis` 含源码，已查看构建清单，不按目录名一概排除。
- E016_QPCR：qPCR 通信、结果存储、曲线绘制、报表、LIS 消息与文件传输。
- LogService：自有日志库，不因名称含 Service 就视为独立网络服务。
- E015_AXE.zip：只读列出 977 个成员，并在内存读取任务管理器数据库和执行模块；确认 QSQLITE、QThread 使用，不解压或执行。未逐文件审计整个压缩包。
- 跳过生成的 protobuf 实现、第三方库大段实现、缓存、二进制与实验数据。不同项目的相同技术合并登记。
- 没有发现适用的 AGENTS.md。目录名 2021Codes 不代表所有文件均创建于 2021 年；部分构建文件标注 2022 年。

## 一、音频处理

本轮未确认值得新增的音频技术；不沿用前两批项目的技术清单。

## 二、语音技术与 SDK

本轮未确认语音 SDK 使用。机器人和电机 SDK 归入下方设备接入暂缓项。

## 三、网络与数据处理

下列新增项均无现有正式页面；catalog/candidates.md 中的历史名称仅作线索，不当作已验证页面。

| 候选 | 用途与实际证据 | 建议及不确定性 |
| --- | --- | --- |
| Protocol Buffers | E009/messages/*.proto；E009/AWSconsole/MessageProcessor.cpp:334 的 ParseFromArray；E016_QPCR/src/resultdata/resultdata.cpp:278、294 的序列化/反序列化；HGT-QPCR.pro 纳入 ProcedureData.pb.cc | 新增；核对 protoc 与运行库版本，演示用新写 schema |
| SQLite | E009/HGTDataAccessService/HGTDataAccessService.cpp:25、50 的 sqlite3_open/exec；E015/E015/Sln_ApplicationModules/HAllinoneMachine/CommonModules/ConnectDatabase.cpp:103 的 QSQLITE | 新增；原生 API 与 Qt SQL 分开说明，运行时数据库不读取 |
| UDP / QUdpSocket | E016_QPCR/src/communication/netcomm/udpthread.cpp:304、368 的 readDatagram/writeDatagram | 新增；设备报文语义和可靠性未验证，不能据文件名把 simulateftp 当标准 FTP |
| Qt JSON | E016_QPCR/src/dataTransmission/jsonkeyvalue.cpp:123、158 的 QJsonDocument::fromJson | 新增；与现有 JSON/cJSON 页互链，不混用 API |
| XML / TinyXML | E009/HGTATCService/XML/TinyxmlControl.cpp 的 TiXmlElement、SetAttribute、SaveFile；E016 的 Qt XML 与报表使用 | 新增；已确认封装内 API 使用，TinyXML 封装的完整业务可达性未验证，不将 TinyXML 与 TinyXML2 混为一谈 |
| TCP 分包 | E009/HGTATCService/HGTATCService.cpp:35、59 的 readyRead/readAll | 更新 [TCP 分包](../topics/network/tcp-framing.md)，强调 readAll 不保证一份完整设备报文，未证明现有处理正确 |

## 四、物联网通信

| 候选 | 用途与实际证据 | 建议及不确定性 |
| --- | --- | --- |
| MQTT | E009/mqproxy/MosqMessageProxy.cpp:64、101、160 的订阅、连接、发布；E015 同类代理 | 更新 [MQTT](../topics/iot/mqtt.md)，补充仪器服务间消息流；未连接 Broker |
| libmosquitto 客户端 | 上述代理调用；E009/mqproxy/mqproxy.vcxproj:99 链接 mosquitto.lib | 新增；区别客户端库和 Mosquitto Broker 部署，不推断库版本 |
| Paho Android / Java | E015/E015/mqttdemo(android)/app/src/main/java/com/iot/mqttdemo/MainActivity.java:368、408、428 的 connect/publish/subscribe；app/build.gradle:49、50 声明 service 1.1.0/client 1.2.0 | 新增；与 [Paho C](../topics/iot/paho-c.md) 分页，不以 Gradle 声明证明运行兼容性 |

## 五、具体编程机制

| 候选 | 用途与实际证据 | 建议及不确定性 |
| --- | --- | --- |
| Qt 线程、对象归属与队列信号槽 | E016_QPCR/src/userManagement/usermanagement.cpp:302、src/dataTransmission/filetransfertask.cpp:54 的 moveToThread；src/browserecordsdialog/browserecordsdialog.cpp:79 的 QueuedConnection | 新增；讲事件循环、对象归属和退出回收，不用 pthread 示例冒充 Qt 实现 |
| Qt 串口 / QextSerialPort | E016_QPCR/src/communication/serialcomm/serialcomm.cpp:79、88、134 的创建、波特率设置和读取；HGT-QPCR.pro:36 纳入 qextserialport | 新增；实际调用为 QextSerialPort，QT += serialport 仅证明 Qt SerialPort 模块声明；现代 API 需另外核对 |

### 建议增加导航分类：可视化与报表、实验室数据交换

| 候选 | 用途与实际证据 | 建议及不确定性 |
| --- | --- | --- |
| QCustomPlot | E016_QPCR/src/qmycustomplot/qmycustomplot.cpp:6、36 的继承与 replot；HGT-QPCR.pro 编入绘图库 | 新增；独立曲线交互示例，许可证与版本须再核对 |
| QXlsx | E016_QPCR/src/browserecordsdialog/browserecordsdialog.cpp:987、1030、1172 的 Document、write、工作簿读取；HGT-QPCR.pro:40 | 新增；新建合成数据工作簿，不使用实验或个人数据 |
| QtRPT | E016_QPCR/src/resultdata/printreport.cpp:295、301、316 的 QtRPT/loadReport/printExec；HGT-QPCR.pro:39 | 新增；旧 Qt 模块兼容性未验证，只用新写模板与合成数据 |
| HL7 v2 / LIS 消息 | E016_QPCR/src/LIS/hl7handler.cpp:96 的 ORU_R01 构造及 QRY、MSH 处理；HGT-QPCR.pro:38 纳入 HL7.pri | 新增；具体版本、字段约定、传输封装需核对，不声称已接通 LIS |

## 合并决定（2 项，不额外建页）

1. Qt SQL / QSQLITE 并入拟新增 SQLite 页：E016_QPCR/src/resultdata/resultdata.cpp:638 也有实际调用；区分连接归属与原生 C API。
2. Auriga HL7 库并入拟新增 HL7 页：E016_QPCR/src/LIS/hl7 的随包库与 hl7handler.cpp 调用，不另建同内容的库页面；确认版本和许可后再决定示例实现。

## 六、暂缓独立成篇（6 组）

| 项目 | 证据与暂缓原因 | 恢复条件 |
| --- | --- | --- |
| Hitbot 机械臂 SDK | E009/HGTMechanicalArmService/HGTMechanicalArmService.cpp:230 的 net_port_initial、get_robot、运动方法；有真实调用但未运行 | 明确 SDK 版本、授权、目标设备和受控测试条件 |
| UIRobot / UISimCanFunc | E009/UIMotorDriverService/LoadSimCanFunc.cpp:281、289 起动态加载与符号解析；不能仅凭加载器证明电机动作成功 | 有厂商文档、可用库与设备；核对调用链 |
| qPCR 平滑、Ct、温度和荧光算法 | E016_QPCR/src/dataAnalysis、src/resultdata/calculatect.cpp、src/testing；领域算法不等同临床有效性 | 确定算法定义、合成与参考数据、误差指标后单独评估 |
| QuaZip / ZIP | HGT-QPCR.pro 中链接 libquazip；本轮未确认业务调用 | 查明非第三方调用点与实际压缩用途 |
| Boost、Retrofit/Gson/OkHttp 等声明依赖 | E009 vcxproj 的 BOOST_ROOT；Android app/build.gradle:46–48 | 逐项定位调用与用途，不能仅由依赖声明建页 |
| 自有日志、任务流程、设备协议与重复工程 | LogService/Log、E015_AXE.zip 中 AXETaskManager、simulateftp 等 | 只有抽离出独立查询价值且有明确协议/接口时恢复；通用知识归入已列候选 |

## 数量、示例建议与验证边界

- 新增候选 13 项，更新已有页 2 项，合并 2 项，暂缓 6 组。分类互斥计数，合并项不增加页面；本阶段正式新增页为 0。
- 已阅读 sources.md 并核对当前 topics/examples。TCP 可优先复用现有本地分包示例；MQTT 保留已有协议说明。Paho C 示例不能直接当 Java 或 libmosquitto 示例。
- 其他新增项建议确认后新写独立最小示例；仍须先按 sources.md 检查可访问旧组件的适用性和许可。本轮未恢复旧备份或复制旧工程代码。
- Qt 示例优先离线合成数据；UDP/TCP 使用本地回环；SDK、LIS 和 Broker 不自动联调。缺少专有库时只能明确给接入契约。
- 只进行文件清单、构建声明、源码符号和压缩包只读检查，没有编译、性能测试、设备测试或算法正确性验证。
- 原始扫描阶段等待确认；本轮已按页首限定范围完成编写。保留先前项目的扫描证据和未提交修改。

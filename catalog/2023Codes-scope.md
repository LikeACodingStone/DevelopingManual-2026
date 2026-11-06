# 2023Codes 技术扫描（候选待确认）

源目录：`/mnt/samsung4t/lost+found/usr/bin/github/Coding_0001_HistoryTree/2023Codes`。遵循 command_for_ai.md，仅静态读取；不执行程序、构建、设备访问或网络联调。不复制原工程代码。下列路径相对于源目录，只是扫描证据，不用于正式页代码引用。

## 范围和限制

覆盖 LT_COFAVI_SysSW、LT_AP、FlexceedAVI-AP、ThreeDTool、FeedingTest、JPEG_Tools 的文件清单，并抽查主要应用调用。文件清单约 25,146 个文件，含大量第三方实现、trunk/tags、用户实验和重复模块，不是逐行审计。build 目录包含主要源码，不能直接排除；tags 和重复第三方实现不重复计数。部分源码使用 UTF-16 或旧编码，定位按解码后的行号记录。

未发现适用 AGENTS.md；未找到 .sln/.vcxproj/.csproj/.pro/CMakeLists.txt 构建入口。因此本轮证据等级为源码调用，不能证明所有模块参与同一构建，也不确认依赖版本和可编译性。目录名 2023Codes 不证明代码年代。

## 一、音频处理

没有确认需要新增或更新的音频条目；本轮 FFT 用于图像/位置序列分析，不据此归为音频处理。

## 二、语音技术与 SDK

未确认语音技术使用。相机 SDK 放入设备接入暂缓项。

## 三、网络与数据处理

没有足够证据建议更新现有 TCP/HTTP/MQTT 页面。`LT_COFAVI_SysSW/trunk/build/CommonLibrary/Seq/InspectControlSeqDLL/InspectControlSeq_SHINDOAVI.cpp:5064` 的 WSAStartup 是注释，不算实际调用；方法名 send 也不自动代表 socket API。

## 四、物联网通信

设备控制不自动等同 MQTT/Modbus 等标准协议。本轮保留 Win32 串口候选，但未确认业务报文符合某个既有工业协议。

## 五、具体编程机制：新增候选 7 项

以下均没有现成的同生态正式页；Win32 机制不并入 pthread 或 Qt 页面。

| 候选 | 用途与源码证据 | 示例建议与限制 |
| --- | --- | --- |
| Win32 命名管道 | LT_COFAVI_SysSW/trunk/build/CommonModule/PipeLibServer.cpp:323、352：CreateNamedPipe、ConnectNamedPipe；PipeLibClient.cpp:542 有读取 | 独立新写本地客户端/服务端；说明字节/消息模式、部分读取、超时和句柄释放，Windows 验证 |
| Win32 文件映射与共享内存 | LT_COFAVI_SysSW/trunk/build/IP/Common/IppiImageDLL/IppiImage.cpp:296、320：CreateFileMapping、MapViewOfFile | 新写两个本地进程共享固定结构；同步、长度与 ABI 单独说明，不复制图像共享区布局 |
| Win32 事件与等待 | LT_COFAVI_SysSW/trunk/build/IPC/IP_Control/IP_ControlImpl.cpp:332、473：CreateEvent、WaitForSingleObject | 新写 auto/manual reset、超时和退出示例；区别 POSIX 信号量 |
| Win32 串口 API | LT_AP/build/CommonLibrary/SerialDriverDLL/SerialDriverDLL/SerialIF.cpp:68、143、171：CreateFile、SetCommState、SetCommTimeouts | 新写默认不打开设备的只读示例；与已有 Qt 串口互链，硬件需另行验证 |
| MFC 消息映射 | ThreeDTool/ThreeDToolDlg.cpp:48、73：BEGIN_MESSAGE_MAP；配套对话框事件处理 | 新写小型对话框事件示例；需 Windows/MSVC/MFC，不建立笼统 Windows/C++ 页面 |
| C# P/Invoke | LT_COFAVI_SysSW/trunk/build/MMI/MMI_Verify/Verify_GUI/Cls_UC_Verify_OP.cs:38–42 声明 user32/kernel32 导入 | 当前只确认导入声明；确认清单后补核调用可达性。教学用自建 C DLL 与 C#，不依赖厂商 DLL，不把声明当运行证据 |
| C# UI 后台任务与线程切换 | LT_COFAVI_SysSW/trunk/build/MMI/ChipAVI_GUI/ImsSupoort.cs:35、78：DoWork、RunWorkerAsync；MMI_CommonModule/Class/Cls_CommonMMIClass.cs:7383：Dispatcher.Invoke | 新写 UI/后台任务示例；区分 BackgroundWorker 和 WPF Dispatcher，说明取消、异常与 UI 线程约束 |

### 建议增加图像与数值处理分类：新增候选 5 项

| 候选 | 用途与源码证据 | 示例建议与限制 |
| --- | --- | --- |
| BMP / DIB 像素布局 | ThreeDTool/BMPLib.cpp:63、71、81、295：位图文件头、信息头、位深和读取 | 新写合成图像往返；检查 stride、行方向、调色板、长度与整数溢出；不继承旧结构直接读写方式 |
| JPEG 与 GDI+ 图像编解码 | ThreeDTool/JPGLib.cpp:50 起 GdiplusStartup、Bitmap、LockBits、编码器查询与 Save；JPEG_Tools/JPGLib.cpp 同类实现 | 新写 Windows 合成图片编码/解码，说明有损性质与 GDI+ 生命周期；不能把宽度裁剪当对齐处理 |
| OpenCV 阈值、形态学和轮廓 | LT_COFAVI_SysSW/trunk/build/IP/Modules/AlignmentMarkInsp/Lib/AlignmentMarkInsp.cpp:1938 起 threshold、morphologyEx、findContours、drawContours | 新写几何图形掩码示例；明确目标 OpenCV 版本，不复用旧 CV_* 常量或专用检测逻辑 |
| Intel IPP 图像原语 | LT_COFAVI_SysSW/trunk/build/IPC/IP_Control/IP_ControlImpl.cpp:75、590：ippiCopy_8u_P3C3R、ippiRotate_8u_C1R | 新写复制/通道转换最小例，核对目标版本 API、ROI、步长和许可；不默认旧旋转接口仍可用 |
| FFT / 频谱分析 | FeedingTest/FeedingTest/FeedingTestDlg.cpp:307 创建 FFT，FeedingTest/CommonLibrary/FFT.cpp 为实现；同目录处理孔位间距序列 | 新写已知频率合成信号，与直接 DFT 对照；不复制自有 FFT，不声称检测算法准确性 |

## 合并 2 项

1. 三个小工具中的重复 BMP 读写与像素缓冲辅助代码，作为同一 BMP/DIB 条目的扫描线索，不分别建页。
2. 多处 GDI+ JPEG 封装，合并为 JPEG/GDI+ 条目，不按工具或 DLL 名另立条目。

## 六、暂缓独立成篇：5 组

| 内容 | 原因与证据 | 恢复条件 |
| --- | --- | --- |
| Sapera 相机采集 SDK | LT_COFAVI_SysSW/trunk/users/haga/SAPERA/ImgFuncsSaperaLine.cpp:152–158 创建 SapAcquisition/SapBuffer/SapAcqToBuf；属于用户实验路径，未确认主构建 | 明确版本、硬件、授权和主程序调用关系；仅有源码调用不代表采集成功 |
| OpenMP | 多处 JPegIF/jpegcodec/decoder.cpp 有 pragma；位于随包编码器内部，无构建开关证据 | 找到应用级并行用途、构建启用证据和可独立说明的任务 |
| 随包库、SDK 示例和版本拷贝 | Boost/OpenCV 等大量附带源码与头文件，不能每个依赖单独认定实际使用 | 各自建立自有应用调用证据和独立查询价值 |
| 专用 AVI 检测、送料、引脚与三维算法 | FeedingTest/Perforation、InnerLeadTest/PinInspect、ThreeDTool/Make3DImage 等业务实现 | 明确数学定义、输入输出、参考数据与误差指标；目录名不证明标准三维重建方法 |
| 自有设备顺控、报表、日志及版本重复工程 | 多套 AP/MMI/IPC 和 tags，共享大量实现 | 抽出独立通用机制再评估；不生成项目回顾或全部依赖目录 |

## 数量与交付边界

新增候选 12 项（其中 P/Invoke 尚需确认调用可达性），更新 0 项，合并 2 项，暂缓 5 组。合并项不增加页面。当前正式新增页和示例均为 0。

已核对 README、现有正式条目与 sources.md。现有 pthread/Qt 串口例不能作为 Win32 API 示例直接复用；主要候选需独立新写。所有后续教学源码只放 DevelopingManual/examples；历史路径只留在本扫描记录。Windows/.NET、IPP、相机依赖缺失时明确未编译或未联调，不借 Linux 测试冒充 Windows 验证。

确认后 README 继续按语言/框架导航：C/C++、Python 与新增 C#/.NET 表；不改变先前项目范围。本阶段只保存扫描记录，等待候选确认后再写正式页。

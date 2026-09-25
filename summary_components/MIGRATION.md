# Source Migration

全部 25 个源码及构建文件已迁移，原有函数行为保持不变。此目录保留历史架构说明、ms/PDF 手册及 Python 缓存；历史文档中的目录树是迁移前快照，以本清单和分类手册为准。

## Manuals

- [operating_system_manual.md](../S001_OperatingSystem/operating_system_manual.md)
- [library_manual.md](../S007_Library/library_manual.md)
- [platform_sdk_manual.md](../S004_PlatformSDK/platform_sdk_manual.md)
- [software_service_manual.md](../S003_IndepentService/software_service_manual.md)
- [development_tools_manual.md](../S002_Development_Tools/development_tools_manual.md)
- [programming_language_manual.md](../S008_ProgramLanguage/programming_language_manual.md)
- [middleware_manual.md](../S005_Middleware/middleware_manual.md)
- [framework_manual.md](../S006_Framework/framework_manual.md)
- [engine_manual.md](../S009_Engine/engine_manual.md)
- [runtime_manual.md](../S010_Runtime/runtime_manual.md)

## Build

在主仓库根目录运行 `make test`。需要 GCC、Make 和 pthread。三个原有测试套件覆盖原模块；音频测试同时编译 S007 的音频源码和 S004 的语音源码。共享头文件和完整音频测试位于 S007_Library/audio_speech_processing，S004_PlatformSDK/speech/Makefile 提供同一套测试入口。

这些 S00 目录中已有八个是独立 Git 子模块；跨分类链接及构建以完整父仓库检出为前提。新增 S009_Engine 和 S010_Runtime 是普通目录。

PDF 工具运行示例：

```sh
python3 S002_Development_Tools/documentation/tools/render_manual_pdf.py summary_components/SUMMARY_COMPONENTS_MANUAL.ms /tmp/summary_components_manual.pdf
```

## File Mapping

| Original path | Current file |
| --- | --- |
| `summary_components/core_engineering/Makefile` | [S001_OperatingSystem/linux/core_engineering/Makefile](../S001_OperatingSystem/linux/core_engineering/Makefile) |
| `summary_components/core_engineering/include/core_interfaces.h` | [S001_OperatingSystem/linux/core_engineering/include/core_interfaces.h](../S001_OperatingSystem/linux/core_engineering/include/core_interfaces.h) |
| `summary_components/core_engineering/source/core_log_example.c` | [S001_OperatingSystem/linux/core_engineering/source/core_log_example.c](../S001_OperatingSystem/linux/core_engineering/source/core_log_example.c) |
| `summary_components/core_engineering/source/core_process_monitor_example.c` | [S001_OperatingSystem/linux/core_engineering/source/core_process_monitor_example.c](../S001_OperatingSystem/linux/core_engineering/source/core_process_monitor_example.c) |
| `summary_components/core_engineering/source/core_socket_example.c` | [S001_OperatingSystem/linux/core_engineering/source/core_socket_example.c](../S001_OperatingSystem/linux/core_engineering/source/core_socket_example.c) |
| `summary_components/core_engineering/source/core_thread_example.c` | [S001_OperatingSystem/linux/core_engineering/source/core_thread_example.c](../S001_OperatingSystem/linux/core_engineering/source/core_thread_example.c) |
| `summary_components/core_engineering/tests/test_core_interfaces.c` | [S001_OperatingSystem/linux/core_engineering/tests/test_core_interfaces.c](../S001_OperatingSystem/linux/core_engineering/tests/test_core_interfaces.c) |
| `summary_components/business_interaction/Makefile` | [S007_Library/business_interaction/Makefile](../S007_Library/business_interaction/Makefile) |
| `summary_components/business_interaction/include/business_interfaces.h` | [S007_Library/business_interaction/include/business_interfaces.h](../S007_Library/business_interaction/include/business_interfaces.h) |
| `summary_components/business_interaction/source/business_command.c` | [S007_Library/business_interaction/source/business_command.c](../S007_Library/business_interaction/source/business_command.c) |
| `summary_components/business_interaction/source/business_http.c` | [S007_Library/business_interaction/source/business_http.c](../S007_Library/business_interaction/source/business_http.c) |
| `summary_components/business_interaction/source/business_json.c` | [S007_Library/business_interaction/source/business_json.c](../S007_Library/business_interaction/source/business_json.c) |
| `summary_components/business_interaction/source/business_protocol.c` | [S007_Library/business_interaction/source/business_protocol.c](../S007_Library/business_interaction/source/business_protocol.c) |
| `summary_components/business_interaction/tests/test_business_interfaces.c` | [S007_Library/business_interaction/tests/test_business_interfaces.c](../S007_Library/business_interaction/tests/test_business_interfaces.c) |
| `summary_components/audio_speech_processing/Makefile` | [S007_Library/audio_speech_processing/Makefile](../S007_Library/audio_speech_processing/Makefile) |
| `summary_components/audio_speech_processing/include/audio_interfaces.h` | [S007_Library/audio_speech_processing/include/audio_interfaces.h](../S007_Library/audio_speech_processing/include/audio_interfaces.h) |
| `summary_components/audio_speech_processing/source/audio_alsa_device.c` | [S007_Library/audio_speech_processing/source/audio_alsa_device.c](../S007_Library/audio_speech_processing/source/audio_alsa_device.c) |
| `summary_components/audio_speech_processing/source/audio_mp3_format.c` | [S007_Library/audio_speech_processing/source/audio_mp3_format.c](../S007_Library/audio_speech_processing/source/audio_mp3_format.c) |
| `summary_components/audio_speech_processing/source/audio_opus_format.c` | [S007_Library/audio_speech_processing/source/audio_opus_format.c](../S007_Library/audio_speech_processing/source/audio_opus_format.c) |
| `summary_components/audio_speech_processing/source/audio_pcm_format.c` | [S007_Library/audio_speech_processing/source/audio_pcm_format.c](../S007_Library/audio_speech_processing/source/audio_pcm_format.c) |
| `summary_components/audio_speech_processing/source/audio_unisound_asr.c` | [S004_PlatformSDK/speech/source/audio_unisound_asr.c](../S004_PlatformSDK/speech/source/audio_unisound_asr.c) |
| `summary_components/audio_speech_processing/source/audio_vad_voice.c` | [S004_PlatformSDK/speech/source/audio_vad_voice.c](../S004_PlatformSDK/speech/source/audio_vad_voice.c) |
| `summary_components/audio_speech_processing/source/audio_wav_format.c` | [S007_Library/audio_speech_processing/source/audio_wav_format.c](../S007_Library/audio_speech_processing/source/audio_wav_format.c) |
| `summary_components/audio_speech_processing/tests/test_audio_interfaces.c` | [S007_Library/audio_speech_processing/tests/test_audio_interfaces.c](../S007_Library/audio_speech_processing/tests/test_audio_interfaces.c) |
| `summary_components/tools/render_manual_pdf.py` | [S002_Development_Tools/documentation/tools/render_manual_pdf.py](../S002_Development_Tools/documentation/tools/render_manual_pdf.py) |


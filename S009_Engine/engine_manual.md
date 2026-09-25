# Engine

以下条目来自 SkEgn SDK；按源码调用和构建声明记录。

| classify area | name | function | code example |
| --- | --- | --- | --- |
| Speech / Native Backend | SkEgn 本地评测后端 | 按 USE_NATIVE 宏启用 eval、rec、ali、vad 等适配模块；算法核心通过外部库提供。 | [sgn_native](../S004_PlatformSDK/speech/skegn_2.0.22/src/egn/native/sgn_native.c) |
| Speech / Toolkit | Kaldi | 以语音工具包及本地识别引擎依赖归入此类；Android 构建声明 kaldi-*，算法源码未随本次导入提供。 | [Android](../S004_PlatformSDK/speech/skegn_2.0.22/jni/Android.mk) |


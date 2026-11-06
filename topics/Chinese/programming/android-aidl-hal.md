# Android 稳定 AIDL HAL（NDK Binder 与 VINTF）

- 别名与生态：稳定 AIDL / AIDL HAL / `@VintfStability`；NDK Binder（`libbinder_ndk`）
- 适用版本与平台：AOSP 11 及以后的 AIDL HAL；库后缀、构建规则随 AOSP 版本变化，以所用版本文档为准
- 标签：programming
- 示例状态：结构示意，未构建：需要 AOSP 源码树
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

硬件抽象层（HAL）是厂商分区里的用户空间进程，向框架提供稳定接口。稳定 AIDL 是用 AIDL 编写这种接口的方式：接口标注 `@VintfStability`，每个版本冻结后不再改变，服务通过 VINTF 清单声明，框架与厂商分区可以独立升级。它是用户空间进程，不是内核驱动。

与[Java AIDL 服务](android-aidl.md)的区别：这里的接口跨越系统/厂商分区边界，因此必须版本冻结、声明清单并配置 SELinux。

## 何时使用

在 Android 上给框架提供设备访问能力（读卡器、传感器、车载设备等），且该能力由厂商分区的进程实现时。普通应用之间的调用不需要 HAL。

## 如何使用

1. 编写 `.aidl` 并标注 `@VintfStability`。
2. 在 `Android.bp` 里用 `aidl_interface` 定义，设置 `stability: "vintf"` 和 NDK 后端；首次发布时冻结版本（`m <名称>-freeze-api`）并列入 `versions`；开发期用 `m <名称>-update-api` 更新当前快照。冻结后的快照目录里带有哈希，修改接口会让构建失败。
3. 服务进程：继承生成的 `Bn<接口>`，调用 `ABinderProcess_setThreadPoolMaxThreadCount`，用 `AServiceManager_addService` 以 `<接口描述符>/<实例名>`（如 `.../default`）注册，最后 `ABinderProcess_joinThreadPool()`，它不应返回。
4. 构建服务：`cc_binary`，`vendor: true`，链接 `libbinder_ndk` 与生成的接口库（名称为 `<接口名>-V<版本>-ndk`，旧版 AOSP 用 `-ndk_platform`）。
5. 启动：`init_rc` 声明服务，其中 `interface aidl <名称>/<实例>` 声明该服务提供的 AIDL 实例，必须与 VINTF 清单一致。
6. 声明：用 `vintf_fragments` 提供 VINTF 清单片段（HAL 格式 `aidl`、名称、版本、实例）；框架一侧的兼容性矩阵把该 HAL 列为必需或可选。
7. SELinux：为服务进程、可执行文件（`file_contexts`）和服务名（`service_contexts`）定义类型与规则。
8. 客户端：用 NDK 的 `AServiceManager_getService` / `waitForService` 取得 Binder，再 `fromBinder` 成接口；回调对象要处理对端死亡。
9. 验证：写 VTS 测试，对每个已声明的实例连接并调用接口。

## 最小示例

[aidl-hal 示例](../../../examples/android/aidl-hal/hardware/handbook/echo/IEcho.aidl)包含接口 [IEcho.aidl](../../../examples/android/aidl-hal/hardware/handbook/echo/IEcho.aidl)、构建文件 [Android.bp](../../../examples/android/aidl-hal/Android.bp)、服务进程 [Service.cpp](../../../examples/android/aidl-hal/Service.cpp)、init 脚本 [hardware.handbook.echo.rc](../../../examples/android/aidl-hal/hardware.handbook.echo.rc) 和 VINTF 片段 [hardware.handbook.echo.xml](../../../examples/android/aidl-hal/hardware.handbook.echo.xml)。

这些是结构示意，不是可运行工程：没有 AOSP 源码树，也没有设备，所以既没有构建，也没有联调。SELinux 策略、VTS 测试和冻结后的 `aidl_api` 快照需要在真实 AOSP 工程里生成，示例没有伪造它们。

## 常见问题

- `AServiceManager_addService` 失败：实例没有在 VINTF 清单中声明、SELinux 拒绝，或接口未标注 `@VintfStability`。
- 修改已冻结的接口会让构建报错：增加新版本，不要原地修改。
- 接口库名称后缀、`vendor_available`、NDK 后端开关随 AOSP 版本变化，复制旧工程配置前先核对。
- 服务端线程池设置为 0 时，调用 `joinThreadPool()` 的线程就是处理请求的线程；耗时回调会阻塞它。
- 回调对象由客户端进程持有，客户端死亡后要及时释放，使用 `AIBinder_linkToDeath`。
- 离线单元测试不能证明真实设备或 HAL 联调成功。

## 参考资料

- [AOSP：AIDL HAL](https://source.android.com/docs/core/architecture/aidl/aidl-hals)
- [AOSP：稳定 AIDL](https://source.android.com/docs/core/architecture/aidl/stable-aidl)
- [AOSP：VINTF 对象](https://source.android.com/docs/core/architecture/vintf)
- [示例验证范围](../../../examples/README.md)

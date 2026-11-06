# Android AIDL：Java 服务与 Binder 跨进程调用

- 别名与生态：AIDL（Android Interface Definition Language）/ Binder；与 [FIDL](../../ipc/fidl.md)（Fuchsia、Franca）不是同一种语言
- 适用版本与平台：Android；结构化 parcelable 需要较新的 AIDL 工具链（Android 10 及以后的平台工具）
- 标签：programming
- 示例状态：语法和结构示意，未构建：本机缺 JDK 和 Android SDK
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

AIDL 用接口文件描述跨进程方法，编译器生成 Java（以及 C++/NDK/Rust）的 `Stub`（服务端基类）和 `Proxy`（客户端代理），底层通过 Binder 事务传输。参数方向分为 `in`、`out`、`inout`；`oneway` 方法不等待返回；`parcelable` 描述可跨进程传递的数据。

本页讲应用/系统服务一侧的 Java AIDL。为系统与厂商分区之间的硬件抽象层定义接口，见[稳定 AIDL HAL](android-aidl-hal.md)。

## 何时使用

应用与自己的服务、不同应用之间、应用与系统服务的跨进程调用。同一进程内直接调用即可，不需要 AIDL。接口一旦对外发布，就要按兼容规则演进。

## 如何使用

1. 编写 `.aidl`：`package`、`import`、接口方法；非基本类型参数要写方向（如 `in String name`）。
2. 构建系统生成绑定：Android Gradle 使用 `aidl` 源集，AOSP 使用 `aidl_interface`。
3. 服务端继承 `Stub`，在 `onBind` 里返回它。方法在 Binder 线程池里执行，不在主线程，共享状态要自行保证线程安全。
4. 客户端 `bindService`，在 `onServiceConnected` 里用 `Stub.asInterface(binder)` 取得代理。
5. 回调：用 `oneway` 的 listener 接口，服务端用 `RemoteCallbackList` 保存，它会在对端进程消失后自动移除条目。
6. 客户端对同步方法的调用会阻塞到服务端返回，不要在主线程调用；用 `linkToDeath` 监听服务进程死亡。
7. 演进：已发布的方法不要删除、改签名或重排；只在末尾追加，并考虑旧客户端调用新服务（或反过来）时的行为。
8. 一次事务的数据有大小限制（进程内共享约 1 MB 的 Binder 缓冲区），过大会抛出 `TransactionTooLargeException`；大数据改用文件描述符或共享内存。

## 最小示例

[aidl-service 示例](../../../examples/android/aidl-service/com/example/handbook/IGreeter.aidl)包含接口 [IGreeter.aidl](../../../examples/android/aidl-service/com/example/handbook/IGreeter.aidl)、回调 [IGreeterListener.aidl](../../../examples/android/aidl-service/com/example/handbook/IGreeterListener.aidl)、数据 [Greeting.aidl](../../../examples/android/aidl-service/com/example/handbook/Greeting.aidl)，以及服务端 [GreeterService.java](../../../examples/android/aidl-service/com/example/handbook/GreeterService.java) 和客户端 [GreeterClient.java](../../../examples/android/aidl-service/com/example/handbook/GreeterClient.java)。

这些文件是结构示意，没有对应的 Gradle 工程，本机也没有 Android SDK，所以没有编译或运行。要验证，需要把它们放进带 `aidl` 源集的 Android 工程，再在设备或模拟器上运行；这些条件缺失，本页不声称任何联调结果。

## 常见问题

- `RemoteException` / `DeadObjectException`：对端进程已死亡；清理代理并按需重新绑定。
- 主线程卡顿（ANR）：同步调用放在工作线程。
- `oneway` 只保证同一个 Binder 对象上的调用顺序，不保证不同对象之间的顺序，也不保证对端已处理完。
- 权限：服务端用 `Binder.getCallingUid()` 或权限检查识别调用方，不能默认信任。
- `ServiceManager.getService(...)` 是平台内部接口，普通应用使用 `bindService`。
- `in`/`out`/`inout` 决定数据的拷贝方向，选错会导致多余拷贝或修改丢失。

## 参考资料

- [Android 开发者：AIDL](https://developer.android.com/develop/background-work/services/aidl)
- [AOSP：AIDL 概览](https://source.android.com/docs/core/architecture/aidl)
- [示例验证范围](../../../examples/README.md)

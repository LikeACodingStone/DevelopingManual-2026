# Android AIDL: Java Services and Binder Cross-Process Calls

- Aliases and ecosystem: AIDL (Android Interface Definition Language) / Binder; not the same language as [FIDL](../ipc/fidl.md) (Fuchsia, Franca)
- Versions and platforms: Android; structured parcelables need a recent AIDL toolchain (platform tools of Android 10 and later)
- Tags: programming
- Example status: syntax and structure sketch, not built: this machine lacks a JDK and the Android SDK
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

AIDL describes cross-process methods in an interface file; the compiler generates Java (and C++/NDK/Rust) `Stub` (server base class) and `Proxy` (client proxy) classes, and transport underneath uses Binder transactions. Parameter directions are `in`, `out` and `inout`; a `oneway` method does not wait for a return; `parcelable` describes data that can be passed across processes.

This page covers Java AIDL for the application/system-service side. For hardware-abstraction interfaces between the system and vendor partitions, see the [stable AIDL HAL](android-aidl-hal.md).

## When to use

Calls between an application and its own service, between different applications, or between an application and a system service. Within one process a direct call is enough and AIDL is unnecessary. Once an interface is published externally it must evolve under compatibility rules.

## How to use

1. Write the `.aidl`: `package`, `import` and the interface methods; non-primitive parameters need a direction (for example `in String name`).
2. The build system generates the bindings: Android Gradle uses the `aidl` source set, AOSP uses `aidl_interface`.
3. The server extends `Stub` and returns it from `onBind`. Methods run on the Binder thread pool, not the main thread, so shared state needs its own thread safety.
4. The client calls `bindService` and in `onServiceConnected` obtains the proxy with `Stub.asInterface(binder)`.
5. Callbacks: use a `oneway` listener interface and keep the listeners in a `RemoteCallbackList` on the server, which removes entries automatically after the peer process disappears.
6. A synchronous call from the client blocks until the server returns, so do not make it on the main thread; use `linkToDeath` to watch for the service process dying.
7. Evolution: do not delete, change the signature of, or reorder a published method; only append at the end, and consider what happens when an old client calls a new service (or the reverse).
8. A transaction has a size limit (about 1 MB of Binder buffer shared within the process); exceeding it throws `TransactionTooLargeException`. Use a file descriptor or shared memory for large data.

## Minimal example

The [aidl-service example](../../../examples/android/aidl-service/com/example/handbook/IGreeter.aidl) contains the interface [IGreeter.aidl](../../../examples/android/aidl-service/com/example/handbook/IGreeter.aidl), the callback [IGreeterListener.aidl](../../../examples/android/aidl-service/com/example/handbook/IGreeterListener.aidl), the data type [Greeting.aidl](../../../examples/android/aidl-service/com/example/handbook/Greeting.aidl), the server [GreeterService.java](../../../examples/android/aidl-service/com/example/handbook/GreeterService.java) and the client [GreeterClient.java](../../../examples/android/aidl-service/com/example/handbook/GreeterClient.java).

These files are a structural sketch. There is no matching Gradle project and this machine has no Android SDK, so nothing was compiled or run. To verify, put them in an Android project with an `aidl` source set and run it on a device or emulator; those conditions are missing, so this page claims no integration result.

## FAQ

- `RemoteException` / `DeadObjectException`: the peer process has died; clean up the proxy and rebind if needed.
- Main-thread stalls (ANR): put synchronous calls on a worker thread.
- `oneway` only guarantees call order on the same Binder object, not across different objects, and does not guarantee that the peer has finished processing.
- Permissions: the server identifies the caller with `Binder.getCallingUid()` or permission checks and must not trust it by default.
- `ServiceManager.getService(...)` is a platform-internal interface; ordinary applications use `bindService`.
- `in`/`out`/`inout` decide the direction in which data is copied; the wrong choice causes extra copies or lost modifications.

## References

- [Android Developers: AIDL](https://developer.android.com/develop/background-work/services/aidl)
- [AOSP: AIDL overview](https://source.android.com/docs/core/architecture/aidl)
- [Example verification scope](../../../examples/README_EN.md)

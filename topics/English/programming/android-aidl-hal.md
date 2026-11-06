# Android Stable AIDL HAL (NDK Binder and VINTF)

- Aliases and ecosystem: stable AIDL / AIDL HAL / `@VintfStability`; NDK Binder (`libbinder_ndk`)
- Versions and platforms: AIDL HALs of AOSP 11 and later; library suffixes and build rules change with the AOSP release, so follow the documentation of the version used
- Tags: programming
- Example status: structure sketch, not built: needs an AOSP source tree
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

A hardware abstraction layer (HAL) is a user-space process in the vendor partition that offers a stable interface to the framework. Stable AIDL is the way to write such an interface in AIDL: the interface is annotated `@VintfStability`, each version is frozen and never changes afterwards, services are declared in a VINTF manifest, and the framework and vendor partitions can be upgraded independently. It is a user-space process, not a kernel driver.

The difference from a [Java AIDL service](android-aidl.md): this interface crosses the system/vendor partition boundary, so it must be version-frozen, declared in a manifest and given SELinux configuration.

## When to use

When you give the framework access to a device (card reader, sensor, in-vehicle device and so on) on Android and that capability is implemented by a process in the vendor partition. Calls between ordinary applications do not need a HAL.

## How to use

1. Write the `.aidl` and annotate it `@VintfStability`.
2. Define it in `Android.bp` with `aidl_interface`, set `stability: "vintf"` and the NDK backend; at the first release freeze a version (`m <name>-freeze-api`) and list it in `versions`; during development update the current snapshot with `m <name>-update-api`. The frozen snapshot directory carries a hash, and changing the interface makes the build fail.
3. Service process: extend the generated `Bn<Interface>`, call `ABinderProcess_setThreadPoolMaxThreadCount`, register with `AServiceManager_addService` under `<interface descriptor>/<instance name>` (such as `.../default`), and finally call `ABinderProcess_joinThreadPool()`, which must not return.
4. Build the service: `cc_binary` with `vendor: true`, linking `libbinder_ndk` and the generated interface library (named `<interface name>-V<version>-ndk`, or `-ndk_platform` on older AOSP).
5. Start-up: `init_rc` declares the service, and its `interface aidl <name>/<instance>` line declares the AIDL instance the service provides, which must match the VINTF manifest.
6. Declaration: provide a VINTF manifest fragment with `vintf_fragments` (HAL format `aidl`, name, version, instance); the framework-side compatibility matrix lists the HAL as required or optional.
7. SELinux: define types and rules for the service process, the executable (`file_contexts`) and the service name (`service_contexts`).
8. Client: obtain the Binder with the NDK's `AServiceManager_getService` / `waitForService`, then turn it into the interface with `fromBinder`; callback objects must handle the peer's death.
9. Verify: write a VTS test that connects to every declared instance and calls the interface.

## Minimal example

The [aidl-hal example](../../../examples/android/aidl-hal/hardware/handbook/echo/IEcho.aidl) contains the interface [IEcho.aidl](../../../examples/android/aidl-hal/hardware/handbook/echo/IEcho.aidl), the build file [Android.bp](../../../examples/android/aidl-hal/Android.bp), the service process [Service.cpp](../../../examples/android/aidl-hal/Service.cpp), the init script [hardware.handbook.echo.rc](../../../examples/android/aidl-hal/hardware.handbook.echo.rc) and the VINTF fragment [hardware.handbook.echo.xml](../../../examples/android/aidl-hal/hardware.handbook.echo.xml).

These are a structural sketch, not a runnable project: there is no AOSP source tree and no device, so nothing was built or integrated. The SELinux policy, the VTS test and the frozen `aidl_api` snapshot must be produced inside a real AOSP project, and the example does not fake them.

## FAQ

- `AServiceManager_addService` fails: the instance is not declared in the VINTF manifest, SELinux denies it, or the interface is not annotated `@VintfStability`.
- Changing a frozen interface makes the build fail: add a new version instead of editing in place.
- The interface-library suffix, `vendor_available` and the NDK-backend switch change with the AOSP release; check them before copying an older project's configuration.
- With the server thread pool set to 0, the thread that calls `joinThreadPool()` is the one that handles requests, and a slow callback blocks it.
- Callback objects are held by the client process; release them promptly when the client dies, using `AIBinder_linkToDeath`.
- Offline unit tests cannot prove that a real device or HAL integration works.

## References

- [AOSP: AIDL HAL](https://source.android.com/docs/core/architecture/aidl/aidl-hals)
- [AOSP: stable AIDL](https://source.android.com/docs/core/architecture/aidl/stable-aidl)
- [AOSP: VINTF objects](https://source.android.com/docs/core/architecture/vintf)
- [Example verification scope](../../../examples/README_EN.md)

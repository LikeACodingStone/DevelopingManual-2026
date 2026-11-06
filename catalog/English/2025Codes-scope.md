# 2025Codes Technology Scan (Candidates Pending Confirmation)

[中文版](../Chinese/2025Codes-scope.md) (same content, different language)

Source directory: `/mnt/samsung4t/lost+found/usr/bin/github/Coding_0001_HistoryTree/2025Codes`. Scan date: 2026-11-06. Follows command_for_ai.md: static reading only; no programs run, no builds, no device access, no network integration, and the Node/Chrome tools bundled in the source directory were not run. No original project code is copied. Paths below are relative to the source directory; they are scan evidence only and are not used as code references in formal pages.

Path shorthand: `SVC` = `ccs20/aosp/vendor/neusoft/services/etcvics`; `HAL` = `hardware/etcvics`.

## Confirmation and implementation status (2026-11-06)

The user replied "go ahead" without ticking items one by one, so the recommended scope in this record was carried out.

12 items done:

- 9 new pages: [WebSocket](../../topics/English/network/websocket.md), [zlib](../../topics/English/network/zlib.md), [JsonCpp](../../topics/English/network/jsoncpp.md), [POSIX serial termios](../../topics/English/iot/posix-termios.md), [Unix domain sockets](../../topics/English/programming/unix-domain-socket.md), [Lua embedding](../../topics/English/programming/lua-embed.md), [JNI](../../topics/English/programming/jni.md), [Android AIDL](../../topics/English/programming/android-aidl.md) and [Android stable AIDL HAL](../../topics/English/programming/android-aidl-hal.md). Each page also has a [Chinese version](../../topics/Chinese/).
- 3 updates: [SQLite](../../topics/English/network/sqlite.md), [Protobuf](../../topics/English/network/protobuf.md) and [FIDL](../../topics/English/ipc/fidl.md); the Chinese versions stay in `topics/`.

Verification: 4 pages run and verified (WebSocket, zlib, termios on a pseudo-terminal, Unix domain sockets); 3 pages not compiled, plus the C/C++ parts of SQLite and Protobuf (jsoncpp, Lua, a JDK, the sqlite3 headers and protoc are missing); 2 structure sketches (AIDL, AIDL HAL), plus the syntax sketch for FIDL. See [examples/README_EN.md](../../examples/README_EN.md).

Still pending, 8 optional items (not written): Android TextToSpeech, D-Bus, CMake, Android Gradle and NDK, OpenGL ES / EGL, Boost.Test, GoogleTest and Mermaid. The 3 merges and 7 deferred groups are unchanged.

## Scope and limits

The source directory holds 62,457 files (including version-control metadata and bundled tools). Of these, `ccs20/external/` (third-party submodules) has 20,910; `document_ver2.0` has 35,093, of which 34,986 are under `architecture/tools/` (bundled mermaid, Node, headless Chrome, fontTools) and only 107 are handwritten documents. Neither part was audited file by file. Handwritten code is mainly in `ccs20` (an ETC/VICS in-vehicle toll and traffic-information project: C/C++, Java/Kotlin, AIDL, Franca IDL; 26,245 files excluding version-control metadata, of which 20,910 are the `external/` above and about 5,300 are the project's own), `hardware/etcvics` (an Android vendor HAL, 68 files) and `documents_ver1.0` (5 files). The handwritten part of `document_ver2.0` is the project's existing Chinese/English architecture documentation; it was used as a lead only, not as a source for technology pages.

No applicable AGENTS.md was found. Build entry points exist (root `CMakeLists.txt`, `app/bosch/ccs20/settings.gradle.kts`), but nothing was built this round, so the evidence level is source-level calls and does not prove that all modules go into one artifact. Branch names in `.gitmodules` and `external/` (for example protobuf `nts-3.1.0`, OpenSSL `nts-1.0.2u`) only show declared versions, not the versions actually linked. `ccs20/.git_ccs2` and `hardware/etcvics/.git_bak` are version-control metadata and were skipped. The directory name 2025Codes does not prove the age of the code.

Tools on this machine: g++/gcc, python3 (with sqlite3, pty, termios, socket, zlib), node, and `zlib.h` are present; cmake, a JDK, protoc, Lua, Boost, GoogleTest and development headers for SQLite/jsoncpp/D-Bus are absent, and Python has neither the websockets nor the protobuf package. The "verification feasibility" notes below rely on this and are only estimates.

## 1. Audio processing

No audio entry is confirmed for addition or update. The `.wav` files in `ccs20/res/vics/bosch_ccs20` and `SVC/res/raw` are notification-sound resources; they are not evidence of audio-processing technology, and the playback code was not checked this round.

## 2. Speech technology and SDKs: 1 new candidate

| Candidate | Purpose and source evidence | Example suggestion and limits |
| --- | --- | --- |
| Android TextToSpeech | `SVC/java_common/vendor/neusoft/service/etcvics/AndroidTtsEngine.java:10–12` imports `TextToSpeech`, `UtteranceProgressListener` and `Voice`; `:49` factory field, `:116` constructor; implements the project's own TtsEngine interface on top of TextToSpeech | Separate page from the existing [Baidu TTS](../../topics/speech/baidu-tts.md) (cloud API). No Android SDK is available, so write only a syntax / integration-contract sketch of initialization callbacks, progress listening and language selection; do not claim device integration |

## 3. Networking and data processing

### 3 new candidates

| Candidate | Purpose and source evidence | Example suggestion and limits |
| --- | --- | --- |
| WebSocket (websocketpp server) | `ccs20/iface/adaptor/jsonws/src/WebsocketppServer.hpp:17, 32, 78, 80`: `websocketpp::server<config::asio>`, onOpen/onClose; protocol document `iface/adaptor/jsonws/doc/JsonWsProtocolSpec.adoc`; root `CMakeLists.txt:110` enables JSONWS_ADAPTOR by default, while `app/bosch/ccs20/nativelib/build.gradle.kts` turns it off in the Android build | Cover the RFC 6455 handshake, frames, close and heartbeat. A newly written minimal handshake/frame example using only the Python standard library can be verified locally; websocketpp itself needs Boost/Asio, so give syntax only. Which products enable this adaptor is not confirmed |
| JsonCpp | `ccs20/iface/adaptor/jsonws/src/DefaultCommunicationTask.cpp:122, 124`: `Json::Value`, `objectValue`; root `CMakeLists.txt:93` (SYSTEM_JSONCPP), `:348–371` | Cross-link with [cJSON](../../topics/network/json-cjson.md) and [Qt JSON](../../topics/network/qt-json.md); do not mix their APIs. The jsoncpp development package is missing, so the example will probably be marked "not compiled"; the declared submodule version 1.9.5 is not the linked version |
| zlib / DEFLATE | `ccs20/nabase/src/log/shared_lib/IMessageLogger_zlib.cpp:15, 39`: `deflateInit`, `deflate(Z_FINISH)`, `deflateEnd`, guarded by the `NA_HAVE_ZLIB` switch; the NDS tools `funit/nds/tools/hybrid_db_stripper/hybrid_db_stripper.cpp:29`, `downlink_export/downlink_export.cpp:22` and `flat_blob_export/flat_blob_export.cpp:25` include `zlib.h` | Write a compress/decompress round-trip example; explain the difference between the zlib, gzip and raw-deflate wrappers, and the "discard if not smaller" boundary. This machine has `zlib.h` and Python zlib, so both C and Python can be run and verified. Whether the switch is enabled is not confirmed |

### 2 updates to existing pages

| Page | Content to add and source evidence | Limits |
| --- | --- | --- |
| [SQLite](../../topics/network/sqlite.md) | Add C API read-only queries: `ccs20/app/na_vics/mgr/toll/src/EtcVicsTollDeterminator.cpp:54, 96, 122` (`sqlite3_open_v2` READONLY, `prepare_v2`, `step`); `mgr/location/src/EtcVicsPrefectureDeterminator.cpp:48, 82, 94`; `mgr/etcvics/src/vics/VEVicsController.cpp:3935, 3946, 3980`; `funit/nds/util/src/Sqlite3File.cpp:155, 313, 332`. The resource databases `ccs20/res/vics/bosch_ccs20/*.sqlite` (3 files) are recorded by name only and not read | The existing page centers on Python and Qt; the new C section must be written independently and cover prepared statements, parameter binding, finalize and error codes. `sqlite3.h` is missing, so the C example will probably be marked "not compiled"; the Python part can already run |
| [Protobuf](../../topics/network/protobuf.md) | Add C++ runtime usage and proto2/proto3 coexistence: `ccs20/mgr/vics/src/VicsManager.cpp:597`, `app/na_vics/mgr/etcvics/src/vics/VEVicsController.cpp:442`, `etc/VEEtcController.cpp:599`, `proto/include/helper.hpp:23` (`ParseFromArray` / `SerializeToArray`); `nabase/src/ipc/IPCEncoder.cpp:117`, `IPCDecoder.cpp:199` (IPC packets); `nabase/src/persistency/Persistency.cpp:113, 176`. There are 78 non-third-party `.proto` files: 27 proto2 and 51 proto3 | The existing page leans on Python; the new section must explain proto2 vs proto3 required/default-value differences and that protoc and the runtime library versions must match. protoc is missing, so the example is marked "not run"; the declared `nts-3.1.0` version is not inherited |

## 4. IoT communication

There is no evidence to update MQTT, Modbus or other existing pages. ETC/beacon device messages are a project-specific protocol; see the deferred items. The following is the general mechanism needed for device access:

### 1 new candidate

| Candidate | Purpose and source evidence | Example suggestion and limits |
| --- | --- | --- |
| POSIX serial termios (Linux) | `ccs20/funit/etc20/src/vics_etc_adapter.c:495, 509, 581, 678, 700`: `struct termios`, `B115200`, `tcsetattr(TCSAFLUSH)`; `funit/etc20/src/beacon_comm.c:23–25, 248–250`: `termios` and `termios2` (custom baud rate) branches; test tool `funit/etc20/test/main_test.c:776–794` | Write a new loopback example on a pseudo-terminal (pty): raw mode, baud rate, read timeout (VMIN/VTIME), flush and close. Cross-link with [Qt serial](../../topics/programming/qt-serial.md). Verifiable locally; integration with a real ETC box and `/dev/ttyUSB0` is out of scope |

## 5. Specific programming mechanisms

### 6 new candidates

| Candidate | Purpose and source evidence | Example suggestion and limits |
| --- | --- | --- |
| Android AIDL (Java service and Binder) | `SVC/aidl/com/neusoft/service/etcvics/IVicsService.aidl:17` (51 `.aidl` files in that directory); `SVC/java_common/vendor/neusoft/service/etcvics/VicsServiceImpl.java:60` (`extends IVicsService.Stub`); `SVC/aidl/.../EtcVicsManager.java:16` (`Stub.asInterface(ServiceManager.getService(...))`); `VicsUserService.java:41` (`onBind`); `SVC/java/.../VicsUserManager.java:58` (`bindServiceAsUser`); client `ccs20/app/bosch/ccs20/hmi/.../base/ServiceConnector.java:26` | Cover in/out/oneway, Parcelable, callbacks and the threading model. Distinguish ordinary-app `bindService` from the platform-internal `ServiceManager`. No JDK/AOSP, so give only a syntax and integration-contract sketch |
| Android stable AIDL HAL (NDK Binder, VINTF) | `HAL/Android.bp` (`aidl_interface`, `stability: "vintf"`, `versions: ["1"]`, ndk backend); `HAL/default/src/Service.cpp:24, 30, 43` (`ABinderProcess_*`, `AServiceManager_addService`); `Etc20.h:12, 27` (`BnEtc20`); `default/Android.bp`; `default/*.rc` and `*.xml` (init and VINTF declarations); `HAL/vendor_framework_compatibility_matrix.xml`; `HAL/sepolicy/`; frozen interface `HAL/aidl_api/.../1/.hash`; `HAL/vts/functional/VtsNeusoftEtcVicsEtc20V1TargetTest.cpp:28, 30, 68, 69`; client `SVC/cpp/EtcDriver.cpp:79, 106` | Separate page from the previous item: Java public service vs vendor HAL. Needs an AOSP build environment; give only a syntax and build-contract sketch and list the missing conditions; do not describe it as integrated |
| JNI | `ccs20/app/na_vics/src/jni/VicsJni.cpp:164, 178, 188` (`Java_com_neusoft_na_onecore_Vics_nativeStart/nativeStop/getCommunicationTaskPeer`, exported by naming convention; no `JNI_OnLoad` or `RegisterNatives` seen); `jni/java/com/neusoft/na/onecore/Vics.java:22, 26, 137, 139` (`System.loadLibrary`, a C++ object pointer stored in a `long`, `native` methods); `iface/adaptor/jni/src/JniCommunicationTask.cpp`, `TypeAdaptionTraits.cpp` (type conversion) | JNI in [candidates.md](../candidates.md) is only a historical lead, and the existing [SkEgn](../../topics/speech/skegn.md) page mentions JNI only in passing. Write a new standalone minimal example: string/array conversion, global references, exceptions, thread attachment. No JDK here, so it will probably be marked "not compiled" |
| Lua embedding (C API) | `ccs20/funit/laser/src/Laser.cpp:21, 56, 87, 91, 109, 114, 117, 130–132`: `lua_State` callback, `luaL_newstate`, `luaL_loadfile`, `lua_pcall`, `lua_register`, `lua_settable`; 7 test scripts `funit/laser/test/lua/*.lua`; root `CMakeLists.txt:455` includes `funit/laser`; declared submodule version 5.4.6 | Cross-link with [C calling Python](../../topics/programming/embed-python.md). Write a new "register a C function + load a script + error handling + stack balance" example; the Lua development package is missing, so mark it "not compiled". The linked version is not confirmed |
| Unix domain sockets | `ccs20/iface/adaptor/jsonws/src/UnixSocketServer.hpp:105–106`, `UnixSocketServer.cpp:64`, `UnixSocketClient.cpp:117`, `UnixSocketConnection.cpp:18`: `boost::asio::local::stream_protocol` endpoint, acceptor and socket | Take POSIX `AF_UNIX` as the subject and write a new Python loopback (with length-prefix framing, socket-file cleanup and permissions); show the Boost.Asio form as syntax only. Can be run and verified locally. Cross-link with [TCP framing](../../topics/network/tcp-framing.md) |
| D-Bus (low-level libdbus API) | `ccs20/iface/adaptor/libdbus/src/DBusCommunicationTask.cpp:301, 316, 327, 343, 442, 490`: connection, filter, `dbus_connection_send`, `send_with_reply` (timeout hard-coded to 60000 ms), `read_write_dispatch`, message handler; the comment at `app/na_vics/iface/mgr/fidl/.../Etc.fidl:15` says the interface is for D-Bus communication; root `CMakeLists.txt:107` defaults DBUS_ADAPTOR to OFF, and the Android build also turns it off | The source exists but is not enabled by default, so product use is not inferred. This machine has `dbus-daemon` but no development headers, and the Python standard library has no D-Bus client, so the example will probably be marked "unverified" or "syntax sketch" |

### 1 update to an existing page

| Page | Content to add and source evidence | Limits |
| --- | --- | --- |
| [FIDL](../../topics/ipc/fidl.md) (Franca IDL section) | The project uses Franca IDL, with 222 `.fidl` files; `ccs20/app/na_vics/iface/mgr/fidl/com/neusoft/etcvics/interfaces/Etc.fidl` has `package`, `import ... from`, `version { major minor }` and `<** @description **>` doc comments; the generator is the in-house ApiFiddler (`ccs20/cmake/Modules/UseApiFiddler.cmake`, requires ≥ 1.45.0), and `iface/adaptor/CMakeLists.txt:81` also has a `DBUS_ADAPTOR_COMMONAPI` option; `app/adaptor/FixFidlPaths.cmake` and `CMakeLists.txt:101–116` rewrite import paths | Add "versions, cross-file imports, doc comments, broadcast callbacks" and "the generator is not necessarily CommonAPI", while keeping the Fuchsia FIDL distinction. ApiFiddler is an internal tool and its usage is not expanded; syntax sketch only, no Franca toolchain installed |

### Suggested new category: build and engineering tools, 5 new candidates

| Candidate | Purpose and source evidence | Example suggestion and limits |
| --- | --- | --- |
| CMake | Root `ccs20/CMakeLists.txt:93–110` (`GLOBAL_OPTION` switches), `:331–337`, `:348–376` (`add_subdirectory(external/...)`), `:455`; custom `Find*/Use*` modules in `cmake/Modules/` (FindGLES2, FindAsciiDoc, UseApiFiddler, etc.); `add_custom_command` in `app/adaptor/CMakeLists.txt:101–116`; entry points `run_cmake.pl`, `build_linux.bash` | Write a new minimal multi-target project: options, `add_subdirectory`, custom commands, `find_package`. cmake is not installed here, so mark it "unverified"; the project's own macros are not inherited |
| Android Gradle and NDK (externalNativeBuild) | `ccs20/app/bosch/ccs20/nativelib/build.gradle.kts` (`ndkVersion`, `externalNativeBuild { cmake { arguments … } }`, `abiFilters`, pointing at the root CMakeLists); `settings.gradle.kts` includes `aidl/app_demo/app_dev/hmi/nativelib/service/newhmi`; `buildSrc/` | The Android NDK and Gradle entries in [candidates.md](../candidates.md) are only historical leads. No SDK/JDK, so syntax sketch only; AGP/Gradle versions were not checked this round |
| Boost.Test | 175 files include `boost/test/`; for example `ccs20/funit/vics/test/test_funit_vics_storage.cpp:15, 17, 220` (`BOOST_AUTO_TEST_SUITE/CASE`) and `iface/adaptor/common/test/test_Provider.cpp:55` (`BOOST_TEST`) | Optional. Write new suite/fixture/floating-point comparison examples; Boost is not installed, so mark "not compiled" |
| GoogleTest | 93 files use gtest macros, concentrated in `ccs20/funit/vics/test/case/**` (for example 25 in `Reception/RW`) | Optional. Write new `TEST_F` / parameterized examples and compare with Boost.Test; GoogleTest is not installed, so mark "not compiled" |
| Mermaid | `document_ver2.0/architecture/diagrams/`: all 28 diagrams have `.mmd`, SVG and PNG; rendering chain `architecture/tools/mermaid/render.mjs`, `package.json`, `package-lock.json`; regeneration notes in `diagrams/README.md` | Optional. The evidence comes from the documentation folder, not product code, so you decide whether to include it. Write new flowchart/sequence-diagram syntax examples; the bundled Chrome and Node were not run and mmdc is absent, so mark "syntax sketch" |

### Suggested new category: images and graphics, 1 new candidate

Suggested to merge with the "image and numeric processing" category proposed in the 2023Codes list, under the name "images, graphics and numeric processing".

| Candidate | Purpose and source evidence | Example suggestion and limits |
| --- | --- | --- |
| OpenGL ES 2.0 / EGL | `ccs20/nabase/src/graphics/opengl/material/Shader.cpp:152, 155` (`glCreateShader`, `glCompileShader`); `nabase/src/graphics/opengl/OffscreenContext.cpp:183, 214, 292, 344` (`eglCreatePbufferSurface`, `eglCreateContext`, `eglMakeCurrent`); `cmake/Modules/FindGLES2.cmake`; Android build argument `-DUSE_GLESV2=ON` | nabase is a general library, and its relation to the ETC/VICS runtime path is not confirmed. Write a new minimal offscreen-rendering example covering context, shader compilation and resource release; no GPU/EGL development environment here, so mark "unverified" |

## 3 merges

1. SQLite call sites across several modules (Toll, Prefecture, VEVics, NDS) are merged into 1 SQLite update.
2. The 78 non-third-party `.proto` files (nabase IPC/persistence, funit/vics, positioning, etc.) are merged into 1 Protobuf update, not split by module.
3. The `IVicsService`, `IUserService` and callback AIDL files inside the same Java service are merged into one Android AIDL entry; the duplicated `current` and `1` snapshots under `HAL/aidl_api` are merged into the HAL entry.

## 6. Deferred, no standalone page: 7 groups

| Content | Reason and evidence | Resume condition |
| --- | --- | --- |
| ETC 2.0 / DSRC / VICS device protocols and traffic business logic | `ccs20/funit/etc20/src/*.c`, `funit/vics/src/Vics*Handler.cpp`, `Level3Converter.cpp`, `dsss/`: project-specific messages and business decisions; no official specification is in the repository | Obtain the official specifications and publishable sample messages, and extract a format description independent of the proprietary implementation |
| Bundled third-party libraries and tool binaries | `ccs20/external/` (20,910 files); TinyXML2 appears only in the memory report at `nabase/src/memory/GlobalAlloc_libc.cpp:35, 152, 215`; OpenSSL appears only in the AWS signature in the next group; other Boost libraries (units, geometry, format, etc.) and the fontTools/Chrome/node_modules under `document_ver2.0/architecture/tools/`. Djinni has only the wrappers `buildSrc/.../DjinniGenerator.kt` and `cmake/Modules/FindDjinniGenerator.cmake`; no `.djinni` input was found | Each needs its own application-level call evidence and independent lookup value; Djinni needs input files and generated output. The existing [XML / TinyXML](../../topics/network/xml-tinyxml.md) page already distinguishes TinyXML2, so no update is needed here |
| AWS Signature V4 | `ccs20/nabase/src/signature/awsv4/AwsV4.cpp:274–317` (`HMAC(EVP_sha256…)`, `SHA256_*`); it is only compiled in via `nabase/CMakeLists.txt:795–796`, and no call site was found anywhere in the repository | Find the call chain and request flow; the official test vectors can verify it. It could then be a cross-reference from [HMAC-SHA256](../../topics/network/hmac-sha256.md) rather than a standalone page |
| NDS (Navigation Data Standard) navigation database | `ccs20/funit/nds/`: in-house reading/export code, database-encryption and hybrid-database documents; an ETC/VICS delivery does not prove a complete navigation feature | Obtain access to the official NDS specification and a publishable sample database, and define the format boundary |
| Documentation toolchain (AsciiDoc, Doxygen, PlantUML, UMLet) | 195 `.adoc` files, `cmake/Modules/FindAsciiDoc.cmake`, 1 Doxyfile (`funit/etc20/doc/Doxyfile`), 3 plantuml files, 5 `.uxf` files; the Android build passes `-DWITH_DOCS=OFF` | Decide to add a documentation-tools category and have runnable samples; Mermaid is the exception because it has 28 diagrams and a render script |
| Online-service and navigation business interface definitions | `ccs20/iface/mgr/fidl/com/neusoft/onlineservices` (30 files), the onecore route/poi/weather/adas `.fidl` files, and the Carwings `.aidl` files in `SVC/aidl`: business interfaces; the manual covers only Franca/AIDL syntax | Extract an independent general mechanism and reassess; the existence of Carwings or navigation interfaces does not mean the corresponding service is deployed |
| In-house base framework, thread wrappers and duplicate projects | Agent, Deploy, logging, performance and memory statistics, and plugin base classes in `ccs20/nacl`, `nabase`, `nacm`; `std::thread` appears in only 6 files, `std::mutex` in 7 and `pthread_create` in 6, all wrapped by the in-house framework; the `hardware/etcvics/.git_bak` and `ccs20/.git_ccs2` metadata; duplicate `aidl_api` snapshots | Reassess once an independently queryable general mechanism (such as C++ concurrency primitives) has application-level call evidence; there is already a [pthread](../../topics/programming/pthread.md) page |

## Counts and delivery boundary

17 new candidates (section 2: 1, section 3: 3, section 4: 1, section 5: 6, build and engineering tools: 5, images and graphics: 1), 3 updates to existing pages (SQLite, Protobuf, FIDL), 3 merges and 7 deferred groups. Merged items do not add pages. At the scan stage the number of formal new pages and examples was 0; see "Confirmation and implementation status" above for the result.

Recommended to include first: Android AIDL, Android stable AIDL HAL, JNI, POSIX serial termios, Lua embedding, Unix domain sockets, zlib, WebSocket, JsonCpp and the 3 updates; the rest are optional and up to you.

README, the existing formal entries and sources.md were checked: the existing SQLite/Protobuf/FIDL pages can be extended, and the other candidates have no formal page in the same ecosystem. All later teaching source goes only in DevelopingManual/examples and does not reference the historical paths above. Candidates expected to be verifiable locally: POSIX termios (pty), Unix domain sockets, zlib (C and Python), and WebSocket (minimal Python standard-library implementation); the rest lack a JDK, AOSP, cmake, Boost, Lua or similar dependencies and will be clearly marked "not compiled / unverified / syntax sketch", without using Linux tests to pose as Android integration.

After confirmation, the README will continue to be organized by language/framework, adding tables such as Java/Kotlin (Android) and Lua; the scope of earlier projects is unchanged. This phase only saves the scan record and waits for candidate confirmation before writing formal pages.

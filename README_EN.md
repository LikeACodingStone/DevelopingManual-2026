# Technology Reference Handbook

English (this file) · [中文](README_CH.md)

Look up what a specific technology is, when to use it, how to use it, plus examples and common problems. Technology categories are for navigation only; no sub-repository is created per category.

The [2016 confirmed list](catalog/2016-scope.md) (zh) has 31 formal entries; the [2019 list](catalog/2019Codes-scope.md) (zh) records SkEgn; the [2021 list](catalog/2021Codes-scope.md) (zh) adds 9 entries and updates MQTT/TCP. There is also a FIDL page, for 42 pages in total. The [2023 list](catalog/2023Codes-scope.md) (zh) is still a set of candidates awaiting confirmation and has no formal pages yet. The [2025 list](catalog/English/2025Codes-scope.md) was carried out for the recommended scope; see "2025Codes scan results" below. The tables below are organized by the main language or framework of the handbook's examples; cross-language topics can appear in several tables. All teaching code is in this repository's `examples/`.

## Language versions and layout

- Root indexes: `README.md` is the main README (Chinese), `README_CH.md` is its Chinese copy with the same content, and `README_EN.md` is the English version. The bodies of `README.md` and `README_CH.md` must be identical; the check script compares them.
- New pages from 2025Codes onward are split by language: `topics/Chinese/<category>/` and `topics/English/<category>/`, same content in different languages. Scan records follow the same rule: `catalog/Chinese/` and `catalog/English/`.
- The 42 pages from before 2025Codes remain in `topics/<category>/` and exist only in Chinese. SQLite, Protobuf and FIDL were updated in the 2025 round and now have English versions in `topics/English/`; the others have no English version yet, and links to them are marked (zh).
- Teaching code exists once, in `examples/`, and is not split by language. The English version of `examples/README.md` is `examples/README_EN.md`; the sources document is `catalog/Chinese/sources.md` with the English version `catalog/English/sources.md`. No sources file is kept in the repository root.

## C / C++ examples

| Area | Technology entries |
| --- | --- |
| Audio processing | [ALSA](topics/audio/alsa.md) (zh), [ALSA Mixer](topics/audio/alsa-mixer.md) (zh), [AAC / ADTS / FAAD2](topics/audio/aac-adts-faad.md) (zh), [MP3 / libmad](topics/audio/mp3-libmad.md) (zh), [Opus](topics/audio/opus.md) (zh), [SpeexDSP resampling](topics/audio/resampling.md) (zh), [tinyalsa](topics/audio/tinyalsa.md) (zh) |
| Networking and data | [JSON / cJSON](topics/network/json-cjson.md) (zh), [JsonCpp](topics/English/network/jsoncpp.md), [libcurl](topics/network/libcurl.md) (zh), [TLS / OpenSSL](topics/network/tls-openssl.md) (zh), [zlib / DEFLATE](topics/English/network/zlib.md) |
| IoT | [libmosquitto](topics/iot/libmosquitto.md) (zh), [Modbus](topics/iot/modbus.md) (zh), [MQTT](topics/iot/mqtt.md) (zh), [Paho C](topics/iot/paho-c.md) (zh), [POSIX serial termios](topics/English/iot/posix-termios.md) |
| Programming mechanisms | [Calling Python from C](topics/programming/embed-python.md) (zh), [Lua embedding](topics/English/programming/lua-embed.md), [pthread](topics/programming/pthread.md) (zh), [Semaphores](topics/programming/semaphore.md) (zh), [Unix domain sockets](topics/English/programming/unix-domain-socket.md), [C variadic arguments](topics/programming/varargs.md) (zh), [XML / TinyXML](topics/network/xml-tinyxml.md) (zh) |

## Python examples

| Area | Technology entries |
| --- | --- |
| Audio processing | [PCM](topics/audio/pcm.md) (zh), [WAV](topics/audio/wav.md) (zh), [Opus / FFmpeg](topics/audio/opus.md) (zh) |
| Networking and data | [Base64](topics/network/base64.md) (zh), [HMAC-SHA256](topics/network/hmac-sha256.md) (zh), [HTTP](topics/network/http.md) (zh), [Protobuf](topics/English/network/protobuf.md), [SQLite](topics/English/network/sqlite.md), [TCP framing](topics/network/tcp-framing.md) (zh), [WebSocket](topics/English/network/websocket.md), [zlib / DEFLATE](topics/English/network/zlib.md) |
| IoT | [BACnet](topics/iot/bacnet.md) (zh) |
| Programming mechanisms | [Selenium](topics/programming/selenium.md) (zh), [Unix domain sockets](topics/English/programming/unix-domain-socket.md) |
| Speech and SDK integration contracts | [Baidu ASR](topics/speech/baidu-asr.md) (zh), [Baidu TTS](topics/speech/baidu-tts.md) (zh), [SkEgn](topics/speech/skegn.md) (zh), [Unisound ASR](topics/speech/unisound-asr.md) (zh), [VAD](topics/speech/vad.md) (zh), [Voice pre-processing](topics/speech/voice-preprocessing.md) (zh), [Wake word](topics/speech/wake-word.md) (zh) |

## Qt (C++) examples

| Area | Technology entries |
| --- | --- |
| Data, networking and devices | [Qt JSON](topics/network/qt-json.md) (zh), [SQLite / Qt SQL](topics/English/network/sqlite.md), [UDP / QUdpSocket](topics/network/udp-qt.md) (zh), [Qt serial / QextSerialPort](topics/programming/qt-serial.md) (zh) |
| Concurrency | [Qt threads and queued signals/slots](topics/programming/qt-threads.md) (zh) |

## Java / Android examples

| Platform | Technology entries |
| --- | --- |
| JVM / Android integration | [Paho Java / Android](topics/iot/paho-java.md) (zh), [JNI](topics/English/programming/jni.md) |
| Android system interfaces | [Android AIDL (Java service and Binder)](topics/English/programming/android-aidl.md), [Android stable AIDL HAL](topics/English/programming/android-aidl-hal.md) |

## Interface description languages

[FIDL](topics/English/ipc/fidl.md) distinguishes Fuchsia FIDL from Franca IDL; the 2025 round added notes on Franca versions, imports, broadcasts and in-house generators. The page provides syntax sketches and does not depend on a particular handbook example language.

## 2025Codes scan results

The scanned project is an ETC/VICS in-vehicle toll and traffic-information project. It was read statically; nothing was built or integrated. The full evidence, counts and limits are in the [scan record](catalog/English/2025Codes-scope.md).

Result: 17 new candidates, 3 updates to existing pages, 3 merges and 7 deferred groups. The recommended scope was carried out: this round wrote 9 of them as new pages plus the 3 updates; the other 8 optional candidates remain pending.

### Done: 9 new pages and 3 updates

| Page | Example status |
| --- | --- |
| [WebSocket](topics/English/network/websocket.md) | Run and verified (Python standard library + RFC 6455 vectors) |
| [zlib / DEFLATE](topics/English/network/zlib.md) | Run and verified (Python and C) |
| [JsonCpp](topics/English/network/jsoncpp.md) | Not compiled: jsoncpp missing |
| [POSIX serial termios](topics/English/iot/posix-termios.md) | Run and verified (pseudo-terminal, no real device) |
| [Unix domain sockets](topics/English/programming/unix-domain-socket.md) | Run and verified (Python) |
| [Lua embedding](topics/English/programming/lua-embed.md) | Not compiled: Lua development package missing |
| [JNI](topics/English/programming/jni.md) | Not compiled: JDK missing |
| [Android AIDL](topics/English/programming/android-aidl.md) | Structure sketch: Android SDK missing |
| [Android stable AIDL HAL](topics/English/programming/android-aidl-hal.md) | Structure sketch: AOSP missing |
| Update: [SQLite](topics/English/network/sqlite.md) | Added the C API; the C example was not compiled |
| Update: [Protobuf](topics/English/network/protobuf.md) | Added proto2/proto3 and the C++ runtime; the C++ example was not compiled |
| Update: [FIDL](topics/English/ipc/fidl.md) | Added Franca versions, imports, broadcasts and in-house generators; syntax sketch |

### Pending: 8 optional candidates (not written)

Android TextToSpeech, D-Bus (libdbus), CMake, Android Gradle and NDK, OpenGL ES / EGL, Boost.Test, GoogleTest and Mermaid. Which of them to write is to be confirmed when needed.

### 3 merges and 7 deferred groups

Merged: the SQLite call sites in several modules into the SQLite update; the 78 `.proto` files into the Protobuf update; the AIDL files inside one Java service and the duplicated `aidl_api` snapshots into the matching AIDL entries.

Deferred: ETC/DSRC/VICS device protocols and business logic; bundled third-party libraries and tool binaries; AWS Signature V4 (no call site); the NDS navigation database; the documentation toolchain (AsciiDoc, Doxygen, PlantUML, UMLet); online-service and navigation business interfaces; the in-house base framework and duplicate projects. The reason and the resume condition for each group are in the scan record.

## Use and maintenance

- [Extraction instructions for Codex](command_for_ai.md) (zh): the process and prompt template for scanning other projects, including the bilingual-version rule.
- [Examples and verification scope](examples/README_EN.md): the difference between run, needs-libraries/devices, and interface contracts.
- [Entry template](topics/TEMPLATE_EN.md) ([Chinese template](topics/TEMPLATE.md)), [Maintenance conventions](CONTRIBUTING.md) (zh).
- [Code sources and reuse decisions](catalog/English/sources.md) (the Chinese original is [catalog/Chinese/sources.md](catalog/Chinese/sources.md)): the independent origin of teaching examples, the historical-reuse cleanup and verification boundaries.
- [Other candidates to screen](catalog/candidates.md) (zh): historical leads, not yet checked one by one.

```sh
make demo          # write PCM and WAV to /tmp/pcm-demo
make test          # docs, Python, local network and basic C examples
make test-media    # the above + real FFmpeg MP3/AAC/Opus encoding and decoding
```

You do not need to install every external SDK to use the handbook. Each page states its own dependencies and verification scope, and never labels a mock or a syntax sketch as a real integration.

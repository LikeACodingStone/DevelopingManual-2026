# Examples and Verification Scope

[中文](README.md) · English (this file)

All paths are run from the repository root. Development dependencies are installed by the user for the system; this repository ships no old binaries, accounts, models or copies of third-party source.

## Verified

| Example | Content | How to run |
| --- | --- | --- |
| pcm-read-write/ | PCM/WAV round trip, streaming framing, channel extraction | `make demo`, `make test` |
| python/framed_tcp.py | Local TCP length-prefixed messages | `python3 examples/python/framed_tcp.py` |
| python/http_local.py | Local UTF-8 JSON POST | `python3 examples/python/http_local.py` |
| python/encoding.py | Base64 and HMAC standard vectors | `python3 examples/python/encoding.py` |
| python/vad.py | A new energy-gate state machine, not real speech classification | `python3 examples/python/vad.py` |
| python/bacnet_whois.py | Builds the discovery message only by default | `python3 examples/python/bacnet_whois.py` |
| native/threads.c | An independently written mutex counter verified with two threads | compiled and run automatically by `make test` |
| native/semaphore.c, varargs.c | Semaphores, variadic arguments | compiled and run automatically by `make test` |
| native/embed_python.c | Embedding Python 3.12 | development package present here; compiled and run successfully |
| native/tls.c | OpenSSL TLS identity-verification configuration | compiled here; no external network access |
| media/codec_demo.py | FFmpeg MP3, ADTS AAC and Ogg Opus encoding and decoding | `make test-media` |

`make test` checks document links, Python tests, local TCP/HTTP and the basic C examples. It needs Python 3, a C compiler and pkg-config; when the optional development packages for the Python embedding and OpenSSL compile checks are missing, it prints SKIP explicitly. `make test-media` also needs an FFmpeg with the relevant encoders.

FFmpeg verification cannot replace build verification of the libopus, libmad and FAAD2 C interface examples. Codecs are lossy conversions, so only decodability, sample format and duration range are verified, not byte-for-byte equality of samples.

## Needs external dependencies; not yet compiled or integrated

| File | Dependency | Scope |
| --- | --- | --- |
| native/alsa.c, mixer.c | alsa-lib development package; a real mixer needs a device | write silence / read-only volume query |
| native/tinyalsa.c | tinyalsa development package and an audio device | write silence |
| native/opus.c | libopus development package | real packet encode/decode in memory |
| native/resample.c | SpeexDSP development package | stateful resampling |
| native/mad.c | libmad development package and an MP3 file | count actually decoded frames |
| native/faad.c | FAAD2 development package and an ADTS file | count actually decoded samples |
| native/cjson.c | cJSON development package | structured parsing and type checks |
| native/curl.c | libcurl development package | request to a given URL |
| native/paho.c | Paho MQTT C, a local broker | QoS 1 publish |
| native/modbus.c | libmodbus, a local Modbus simulator | read-only holding registers |
| python/selenium_demo.py | Selenium 4, Chrome and a matching driver | local HTML automation |
| integrations/baidu_speech.py | current token / service permission | construction code verified offline; cloud request not executed |

Each entry provides build and run commands. Calling cloud services or connecting to devices or brokers is not part of the automatic tests.

## Integration contract, not a vendor implementation

[integrations/sdk_session.py](integrations/sdk_session.py) illustrates the resource lifecycle of a proprietary SDK; it does not call the Unisound, Voice or wake-word SDKs and does not produce simulated recognition results. The fault-injection test only verifies that resources are released on the failure path and does not mean SDK integration succeeded.

## New examples for the 2021 technology entries

All teaching source files were written independently for this handbook. Nothing was copied from historical projects or backups; build products may be written to a temporary directory, and external development libraries are installed dependencies, not handbook source references.

| File | Verification scope |
| --- | --- |
| python/sqlite_demo.py | Python standard library; in-memory transaction and rollback on a constraint failure; run |
| protobuf/sample.proto, roundtrip.py | New schema and malformed-input checks; protoc / Python protobuf missing, not run |
| qt/json_demo.cpp, udp_demo.cpp, threads_demo.cpp, sqlite_demo.cpp | Qt 5/6 Core/Network/Sql; development packages missing, not compiled; UDP is loopback only |
| qt/serial/serial_demo.cpp, serial.pro | QextSerialPort 1.2 / Qt 5; not compiled, no device opened, prints only a description by default |
| native/tinyxml_demo.cpp | TinyXML 2.6 API; development package missing, not compiled |
| native/mosquitto_demo.c | libmosquitto; development package missing, not compiled, no broker connection |
| java/PahoLocal.java | Java SE / Paho 1.2.x; JDK/JAR missing, not compiled; not an Android APK |

Build and run commands are on the matching technology pages. The Android Service remains a lifecycle integration description; no runnable Android project was faked. When optional dependencies are missing, the check script reports SKIP explicitly and does not count it as a pass.

Environment of that round's actual checks: Linux x86_64, Python 3.12.3. `make test` passed the document link/structure check, Python syntax and 9 unit tests, local TCP/HTTP, the SQLite rollback and the basic C examples; Qt, TinyXML, libmosquitto, Protobuf and Java were skipped explicitly because their dependencies are missing. `git diff --check` passed; no media re-encoding, broker, device or cloud integration was run.

## New examples for the 2025 technology entries

All teaching source files were written independently for this handbook, and no historical project source was copied. The run commands are on the matching technology pages; `make test` runs automatically the items marked "run" in the table.

| File | Verification scope |
| --- | --- |
| python/websocket_minimal.py | standard library; loopback handshake, frames, masking, fragmentation, ping/pong, close; run |
| python/unix_socket.py | standard library; AF_UNIX loopback with stale file, permissions and peer uid; run |
| python/zlib_demo.py, native/zlib_demo.c | the three zlib wrappers, corrupted/truncated/over-limit input; both Python and C run |
| native/termios_pty.c | termios configuration and read timeout on a pseudo-terminal; run, no real serial port opened |
| python/test_ipc_examples.py | RFC vectors and rejection-path tests for the Python examples above, 23 tests |

| File | Dependency | Scope |
| --- | --- | --- |
| native/jsoncpp_demo.cpp | jsoncpp development package | strict parsing and type checks; not compiled |
| native/lua_embed.c | Lua 5.4 development package | register a C function, protected calls, stack balance; not compiled |
| native/sqlite_c_readonly.c | sqlite3 development package | read-only connection and failure paths; not compiled |
| protobuf/legacy_v2.proto, cpp_roundtrip.cpp | protoc, libprotobuf | proto2 required fields and presence; not compiled |
| java/jni/ | JDK, `jni.h` | strings, arrays, exceptions, handles; not compiled |
| android/aidl-service/ | Android SDK | Java AIDL service and client; structure sketch, not built |
| android/aidl-hal/ | AOSP source tree | stable AIDL HAL; structure sketch, not built |

For the items in the table above that can be built automatically (jsoncpp, Lua, SQLite C, Protobuf C++, JNI), the check script compiles and runs them when the dependencies exist and prints SKIP explicitly when they are missing; their behavior once the dependencies are installed was not actually exercised in this round. The two Android directories have no matching Android project or device, and no build result was faked.

Environment of this (2025) round's actual checks: Linux x86_64, Python 3.12.3, gcc 13.3. `make test` passed: the document link/structure check on 82 files, 32 Python unit tests (3 for pcm + 29 for examples, 23 of which are new this round), local TCP/HTTP, the new WebSocket / Unix socket / zlib (Python and C) / termios pseudo-terminal examples, and the existing basic C examples. jsoncpp, Lua, SQLite C, Protobuf, Protobuf C++, JNI, Android, Qt, TinyXML, libmosquitto and Paho Java were skipped explicitly because their dependencies are missing. No Android build, real serial port, browser WebSocket or other device/cloud integration was run.

# Code Sources, Reuse Decisions and Migration

[中文](../Chinese/sources.md) · English (this file)

## Principles of this round

`2016Codes` was used only to identify technologies worth recording; no code was copied or used as an example reference. Technology pages use official material and this repository's examples. The original candidate list is still a set of leads and must not be taken for verified technical documentation.

This round compared the source migrated from the original `summary_components`, read from a backup outside the repository taken before deletion. The current `summary_components` working directory holds only empty directories, and the old category structure is not restored.

| Original component | Decision | Current handling |
| --- | --- | --- |
| core_thread_example.c | A mutex counter in a normal lifecycle is usable for teaching | reused at first; the reused file was removed on 2026-10-26 and replaced by an independently written threads.c |
| core_socket_example.c | Not enough to show full message boundaries, length limits and truncation handling | new local TCP example written |
| audio_pcm_format.c | The chunking function risks losing the tail across several short inputs; multi-channel indexing is hard-coded | new PCM example kept, with explicit channel extraction and boundary tests added |
| audio_wav_format.c | The in-memory structure model cannot serve directly as a general portable WAV reader/writer | container round trip re-implemented with Python wave |
| audio_mp3_format.c, audio_opus_format.c | mocks with no real encoding or decoding | new libmad/libopus calls and FFmpeg examples written |
| audio_alsa_device.c | only simulates device state | new real ALSA/tinyalsa API examples written |
| audio_vad_voice.c | a simple energy gate and gain, not a vendor VAD/Voice algorithm | new, clearly labeled energy state machine written; Voice is not disguised as an integration |
| audio_unisound_asr.c | a mock that cannot recognize speech | new SDK integration contract written; produces no fake text |
| business_json.c | string search, not a full JSON parser | new real cJSON example written |
| business_http.c | only builds a message, incomplete URL encoding, bound to a historical service address | new local HTTP, libcurl and REST examples written |
| logging / monitoring / own business protocols | confirmed deferred or merged items | old components not restored; general knowledge folded into the relevant technology pages |
| other technologies this round | no applicable component | written fresh for the handbook, classified by dependency and verification status |

## 2019Codes / SkEgn SDK scan

This round read `Coding_0001_HistoryTree/2019Codes/sdk_2.0.x_8_29`. SkEgn's C headers, its C/Java/Python/C#/LuaJIT demos and its Makefile provided evidence of actual calls and builds; the third-party Opus, cJSON, Mongoose and OpenSSL sources were only checked for dependency relationships and not copied into handbook examples. Credentials, provision files and service addresses in the historical demos are not used as documented configuration.

An earlier version once reused a thread component from the summary_components backup; it has since been rewritten as an independent example and no longer depends on or references that component.

## Verification scope

The [example list](../../examples/README_EN.md) separates run, compiled-only, missing-dependency and SDK integration contracts. Offline tests do not prove that external cloud services, devices, brokers or proprietary SDKs work. FIDL remains a syntax sketch.

## Old structure and backups

The S001–S010 category directories and the eight submodules have been moved out of the working tree. The snapshot taken before deletion is `../DevelopingManual-backups/before-handbook-20261021.tar.gz`, including uncommitted files; it is not a runtime dependency and is not distributed with the main repository.

The old submodule Git objects remain in the local `.git/modules`. To restore, combine the submodule commits in the main repository history with the snapshot; the `.git` inside the snapshot may be a local metadata pointer and cannot be guaranteed to clone on its own.

## 2021 scoped round and repository-wide reference review (2026-10-26)

- 9 pages added, up to Qt serial; MQTT/TCP updated; Qt SQL folded into SQLite. No visualization, report or HL7 pages were written.
- The currently available examples were checked: the handbook's independently written TCP / SDK contracts were reused; new Protobuf, SQLite, Qt JSON/UDP/threads/SQL/serial, TinyXML, libmosquitto and Paho Java examples were written. No historical project or backup source was copied.
- On the user's new requirement the existing body text was cleaned up: historical project descriptions were removed from Opus, VAD, HTTP and cJSON; SkEgn became a local contract with the historical C interface references deleted; pthread was rewritten as a new independent counter, with the old reused component and its header removed.
- The 2016/2019 records are kept; 2016 restored its original count of 31; the SkEgn addition of 2019 is archived separately. Historical paths are allowed only in scan / source-audit records; formal pages must not use them as source references.
- All teaching-code links in the handbook should resolve to examples inside DevelopingManual; official API / standard documents may be linked externally, and third-party development libraries may be installed dependencies. The check script rejects historical source paths and out-of-bounds local links in formal pages.
- Actual verification follows examples/README.md; development libraries, JDKs and vendor SDKs that are not installed are not falsely reported as passing. Old backups are not restored and not a build dependency.

## 2025Codes scan and new examples (2026-11-06)

- Subject: `Coding_0001_HistoryTree/2025Codes` (an ETC/VICS in-vehicle toll and traffic-information project that includes an Android vendor HAL). Read-only static scan: no program, build script or bundled Node/Chrome tool in the directory was run. Evidence and limits are in [2025Codes-scope.md](2025Codes-scope.md).
- Scope carried out: the recommended 9 new pages (WebSocket, zlib, JsonCpp, POSIX termios, Unix domain sockets, Lua embedding, JNI, Android AIDL, Android stable AIDL HAL) and 3 updates (the SQLite C API, Protobuf C++/proto2, and the Franca part of FIDL). The other 8 optional candidates were not written.
- Source decision: the historical project was used only to identify technologies; none of its code was copied, renamed and moved, or referenced. Every new example was written independently, and the protocol vectors come from the public standard (the RFC 6455 handshake key and masked-frame examples). The length-prefix framing in `unix_socket.py` follows the same idea as the existing `framed_tcp.py`, but the example is kept self-contained and they do not import each other.
- Run and verified: `websocket_minimal.py`, `unix_socket.py`, `zlib_demo.py`, `zlib_demo.c`, `termios_pty.c` and 23 unit tests. termios uses a pseudo-terminal and opens no real serial port; WebSocket only loops back to its own client and was not tested against a browser or another implementation.
- Not compiled: `jsoncpp_demo.cpp`, `lua_embed.c`, `sqlite_c_readonly.c`, `cpp_roundtrip.cpp` (development packages or protoc missing) and `java/jni/` (JDK missing); `android/aidl-service/` and `android/aidl-hal/` are only structure sketches because the Android SDK and AOSP are missing. These files were written from the official API documentation and have not been checked by a compiler, so build them before relying on them.
- Cleanup: formal pages contain no historical project paths; the check script rejects the 2016/2019/2021/2023/2025 scan directory names in formal pages.

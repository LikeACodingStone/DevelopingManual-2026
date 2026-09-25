# summary_components Architecture Overview

> Historical architecture snapshot. All source, headers, tests and Makefiles have moved to the S00 categories. See [MIGRATION](MIGRATION.md) for current paths and build commands.

This document summarizes the current three-module architecture, the code logic, and the technology stacks used by the new example interfaces and unit tests.

The new code does not replace the legacy projects. Its purpose is to organize the scattered legacy technical concepts into clearer, testable, and extensible C interface examples.

## 1. Overall Design

The project is now organized into three responsibility-based modules:

```text
summary_components
|-- core_engineering
|   |-- include
|   |-- source
|   `-- tests
|-- audio_speech_processing
|   |-- include
|   |-- source
|   `-- tests
`-- business_interaction
    |-- include
    |-- source
    `-- tests
```

The intended dependency direction is:

```text
core_engineering
    |
    | provides socket/thread/log/process helper interfaces
    v
audio_speech_processing
    |
    | provides PCM/WAV/MP3/Opus/ALSA/VAD/ASR style interfaces
    v
business_interaction
    |
    | provides packet protocol, HTTP request, and JSON command parsing
    v
speech client / speech server application
```

## 2. core_engineering

### 2.1 Directory Layout

```text
core_engineering
|-- include/core_interfaces.h
|-- source/core_socket_example.c
|-- source/core_thread_example.c
|-- source/core_log_example.c
|-- source/core_process_monitor_example.c
|-- tests/test_core_interfaces.c
`-- Makefile
```

### 2.2 Responsibility

- Wrap low-level C/Linux engineering concepts.
- Provide TCP and UDP socket interface examples.
- Provide a pthread mutex protected counter example.
- Provide log rotation decision helpers.
- Provide process monitor decision helpers.

### 2.3 Code Logic

```text
core_tcp_server_open()
    -> validate port
    -> socket()
    -> bind()
    -> listen()

core_thread_counter_add()
    -> pthread_mutex_lock()
    -> update shared value
    -> pthread_mutex_unlock()

core_log_need_rotate()
    -> compare current_size with max_size
    -> return rotate or keep

core_monitor_decide()
    -> current_count == 0        => start process
    -> current_count == expected => keep
    -> current_count > expected  => kill extra process
```

### 2.4 Notes

- The legacy code is mainly Linux/POSIX oriented.
- The current Windows/MinGW environment does not provide POSIX socket headers.
- `core_socket_example.c` therefore includes a `_WIN32` stub branch so that the unit tests can still compile and run in the current environment.

## 3. audio_speech_processing

### 3.1 Directory Layout

```text
audio_speech_processing
|-- include/audio_interfaces.h
|-- source/audio_pcm_format.c
|-- source/audio_wav_format.c
|-- source/audio_mp3_format.c
|-- source/audio_opus_format.c
|-- source/audio_alsa_device.c
|-- source/audio_vad_voice.c
|-- source/audio_unisound_asr.c
|-- tests/test_audio_interfaces.c
`-- Makefile
```

### 3.2 Responsibility

- Organize audio and speech processing technology stacks.
- Keep different audio format handling in different source files.
- Provide interface shapes and mock/stub implementations for external SDKs.

### 3.3 Audio Format Files

| File | Responsibility |
|---|---|
| `audio_pcm_format.c` | PCM byte calculation, 640-byte chunk splitting, 12-mic short-to-float conversion |
| `audio_wav_format.c` | WAV PCM header build and parse helpers |
| `audio_mp3_format.c` | MP3 decoder interface example with mock PCM output |
| `audio_opus_format.c` | Opus decoder interface example with mock PCM output |

### 3.4 Speech and Device Files

| File | Responsibility |
|---|---|
| `audio_alsa_device.c` | ALSA/tinyalsa record/play device state interface example |
| `audio_vad_voice.c` | VAD energy detector example and Voice processing mock |
| `audio_unisound_asr.c` | UniSound ASR lifecycle mock |

### 3.5 Code Logic

```text
audio_pcm_split_to_640()
    -> merge previous rest bytes
    -> emit full 640 byte chunks
    -> save remaining bytes for next feed

audio_wav_build_header()
    -> write RIFF/WAVE/fmt/data markers
    -> fill sample rate, channels, and bit depth
    -> calculate byte rate and block align

audio_opus_decode_mock()
    -> validate decoder state
    -> validate packet length
    -> produce deterministic PCM samples for tests

audio_vad_feed_pcm()
    -> calculate average absolute PCM energy
    -> energy >= start_score => speech
    -> low energy for enough frames => speech end

audio_unisound_*_example()
    -> initialize session
    -> start recognizer
    -> feed PCM bytes
    -> stop recognizer
    -> return mock result
```

### 3.6 Legacy Project Mapping

```text
ALSA/tinyalsa -> record audio from device
Voice SDK     -> process microphone array data
Huwen VAD     -> detect speech start/end
Opus          -> decode compressed network audio
PCM           -> final input to ASR
UniSound SDK  -> speech recognition
MP3/libmad    -> TTS/music playback decode
```

## 4. business_interaction

### 4.1 Directory Layout

```text
business_interaction
|-- include/business_interfaces.h
|-- source/business_protocol.c
|-- source/business_http.c
|-- source/business_json.c
|-- source/business_command.c
|-- tests/test_business_interfaces.c
`-- Makefile
```

### 4.2 Responsibility

- Organize business interaction technology stacks.
- Wrap the audio transfer packet protocol.
- Build HTTP request text.
- Provide lightweight JSON field extraction and command routing examples.

### 4.3 Code Logic

```text
business_protocol_pack()
    -> validate contType
    -> validate payload length
    -> copy payload into post_content

business_http_build_get()
    -> format HTTP GET request

business_http_build_post()
    -> format HTTP POST request with Content-Length

business_http_build_baidu_tts()
    -> encode text
    -> build Baidu text2audio GET request

business_json_get_string()
    -> find "key"
    -> find ':'
    -> copy string value

business_command_parse_json()
    -> detect resultMusic/songUrl => music play
    -> detect chat/chatAnswer     => TTS
    -> detect mediaPause          => pause
    -> detect mediaResume         => resume
    -> detect mediaStop           => stop
    -> detect volume command      => volume up/down
```

## 5. End-to-End Data Flow

The complete speech interaction path can be described as:

```text
Microphone
    -> ALSA/tinyalsa record
    -> Voice processing
    -> VAD speech detection
    -> PCM or Opus packet
    -> TCP post_content protocol
    -> UniSound ASR
    -> text result
    -> command server HTTP/TCP request
    -> JSON command response
    -> TTS/music/control action
    -> MP3 decode if needed
    -> ALSA/tinyalsa playback
```

The new modules map to this flow as follows:

```text
core_engineering:
    socket, thread, log, process monitor

audio_speech_processing:
    PCM, WAV, MP3, Opus, ALSA, VAD, Voice, UniSound ASR

business_interaction:
    post_content protocol, HTTP request, JSON parsing, command routing
```

## 6. Technology Stack Summary

| Category | Technology | Usage |
|---|---|---|
| Language | C / C++ | The legacy project is mostly C; the Baidu ASR example is C++ |
| Build | Makefile / gcc / Android NDK | Build Linux or Android ARM executables |
| System API | POSIX socket / pthread / file API | Network services, multithreading, log files, process monitoring |
| Network | TCP / UDP / HTTP | Audio transfer, command request, TTS/ASR request |
| Audio IO | ALSA / tinyalsa | Record and playback |
| Audio Format | PCM / WAV / MP3 / Opus | Recognition input, test files, TTS/music, compressed transfer |
| Codec | libopus / libmad | Opus decode and MP3 decode |
| Speech SDK | UniSound libusc.so | Main speech recognition SDK |
| Speech Preprocess | Voice SDK / Huwen VAD | Microphone array processing and speech activity detection |
| JSON | cJSON-style parsing | Parse command server responses |
| Test | Lightweight C unit tests | Run without a third-party test framework |

## 7. Unit Tests

Each module has one test entry:

```text
core_engineering/tests/test_core_interfaces.c
audio_speech_processing/tests/test_audio_interfaces.c
business_interaction/tests/test_business_interfaces.c
```

If `make` is available, run:

```sh
cd core_engineering
make run

cd ../audio_speech_processing
make run

cd ../business_interaction
make run
```

The current machine does not have `make`, so verification was done by compiling with `gcc` directly and running the test executables from a local temporary directory.

Test results:

```text
core_engineering tests passed
audio_speech_processing tests passed
business_interaction tests passed
```

## 8. Design Notes

- The new code focuses on interface examples and unit tests.
- External libraries such as UniSound, Opus, ALSA, curl, and libmad are not linked directly in the new tests.
- External dependencies are represented by small mock/stub interfaces so the code can compile without the original SDKs.
- `audio_speech_processing` keeps different audio format handling in separate source files.
- `business_interaction` uses lightweight JSON extraction for examples only; production code should use cJSON or another structured JSON parser.
- `core_engineering` keeps Linux/POSIX socket style to match the legacy code; Windows builds use stubs for testability.

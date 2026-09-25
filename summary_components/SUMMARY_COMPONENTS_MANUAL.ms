.nr HM 0.65i
.nr FM 0.55i
.nr PO 0.75i
.nr LL 7.0i
.nr PS 10
.nr VS 12
.ds CH ""
.ds CF "summary_components Module Manual - Page \\n%"
.TL
summary_components Module Manual
.AU
MyCodingRiver_2016_2026
.AI
Generated: 2026-08-18
.AB no
This manual explains the purpose, structure, interfaces, build flow, and expected integration pattern of the
summary_components folder. The code is organized as a testable C component summary for a speech interaction
pipeline. It is not a complete production speech client or server; it is a clean reference layer that captures
legacy system concepts behind small interfaces and unit tests.
.AE
.NH 1
Purpose
.PP
The summary_components folder groups old speech-client and speech-server engineering ideas into three clear C
modules:
.IP "\(bu" 2
core_engineering: low-level Linux/C helpers.
.IP "\(bu" 2
audio_speech_processing: audio format, device, VAD, voice, and ASR interface examples.
.IP "\(bu" 2
business_interaction: packet protocol, HTTP request generation, JSON extraction, and command routing examples.
.PP
The practical function of this folder is to provide a readable and testable map of a voice assistant style
system:
.DS L
Microphone
  -> ALSA/tinyalsa record
  -> voice preprocessing
  -> VAD speech detection
  -> PCM or Opus packet
  -> TCP post_content protocol
  -> UniSound ASR
  -> text result
  -> command server HTTP/TCP request
  -> JSON command response
  -> TTS / music / media control action
  -> MP3/audio playback
.DE
.NH 1
Directory Layout
.PP
The folder layout is intentionally responsibility-based:
.DS L
summary_components
|-- ARCHITECTURE_OVERVIEW.md
|-- core_engineering
|   |-- include/core_interfaces.h
|   |-- source
|   |-- tests/test_core_interfaces.c
|   `-- Makefile
|-- audio_speech_processing
|   |-- include/audio_interfaces.h
|   |-- source
|   |-- tests/test_audio_interfaces.c
|   `-- Makefile
`-- business_interaction
    |-- include/business_interfaces.h
    |-- source
    |-- tests/test_business_interfaces.c
    `-- Makefile
.DE
.PP
The intended dependency direction is:
.DS L
core_engineering
  -> audio_speech_processing
  -> business_interaction
  -> speech client / speech server application
.DE
.PP
The modules are currently independent for testing. The dependency direction documents the intended application
architecture, not a strict linker dependency in the current examples.
.NH 1
Build and Test
.PP
Each module has its own Makefile. Build and run each test binary from the module directory:
.DS L
cd core_engineering
make run

cd ../audio_speech_processing
make run

cd ../business_interaction
make run
.DE
.PP
The tests use simple C assertions implemented inside the test source files. No third-party C test framework is
required.
.PP
Expected success messages:
.DS L
core_engineering tests passed
audio_speech_processing tests passed
business_interaction tests passed
.DE
.NH 1
General Coding Conventions
.PP
All three modules use a small C-style status convention:
.IP "\(bu" 2
Success is zero: CORE_OK, AUDIO_OK, or BUSINESS_OK.
.IP "\(bu" 2
Failure is negative one: CORE_ERROR, AUDIO_ERROR, or BUSINESS_ERROR.
.IP "\(bu" 2
Most functions validate pointers and sizes before using caller-provided data.
.IP "\(bu" 2
External systems are wrapped by small interfaces, and several are implemented as mocks for testability.
.PP
The code follows an old-server compatible style: plain C structs, explicit buffer sizes, direct return codes,
and dependency-free test programs.
.NH 1
core_engineering Module
.NH 2
Responsibility
.PP
The core_engineering module captures low-level system utilities that a speech server or client normally needs:
.IP "\(bu" 2
TCP server socket setup, accept, send-all, and close.
.IP "\(bu" 2
UDP server socket setup.
.IP "\(bu" 2
pthread mutex protected counter.
.IP "\(bu" 2
Log rotation decision helpers.
.IP "\(bu" 2
Process monitor decision helpers.
.NH 2
Files
.DS L
core_engineering/include/core_interfaces.h
core_engineering/source/core_socket_example.c
core_engineering/source/core_thread_example.c
core_engineering/source/core_log_example.c
core_engineering/source/core_process_monitor_example.c
core_engineering/tests/test_core_interfaces.c
.DE
.NH 2
Main Data Structures
.IP "struct core_tcp_server" 4
Stores a TCP socket file descriptor, bound port, and listen backlog.
.IP "struct core_udp_server" 4
Stores a UDP socket file descriptor and bound port.
.IP "struct core_thread_counter" 4
Stores a pthread mutex and an integer counter protected by that mutex.
.IP "struct core_log_config" 4
Stores log file name, log path, max size, and number of backups to retain.
.IP "struct core_monitor_status" 4
Stores expected and current process counts for monitor decisions.
.NH 2
API Reference
.IP "core_is_valid_port(port)" 4
Returns nonzero when the port is in the valid explicit TCP/UDP range, 1 through 65535.
.IP "core_tcp_server_open(server, port)" 4
Validates the port, creates a TCP socket, binds to the port, and starts listen with CORE_TCP_BACKLOG.
.IP "core_tcp_server_accept(server)" 4
Accepts one TCP client from an opened server socket and returns the client file descriptor.
.IP "core_tcp_send_all(fd, buffer, length)" 4
Sends all requested bytes to a connected TCP peer. Returns CORE_OK on success.
.IP "core_socket_close(fd_pointer)" 4
Closes a valid socket descriptor and resets it to an invalid value.
.IP "core_udp_server_open(server, port)" 4
Validates the port, creates a UDP socket, and binds it to the requested port.
.IP "core_thread_counter_init(counter)" 4
Initializes the mutex and sets the counter value to zero.
.IP "core_thread_counter_add(counter, delta)" 4
Locks the mutex, adds delta, unlocks the mutex, and returns CORE_OK on success.
.IP "core_thread_counter_get(counter)" 4
Reads the counter value with mutex protection.
.IP "core_thread_counter_destroy(counter)" 4
Destroys the counter mutex.
.IP "core_log_need_rotate(config, current_size)" 4
Returns one when current_size is greater than or equal to config->max_size. Returns zero when rotation is not
needed.
.IP "core_log_format_backup_name(config, index, out, out_size)" 4
Formats a backup log name using the configured path and file name, for example:
.DS L
logSystem/Server_Runing.log~3.log
.DE
.IP "core_monitor_decide(status)" 4
Returns CORE_MONITOR_START when current_count is zero, CORE_MONITOR_KEEP when current_count equals
expect_count, and CORE_MONITOR_KILL_EXTRA when current_count is greater than expect_count.
.NH 2
Implementation Notes
.PP
The socket code is Linux/POSIX oriented. The source includes a Windows stub branch so interface tests can still
compile in environments that do not provide POSIX socket headers.
.PP
This module is suitable as a reference for server infrastructure behavior, but production code should add
nonblocking I/O handling, timeout strategy, structured logging, and real process discovery.
.NH 1
audio_speech_processing Module
.NH 2
Responsibility
.PP
The audio_speech_processing module captures the audio and speech processing stack behind small C interfaces:
.IP "\(bu" 2
PCM byte calculations and frame splitting.
.IP "\(bu" 2
WAV PCM header build and parse helpers.
.IP "\(bu" 2
MP3 and Opus decoder interface examples.
.IP "\(bu" 2
ALSA/tinyalsa device state interface example.
.IP "\(bu" 2
Energy-based VAD example.
.IP "\(bu" 2
Voice processing mock.
.IP "\(bu" 2
UniSound ASR session lifecycle mock.
.NH 2
Files
.DS L
audio_speech_processing/include/audio_interfaces.h
audio_speech_processing/source/audio_pcm_format.c
audio_speech_processing/source/audio_wav_format.c
audio_speech_processing/source/audio_mp3_format.c
audio_speech_processing/source/audio_opus_format.c
audio_speech_processing/source/audio_alsa_device.c
audio_speech_processing/source/audio_vad_voice.c
audio_speech_processing/source/audio_unisound_asr.c
audio_speech_processing/tests/test_audio_interfaces.c
.DE
.NH 2
Main Data Structures
.IP "struct audio_pcm_format" 4
Describes sample rate, channel count, and bits per sample.
.IP "struct audio_pcm_split_state" 4
Stores remaining bytes that did not fill a complete 640-byte UniSound feed chunk.
.IP "struct audio_wav_header" 4
Models a basic 44-byte PCM WAV header.
.IP "struct audio_mp3_decoder" 4
Stores mock MP3 decoder state, sample rate, and channels.
.IP "struct audio_opus_decoder" 4
Stores mock Opus decoder state, sample rate, and channels.
.IP "struct audio_alsa_device" 4
Stores mock ALSA device name, mode, PCM format, and started state.
.IP "struct audio_vad_state" 4
Stores speech active state, start and end thresholds, silence frame limit, and current silence count.
.IP "struct audio_unisound_session" 4
Stores mock UniSound session state, credentials, fed byte count, and recognition result.
.NH 2
API Reference
.IP "audio_pcm_bytes_per_sample(format)" 4
Returns the byte width for one PCM sample in one channel. For 16-bit PCM this returns 2.
.IP "audio_pcm_frame_bytes(format, sample_count)" 4
Returns sample_count * channels * bytes_per_sample.
.IP "audio_pcm_split_to_640(state, input, input_length, chunk_func, user_data)" 4
Combines previous rest bytes with new input, emits full 640-byte chunks through the callback, and stores trailing
bytes for the next call. This matches the legacy UniSound feed pattern.
.IP "audio_pcm_12mic_to_float(input, voice_out, aec_out, mic_count, sample_count)" 4
Converts interleaved 12-microphone short samples into normalized float buffers for voice and AEC style
processing.
.IP "audio_wav_build_header(header, format, pcm_bytes)" 4
Builds a basic RIFF/WAVE PCM header and calculates byte rate, block align, file size, and data size.
.IP "audio_wav_parse_format(header, format, pcm_bytes)" 4
Validates a basic WAV PCM header and extracts sample rate, channels, bit depth, and PCM byte count.
.IP "audio_mp3_decoder_open(decoder, sample_rate, channels)" 4
Initializes a mock MP3 decoder state.
.IP "audio_mp3_decode_mock(decoder, mp3_data, mp3_length, pcm_out, pcm_capacity)" 4
Validates input and writes deterministic mock PCM samples. It does not call libmad or another real MP3 decoder.
.IP "audio_mp3_decoder_close(decoder)" 4
Clears mock MP3 decoder state.
.IP "audio_opus_decoder_open(decoder, sample_rate, channels)" 4
Initializes a mock Opus decoder state.
.IP "audio_opus_decode_mock(decoder, packet, packet_length, pcm_out, max_samples)" 4
Validates input and writes deterministic mock PCM samples. It does not call libopus.
.IP "audio_opus_decoder_close(decoder)" 4
Clears mock Opus decoder state.
.IP "audio_alsa_open_example(device, device_name, mode, format)" 4
Initializes mock ALSA/tinyalsa device state for record or playback mode.
.IP "audio_alsa_start_example(device)" 4
Marks the mock device as started.
.IP "audio_alsa_stop_example(device)" 4
Marks the mock device as stopped.
.IP "audio_vad_init(state, start_score, end_score, end_frame_count)" 4
Initializes the energy-based VAD state.
.IP "audio_vad_feed_pcm(state, pcm, sample_count)" 4
Computes average absolute PCM energy. Returns silence, speech, or end-of-speech according to configured
thresholds.
.IP "audio_voice_process_mock(input, output, sample_count, gain)" 4
Converts normalized float samples to 16-bit PCM with gain and clipping.
.IP "audio_unisound_init_example(session, app_key, secret_key)" 4
Initializes a mock UniSound ASR session and stores credentials in the session object.
.IP "audio_unisound_start_example(session)" 4
Marks the mock recognizer as started.
.IP "audio_unisound_feed_example(session, pcm, pcm_length)" 4
Adds PCM bytes to the mock recognizer input count.
.IP "audio_unisound_stop_example(session)" 4
Stops the mock recognizer and produces a deterministic mock recognition result.
.IP "audio_unisound_get_result_example(session)" 4
Returns the mock recognition result string.
.NH 2
Audio Stack Mapping
.PP
The module maps legacy technology names into isolated interfaces:
.DS L
ALSA/tinyalsa -> record and playback device layer
Voice SDK     -> microphone array preprocessing
Huwen VAD     -> speech start/end detection
Opus          -> compressed network audio
PCM           -> recognition input format
UniSound SDK  -> ASR recognition
MP3/libmad    -> TTS or music playback decode
.DE
.NH 2
Implementation Notes
.PP
This module deliberately avoids linking real external audio libraries in the tests. The mock interfaces allow
the code to compile and verify lifecycle, buffer, and routing logic without SDK or hardware dependencies.
.PP
Production replacement points are clear: replace the mock MP3, Opus, ALSA, Voice, VAD, and UniSound
implementations with adapters around the real libraries while preserving the public interface shape where useful.
.NH 1
business_interaction Module
.NH 2
Responsibility
.PP
The business_interaction module captures the network and command layer:
.IP "\(bu" 2
Binary post_content packet packing, unpacking, and validation.
.IP "\(bu" 2
HTTP GET and POST request text builders.
.IP "\(bu" 2
Baidu TTS style HTTP request generation.
.IP "\(bu" 2
Lightweight JSON string extraction.
.IP "\(bu" 2
Command JSON routing to media, TTS, music, and volume actions.
.NH 2
Files
.DS L
business_interaction/include/business_interfaces.h
business_interaction/source/business_protocol.c
business_interaction/source/business_http.c
business_interaction/source/business_json.c
business_interaction/source/business_command.c
business_interaction/tests/test_business_interfaces.c
.DE
.NH 2
Main Data Structures
.IP "struct business_post_content" 4
Represents the binary packet exchanged between client and speech server. It contains contType, contLength, and a
fixed 2048-byte payload buffer.
.IP "struct business_http_request" 4
Stores host, port, and generated HTTP request text.
.IP "struct business_command_result" 4
Stores parsed command action, text payload, and optional media URL.
.NH 2
API Reference
.IP "business_protocol_pack(packet, cont_type, payload, payload_length)" 4
Validates packet type and length, clears the packet, stores type and length, and copies payload bytes.
.IP "business_protocol_unpack(packet, cont_type, out, out_size)" 4
Validates the packet and copies payload bytes to the caller buffer. Returns copied payload length.
.IP "business_protocol_validate(packet)" 4
Checks that packet type is start, data, or stop and that payload length fits the fixed buffer.
.IP "business_http_build_get(request, host, path)" 4
Builds a simple HTTP/1.0 GET request string.
.IP "business_http_build_post(request, host, path, body)" 4
Builds a simple HTTP/1.0 POST request string with Content-Length.
.IP "business_http_build_baidu_tts(request, text)" 4
URL-encodes text for the supported subset and builds a Baidu text2audio style GET request.
.IP "business_json_get_string(json, key, out, out_size)" 4
Extracts a simple JSON string value by key using lightweight string scanning.
.IP "business_json_has_token(json, token)" 4
Returns nonzero when the JSON text contains the requested token.
.IP "business_command_parse_json(json, result)" 4
Routes recognized JSON snippets to one of the BUSINESS_ACTION values.
.NH 2
Command Routing
.PP
The command parser maps response content to action constants:
.DS L
resultMusic or songUrl       -> BUSINESS_ACTION_MUSIC_PLAY
"cmdType":"chat" or chatAnswer -> BUSINESS_ACTION_CHAT_TTS
mediaPause                   -> BUSINESS_ACTION_MEDIA_PAUSE
mediaResume                  -> BUSINESS_ACTION_MEDIA_RESUME
mediaStop                    -> BUSINESS_ACTION_MEDIA_STOP
mediaVolumeIncrease          -> BUSINESS_ACTION_VOLUME_UP
mediaVolumeDecrease          -> BUSINESS_ACTION_VOLUME_DOWN
unknown command              -> BUSINESS_ACTION_NONE
.DE
.NH 2
Implementation Notes
.PP
The JSON extraction is intentionally lightweight. It is suitable for small examples and deterministic unit tests,
but production code should use a real JSON parser such as cJSON or another structured parser. A real parser is
needed for escaped characters, nested objects, arrays, numbers, booleans, null values, malformed input handling,
and security hardening.
.NH 1
End-to-End Integration Pattern
.PP
A complete application built on the concepts in this folder would normally connect the modules in this sequence:
.DS L
1. Start infrastructure:
   - configure logging
   - start process monitor
   - open TCP or UDP server/client sockets

2. Start audio path:
   - open ALSA/tinyalsa record device
   - initialize voice processing and VAD
   - initialize ASR session

3. Capture and detect speech:
   - read PCM frames from microphone
   - convert microphone array samples if needed
   - feed VAD
   - begin packet transfer when speech starts

4. Transfer recognition audio:
   - split PCM into required chunk sizes
   - pack start/data/stop packets
   - send packets over TCP

5. Recognize and route text:
   - feed PCM into ASR
   - stop ASR and read recognized text
   - send text to command server
   - parse JSON response

6. Execute response:
   - chat answer -> TTS
   - music result -> play URL
   - media control -> pause/resume/stop
   - volume command -> adjust output volume

7. Playback:
   - decode MP3 or other stream when needed
   - send PCM to ALSA/tinyalsa playback device
.DE
.NH 1
Example Pseudocode
.PP
The following pseudocode shows how the interface concepts fit together. It is not a complete source file.
.DS L
struct audio_vad_state vad;
struct audio_unisound_session asr;
struct business_post_content packet;
struct business_command_result command;

audio_vad_init(&vad, 0.10f, 0.04f, 3);
audio_unisound_init_example(&asr, "app-key", "secret-key");
audio_unisound_start_example(&asr);

while (recording) {
    read_pcm_frame(pcm, sample_count);

    vad_state = audio_vad_feed_pcm(&vad, pcm, sample_count);
    if (vad_state == AUDIO_VAD_SPEECH) {
        business_protocol_pack(&packet,
                               BUSINESS_CONT_DATA,
                               (const char *)pcm,
                               pcm_bytes);
        send_packet(packet);
        audio_unisound_feed_example(&asr, (const char *)pcm, pcm_bytes);
    }

    if (vad_state == AUDIO_VAD_END) {
        audio_unisound_stop_example(&asr);
        text = audio_unisound_get_result_example(&asr);
        json = request_command_server(text);
        business_command_parse_json(json, &command);
        execute_command(command);
        break;
    }
}
.DE
.NH 1
Known Limitations
.PP
This folder is useful as a component summary and test harness, but it should not be treated as production-ready
without additional work.
.IP "\(bu" 2
The audio SDK integrations are mocks or examples, not real hardware/codec/ASR integrations.
.IP "\(bu" 2
The JSON parser is string-scanning only and is not safe for general JSON input.
.IP "\(bu" 2
HTTP request builders generate request text but do not implement a complete HTTP client.
.IP "\(bu" 2
Socket helpers are basic blocking examples.
.IP "\(bu" 2
Fixed-size buffers simplify tests but require careful bounds management in production.
.IP "\(bu" 2
The manual protocol uses simple integer fields and does not define byte order, framing across architectures, or
version negotiation.
.IP "\(bu" 2
Security features such as TLS, authentication, input sanitization, and robust error recovery are out of scope.
.NH 1
Recommended Production Hardening
.PP
If this component model is promoted into a real product, prioritize the following changes:
.IP "1." 4
Replace mock SDK code with adapters around the real ALSA/tinyalsa, Opus, MP3, Voice/VAD, and UniSound APIs.
.IP "2." 4
Replace lightweight JSON scanning with a structured parser.
.IP "3." 4
Define a stable wire protocol: byte order, packet framing, version, checksum or length validation, and error
responses.
.IP "4." 4
Add timeout, retry, reconnect, and partial-read/partial-write handling for network code.
.IP "5." 4
Add structured logs and real log rotation.
.IP "6." 4
Move secrets such as ASR app keys out of source and into secure configuration.
.IP "7." 4
Add integration tests with real or simulated audio streams.
.IP "8." 4
Add sanitizers, static analysis, and CI build targets for the supported platforms.
.NH 1
Quick Reference
.PP
Module responsibility summary:
.DS L
core_engineering
  socket, thread, log, process monitor

audio_speech_processing
  PCM, WAV, MP3, Opus, ALSA, VAD, Voice, UniSound ASR

business_interaction
  post_content protocol, HTTP request, JSON parsing, command routing
.DE
.PP
Common constants:
.DS L
CORE_OK / AUDIO_OK / BUSINESS_OK       = 0
CORE_ERROR / AUDIO_ERROR / BUSINESS_ERROR = -1
AUDIO_UNISOUND_CHUNK                   = 640
AUDIO_PCM_BLOCK                        = 2048
BUSINESS_POST_BUFF                     = 2048
BUSINESS_CONT_START                    = 1
BUSINESS_CONT_DATA                     = 2
BUSINESS_CONT_STOP                     = 3
.DE
.NH 1
Maintenance Notes
.PP
Keep headers as the public contract for each module. When changing behavior, update the relevant interface
header, source implementation, unit test, architecture overview, and this manual together.

# WebSocket: Handshake, Frames and Close

- Aliases and ecosystem: WebSocket / RFC 6455; a common C++ library is websocketpp (depends on Asio)
- Versions and platforms: RFC 6455 (protocol version 13); the example uses only the Python 3 standard library, loopback only
- Tags: network
- Example status: the Python standard-library implementation has been run and verified (handshake, frames, masking, fragmentation, ping/pong, close and rejection paths); the websocketpp notes are syntax descriptions only and were not compiled
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

WebSocket starts with one HTTP/1.1 `Upgrade` handshake and then exchanges "frames" in both directions over the same TCP (or TLS) connection. Frames carry their own length, so you do not have to handle message boundaries yourself. The opcode gives the frame type: text, binary, continuation, close, ping, pong.

- Frames sent by a client MUST be masked; frames sent by a server MUST NOT be masked.
- `ws://` is unencrypted; `wss://` is WebSocket over TLS.
- The protocol defines frames, not message content; JSON, Protobuf and similar formats are an application decision.

## When to use

Server push, low-latency two-way messaging, and channels that browsers can connect to directly. Strict request/response fits [HTTP](../../network/http.md) better (Chinese only); processes on the same machine can consider [Unix domain sockets](../programming/unix-domain-socket.md); large file transfer is not its strength.

## How to use

1. Handshake: the client sends `GET` with `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key` (Base64 of 16 random bytes) and `Sec-WebSocket-Version: 13`. The server validates the request and answers `101`; `Sec-WebSocket-Accept` is `Base64(SHA1(Key + fixed GUID))`. A failed validation gets `400`.
2. Frame header: the FIN bit, RSV1–3 (must be 0 when no extension is negotiated), the opcode, the MASK bit, a 7-bit length (126 means a 16-bit length follows, 127 means a 64-bit length follows), the masking key (client frames only) and the payload.
3. Fragmentation: the first frame has a text/binary opcode and FIN=0, later frames are continuation, and the last frame has FIN=1. Control frames may be interleaved between fragments but cannot be fragmented and are at most 125 bytes.
4. Close: one side sends a close frame (optionally with a 2-byte status code, such as 1000 normal, 1002 protocol error, 1007 invalid data, 1009 message too big); the peer answers with close, and only then is the TCP connection closed.
5. Validation: text messages must be UTF-8; check the length limit before reading the payload; set read timeouts and use ping/pong as keep-alive; in browser scenarios check `Origin`.
6. In C++, websocketpp is a common server library: create `websocketpp::server<websocketpp::config::asio>`, set open/close/message handlers, then call `init_asio()`, `listen()`, `start_accept()` and `run()`. It depends on Asio (Boost.Asio or standalone Asio), so it is not a dependency-free header-only library.

## Minimal example

Run the commands from the handbook root.

[websocket_minimal.py](../../../examples/python/websocket_minimal.py) uses only the standard library and, on the loopback address, completes a handshake, a text echo, ping/pong, fragment reassembly and the close handshake. The [test file](../../../examples/python/test_ipc_examples.py) contains the `Sec-WebSocket-Accept` and masked-frame vectors from RFC 6455 and these rejection paths: unmasked client frame, masked server frame, reserved bits, over-long or fragmented control frames, an oversize payload (rejected from the header alone), invalid UTF-8, a continuation without a start frame, and a handshake with a missing key or wrong version.

```sh
python3 examples/python/websocket_minimal.py
python3 -m unittest discover -s examples/python -p 'test_ipc_*.py'
```

Expected: `WebSocket handshake, framing, ping and close OK`, and all tests pass. Run on Linux x86_64 with Python 3.12.3. The example has no TLS, subprotocols, extensions, backpressure or concurrent-write protection and must not be treated as a production server.

## FAQ

- One `recv` is not one frame: read exactly as many bytes as the header says; see TCP framing ([Chinese only](../../network/tcp-framing.md)).
- A server must close the connection when it receives an unmasked frame; a client must abandon the connection if the response's `Sec-WebSocket-Accept` does not match.
- Reverse proxies and load balancers must be told to forward `Upgrade`, and idle timeouts matter; use ping to keep the connection alive.
- After negotiating permessage-deflate, limit the decompressed size; see [zlib](zlib.md).
- Masking exists to keep intermediaries' caches from being misled; it is not encryption. Use `wss://` for confidentiality.
- Check websocketpp's version and maintenance status yourself; its snippet on this page was not compiled.

## References

- [RFC 6455: The WebSocket Protocol](https://www.rfc-editor.org/rfc/rfc6455)
- [MDN: WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [websocketpp](https://github.com/zaphoyd/websocketpp)
- [Example verification scope](../../../examples/README_EN.md)

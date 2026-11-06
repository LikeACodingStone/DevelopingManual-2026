# zlib and DEFLATE Compression

- Aliases and ecosystem: zlib / DEFLATE (RFC 1951) / gzip (RFC 1952); the C library and Python's `zlib` module
- Versions and platforms: zlib 1.x C API; Python 3 standard library; verified on local Linux
- Tags: network
- Example status: both the Python and C examples have been run and verified, including the failure paths for corrupted, truncated, over-limit and wrong-wrapper input
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

DEFLATE is a lossless compression algorithm. The zlib library implements it and offers three outer wrappers; the algorithm is the same but the header and trailer differ:

| Wrapper | Header | Check | Python wbits |
| --- | --- | --- | --- |
| zlib (RFC 1950) | 2 bytes, commonly `78 ..` | Adler-32 | `15` |
| gzip (RFC 1952) | at least 10 bytes, starts with `1f 8b` | CRC-32 | `31` |
| raw deflate | none | none | `-15` |

zlib is neither encryption nor an archive format: it has no file names or directories; zip and tar are a different kind of technology.

## When to use

Log and message compression, HTTP `Content-Encoding`, and the compressed streams inside formats such as PNG. Data that is already compressed (JPEG, MP3, video) usually does not shrink; for very short messages the gain is small and the latency and CPU cost stand out.

## How to use

1. Choose the wrapper: agree with the peer on zlib, gzip or raw. In Python the `wbits` used to decompress must match (`32 + 15` auto-detects zlib/gzip).
2. One-shot API: in C use `compress2()` / `uncompress()` and size the destination with `compressBound()`; decompression needs a known or limited output size.
3. Streaming API: `deflateInit` → loop `deflate` → `deflateEnd`; `inflateInit` → loop `inflate` → `inflateEnd`. Flush modes: `Z_NO_FLUSH`, `Z_SYNC_FLUSH` (makes everything written so far decodable) and `Z_FINISH` (ends the stream).
4. Read the return codes: `Z_STREAM_END` means the stream ended completely; `Z_OK` and `Z_BUF_ERROR` in a streaming loop usually mean "more input or output space is needed", not a fatal error; `Z_DATA_ERROR` means corrupted data or a wrapper mismatch; `Z_MEM_ERROR` means out of memory.
5. When decompressing, limit the output size, confirm that the stream really ended (`Z_STREAM_END` in C, `decompressobj().eof` in Python), and check for extra trailing data.
6. If compression does not make the data smaller, keep the original and tell the receiver with a flag.

## Minimal example

Run the commands from the handbook root.

The [Python example](../../../examples/python/zlib_demo.py) shows the headers of the three wrappers, the matching `wbits`, rejection of corrupted/truncated/over-limit/trailing data, the fallback for incompressible data, and `Z_SYNC_FLUSH`. The [C example](../../../examples/native/zlib_demo.c) shows `compress2` / `uncompress`, a streaming `deflate` loop with a 64-byte output chunk, a limited `inflate`, and truncated and corrupted input.

```sh
python3 examples/python/zlib_demo.py
cc -std=c11 -Wall -Wextra -Werror examples/native/zlib_demo.c -lz -o /tmp/zlib-demo
/tmp/zlib-demo
```

Expected output, in order: `zlib formats, limits and corruption checks OK` and `zlib C round trip OK`. Run on Linux x86_64, gcc 13.3, Python 3.12.3. The [tests](../../../examples/python/test_ipc_examples.py) additionally cover a decompression bomb of 10 million zero bytes being rejected by a 1 MiB limit.

## FAQ

- A streaming `deflate(Z_FINISH)` is only complete when it returns `Z_STREAM_END`; on `Z_OK` or `Z_BUF_ERROR`, supply a fresh output buffer and call again.
- Small, highly repetitive input can decompress to a huge output (a decompression bomb): always limit the output and never trust a size declared by the peer.
- If you compress and then encrypt, and the compressed content mixes a secret with attacker-controlled data, the compressed length leaks information (the CRIME/BREACH class of problems).
- Do not use one `z_stream` from several threads at the same time.
- Different implementations (such as zlib-ng) may produce different compressed bytes, but each should decompress the other's output; do not use compressed bytes for stable hashing or comparison.
- zlib does not restrict trailing data after the end of the stream; whether it is allowed is up to the protocol above it. The examples on this page choose to reject it.

## References

- [zlib manual](https://www.zlib.net/manual.html)
- [RFC 1950 zlib](https://www.rfc-editor.org/rfc/rfc1950), [RFC 1951 DEFLATE](https://www.rfc-editor.org/rfc/rfc1951), [RFC 1952 gzip](https://www.rfc-editor.org/rfc/rfc1952)
- [Python zlib](https://docs.python.org/3/library/zlib.html)
- [Example verification scope](../../../examples/README_EN.md)

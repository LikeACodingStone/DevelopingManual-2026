# Unix Domain Sockets (AF_UNIX)

- Aliases and ecosystem: Unix domain socket / local socket / `AF_UNIX`; in C++ it is `boost::asio::local::stream_protocol`
- Versions and platforms: POSIX / Linux; the example uses the Python 3 standard library, and `SO_PEERCRED` is Linux-only
- Tags: programming
- Example status: the Python example has been run and verified, including failure paths; the Boost.Asio form is a syntax description only and was not compiled
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

A Unix domain socket is a socket for communication between processes on the same host. It uses a file-system path (Linux also supports abstract names that begin with `\0`) as the address, and the types are `SOCK_STREAM`, `SOCK_DGRAM` and `SOCK_SEQPACKET`. Compared with TCP loopback: it bypasses the network protocol stack, access control comes from the permissions of the socket file, it can report the peer process's credentials (`SO_PEERCRED`, Linux), and it can pass file descriptors with `SCM_RIGHTS`.

## When to use

Control interfaces of local daemons and cooperation between processes on one machine. Use TCP across hosts, and [WebSocket](../network/websocket.md) when a browser must connect. AF_UNIX support on Windows differs semantically from Linux and is not verified here.

## How to use

1. Put the socket in a private directory (mode `0700`) and keep the path short: `sun_path` has only about 108 bytes.
2. Server: `bind` → `chmod` (for example `0600`) → `listen` → `accept`.
3. Leftover files: after a crash the path may still hold a file, and `bind` fails with `EADDRINUSE`. Try `connect` first: only a refusal (`ECONNREFUSED`) shows nobody is listening, and only then `unlink` and bind again; if the connect succeeds, a process is serving and you should report an error rather than take the path.
4. `SOCK_STREAM` is a byte stream with no message boundaries: use a length prefix and check the limit before reading the content; see TCP framing ([Chinese only](../../network/tcp-framing.md)).
5. Optional identity check: read `SO_PEERCRED` to get the peer's pid/uid/gid and compare it with the expected user.
6. On exit, close the socket and delete the file.
7. Boost.Asio form: `boost::asio::local::stream_protocol::acceptor` and `::endpoint`; you usually need to `unlink` the old file before constructing the acceptor, and the acceptor does not delete the file for you on destruction.

## Minimal example

Run the commands from the handbook root.

[unix_socket.py](../../../examples/python/unix_socket.py) creates a socket in a private temporary directory: it first leaves a stale file and verifies that it is replaced, sets mode `0600`, has a client send a length-prefixed message, has the server verify the peer uid and return an upper-cased echo, and finally cleans up the directory. The [tests](../../../examples/python/test_ipc_examples.py) cover: a length header above the limit is refused (the body is not read), a truncated message, not taking over the path while a live listener exists, and a path that is too long.

```sh
python3 examples/python/unix_socket.py
python3 -m unittest discover -s examples/python -p 'test_ipc_*.py'
```

Expected: `Unix domain socket framed echo OK`, and all tests pass. Run on Linux x86_64 with Python 3.12.3.

## FAQ

- `Address already in use`: a leftover file or another listening process holds the path; tell them apart as in step 3.
- `AF_UNIX path too long`: shorten the directory name; the example uses `tempfile.mkdtemp()` to get a short path.
- A socket in a world-writable directory (such as `/tmp`) can have its path taken first by someone else; use a private subdirectory and, if needed, check the peer uid.
- Linux abstract-namespace sockets have no file permissions; access control can only come from checks such as `SO_PEERCRED`.
- One `recv` is not one message; when the peer closes, `recv` returns 0 bytes.
- Writing to a closed peer raises `EPIPE` and, by default, also delivers `SIGPIPE`.

## References

- [Linux unix(7)](https://man7.org/linux/man-pages/man7/unix.7.html)
- [Python socket](https://docs.python.org/3/library/socket.html)
- [Boost.Asio local sockets](https://www.boost.org/doc/libs/release/doc/html/boost_asio/reference/local__stream_protocol.html)
- [Example verification scope](../../../examples/README_EN.md)

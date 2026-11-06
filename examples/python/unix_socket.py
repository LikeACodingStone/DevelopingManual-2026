"""Unix domain stream socket with length-prefixed messages (Linux/POSIX, local only).

Covers: private socket directory, stale socket file handling, peer credentials,
message framing with a size limit, and cleanup. Run: python3 examples/python/unix_socket.py
"""
import errno
import os
import shutil
import socket
import stat
import struct
import tempfile
import threading

LIMIT = 64 * 1024


def receive_exact(sock, count):
    data = bytearray()
    while len(data) < count:
        part = sock.recv(count - len(data))
        if not part:
            raise EOFError('peer closed before complete message')
        data.extend(part)
    return bytes(data)


def send_message(sock, data):
    if len(data) > LIMIT:
        raise ValueError('message too large')
    sock.sendall(struct.pack('!I', len(data)) + data)


def receive_message(sock):
    size, = struct.unpack('!I', receive_exact(sock, 4))
    if size > LIMIT:  # reject before allocating or reading the body
        raise ValueError('message too large')
    return receive_exact(sock, size)


def listen_unix(path):
    """Bind a listening socket. A leftover file is removed only if nobody listens on it."""
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        server.bind(path)
    except OSError as exc:
        if exc.errno != errno.EADDRINUSE:
            server.close()
            raise
        probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            probe.connect(path)
        except OSError as probe_exc:
            if probe_exc.errno not in (errno.ECONNREFUSED, errno.ENOENT):
                server.close()
                raise
            os.unlink(path)  # stale: file exists but no process accepts connections
            server.bind(path)
        else:
            server.close()
            raise RuntimeError('another process is already listening on ' + path) from exc
        finally:
            probe.close()
    os.chmod(path, 0o600)  # access control is the file mode of the socket path
    server.listen(1)
    return server


def peer_uid(conn):
    """SO_PEERCRED is Linux-specific: returns the connecting process's (pid, uid, gid)."""
    raw = conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i'))
    return struct.unpack('3i', raw)


def demo():
    directory = tempfile.mkdtemp(prefix='handbook-uds-')  # mode 0700, short path
    path = os.path.join(directory, 'echo.sock')
    errors = []
    try:
        # A stale file left by a crashed process must not block the next start.
        leftover = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        leftover.bind(path)
        leftover.close()
        assert stat.S_ISSOCK(os.stat(path).st_mode)

        server = listen_unix(path)
        assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
        server.settimeout(5)

        def serve():
            try:
                conn, _ = server.accept()
                with conn:
                    conn.settimeout(5)
                    pid, uid, _gid = peer_uid(conn)
                    if uid != os.getuid():
                        raise RuntimeError('unexpected peer uid')
                    send_message(conn, receive_message(conn).upper())
            except Exception as exc:  # reported to the main thread below
                errors.append(exc)

        thread = threading.Thread(target=serve)
        thread.start()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.settimeout(5)
            client.connect(path)
            send_message(client, b'hello unix socket')
            reply = receive_message(client)
        thread.join(5)
        server.close()
        if errors:
            raise errors[0]
        assert reply == b'HELLO UNIX SOCKET', reply
    finally:
        shutil.rmtree(directory, ignore_errors=True)
    assert not os.path.exists(directory)
    print('Unix domain socket framed echo OK')


if __name__ == '__main__':
    demo()

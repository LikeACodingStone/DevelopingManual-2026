"""Length-prefixed messages; deterministic local TCP server, no external services."""
import socket
import struct
import threading

LIMIT = 1024 * 1024

def receive_exact(sock, count):
    data = bytearray()
    while len(data) < count:
        part = sock.recv(count - len(data))
        if not part:
            raise EOFError('peer closed before complete message')
        data.extend(part)
    return bytes(data)

def receive_message(sock):
    size, = struct.unpack('!I', receive_exact(sock, 4))
    if size > LIMIT:
        raise ValueError('message too large')
    return receive_exact(sock, size)

def send_message(sock, data):
    if len(data) > LIMIT:
        raise ValueError('message too large')
    sock.sendall(struct.pack('!I', len(data)) + data)

def demo():
    errors = []
    with socket.socket() as server:
        server.bind(('127.0.0.1', 0))
        server.listen(1)
        server.settimeout(5)
        def serve():
            try:
                conn, _ = server.accept()
                with conn:
                    conn.settimeout(5)
                    send_message(conn, receive_message(conn))
            except Exception as exc:
                errors.append(exc)
        thread = threading.Thread(target=serve)
        thread.start()
        try:
            with socket.create_connection(server.getsockname(), timeout=5) as client:
                send_message(client, b'PCM\x00data')
                result = receive_message(client)
        finally:
            thread.join(timeout=6)
        if errors:
            raise errors[0]
        if thread.is_alive():
            raise RuntimeError('server did not terminate')
        if result != b'PCM\x00data':
            raise RuntimeError('echo mismatch')
        print('TCP framed echo OK')

if __name__ == '__main__':
    demo()

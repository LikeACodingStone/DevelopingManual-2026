"""Minimal RFC 6455 WebSocket: handshake, framing, masking, ping/pong, close.

Standard library only, loopback only. This teaches the wire format; it is not a
production server (no TLS, no extensions, no per-message-deflate, no backpressure).
Run: python3 examples/python/websocket_minimal.py
"""
import base64
import hashlib
import os
import socket
import struct
import threading

GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
OP_CONT, OP_TEXT, OP_BINARY, OP_CLOSE, OP_PING, OP_PONG = 0x0, 0x1, 0x2, 0x8, 0x9, 0xA
MAX_PAYLOAD = 1 << 20


class ProtocolError(Exception):
    def __init__(self, message, close_code=1002):
        super().__init__(message)
        self.close_code = close_code


def accept_key(client_key):
    return base64.b64encode(hashlib.sha1((client_key + GUID).encode('ascii')).digest()).decode('ascii')


def receive_exact(sock, count):
    data = bytearray()
    while len(data) < count:
        part = sock.recv(count - len(data))
        if not part:
            raise EOFError('peer closed')
        data.extend(part)
    return bytes(data)


def apply_mask(payload, key):
    return bytes(b ^ key[i % 4] for i, b in enumerate(payload))


def encode_frame(opcode, payload=b'', mask=False, fin=True, mask_key=None):
    """Clients MUST mask; servers MUST NOT (RFC 6455 section 5.1)."""
    first = (0x80 if fin else 0) | opcode
    length = len(payload)
    mask_bit = 0x80 if mask else 0
    if length < 126:
        header = struct.pack('!BB', first, mask_bit | length)
    elif length < 1 << 16:
        header = struct.pack('!BBH', first, mask_bit | 126, length)
    else:
        header = struct.pack('!BBQ', first, mask_bit | 127, length)
    if mask:
        key = mask_key if mask_key is not None else os.urandom(4)
        return header + key + apply_mask(payload, key)
    return header + payload


def read_frame(sock, expect_masked, limit=MAX_PAYLOAD):
    """Return (fin, opcode, payload); raise ProtocolError for anything RFC 6455 forbids."""
    b0, b1 = receive_exact(sock, 2)
    fin, rsv, opcode = bool(b0 & 0x80), b0 & 0x70, b0 & 0x0F
    masked, length = bool(b1 & 0x80), b1 & 0x7F
    if rsv:
        raise ProtocolError('reserved bits set without a negotiated extension')
    if masked != expect_masked:
        raise ProtocolError('wrong masking direction')
    if opcode not in (OP_CONT, OP_TEXT, OP_BINARY, OP_CLOSE, OP_PING, OP_PONG):
        raise ProtocolError('unknown opcode')
    if opcode >= 0x8 and (not fin or length > 125):
        raise ProtocolError('control frames must be unfragmented and at most 125 bytes')
    if length == 126:
        length, = struct.unpack('!H', receive_exact(sock, 2))
    elif length == 127:
        length, = struct.unpack('!Q', receive_exact(sock, 8))
    if length > limit:  # check before reading or allocating the body
        raise ProtocolError('payload too large', close_code=1009)
    key = receive_exact(sock, 4) if masked else None
    payload = receive_exact(sock, length)
    return fin, opcode, apply_mask(payload, key) if masked else payload


def read_message(sock, expect_masked):
    """Reassemble fragments. Control frames may appear between fragments; returns
    (opcode, payload) for data messages, or (OP_PING/OP_PONG/OP_CLOSE, payload)."""
    message_opcode, parts = None, []
    while True:
        fin, opcode, payload = read_frame(sock, expect_masked)
        if opcode >= 0x8:
            return opcode, payload
        if opcode == OP_CONT:
            if message_opcode is None:
                raise ProtocolError('continuation without a start frame')
        else:
            if message_opcode is not None:
                raise ProtocolError('new data frame inside a fragmented message')
            message_opcode = opcode
        parts.append(payload)
        if fin:
            data = b''.join(parts)
            if message_opcode == OP_TEXT:
                try:
                    data.decode('utf-8')
                except UnicodeDecodeError:
                    raise ProtocolError('invalid UTF-8 in text message', close_code=1007)
            return message_opcode, data


def parse_http_headers(raw):
    lines = raw.decode('latin-1').split('\r\n')
    headers = {}
    for line in lines[1:]:
        if ':' in line:
            name, value = line.split(':', 1)
            headers[name.strip().lower()] = value.strip()
    return lines[0], headers


def read_http_head(sock, limit=8192):
    data = bytearray()
    while b'\r\n\r\n' not in data:
        part = sock.recv(1024)
        if not part:
            raise EOFError('peer closed during handshake')
        data.extend(part)
        if len(data) > limit:
            raise ProtocolError('handshake too large')
    return bytes(data)


def server_handshake(sock):
    """Validate an Upgrade request; answer 101 or 400. Returns True when upgraded."""
    request_line, headers = parse_http_headers(read_http_head(sock))
    key = headers.get('sec-websocket-key', '')
    try:
        valid_key = len(base64.b64decode(key, validate=True)) == 16
    except ValueError:
        valid_key = False
    ok = (request_line.startswith('GET ') and headers.get('upgrade', '').lower() == 'websocket'
          and 'upgrade' in headers.get('connection', '').lower()
          and headers.get('sec-websocket-version') == '13' and valid_key)
    if not ok:
        sock.sendall(b'HTTP/1.1 400 Bad Request\r\nSec-WebSocket-Version: 13\r\nContent-Length: 0\r\n\r\n')
        return False
    sock.sendall(('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                  'Sec-WebSocket-Accept: %s\r\n\r\n' % accept_key(key)).encode('ascii'))
    return True


def client_handshake(sock, host):
    key = base64.b64encode(os.urandom(16)).decode('ascii')
    sock.sendall(('GET /echo HTTP/1.1\r\nHost: %s\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                  'Sec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\n\r\n' % (host, key)).encode('ascii'))
    status, headers = parse_http_headers(read_http_head(sock))
    if '101' not in status or headers.get('sec-websocket-accept') != accept_key(key):
        raise ProtocolError('server did not accept the upgrade')


def serve_connection(conn):
    """Echo data messages, answer pings, finish the close handshake."""
    if not server_handshake(conn):
        return
    while True:
        try:
            opcode, payload = read_message(conn, expect_masked=True)
        except ProtocolError as exc:
            conn.sendall(encode_frame(OP_CLOSE, struct.pack('!H', exc.close_code)))
            return
        if opcode == OP_CLOSE:
            conn.sendall(encode_frame(OP_CLOSE, payload[:2]))
            return
        if opcode == OP_PING:
            conn.sendall(encode_frame(OP_PONG, payload))
        elif opcode in (OP_TEXT, OP_BINARY):
            conn.sendall(encode_frame(opcode, payload))


def demo():
    errors = []
    with socket.socket() as server:
        server.bind(('127.0.0.1', 0))  # loopback only, ephemeral port
        server.listen(1)
        server.settimeout(5)

        def serve():
            try:
                conn, _ = server.accept()
                with conn:
                    conn.settimeout(5)
                    serve_connection(conn)
            except Exception as exc:
                errors.append(exc)

        thread = threading.Thread(target=serve)
        thread.start()
        with socket.create_connection(server.getsockname(), timeout=5) as client:
            client_handshake(client, '127.0.0.1')
            client.sendall(encode_frame(OP_TEXT, 'héllo'.encode(), mask=True))
            assert read_message(client, expect_masked=False) == (OP_TEXT, 'héllo'.encode())
            client.sendall(encode_frame(OP_PING, b'p', mask=True))
            assert read_message(client, expect_masked=False) == (OP_PONG, b'p')
            client.sendall(encode_frame(OP_TEXT, b'frag', mask=True, fin=False))
            client.sendall(encode_frame(OP_CONT, b'mented', mask=True))
            assert read_message(client, expect_masked=False) == (OP_TEXT, b'fragmented')
            client.sendall(encode_frame(OP_CLOSE, struct.pack('!H', 1000), mask=True))
            assert read_message(client, expect_masked=False) == (OP_CLOSE, struct.pack('!H', 1000))
        thread.join(5)
    if errors:
        raise errors[0]
    print('WebSocket handshake, framing, ping and close OK')


if __name__ == '__main__':
    demo()

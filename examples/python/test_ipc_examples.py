"""Tests for the WebSocket, Unix socket and zlib examples (RFC vectors and failure paths)."""
import os
import shutil
import socket
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import unix_socket
import websocket_minimal as ws
import zlib_demo


def pair():
    a, b = socket.socketpair()
    a.settimeout(2)
    b.settimeout(2)
    return a, b


class WebSocketVectors(unittest.TestCase):
    def test_accept_key_from_rfc_6455_section_1_3(self):
        self.assertEqual(ws.accept_key('dGhlIHNhbXBsZSBub25jZQ=='), 's3pPLMBiTxaQ9kYGzzhZRbK+xOo=')

    def test_unmasked_and_masked_hello_from_rfc_section_5_7(self):
        self.assertEqual(ws.encode_frame(ws.OP_TEXT, b'Hello'), bytes.fromhex('810548656c6c6f'))
        masked = ws.encode_frame(ws.OP_TEXT, b'Hello', mask=True, mask_key=bytes.fromhex('37fa213d'))
        self.assertEqual(masked, bytes.fromhex('818537fa213d7f9f4d5158'))

    def test_extended_length_headers(self):
        self.assertEqual(ws.encode_frame(ws.OP_BINARY, bytes(256))[:4], bytes.fromhex('827e0100'))
        self.assertEqual(ws.encode_frame(ws.OP_BINARY, bytes(65536))[:10], bytes.fromhex('827f0000000000010000'))

    def test_round_trip_for_all_length_classes(self):
        for size in (0, 125, 126, 65535, 65536):
            a, b = pair()
            with a, b:
                payload = bytes(range(256)) * (size // 256 + 1)
                payload = payload[:size]
                a.sendall(ws.encode_frame(ws.OP_BINARY, payload, mask=True))
                self.assertEqual(ws.read_frame(b, expect_masked=True), (True, ws.OP_BINARY, payload))


class WebSocketRejections(unittest.TestCase):
    def read_error(self, wire, expect_masked=True):
        a, b = pair()
        with a, b:
            a.sendall(wire)
            with self.assertRaises(ws.ProtocolError) as ctx:
                ws.read_message(b, expect_masked)
            return ctx.exception

    def test_unmasked_client_frame(self):
        self.read_error(ws.encode_frame(ws.OP_TEXT, b'x'))

    def test_masked_server_frame(self):
        self.read_error(ws.encode_frame(ws.OP_TEXT, b'x', mask=True), expect_masked=False)

    def test_reserved_bit(self):
        wire = bytearray(ws.encode_frame(ws.OP_TEXT, b'x', mask=True))
        wire[0] |= 0x40
        self.read_error(bytes(wire))

    def test_control_frame_too_long_or_fragmented(self):
        self.read_error(ws.encode_frame(ws.OP_PING, bytes(126), mask=True))
        self.read_error(ws.encode_frame(ws.OP_PING, b'', mask=True, fin=False))

    def test_oversize_payload_is_refused_before_reading_it(self):
        # Header announces 2 GiB but no body follows: must fail on the header alone.
        header = struct.pack('!BBQ', 0x82, 0x80 | 127, 1 << 31) + b'\0\0\0\0'
        self.assertEqual(self.read_error(header).close_code, 1009)

    def test_invalid_utf8_text(self):
        self.assertEqual(self.read_error(ws.encode_frame(ws.OP_TEXT, b'\xff\xfe', mask=True)).close_code, 1007)

    def test_continuation_without_start(self):
        self.read_error(ws.encode_frame(ws.OP_CONT, b'x', mask=True))

    def test_new_data_frame_inside_fragmented_message(self):
        wire = ws.encode_frame(ws.OP_TEXT, b'a', mask=True, fin=False) + ws.encode_frame(ws.OP_TEXT, b'b', mask=True)
        self.read_error(wire)

    def test_truncated_frame(self):
        a, b = pair()
        with b:
            a.sendall(ws.encode_frame(ws.OP_TEXT, b'hello', mask=True)[:-2])
            a.close()
            with self.assertRaises(EOFError):
                ws.read_frame(b, expect_masked=True)


class WebSocketHandshake(unittest.TestCase):
    def handshake(self, request):
        a, b = pair()
        with a, b:
            a.sendall(request)
            result = ws.server_handshake(b)
            b.shutdown(socket.SHUT_WR)
            return result, a.recv(4096)

    GOOD = (b'GET /chat HTTP/1.1\r\nHost: x\r\nUpgrade: websocket\r\nConnection: keep-alive, Upgrade\r\n'
            b'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n')

    def test_valid_upgrade(self):
        ok, reply = self.handshake(self.GOOD)
        self.assertTrue(ok)
        self.assertTrue(reply.startswith(b'HTTP/1.1 101'))
        self.assertIn(b'Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=', reply)

    def test_missing_key_wrong_version_and_bad_key_length(self):
        for bad in (self.GOOD.replace(b'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n', b''),
                    self.GOOD.replace(b'Version: 13', b'Version: 8'),
                    self.GOOD.replace(b'dGhlIHNhbXBsZSBub25jZQ==', b'c2hvcnQ=')):
            ok, reply = self.handshake(bad)
            self.assertFalse(ok)
            self.assertTrue(reply.startswith(b'HTTP/1.1 400'))


class UnixSocketTests(unittest.TestCase):
    def test_header_larger_than_limit_is_refused_without_body(self):
        a, b = pair()
        with a, b:
            a.sendall(struct.pack('!I', unix_socket.LIMIT + 1))
            with self.assertRaises(ValueError):
                unix_socket.receive_message(b)

    def test_truncated_message(self):
        a, b = pair()
        with b:
            a.sendall(struct.pack('!I', 10) + b'abc')
            a.close()
            with self.assertRaises(EOFError):
                unix_socket.receive_message(b)

    def test_stale_file_is_replaced_but_live_listener_is_not(self):
        directory = tempfile.mkdtemp(prefix='handbook-test-')
        self.addCleanup(shutil.rmtree, directory, True)
        path = os.path.join(directory, 's.sock')
        dead = socket.socket(socket.AF_UNIX)
        dead.bind(path)
        dead.close()
        live = unix_socket.listen_unix(path)  # stale file removed
        self.addCleanup(live.close)
        with self.assertRaises(RuntimeError):
            unix_socket.listen_unix(path)  # somebody is listening: must not steal the path
        self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)

    def test_path_too_long(self):
        server = socket.socket(socket.AF_UNIX)
        self.addCleanup(server.close)
        with self.assertRaises(OSError):
            server.bind('/tmp/' + 'x' * 200)


class ZlibTests(unittest.TestCase):
    def test_decompression_bomb_is_limited(self):
        bomb = zlib_demo.compress(bytes(10_000_000))
        self.assertLess(len(bomb), 20_000)
        with self.assertRaises(ValueError):
            zlib_demo.decompress_limited(bomb, limit=1 << 20)

    def test_empty_input_round_trip(self):
        self.assertEqual(zlib_demo.decompress_limited(zlib_demo.compress(b'')), b'')

    def test_wrapper_headers(self):
        self.assertEqual(zlib_demo.compress(b'a')[:1], b'\x78')
        self.assertEqual(zlib_demo.compress(b'a', zlib_demo.GZIP)[:2], b'\x1f\x8b')
        with self.assertRaises(zlib.error):
            zlib.decompress(zlib_demo.compress(b'a', zlib_demo.RAW))  # raw has no zlib header

    def test_demo_runs(self):
        zlib_demo.demo()
        unix_socket.demo()
        ws.demo()


if __name__ == '__main__':
    unittest.main()

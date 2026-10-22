import base64
import importlib.util
import socket
import struct
import sys
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from framed_tcp import LIMIT, receive_exact, receive_message, send_message
from vad import EnergyGate
from bacnet_whois import who_is
from encoding import demo as encoding_demo


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

speech = load('speech_demo', 'examples/integrations/baidu_speech.py')
sdk = load('sdk_demo', 'examples/integrations/sdk_session.py')


class FramingTests(unittest.TestCase):
    def test_fragmented_header_and_body(self):
        a, b = socket.socketpair()
        with a, b:
            a.settimeout(2)
            b.settimeout(2)
            data = struct.pack('!I', 7) + b'PCM\x00end'
            def sender():
                try:
                    for value in data:
                        a.sendall(bytes([value]))
                finally:
                    a.shutdown(socket.SHUT_WR)
            thread = threading.Thread(target=sender)
            thread.start()
            try:
                self.assertEqual(receive_message(b), b'PCM\x00end')
            finally:
                thread.join(timeout=2)
            self.assertFalse(thread.is_alive())

    def test_truncation_limit_and_empty(self):
        a, b = socket.socketpair()
        with a, b:
            a.sendall(b'\x00\x00')
            a.shutdown(socket.SHUT_WR)
            with self.assertRaises(EOFError):
                receive_message(b)
        a, b = socket.socketpair()
        with a, b:
            a.sendall(struct.pack('!I', LIMIT + 1))
            with self.assertRaises(ValueError):
                receive_message(b)
        a, b = socket.socketpair()
        with a, b:
            send_message(a, b'')
            self.assertEqual(receive_message(b), b'')


class AudioAndEncodingTests(unittest.TestCase):
    def test_vad_hangover_and_restart(self):
        gate = EnergyGate()
        frames = [[0]*320, [-32768]*320, [0]*320, [0]*320, [12000]*320,
                  [0]*320, [0]*320, [0]*320, [12000]*320]
        self.assertEqual([gate.feed(frame) for frame in frames],
                         ['silence', 'start', 'active', 'active', 'active',
                          'active', 'active', 'end', 'start'])
        with self.assertRaises(ValueError):
            gate.feed([])
        with self.assertRaises(ValueError):
            EnergyGate(start=0.1, stop=0.2)

    def test_known_encoding_vectors(self):
        encoding_demo()
        packet = who_is()
        self.assertEqual(packet.hex(), '810b000c0120ffff00ff1008')
        self.assertEqual(struct.unpack('!H', packet[2:4])[0], len(packet))

    def test_asr_body_raw_length_not_base64_length(self):
        pcm = b'\x00\x00\x01\x00'
        body = speech.asr_body(pcm, 'test-only', 'demo')
        self.assertEqual(body['len'], 4)
        self.assertEqual(base64.b64decode(body['speech']), pcm)
        self.assertEqual(body['rate'], 16000)
        for invalid in (b'', b'1', b'0' * 1920002):
            with self.assertRaises(ValueError):
                speech.asr_body(invalid, 'test-only', 'demo')

    def test_adapter_releases_after_partial_open_failure(self):
        # Fault injection tests resource cleanup, not a fake recognition result.
        class FailingAdapter:
            closed = False
            def open(self):
                raise RuntimeError('partial initialization failed')
            def close(self):
                self.closed = True
        adapter = FailingAdapter()
        with self.assertRaises(RuntimeError):
            sdk.run_session(adapter, [])
        self.assertTrue(adapter.closed)


if __name__ == '__main__':
    unittest.main()

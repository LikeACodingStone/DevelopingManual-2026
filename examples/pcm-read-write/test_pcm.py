import struct
import tempfile
import unittest
from pathlib import Path

from pcm_demo import generate_tone, read_wav, split_chunks, write_files


class PCMTests(unittest.TestCase):
    def test_tone_and_wav_round_trip(self):
        pcm = generate_tone()
        self.assertEqual(len(pcm), 32000)
        samples = struct.unpack('<16000h', pcm)
        self.assertEqual(samples[0], 0)
        self.assertTrue(all(-8191 <= value <= 8191 for value in samples))
        # A 440 Hz sine has 880 sign transitions per second (allow endpoints).
        crossings = sum((a < 0) != (b < 0) for a, b in zip(samples, samples[1:]))
        self.assertTrue(878 <= crossings <= 880)
        with tempfile.TemporaryDirectory() as tmp:
            write_files(tmp, pcm)
            self.assertEqual((Path(tmp) / 'tone.pcm').read_bytes(), pcm)
            metadata, restored = read_wav(Path(tmp) / 'tone.wav')
            self.assertEqual(metadata, (16000, 1, 2, 16000))
            self.assertEqual(restored, pcm)

    def test_arbitrary_input_boundaries_preserve_tail(self):
        data = bytes(range(256)) * 8 + b'end'
        parts = [data[:13], b'', data[13:971], data[971:]]
        chunks = list(split_chunks(parts, 640))
        self.assertEqual([len(c) for c in chunks], [640, 640, 640, 131])
        self.assertEqual(b''.join(chunks), data)
        self.assertEqual(list(split_chunks([], 640)), [])
        with self.assertRaises(ValueError):
            list(split_chunks([data], 0))

class ChannelTests(unittest.TestCase):
    def test_channel_order_and_alignment(self):
        from channels import extract_channel
        data = struct.pack('<hhhhhh', 1, -1, 2, -2, 3, -3)
        self.assertEqual(extract_channel(data, 2, 1), struct.pack('<hhh', -1, -2, -3))
        self.assertEqual(extract_channel(b'', 2, 0), b'')
        with self.assertRaises(ValueError):
            extract_channel(b'\x00\x00', 2, 0)
        with self.assertRaises(ValueError):
            extract_channel(data, 2, 2)


if __name__ == '__main__':
    unittest.main()

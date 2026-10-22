"""Generate and read 16 kHz mono signed 16-bit little-endian PCM."""
import argparse
import math
from pathlib import Path
import struct
import wave

RATE = 16000
CHANNELS = 1
WIDTH = 2


def generate_tone():
    return b''.join(struct.pack('<h', round(8191 * math.sin(2 * math.pi * 440 * i / RATE)))
                    for i in range(RATE))


def split_chunks(parts, size):
    """Yield fixed-size chunks across input boundaries, then the unpadded tail."""
    if size <= 0:
        raise ValueError('size must be positive')
    pending = bytearray()
    for part in parts:
        pending.extend(part)
        while len(pending) >= size:
            yield bytes(pending[:size])
            del pending[:size]
    if pending:
        yield bytes(pending)


def write_files(output, pcm):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'tone.pcm').write_bytes(pcm)
    with wave.open(str(output / 'tone.wav'), 'wb') as wav:
        wav.setnchannels(CHANNELS)
        wav.setsampwidth(WIDTH)
        wav.setframerate(RATE)
        wav.writeframes(pcm)


def read_wav(path):
    with wave.open(str(path), 'rb') as wav:
        return (wav.getframerate(), wav.getnchannels(), wav.getsampwidth(),
                wav.getnframes()), wav.readframes(wav.getnframes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    pcm = generate_tone()
    write_files(args.output, pcm)
    metadata, restored = read_wav(args.output / 'tone.wav')
    if metadata != (RATE, CHANNELS, WIDTH, RATE) or restored != pcm:
        raise RuntimeError('WAV round-trip failed')
    chunks = list(split_chunks((pcm[i:i + 317] for i in range(0, len(pcm), 317)), 640))
    print(f'sample_frames={RATE} pcm_bytes={len(pcm)} chunks_20ms={len(chunks)}')
    print('WAV round-trip OK')


if __name__ == '__main__':
    main()

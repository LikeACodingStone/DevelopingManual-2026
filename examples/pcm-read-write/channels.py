"""Extract one channel from signed 16-bit little-endian interleaved PCM."""
import struct


def extract_channel(pcm, channels, channel):
    if not isinstance(channels, int) or channels < 1 or not 0 <= channel < channels:
        raise ValueError('invalid channel count/index')
    if len(pcm) % (channels * 2):
        raise ValueError('input ends in a partial sample frame')
    samples = struct.unpack('<' + 'h' * (len(pcm) // 2), pcm)
    selected = samples[channel::channels]
    return struct.pack('<' + 'h' * len(selected), *selected)


if __name__ == '__main__':
    stereo = struct.pack('<hhhh', 100, -100, 200, -200)
    mono = extract_channel(stereo, channels=2, channel=1)
    print(struct.unpack('<hh', mono))

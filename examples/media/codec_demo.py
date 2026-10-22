"""Real codec/container exercise through installed FFmpeg; new code, no legacy source."""
import argparse
from pathlib import Path
import shutil
import subprocess
import wave


def run_codec(codec, output):
    if not shutil.which('ffmpeg'):
        raise RuntimeError('ffmpeg required')
    formats = {'mp3': ('libmp3lame', '.mp3'), 'aac': ('aac', '.aac'), 'opus': ('libopus', '.ogg')}
    encoder, extension = formats[codec]
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    encoded, decoded = output / ('tone' + extension), output / 'decoded.wav'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi',
                    '-i', 'sine=frequency=440:sample_rate=48000:duration=1',
                    '-ac', '1', '-c:a', encoder, str(encoded)], check=True, timeout=30)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(encoded),
                    '-c:a', 'pcm_s16le', str(decoded)], check=True, timeout=30)
    with wave.open(str(decoded), 'rb') as wav:
        duration = wav.getnframes() / wav.getframerate()
        if wav.getsampwidth() != 2 or wav.getnchannels() != 1 or not 0.9 <= duration <= 1.2:
            raise RuntimeError('unexpected decoded format/duration')
        print(f'{codec}: decoded PCM OK ({duration:.3f}s)')
    return encoded, decoded


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('codec', choices=['mp3', 'aac', 'opus'])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run_codec(args.codec, args.output)

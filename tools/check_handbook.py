"""Check local links, document structure, offline Python and dependency-free C examples."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(args, **kwargs):
    print('+', ' '.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), cwd=ROOT, check=True, timeout=60, **kwargs)


def check_docs():
    failures = []
    docs = [*ROOT.glob('*.md'), *ROOT.glob('topics/**/*.md'), *ROOT.glob('catalog/*.md'), *ROOT.glob('examples/**/*.md')]
    for doc in docs:
        content = doc.read_text()
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if '://' in target or target.startswith('#'):
                continue
            if not (doc.parent / target.split('#')[0]).exists():
                failures.append(f'{doc.relative_to(ROOT)}: missing {target}')
        if doc.parent != ROOT / 'topics' and ROOT / 'topics' in doc.parents:
            for heading in ['是什么', '何时使用', '如何使用', '最小示例', '常见问题', '参考资料']:
                # Existing PCM and FIDL pages have their own already-established layouts.
                if doc.name not in ('pcm.md', 'fidl.md') and f'## {heading}' not in content:
                    failures.append(f'{doc}: missing heading {heading}')
    if failures:
        raise RuntimeError('\n'.join(failures))
    print(f'Document links/structure OK: {len(docs)} files')


def native_checks(tmp):
    cc = shutil.which('cc')
    if not cc:
        raise RuntimeError('C compiler required for native checks')
    cases = [
        ('threads', ['core_thread_example.c', 'threads.c'], ['-pthread'], 'counter=20000'),
        ('semaphore', ['semaphore.c'], ['-pthread'], 'value=42'),
        ('varargs', ['varargs.c'], [], 'name=PCM count=2 ratio=0.5'),
    ]
    for name, sources, flags, expected in cases:
        out = tmp / name
        run([cc, '-std=c11', '-Wall', '-Wextra', '-Werror', *flags,
             *[ROOT / 'examples/native' / s for s in sources], '-o', out])
        result = subprocess.run([out], check=True, capture_output=True, text=True, timeout=10)
        if expected not in result.stdout:
            raise RuntimeError(f'{name}: unexpected output {result.stdout}')
        print(result.stdout.strip())
    for pkg, source, name in [('python3-embed', 'embed_python.c', 'embed'), ('openssl', 'tls.c', 'tls')]:
        probe = subprocess.run(['pkg-config', '--cflags', '--libs', pkg], capture_output=True, text=True)
        if probe.returncode:
            print(f'SKIP optional native check: {source}, missing {pkg}')
            continue
        import shlex
        out = tmp / name
        run([cc, '-std=c11', '-Wall', '-Wextra', '-Werror', ROOT / 'examples/native' / source,
             *shlex.split(probe.stdout), '-o', out])
        if name == 'embed':
            run([out])
        else:
            print('TLS compile OK; no external handshake performed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--media', action='store_true', help='also run installed FFmpeg codecs')
    args = parser.parse_args()
    check_docs()
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'examples/pcm-read-write', '-p', 'test_*.py'])
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'examples/python', '-p', 'test_*.py'])
    for name in ['framed_tcp.py', 'http_local.py', 'encoding.py', 'vad.py', 'bacnet_whois.py']:
        run([sys.executable, ROOT / 'examples/python' / name])
    with tempfile.TemporaryDirectory(prefix='handbook-check-') as tmp:
        native_checks(Path(tmp))
        if args.media:
            for codec in ['mp3', 'aac', 'opus']:
                run([sys.executable, 'examples/media/codec_demo.py', codec, '--output', Path(tmp) / codec])
    print('Offline checks passed. Vendor SDK, device and broker integration NOT included.')


if __name__ == '__main__':
    main()

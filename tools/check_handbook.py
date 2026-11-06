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
    docs = [*ROOT.glob('*.md'), *ROOT.glob('topics/**/*.md'), *ROOT.glob('catalog/*.md'), *ROOT.glob('catalog/*/*.md'), *ROOT.glob('examples/**/*.md')]
    for doc in docs:
        content = doc.read_text()
        is_topic = ROOT / 'topics' in doc.parents
        if is_topic and re.search(r'Coding_0001_HistoryTree|20(?:16|19|21|23|25)Codes|src/egn/|misc/demos/|summary_components', content):
            failures.append(f'{doc}: historical source reference in a technical page')
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if '://' in target or target.startswith('#'):
                continue
            destination = (doc.parent / target.split('#')[0]).resolve()
            if is_topic and not destination.is_relative_to(ROOT):
                failures.append(f'{doc}: local reference escapes handbook: {target}')
            if is_topic and destination.suffix in {'.c', '.h', '.cpp', '.py', '.java', '.proto', '.fidl'} and not destination.is_relative_to(ROOT / 'examples'):
                failures.append(f'{doc}: teaching source must be in examples/: {target}')
            if not destination.exists():
                failures.append(f'{doc.relative_to(ROOT)}: missing {target}')
        if doc.parent != ROOT / 'topics' and ROOT / 'topics' in doc.parents:
            english = ROOT / 'topics' / 'English' in doc.parents
            headings = (['What it is', 'When to use', 'How to use', 'Minimal example', 'FAQ', 'References'] if english
                        else ['是什么', '何时使用', '如何使用', '最小示例', '常见问题', '参考资料'])
            for heading in headings:
                # Existing PCM and FIDL pages have their own already-established layouts.
                if doc.name not in ('pcm.md', 'fidl.md') and f'## {heading}' not in content:
                    failures.append(f'{doc}: missing heading {heading}')
    failures += check_language_pairs()
    failures += check_bilingual_root_files()
    if failures:
        raise RuntimeError('\n'.join(failures))
    print(f'Document links/structure OK: {len(docs)} files')


def check_bilingual_root_files():
    """README_CH/README_EN and command_for_ai/command_for_ai_EN must have the same structure.
    A README is navigation only: no section whose heading names a scanned project (e.g. '2025Codes ...')."""
    failures = []

    def shape(path):
        text = path.read_text()
        return {
            'headings': len(re.findall(r'^#{2,3} ', text, re.M)),
            'code blocks': len(re.findall(r'^```', text, re.M)) // 2,
            'list items': len(re.findall(r'^\s*(?:- |\d+\. )', text, re.M)),
            'table rows': len(re.findall(r'^\| (?!---)', text, re.M)),
        }

    for first, second in (('README_CH.md', 'README_EN.md'), ('command_for_ai.md', 'command_for_ai_EN.md')):
        for name in (first, second):
            if not (ROOT / name).exists():
                failures.append(f'{name}: missing')
        if all((ROOT / n).exists() for n in (first, second)):
            a, b = shape(ROOT / first), shape(ROOT / second)
            for key in a:
                if a[key] != b[key]:
                    failures.append(f'{first} vs {second}: {key} differ ({a[key]} vs {b[key]})')
    for name in ('README_CH.md', 'README_EN.md'):
        if (ROOT / name).exists():
            for line in (ROOT / name).read_text().splitlines():
                if line.startswith('#') and re.search(r'(?:\d{4}|XXXX)Codes', line):
                    failures.append(f'{name}: scan-result section in a README is not allowed: {line}')
    return failures


def check_language_pairs():
    """Every topics/English page needs a Chinese page with the same name and category, and the
    other way round for topics/Chinese; catalog/English and catalog/Chinese must mirror each other."""
    failures = []
    topics = ROOT / 'topics'
    for page in (topics / 'English').glob('**/*.md'):
        relative = page.relative_to(topics / 'English')
        if not ((topics / 'Chinese' / relative).exists() or (topics / relative).exists()):
            failures.append(f'{page.relative_to(ROOT)}: no Chinese counterpart')
    for page in (topics / 'Chinese').glob('**/*.md'):
        if not (topics / 'English' / page.relative_to(topics / 'Chinese')).exists():
            failures.append(f'{page.relative_to(ROOT)}: no English counterpart')
    for side, other in (('English', 'Chinese'), ('Chinese', 'English')):
        for page in (ROOT / 'catalog' / side).glob('*.md'):
            if not (ROOT / 'catalog' / other / page.name).exists():
                failures.append(f'{page.relative_to(ROOT)}: missing in catalog/{other}')
    return failures


def native_checks(tmp):
    cc = shutil.which('cc')
    if not cc:
        raise RuntimeError('C compiler required for native checks')
    cases = [
        ('threads', ['threads.c'], ['-pthread'], 'counter=20000'),
        ('semaphore', ['semaphore.c'], ['-pthread'], 'value=42'),
        ('varargs', ['varargs.c'], [], 'name=PCM count=2 ratio=0.5'),
    ]
    if Path('/dev/ptmx').exists():
        cases.append(('termios_pty', ['termios_pty.c'], [], 'termios pty loopback OK'))
    else:
        print('SKIP termios_pty.c: /dev/ptmx is not available')
    if subprocess.run(['pkg-config', '--exists', 'zlib']).returncode == 0:
        cases.append(('zlib_demo', ['zlib_demo.c'], ['-lz'], 'zlib C round trip OK'))
    else:
        print('SKIP zlib_demo.c: missing zlib development package')
    for name, sources, flags, expected in cases:
        out = tmp / name
        compile_flags = [f for f in flags if not f.startswith('-l')]
        link_flags = [f for f in flags if f.startswith('-l')]
        run([cc, '-std=c11', '-Wall', '-Wextra', '-Werror', *compile_flags,
             *[ROOT / 'examples/native' / s for s in sources], *link_flags, '-o', out])
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


def new_example_checks(tmp):
    """Only compile/run local teaching examples; no broker or device access."""
    import importlib.util
    import shlex
    for source in [*ROOT.glob('examples/**/*.py'), *ROOT.glob('tools/*.py')]:
        compile(source.read_text(), str(source), 'exec')
    run([sys.executable, 'examples/python/sqlite_demo.py'])
    for pkg, source, compiler in [
        ('tinyxml', 'tinyxml_demo.cpp', 'c++'),
        ('libmosquitto', 'mosquitto_demo.c', 'cc'),
        ('jsoncpp', 'jsoncpp_demo.cpp', 'c++'),
        ('lua5.4', 'lua_embed.c', 'cc'),
        ('sqlite3', 'sqlite_c_readonly.c', 'cc'),
    ]:
        probe = subprocess.run(['pkg-config', '--cflags', '--libs', pkg], capture_output=True, text=True)
        if probe.returncode or not shutil.which(compiler):
            print(f'SKIP {source}: missing {pkg} or {compiler}')
            continue
        out = tmp / pkg
        run([compiler, '-Wall', '-Wextra', '-Werror', ROOT / 'examples/native' / source,
             *shlex.split(probe.stdout), '-o', out])
        run([out])  # libmosquitto default only prints help; never connects.
    qt_available = any(subprocess.run(['pkg-config', '--exists', f'{qt}Core', f'{qt}Network', f'{qt}Sql']).returncode == 0
                       for qt in ['Qt6', 'Qt5'])
    if qt_available and shutil.which('cmake'):
        build = tmp / 'qt'
        run(['cmake', '-S', ROOT / 'examples/qt', '-B', build])
        run(['cmake', '--build', build])
        for name in ['json', 'udp', 'threads', 'sqlite']:
            run([build / (name + '_demo')])
    else:
        print('SKIP Qt examples: missing Core/Network/Sql development packages or CMake')
    print('SKIP QextSerialPort: legacy dependency/device integration not automated')
    try:
        protobuf_available = importlib.util.find_spec('google.protobuf') is not None
    except ModuleNotFoundError:
        protobuf_available = False
    if shutil.which('protoc') and protobuf_available:
        generated = tmp / 'protobuf'
        generated.mkdir()
        run(['protoc', '-I', ROOT / 'examples/protobuf', f'--python_out={generated}',
             ROOT / 'examples/protobuf/sample.proto'])
        env = dict(os.environ, PYTHONPATH=str(generated))
        run([sys.executable, 'examples/protobuf/roundtrip.py'], env=env)
    else:
        print('SKIP Protobuf: missing protoc or Python protobuf')
    pkg_protobuf = subprocess.run(['pkg-config', '--cflags', '--libs', 'protobuf'], capture_output=True, text=True)
    if shutil.which('protoc') and shutil.which('c++') and pkg_protobuf.returncode == 0:
        import shlex
        generated = tmp / 'protobuf-cpp'
        generated.mkdir()
        run(['protoc', '-I', ROOT / 'examples/protobuf', f'--cpp_out={generated}', ROOT / 'examples/protobuf/legacy_v2.proto'])
        run(['c++', '-std=c++17', '-Wall', '-Wextra', f'-I{generated}', ROOT / 'examples/protobuf/cpp_roundtrip.cpp',
             generated / 'legacy_v2.pb.cc', *shlex.split(pkg_protobuf.stdout), '-o', tmp / 'proto-cpp'])
        run([tmp / 'proto-cpp'])
    else:
        print('SKIP Protobuf C++: missing protoc, c++ or libprotobuf development package')
    java_home = os.environ.get('JAVA_HOME')
    if shutil.which('javac') and shutil.which('java') and shutil.which('cc') and java_home and (Path(java_home) / 'include/jni.h').is_file():
        jni = tmp / 'jni'
        (jni / 'include').mkdir(parents=True)
        (jni / 'classes').mkdir()
        run(['javac', '-h', jni / 'include', '-d', jni / 'classes', 'examples/java/jni/handbook/NativeDemo.java'])
        run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-fPIC', '-shared', f'-I{jni / "include"}',
             f'-I{java_home}/include', f'-I{java_home}/include/linux', 'examples/java/jni/handbook_jni.c',
             '-o', jni / 'libhandbook_jni.so'])
        run(['java', f'-Djava.library.path={jni}', '-cp', jni / 'classes', 'handbook.NativeDemo'])
    else:
        print('SKIP JNI: missing JDK (javac/java) or JAVA_HOME with jni.h')
    print('SKIP Android AIDL and AIDL HAL: sketches need the Android SDK / an AOSP source tree')
    jar = os.environ.get('PAHO_JAR')
    if shutil.which('javac') and shutil.which('java') and jar and Path(jar).is_file():
        classes = tmp / 'java'
        classes.mkdir()
        run(['javac', '-cp', jar, '-d', classes, 'examples/java/PahoLocal.java'])
        run(['java', '-cp', os.pathsep.join([str(classes), jar]), 'PahoLocal'])
    else:
        print('SKIP Paho Java: missing JDK or PAHO_JAR')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--media', action='store_true', help='also run installed FFmpeg codecs')
    args = parser.parse_args()
    check_docs()
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'examples/pcm-read-write', '-p', 'test_*.py'])
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'examples/python', '-p', 'test_*.py'])
    for name in ['framed_tcp.py', 'http_local.py', 'encoding.py', 'vad.py', 'bacnet_whois.py',
                 'unix_socket.py', 'zlib_demo.py', 'websocket_minimal.py']:
        run([sys.executable, ROOT / 'examples/python' / name])
    with tempfile.TemporaryDirectory(prefix='handbook-check-') as tmp:
        native_checks(Path(tmp))
        new_example_checks(Path(tmp))
        if args.media:
            for codec in ['mp3', 'aac', 'opus']:
                run([sys.executable, 'examples/media/codec_demo.py', codec, '--output', Path(tmp) / codec])
    print('Offline checks passed. Vendor SDK, device and broker integration NOT included.')


if __name__ == '__main__':
    main()

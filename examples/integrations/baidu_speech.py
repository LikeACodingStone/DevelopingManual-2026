"""Baidu REST examples; require a current access token. Never run in offline checks."""
import argparse
import base64
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def asr_body(pcm, token, cuid):
    if not pcm or len(pcm) % 2 or len(pcm) > 16000 * 2 * 60:
        raise ValueError('expected up to 60s mono 16kHz s16le PCM')
    return {'format': 'pcm', 'rate': 16000, 'channel': 1, 'cuid': cuid,
            'token': token, 'dev_pid': 1537, 'len': len(pcm),
            'speech': base64.b64encode(pcm).decode('ascii')}


def asr(path, token, cuid):
    payload = json.dumps(asr_body(Path(path).read_bytes(), token, cuid)).encode('utf-8')
    request = Request('https://vop.baidu.com/server_api', data=payload,
                      headers={'Content-Type': 'application/json'})
    with urlopen(request, timeout=30) as response:
        value = json.load(response)
    if value.get('err_no') != 0:
        raise RuntimeError(f'ASR service error: {value.get("err_no")}')
    print(json.dumps(value.get('result'), ensure_ascii=False))


def tts(text, path, token, cuid):
    if not text:
        raise ValueError('text required')
    form = {'tex': text, 'tok': token, 'cuid': cuid, 'ctp': 1, 'lan': 'zh', 'aue': 3}
    request = Request('https://tsn.baidu.com/text2audio', data=urlencode(form).encode('ascii'),
                      headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with urlopen(request, timeout=30) as response:
        kind = response.headers.get_content_type()
        body = response.read()
    if not kind.startswith('audio/'):
        # Do not write JSON errors to an MP3 file or print credential-bearing responses.
        raise RuntimeError(f'TTS did not return audio: {kind}')
    Path(path).write_bytes(body)
    print(f'wrote {len(body)} audio bytes')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    recognition = sub.add_parser('asr')
    recognition.add_argument('pcm')
    synthesis = sub.add_parser('tts')
    synthesis.add_argument('text')
    synthesis.add_argument('output')
    args = parser.parse_args()
    token = os.environ['BAIDU_ACCESS_TOKEN']
    cuid = os.environ.get('BAIDU_CUID', 'handbook-demo')
    if args.mode == 'asr':
        asr(args.pcm, token, cuid)
    else:
        tts(args.text, args.output, token, cuid)

if __name__ == '__main__':
    main()

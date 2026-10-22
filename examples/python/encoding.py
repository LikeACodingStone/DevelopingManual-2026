import base64
import hashlib
import hmac

def demo():
    raw = '你好 PCM'.encode('utf-8')
    encoded = base64.b64encode(raw)
    if base64.b64decode(encoded, validate=True) != raw:
        raise RuntimeError('Base64 round-trip failed')
    # RFC 4231 test case 1: known key and message, not a real credential.
    digest = hmac.new(bytes.fromhex('0b' * 20), b'Hi There', hashlib.sha256).hexdigest()
    expected = 'b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7'
    if not hmac.compare_digest(digest, expected):
        raise RuntimeError('HMAC test vector mismatch')
    print('Base64 round-trip OK; HMAC-SHA256 RFC4231 OK')

if __name__ == '__main__':
    demo()

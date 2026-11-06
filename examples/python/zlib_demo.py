"""zlib / DEFLATE: three wrappers, size-limited decompression, and corruption checks.

Run: python3 examples/python/zlib_demo.py   (standard library only)
"""
import zlib

ZLIB, GZIP, RAW = 15, 31, -15  # wbits values: zlib wrapper, gzip wrapper, raw deflate


def compress(data, wbits=ZLIB, level=6):
    c = zlib.compressobj(level, zlib.DEFLATED, wbits)
    return c.compress(data) + c.flush()


def decompress_limited(data, wbits=ZLIB, limit=1 << 20):
    """Decompress at most `limit` bytes; refuse truncated streams and trailing garbage."""
    d = zlib.decompressobj(wbits)
    out = d.decompress(data, limit)
    if d.unconsumed_tail:  # more output would exceed the limit (decompression bomb guard)
        raise ValueError('decompressed data exceeds limit')
    if not d.eof:
        raise ValueError('truncated stream')
    if d.unused_data:
        raise ValueError('data after end of stream')
    return out


def compress_if_smaller(data):
    """Return (compressed, payload). Falls back to the original when compression does not help."""
    packed = compress(data)
    return (True, packed) if len(packed) < len(data) else (False, data)


def demo():
    text = b'ETC log line 0001 status=OK\n' * 200
    for name, wbits, magic in [('zlib', ZLIB, b'\x78'), ('gzip', GZIP, b'\x1f\x8b'), ('raw', RAW, None)]:
        packed = compress(text, wbits)
        if magic:
            assert packed.startswith(magic), name
        assert decompress_limited(packed, wbits) == text
    # A wrapper must be decoded with the matching wbits.
    try:
        decompress_limited(compress(text, GZIP), ZLIB)
    except zlib.error:
        pass
    else:
        raise AssertionError('gzip data decoded as zlib')

    # Corruption: flipping a byte is caught by the Adler-32 check (zlib) or Huffman data errors.
    bad = bytearray(compress(text))
    bad[len(bad) // 2] ^= 0xFF
    try:
        decompress_limited(bytes(bad))
    except zlib.error:
        pass
    else:
        raise AssertionError('corruption not detected')

    # Truncation and size limit.
    good = compress(text)
    for case, call in [
        ('truncated', lambda: decompress_limited(good[:-6])),
        ('limit', lambda: decompress_limited(good, limit=100)),
        ('trailing', lambda: decompress_limited(good + b'junk')),
    ]:
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError(case + ' was accepted')

    # Incompressible data is not stored compressed.
    import os
    random_bytes = os.urandom(512)
    assert compress_if_smaller(random_bytes) == (False, random_bytes)
    assert compress_if_smaller(text)[0] is True

    # Streaming: sync flush makes everything written so far decodable.
    c = zlib.compressobj()
    d = zlib.decompressobj()
    first = c.compress(b'part one ') + c.flush(zlib.Z_SYNC_FLUSH)
    assert d.decompress(first) == b'part one '
    rest = c.compress(b'part two') + c.flush()
    assert d.decompress(rest) == b'part two' and d.eof
    print('zlib formats, limits and corruption checks OK')


if __name__ == '__main__':
    demo()
